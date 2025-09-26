import random
import os
from typing import List, Set
import re

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
    
    print("Начнём? (напиши 'да', чтобы продолжить)")
    
    global stats
    
    start = str(input())
    if start in ['да', 'д', 'yes', 'y']:
    
        while True:
            secret_word = choose_random_word(WORDS)
            guessed_letters = set()
            used_letters = set()
            attempts_left = MAX_ATTEMPTS
            game_won = False
        
            # Игровой цикл
            while attempts_left > 0:
                clear_console()
                print(f"Попыток осталось: {attempts_left}")
                draw_gallows(attempts_left)
                print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
                print("Использованные буквы: " + ", ".join(sorted(used_letters)))

                letter = get_user_guess(guessed_letters, used_letters, secret_word)

                if letter in secret_word:
                    guessed_letters.add(letter)
                    print(f"\nВы угадали букву '{letter}'!")
                else:
                    attempts_left -= 1
                    print(f"Буква '{letter}' не в слове.")

                # Проверка на победу
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
    masked_word = ' '.join(letter if letter in guessed_letters else '_' for letter in secret_word)
    return masked_word

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    stages = [
        """
           --------
           |
           |      
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
           |     
           |    
           -
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |     
           |    
           -
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |    
           -
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \
           -
        """
    ]
    print(stages[MAX_ATTEMPTS - attempts_left])
    

def get_user_guess(guessed_letters: Set[str], used_letters: Set[str], secret_word: str) -> str:
    """Ввод и валидация буквы от пользователя"""
    while True:
        letter = input("Введите букву: ").upper()
        
        if len(letter) != 1 or not letter.isalpha():
            print("Допустим ввод только одной буквы.")
            continue
                
        if letter in used_letters:
            print(f"Буква '{letter}' уже была использована.")
            continue
            
        used_letters.add(letter)
        return letter
            
            
def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    return all(letter in guessed_letters for letter in secret_word)

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    return (MAX_ATTEMPTS - attempts_used) * len(secret_word)

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"] += 1
    stats["total_score"] += score
    
    if won:
        stats["games_won"] += 1
        if score > stats["best_score"]:
            stats["best_score"] = score

def show_stats():
    """Отображение статистики"""
    global stats
    win_percentage = (stats["games_won"] / stats["games_played"] * 100) if stats["games_played"] > 0 else 0
    average_score = (stats["total_score"] / stats["games_won"]) if stats["games_won"] > 0 else 0
    
    print("\n=== Статистика ===")
    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {stats['best_score']}")
    print(f"Средний счет: {average_score:.1f}" if stats["games_won"] > 0 else "Средний счет: N/A")

if __name__ == "__main__":
    main()