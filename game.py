import random
import os
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 6

WORDS = [
    "ПРОГРАММИРОВАНИЕ", "АЛГОРИТМ", "КОМПЬЮТЕР", "ВИСЕЛИЦА",
    "СТУДЕНТ", "УНИВЕРСИТЕТ", "ЛЕКЦИЯ", "ПРАКТИКА",
    "ПИТОН", "КОД", "ФУНКЦИЯ", "ПЕРЕМЕННАЯ", "ЦИКЛ",
    "УСЛОВИЕ", "СПИСОК", "СЛОВАРЬ", "МНОЖЕСТВО"
]

stats = {
    "games_played": 0,
    "games_won": 0,
    "total_score": 0,
    "best_score": 0
}


def main():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать слово по буквам.")

    # Загрузка статистики
    global stats

    while True:
        # Выбор случайного слова
        secret_word = choose_random_word(WORDS)
        guessed_letters = set()
        attempts_left = MAX_ATTEMPTS
        game_won = False

        # Игровой цикл
        while attempts_left > 0:
            # Отрисовка текущего состояния игры
            clear_console()
            print(f"Попыток осталось: {attempts_left}")
            draw_gallows(attempts_left)
            print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
            print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))

            # Ввод буквы
            letter = get_user_guess(guessed_letters)
            guessed_letters.add(letter)

            # Проверка угадана ли буква
            if letter in secret_word:
                print("\nВы угадали букву!")
            else:
                attempts_left -= 1
                print("\nВы не угадали букву((")

            input("\nНажмите Enter чтобы продолжить...")

            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break

        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            score = calculate_score(secret_word, 6 - attempts_left)
            print(f"Ваш счет: {score}")
            update_stats(game_won, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            update_stats(game_won, 0)
            draw_gallows(0)

        show_stats()

        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            break


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)


def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""
    masked_word = ""
    for letter in secret_word:

        if letter in guessed_letters:
            masked_word += letter
        else:
            masked_word += "_"

    return masked_word



def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    if attempts_left == 6:
        print("""
        --------
        |      |
        |
        |
        |
        |
        -
        """)
    elif attempts_left == 5:
        print("""
        --------
        |      |
        |      O
        |
        |
        |
        -
        """)
    elif attempts_left == 4:
        print("""
        --------
        |      |
        |      O
        |      |
        |      |
        |
        -
        """)
    elif attempts_left == 3:
        print("""
        --------
        |      |
        |      O
        |     \\|
        |      |
        |
        -
        """)
    elif attempts_left == 2:
        print("""
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |
        -
        """)
    elif attempts_left == 1:
        print("""
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     /
        -
        """)
    elif attempts_left == 0:
        print("""
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     / \\
        -
        """)


def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    letter = input("\nВведите букву: ").upper()
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    if len(letter) != 1 or letter not in alphabet:
        print("Неверный формат ввода. Попробуйте снова")
        return get_user_guess(guessed_letters)

    if letter in guessed_letters:
        print("Вы уже вводили эту букву. Попробуйте снова")
        return get_user_guess(guessed_letters)

    return letter


def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    return all(letter in guessed_letters for letter in secret_word)


def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    if len(secret_word) > attempts_used:
        return (len(secret_word) - attempts_used) * 10

    else:
        return 10


def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats

    stats["games_played"] += 1
    stats["games_won"] += won
    stats["total_score"] += score

    if stats["best_score"] < score:
        stats["best_score"] = score


def show_stats():
    """Отображение статистики"""
    global stats

    win_percentage = stats["games_won"] / stats["games_played"] * 100
    average_score = stats["total_score"] / stats["games_played"]

    print("\n=== Статистика ===")
    print(f"Всего игр: {stats["games_played"]}")
    print(f"Побед: {stats["games_won"]} ({win_percentage}%)")
    print(f"Лучший счет: {stats["best_score"]}")

    if stats["games_won"] > 0:
        print(f"Средний счет: {average_score}")


if __name__ == "__main__":
    main()