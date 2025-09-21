import random
import os
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 6
WORDS = [
    "ПРОГРАММИРОВАНИЕ",
    "АЛГОРИТМ",
    "КОМПЬЮТЕР",
    "ВИСЕЛИЦА",
    "СТУДЕНТ",
    "УНИВЕРСИТЕТ",
    "ЛЕКЦИЯ",
    "ПРАКТИКА",
    "ПИТОН",
    "КОД",
    "ФУНКЦИЯ",
    "ПЕРЕМЕННАЯ",
    "ЦИКЛ",
    "УСЛОВИЕ",
    "СПИСОК",
    "СЛОВАРЬ",
    "МНОЖЕСТВО",
]

stats = {"games_played": 0, "games_won": 0, "total_score": 0, "best_score": 0}


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
        flag = True

        # Игровой цикл
        while attempts_left > 0:
            # Отрисовка текущего состояния игры
            clear_console()
            print(f"Попыток осталось: {attempts_left}")
            draw_gallows(attempts_left)
            print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
            print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))
            flag = get_user_guess(secret_word, guessed_letters)
            if not flag:
                attempts_left -= 1

            input("\nНажмите Enter чтобы продолжить...")

            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break

        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            score = calculate_score(secret_word, attempts_left)
            print(f"Ваш счет: {score}")
            update_stats(game_won, score)
        else:
            print("К сожалению, вы проиграли.")
            score = 0
            print(f"Загаданное слово: {secret_word}")
            update_stats(game_won, score)
            draw_gallows(attempts_left)

        show_stats()

        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ["да", "д", "yes", "y"]:
            print("Спасибо за игру!")
            break


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)


def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""
    word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            word += letter
        else:
            word += "_"
    return word


def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    if attempts_left == 0:
        print(
            """
    --------
    |      |
    |      O
    |     \|/
    |      |
    |     / \\
    -
    """
        )
    elif attempts_left == 1:
        print(
            """
    --------
    |      |
    |      O
    |     \|/
    |      |
    |     /
    -
    """
        )
    elif attempts_left == 2:
        print(
            """
    --------
    |      |
    |      O
    |     \|/
    |      |
    |
    -
    """
        )
    elif attempts_left == 3:
        print(
            """
    --------
    |      |
    |      O
    |     \|/
    |
    |
    -
    """
        )
    elif attempts_left == 4:
        print(
            """
    --------
    |      |
    |      O
    |     \|
    |
    |
    -
    """
        )
    elif attempts_left == 5:
        print(
            """
    --------
    |      |
    |      O
    |      |
    |
    |
    -
    """
        )
    else:
        print(
            """
    --------
    |      |
    |
    |
    |
    |
    -
    """
        )


def get_user_guess(secret_word: str, guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    print("Введите букву")
    letter = str(input()).upper()
    if letter in guessed_letters:
        print("Вы уже вводили эту букву, попробуйте ещё раз.")
        get_user_guess(secret_word, guessed_letters)
    elif len(letter) > 1:
        print("Вы ввели больше одного символа, попробуйте ещё раз.")
        get_user_guess(secret_word, guessed_letters)
    elif not letter.isalpha():
        print("Вы ввели не букву, попробуйте ещё раз.")
        get_user_guess(secret_word, guessed_letters)
    else:
        if letter in secret_word:
            print("Вы угадали букву")
            guessed_letters.add(letter)
            return True
        else:
            print("К сожалению, вы ошиблись.")
            guessed_letters.add(letter)
            return False


def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    if all(el in guessed_letters for el in secret_word):
        return True
    return False


def calculate_score(secret_word: str, attempts_left: int) -> int:
    """Вычисление счета за игру"""
    score = len(secret_word) - (MAX_ATTEMPTS - attempts_left)
    return score


def update_stats(game_won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"] += 1
    if game_won:
        stats["games_won"] += 1
    stats["total_score"] += score
    if score > stats["best_score"]:
        stats["best_score"] = score


def show_stats():
    """Отображение статистики"""
    global stats
    win_percentage = stats["games_won"] / stats["games_played"] * 100
    average_score = stats["total_score"] / stats["games_played"]

    print("\n=== Статистика ===")
    print(f"Всего игр: {stats["games_played"]}")
    print(f"Побед: {stats["games_won"]} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {stats["best_score"]}")
    if stats["games_played"] >= 1:
        print(f"Средний счет: {average_score}")


if __name__ == "__main__":
    main()
