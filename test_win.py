import pygame


# Инициализация Pygame
pygame.init()

# Установка размера окна
size = (800, 600)
screen = pygame.display.set_mode(size)

# Установка заголовка окна
pygame.display.set_caption("Ввод текста на кириллице")

# Загрузка шрифта с поддержкой кириллицы
font_path = 'comicsans'  # Путь к шрифту, поддерживающему кириллицу
font_size = 36
font = pygame.font.SysFont("comicsans", font_size)

# Цвет текста
text_color = (255, 255, 255)  # Белый цвет

# Переменная для хранения введенного текста
input_text = ""

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter для завершения ввода
                print("Введенный текст:", input_text)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:  # Backspace для удаления символа
                input_text = input_text[:-1]
            else:
                input_text += event.unicode  # Добавление символа в строку

    # Очистка экрана
    screen.fill((0, 0, 0))  # Черный цвет фона

    # Рендеринг текста
    text_surface = font.render(input_text, True, text_color)

    # Отображение текста
    screen.blit(text_surface, (50, 50))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()