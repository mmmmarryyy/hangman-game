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
            # TODO: обработать ввод буквы (используй get_user_guess)

            # print("Введите букву")

            letter = get_user_guess(guessed_letters)
            guessed_letters.add(letter)
            
            # Проверка угадана ли буква
            # TODO: добавить реализацию проверки буквы (используй get_user_guess)

            if secret_word.count(letter) == 0:
                print("Этой буквы нет в слове")
                attempts_left -= 1
            else:
                print("Эта буква есть в слове")

            
            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        
        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            # score = TODO: получи с помощью функции счет (используй calculate_score)
            # print(f"Ваш счет: {score}")
            # TODO: обнови статистику (используй update_stats)

            score = calculate_score(secret_word, MAX_ATTEMPTS - attempts_left)
            print(f"Ваш счет: {score}")
            update_stats(True, score)
        else:
            print("ХАХАХАХАХАХАХ поздравляю ты лох")
            print(f"Загаданное слово: {secret_word}")
            # TODO: обнови статистику (используй update_stats)

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
    # TODO: реализовать генерацию в зависимости от угаданных букв

    masked_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            masked_word += letter
        else:
            masked_word += '*'
    return masked_word

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    # TODO: реализовать отрисовку (нужно вызвать print)
    # Подсказка:
    # """
        # --------
        # |      |
        # |      O
        # |     \|/
        # |      |
        # |     / \
        # -
        # """
    
    body_pieces = [
        """
        --------  
        |      |  
        |      O  
        |     \|/ 
        |      |  
        |     / \ 
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |     \|/ 
        |      |  
        |     / \ 
        -         
        """
        ,
        """
        --------  
        |      |  
        |     \ / 
        |         
        |     / \ 
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |     \   
        |         
        |     / \ 
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |         
        |     / \ 
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |         
        |     /   
        |         
        -         
        """
        ,
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

    print(body_pieces[attempts_left])
    

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    # TODO: проверять, что пользователь ввел только одну букву, что он не вводил уже эту букву и тд
    # Подсказка: не забывай про регистр

    while True:
        print("Введите букву")

        letter = input().upper()

        if letter in guessed_letters:
            print("Эта буква была введена ранее")
            continue
        if len(letter) != 1:
            print("Введено более одного символа")
            continue
        if not letter.isalpha():
            print("Введена не буква")
            continue

        return letter
        




def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    # TODO: реализовать проверку

    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True


    return sorted(set(secret_word)) == sorted(guessed_letters)

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    # TODO: необходимо, используя длину secret_word и количество попыток, посчитать счет

    return len(secret_word) + (MAX_ATTEMPTS - attempts_used)

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    # TODO: необходимо обновить stats

    stats["games_played"] += 1

    if won:
        stats["games_won"] += 1

        if score > stats["best_score"]:
            stats["best_score"] = score

        stats["total_score"] += score
    

def show_stats():
    """Отображение статистики"""
    global stats
    # win_percentage = TODO: посчитай на основе имеющейся статистики процент выигрыша
    # average_score = TODO: посчитай на основе имеющейся статистики средний счет

    win_percentage = stats["games_won"] / stats["games_played"] * 100
    average_score = stats["total_score"] / stats["games_played"]
    
    print("\n=== Статистика ===")
    # print(f"Всего игр: {TODO: количество игр}")
    # print(f"Побед: {TODO: количество побед} ({win_percentage:.1f}%)")
    # print(f"Лучший счет: {TODO: выведи лучший счет}")
    # TODO: выведи средний счет, если была хотя бы одна победа

    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счёт: {stats['best_score']}")
    if stats["games_won"] > 0:
        print(f"Средний счёт: {average_score:.1f}")

if __name__ == "__main__":
    main()

a = """
--------
|      |
|
|
|
|
-"""