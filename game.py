import random
import os
import json
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 6
# WORDS = [
#     "ПРОГРАММИРОВАНИЕ", "АЛГОРИТМ", "КОМПЬЮТЕР", "ВИСЕЛИЦА", 
#     "СТУДЕНТ", "УНИВЕРСИТЕТ", "ЛЕКЦИЯ", "ПРАКТИКА", 
#     "ПИТОН", "КОД", "ФУНКЦИЯ", "ПЕРЕМЕННАЯ", "ЦИКЛ", 
#     "УСЛОВИЕ", "СПИСОК", "СЛОВАРЬ", "МНОЖЕСТВО"
# ]

STATS_FILE = "hangman_stats.json"
WORDS_FILE = "hangman_words.txt"

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
    load_stats()
    
    # Загрузка слов из файла, если он существует
    words = load_words()
    
    while True:
        # Выбор случайного слова
        secret_word = choose_random_word(words)
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
            if guess not in secret_word:
                attempts_left -= 1
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        
        clear_console()
        attempts_used = MAX_ATTEMPTS - attempts_left
        
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            score = calculate_score(secret_word, attempts_used)
            print(f"Ваш счет: {score}")
            update_stats(True, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            update_stats(False, 0)
            draw_gallows(0)
        
        show_stats()
        save_stats()
        
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            break

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_words() -> List[str]:
    """Загрузка слов из файла, если он существует"""
    if os.path.exists(WORDS_FILE):
        try:
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                all_words = []  # Здесь будем хранить все слова
                
                # Читаем файл построчно
                for line in f:
                    # Разбиваем строку на отдельные слова по пробелам
                    words_in_line = line.strip().split()
                    
                    # Добавляем все слова из этой строки в общий список
                    for word in words_in_line:
                        clean_word = word.strip().upper()
                        if clean_word:  # Если слово не пустое
                            all_words.append(clean_word)
                
                # Если нашли слова - возвращаем их
                if all_words:
                    return all_words
                    
        except:
            print(f"Ошибка при чтении файла {WORDS_FILE}, используются стандартные слова")
    
    # Если что-то пошло не так - возвращаем стандартные слова
    return WORDS

def load_stats():
    """Загрузка статистики из файла"""
    global stats
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                loaded_stats = json.load(f)
                stats.update(loaded_stats)
        except:
            print("Не удалось загрузить статистику, используется новая статистика")

def save_stats():
    """Сохранение статистики в файл"""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except:
        print("Не удалось сохранить статистику")

def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)

def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""
    result = []
    for letter in secret_word:
        if letter in guessed_letters:
            result.append(letter)
        else:
            result.append("_")
    return " ".join(result)

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    stages = [
        # 0 попыток - проигрыш
        """
        __________
        |      |
        |      O
        |     \\|/
        |      |
        |     / \\
        |_________
        """,
        # 1 попытка
        """
        __________
        |      |
        |      O
        |     \\|/
        |      |
        |     / 
        |_________
        """,
        # 2 попытки
        """
        __________
        |      |
        |      O
        |     \\|/
        |      |
        |      
        |_________
        """,
        # 3 попытки
        """
        __________
        |      |
        |      O
        |     \\|
        |      |
        |      
        |_________
        """,
        # 4 попытки
        """
        __________
        |      |
        |      O
        |      |
        |      |
        |      
        |_________
        """,
        # 5 попыток
        """
        __________
        |      |
        |      O
        |      
        |      
        |      
        |_________
        """,
        # 6 попыток - начало игры
        """
        __________
        |      |
        |      
        |      
        |      
        |      
        |_________
        """
    ]
    print(stages[attempts_left])

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    while True:
        guess = input("Введите букву: ").upper()
        
        if len(guess) != 1:
            print("Пожалуйста, введите только одну букву!")
            continue
            
        if not guess.isalpha():
            print("Пожалуйста, введите букву!")
            continue
            
        if guess in guessed_letters:
            print("Вы уже вводили эту букву!")
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
    base_score = len(secret_word) * 10
    attempts_bonus = (MAX_ATTEMPTS - attempts_used) * 5
    return base_score + attempts_bonus

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
    
    if stats["games_played"] == 0:
        print("\n=== Статистика ===")
        print("Статистика пока недоступна")
        return
    
    win_percentage = (stats["games_won"] / stats["games_played"]) * 100 if stats["games_played"] > 0 else 0
    average_score = stats["total_score"] / stats["games_won"] if stats["games_won"] > 0 else 0
    
    print("\n=== Статистика ===")
    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {stats['best_score']}")
    
    if stats["games_won"] > 0:
        print(f"Средний счет: {average_score:.1f}")

if __name__ == "__main__":
    main()