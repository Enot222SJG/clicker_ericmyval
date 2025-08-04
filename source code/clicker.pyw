import pgzrun
from pygame.transform import scale
import pygame
import os
import sys
import time

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)

WIDTH = 1200
HEIGHT = 676
TITLE = "Кликер По Жопке Эрика"
FPS = 120

# Загрузка изображений
try:
    # Основной фон
    fon = Actor(resource_path(os.path.join("images", "fon.png")))
    fon._surf = scale(fon._surf, (WIDTH, HEIGHT))
    
    # Фон победы и меню
    win_fon = Actor(resource_path(os.path.join("images", "win_fon.png")))
    win_fon._surf = scale(win_fon._surf, (WIDTH, HEIGHT))
    
    # Персонажи и элементы интерфейса
    enemy = Actor(resource_path(os.path.join("images", "popa.png")), pos=(600, 338))
    enemy._surf = scale(enemy._surf, (512, 512))
    
    bonus_1 = Actor(resource_path(os.path.join("images", "bonus1.png")), (100, 100))
    bonus_2 = Actor(resource_path(os.path.join("images", "bonus2.png")), (100, 200))
    bonus_3 = Actor(resource_path(os.path.join("images", "bonus3.png")), (100, 300))
    button_menu = Actor(resource_path(os.path.join("images", "button_menu.png")), (600, 450))
    
    # Кнопки меню
    button_game = Actor(resource_path(os.path.join("images", "button_menu.png")), (600, 300))
    button_gallery = Actor(resource_path(os.path.join("images", "button_menu.png")), (600, 400))
    
    # Персонажи для галереи (расположены строго по центру)
    gallery_monsters = [
        Actor(resource_path(os.path.join("images", "popa.png")), (WIDTH//2 + 200, 550)),
        Actor(resource_path(os.path.join("images", "popa_2.png")), (WIDTH//2 + 0, 400)),
        Actor(resource_path(os.path.join("images", "popa_3.png")), (WIDTH//2 + 160, 400)),
        Actor(resource_path(os.path.join("images", "popa_4.png")), (WIDTH//2 + 350, 400))
    ]    
    # Масштабируем всех монстров в галерее
    for monster in gallery_monsters:
        monster._surf = scale(monster._surf, (150, 150))
    
    # Кнопка возврата в меню для галереи
    button_menu_2 = Actor(resource_path(os.path.join("images", "button_menu.png")), (WIDTH//2, HEIGHT - 150))
except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    raise

# Игровые переменные
count = 0
hp = 100
max_hp = 100
damage = 1
game_over = False
current_stage = 1
enemy_images = ['popa.png', 'popa_2.png', 'popa_3.png', 'popa_4.png']
enemy_colors = ["#DC143C", "#4B0082", "#006400", "#00008B"]
bg_colors = ["#FFE4B5", "#E6E6FA", "#98FB98", "#ADD8E6"]

# Режимы игры
mode = "menu"  # "menu", "game" или "gallery"

# Цены бонусов
price1 = 50
price2 = 150
price3 = 400
price_multiplier = 1.5

def load_enemy_image(image_name):
    try:
        enemy.image = image_name
        enemy._surf = scale(pygame.image.load(resource_path(os.path.join("images", image_name))), (512, 512))
    except Exception as e:
        print(f"Ошибка загрузки изображения врага: {e}")
        enemy.image = 'popa.png'
        enemy._surf = scale(pygame.image.load(resource_path(os.path.join("images", "popa.png"))), (512, 512))

def next_stage():
    global hp, max_hp, current_stage, game_over
    
    if current_stage < len(enemy_images):
        current_stage += 1
        if current_stage == 2:
            hp = max_hp = 250
        elif current_stage == 3:
            hp = max_hp = 400
        elif current_stage == 4:
            hp = max_hp = 666
        
        try:
            load_enemy_image(enemy_images[current_stage-1])
        except IndexError:
            print("Ошибка: нет изображения для этого уровня")
            game_over = True
    else:
        game_over = True

def draw():
    if mode == "menu":
        # Экран меню
        win_fon.draw()
        
        # Кнопки меню
        button_game.draw()
        screen.draw.text("Играть", 
                       center=(600, 300),
                       color="white",
                       fontsize=30,
                       bold=True,
                       owidth=1.0,
                       ocolor="black")
        
        button_gallery.draw()
        screen.draw.text("Коллекция", 
                       center=(600, 400),
                       color="white",
                       fontsize=30,
                       bold=True,
                       owidth=1.0,
                       ocolor="black")
        
    elif mode == "gallery":
        # Экран галереи
        win_fon.draw()
        
        # Название галереи
        screen.draw.text("Коллекция жопок Эрика", 
                       center=(WIDTH//2, 100),
                       color="white",
                       fontsize=50,
                       owidth=0.5,
                       ocolor="black",
                       shadow=(1,1),
                       scolor="black")
        
        # Отрисовка всех монстров строго по центру экрана
        for monster in gallery_monsters:
            monster.draw()
        
        # Кнопка возврата в меню (внизу по центру)
        button_menu_2.draw()
        screen.draw.text("Вернуться в меню", 
                       center=(WIDTH//2, HEIGHT - 150),
                       color="white",
                       fontsize=30,
                       bold=True,
                       owidth=1.0,
                       ocolor="black")
        
    elif mode == "game":
        if not game_over:
            # Основной игровой экран
            fon.draw()
            enemy.draw()
            
            # Бонусы
            bonus_1.draw()
            screen.draw.text("Автоурон", (150, 80), color="black", fontsize=24)
            screen.draw.text(f"Цена: {int(price1)}", (150, 110), color="black", fontsize=24)

            bonus_2.draw()
            screen.draw.text("Автозаработок", (150, 180), color="black", fontsize=24)
            screen.draw.text(f"Цена: {int(price2)}", (150, 210), color="black", fontsize=24)

            bonus_3.draw()
            screen.draw.text("Супер заработок", (150, 280), color="black", fontsize=24)
            screen.draw.text(f"Цена: {int(price3)}", (150, 310), color="black", fontsize=24)

            # Статистика
            screen.draw.text(f"{int(hp)}/{max_hp}", center=(600, 200), 
                           color=enemy_colors[current_stage-1], 
                           fontsize=30, 
                           background=bg_colors[current_stage-1])
            screen.draw.text(str(int(count)), center=(1100, 50), color="black", fontsize=30)
            
            # Кнопка возврата в меню (дополнительное задание)
            screen.draw.text("Меню", 
                           center=(1100, 600),
                           color="white",
                           fontsize=30,
                           bold=True,
                           background="black")
        else:
            # Экран победы
            win_fon.draw()
            
            # Поздравительный текст
            screen.draw.text("Вы зажмакали все жопки Эрика!!", 
                           center=(WIDTH//2, HEIGHT//2 - 50),
                           color="white", 
                           fontsize=50,
                           owidth=0.5,
                           ocolor="black",
                           shadow=(1,1),
                           scolor="black")
            
            # Кнопка меню
            button_menu.draw()
            screen.draw.text("Вернуться в меню", 
                           center=(600, 450),
                           color="white",
                           fontsize=30,
                           bold=True,
                           owidth=1.0,
                           ocolor="black")

def on_mouse_down(pos, button):
    global count, hp, price1, price2, price3, mode
    
    if mode == "menu":
        if button == mouse.LEFT and button_game.collidepoint(pos):
            mode = "game"
            # Сброс игры при начале новой
            reset_game()
        elif button == mouse.LEFT and button_gallery.collidepoint(pos):
            mode = "gallery"
    
    elif mode == "gallery":
        if button == mouse.LEFT and button_menu_2.collidepoint(pos):
            mode = "menu"
    
    elif mode == "game":
        if game_over:
            if button == mouse.LEFT and button_menu.collidepoint(pos):
                mode = "menu"
            return
        
        # Дополнительное задание - кнопка возврата в меню
        if button == mouse.LEFT and 1050 <= pos[0] <= 1150 and 580 <= pos[1] <= 620:
            mode = "menu"
            return
        
        if button == mouse.LEFT and enemy.collidepoint(pos):
            count += 1
            hp -= damage
            if hp <= 0:
                hp = 0
                next_stage()
            animate(enemy, tween='bounce_end', duration=0.5, y=338)

        if button == mouse.LEFT and bonus_1.collidepoint(pos):
            if count >= price1:
                count -= price1
                price1 = int(price1 * price_multiplier)
                clock.schedule_interval(for_bonus_1, 2)
                animate(bonus_1, tween='bounce_end', duration=0.3, y=100)

        if button == mouse.LEFT and bonus_2.collidepoint(pos):
            if count >= price2:
                count -= price2
                price2 = int(price2 * price_multiplier)
                clock.schedule_interval(for_bonus_2, 2)
                animate(bonus_2, tween='bounce_end', duration=0.3, y=200)

        if button == mouse.LEFT and bonus_3.collidepoint(pos):
            if count >= price3:
                count -= price3
                price3 = int(price3 * price_multiplier)
                clock.schedule_interval(for_bonus_3, 5)
                animate(bonus_3, tween='bounce_end', duration=0.3, y=300)

def reset_game():
    global count, hp, max_hp, damage, game_over, current_stage, price1, price2, price3
    count = 0
    hp = max_hp = 100
    damage = 1
    game_over = False
    current_stage = 1
    price1 = 50
    price2 = 175
    price3 = 300
    load_enemy_image(enemy_images[0])
    # Отмена всех запланированных интервалов
    clock.unschedule(for_bonus_1)
    clock.unschedule(for_bonus_2)
    clock.unschedule(for_bonus_3)

def for_bonus_1():
    global hp
    if not game_over and mode == "game":
        hp -= 1
        if hp <= 0:
            hp = 0
            next_stage()

def for_bonus_2():
    global count
    if not game_over and mode == "game":
        count += 5

def for_bonus_3():
    global count
    if not game_over and mode == "game":
        count += 10

pgzrun.go()