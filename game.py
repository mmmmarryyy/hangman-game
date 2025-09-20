import random
import os
from typing import List, Set


# Константы и данные
RUSSIAN_LETTERS = set('абвгдежзийклмнопрстуфхцчшщъыьэюя'
                       'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
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
            
            new_letter = get_user_guess(guessed_letters)
            if new_letter in secret_word:
                print(f"В слове есть буква \"{new_letter}\"!")
            else:
                print(f"В слове нет буквы \"{new_letter}\"")
                attempts_left -= 1

            guessed_letters.add(new_letter)
            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        clear_console()
        score = calculate_score(secret_word, MAX_ATTEMPTS-attempts_left)
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            print(f"Ваш счет: {score}")
            update_stats(True, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            update_stats(False, score)
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
    mask = ""
    for letter in secret_word:
        if letter in guessed_letters:
            mask += letter
        else:
            mask += "_"
        mask += " "
    return mask

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
        """,
        """
           --------
           |      
           |      
           |      
           |      
           |      
           -
        """
    ]
    
    print(stages[min(attempts_left, 5)])
    

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    
    print("Попробуйте угадать букву из загаданного слова")
    while(True):
        users_input = input().upper()
        if len(users_input) != 1:
            print("Пожалуйста введите только одну букву")
        elif users_input[0] not in RUSSIAN_LETTERS:
            print("Неизвестный символ, введите букву из русского алфавита")
        elif users_input[0] in guessed_letters:
            print("Вы уже пробовали эту букву, введите другую")
        else:
            break
    return users_input[0]

def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    if all(letter in guessed_letters for letter in secret_word):
        return 1
    return 0

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    if (attempts_used != MAX_ATTEMPTS):
        return (len(secret_word)*2 - attempts_used)
    else:
        return 0
def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"] += 1
    stats["games_won"] += won
    stats["total_score"] += score
    stats["best_score"] = max(stats["best_score"], score)

def show_stats():
    """Отображение статистики"""
    global stats
    win_percentage = 100 * stats["games_won"] / stats["games_played"]
    average_score = stats["total_score"] / stats["games_played"]
    
    print("\n=== Статистика ===")
    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {stats["best_score"]}")
    if stats["games_won"] > 0:
        print(f"Средний счет: {average_score}")

if __name__ == "__main__":
    main()