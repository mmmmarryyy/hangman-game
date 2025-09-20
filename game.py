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

            guess=get_user_guess(guessed_letters)
            guessed_letters.add(guess)

            # Проверка угадана ли буква

            if guess not in secret_word:
                attempts_left -= 1
                print(f"Буквы '{guess}' нет в слове")
            else:
                print(f"Буква '{guess}' в слове")




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
    masked_word=''
    for letter in secret_word:
        if letter in guessed_letters:
            masked_word+=letter
        else:
            masked_word+='_'
    return masked_word

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    status = [
        """
        --------
        |      |
        |      
        |     
        |      
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
        |     \\|
        |      |
        |     
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
        |     / \\
        -
        """
    ]
    print(status[MAX_ATTEMPTS - attempts_left])

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    while True:
        guess = input("Введите букву: ").upper()
        if len(guess) != 1:
            print("Введите одну букву!")
            continue
        if not guess.isalpha():
            print("Пожалуйста, введите букву!")
            continue
        if guess in guessed_letters:
            print("Эта буква уже проверялась, введите другую букву")
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

    return len(secret_word)+MAX_ATTEMPTS-attempts_used


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
    win_percentage = stats["games_won"]/stats["games_played"]*100 if stats["games_played"] > 0 else 0
    average_score =  stats["total_score"] / stats["games_won"] if stats["games_won"] > 0 else 0
    
    print("\n=== Статистика ===")
    print(f"Всего игр:  {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {stats['best_score']}")
    if stats['games_won']!=0:
        print(f"Средний счет:{average_score}")


if __name__ == "__main__":
    main()