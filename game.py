import random
import os
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 6

def words_file(file: str) -> List[str]:
    words = []
    with open(file, 'r') as f:
        for line in f:
            word = line.strip().upper()
            words.append(word)
    return words

WORDS = words_file("words.txt")

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
            guess = get_user_guess(guessed_letters)
            guessed_letters.add(guess)

            # Проверка угадана ли буква
            if guess in secret_word:
                print(f"Угадана буква {guess}")
            else:             
                attempts_left -= 1
                print(f"Нет буквы {guess}")

            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        
        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")

            score = calculate_score(secret_word, MAX_ATTEMPTS - attempts_left)
            print(f"Ваш счет: {score}")

            update_stats(True, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")

            update_stats(False, 0)
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
            masked_word += '_'
    return masked_word

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    stages = [
         """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     / \\
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     /
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|
        |      |
        |
        -
        """,
        """
        --------
        |      |
        |      O
        |      |
        |      |
        |
        -
        """,
        """
        --------
        |      |
        |      O
        |
        |
        |
        -
        """,
        """
        --------
        |      |
        |
        |
        |
        |
        -
        """
    ]
    print(stages[attempts_left])

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    while True:
        guess = input("Введите букву: ").upper();
        if len(guess) != 1:
            print("Нужно вводить только одну букву.")
            continue
        elif not guess.isalpha():
            print("Не правильный символ, нужно вводить букву.")
            continue
        elif guess in guessed_letters:
            print("Буква уже была. Введите другую.")
            continue
        return guess

def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    score = len(secret_word) - attempts_used
    return max(score, 1);

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"] += 1
    if won:
        stats["games_won"] += 1
        stats["total_score"] += score
        if score > stats["best_score"]:
            stats["best_score"] = score

def show_stats():
    """Отображение статистики"""
    global stats
    games_played = stats["games_played"]
    games_won = stats["games_won"]
    total_score = stats["total_score"]
    best_score = stats["best_score"]

    win_percentage = 0
    if games_played > 0:
        win_percentage = games_won * 100 / games_played

    average_score = 0
    if games_won > 0:
        average_score = total_score / games_won

    print("\n=== Статистика ===")
    print(f"Всего игр: {games_played}")
    print(f"Побед: {games_won} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {best_score}")
    if games_won > 0:
        print(f"Средний счет: {average_score:.1f}")

if __name__ == "__main__":
    main()
