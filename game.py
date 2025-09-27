import random
import os
from typing import List, Set

# Список слов
WORDS = []

# Константы и данные
MAX_ATTEMPTS = 6

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
            print("Введите букву: ")
            user_letter = get_user_guess(guessed_letters)
            
            # Проверка угадана ли буква
            guessed_letters.add(user_letter)
            if user_letter in secret_word:
                print(f"Верно! Буква {user_letter} есть в слове!")
            else:
                print(f"Вы ошиблись! Буквы {user_letter} нет в слове!")
                attempts_left -= 1
                
            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        
        clear_console()
        score = 0
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            score = calculate_score(secret_word, attempts_left)
            print(f"Ваш счет: {score}")
            update_stats(game_won, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            update_stats(game_won, score)
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
    # TODO: реализовать генерацию в зависимости от угаданных букв
    word = []
    for i in secret_word:
        if i in guessed_letters: word.append(i)
        else: word.append('_')
    return "".join(word)

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    stages = {
        6: """
--------
|      |
|       
|       
|       
|       
-       """,
        5: """
--------
|      |
|      O
|       
|       
|       
-       """,
        4: """
--------
|      |
|      O
|      |
|      |
|       
-       """,
        3: """
--------
|      |
|      O
|     \|
|      |
|       
-       """,
        2: """
--------
|      |
|      O
|     \|/
|      |
|       
-       """,
        1: """
--------
|      |
|      O
|     \|/
|      |
|     / 
-       """,
        0: """
--------
|      |
|      O
|     \|/
|      |
|     / \\
-       """,
    }
    print(stages[attempts_left])
    
def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    guess_letter = ''
    flag = False
    while flag == False:
        guess_letter = input().upper()
        if guess_letter.isalpha() and len(guess_letter) == 1 and guess_letter not in guessed_letters:
            flag = True
        else: print("Ошибка ввода! Повторите ввод.")
    return guess_letter

def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    cnt = 0
    for i in guessed_letters:
        if i in secret_word: cnt += secret_word.count(i)
    if cnt == len(secret_word): 
        return True
    else: 
        return False

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    return len(secret_word) * attempts_used * 100

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"] += 1
    if won: stats["games_won"] += 1
    stats["total_score"] += score
    if stats["best_score"] < score: stats["best_score"] = score

def show_stats():
    """Отображение статистики"""
    global stats
    win_percentage =  int(stats["games_won"] / stats["games_played"] * 100)
    average_score = stats["total_score"] // stats["games_played"]
    
    print("\n=== Статистика ===")
    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage}%)")
    print(f"Лучший счет: {stats['best_score']}")
    if stats["games_won"] > 0: print(f"Ваш средний счёт за игру: {average_score}")

def read_words(WORDS):
    with open("Words.txt", "r", encoding="utf-8") as f:
        for line in f:
            WORDS.append(line.strip())

if __name__ == "__main__":
    read_words(WORDS)
    main()