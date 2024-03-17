import pygame
import random
from tkinter import TclError

def arcanoid(window, window_game_menu):
    global screen_width, screen_height, BLACK, WHITE, BLUE, RED, screen, clock, paddle_width, paddle_height, paddle_x, paddle_y, paddle, ball_height, ball_width, ball_x, ball_y, ball, ball_speed_y, ball_speed_x, block_height, block_width, num_blocks, blocks, prompt

    try:
        window_game_menu.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()
    except TclError:
        window.deiconify()

    # Инициализация Pygame
    pygame.init()

    # Размеры окна игры
    screen_width = 800
    screen_height = 600

    # Цвета
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    # Создание окна игры
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption("Арканоид")

    clock = pygame.time.Clock()

    # Определение платформы (прямоугольник)
    paddle_width = 100
    paddle_height = 10
    paddle_x = screen_width // 2 - paddle_width // 2
    paddle_y = screen_height - 20

    paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

    # Определение шарика (прямоугольник)
    ball_width = 10
    ball_height = 10
    ball_x = screen_width // 2 - ball_width // 2
    ball_y = screen_height // 2 - ball_height // 2

    ball = pygame.Rect(ball_x, ball_y, ball_width, ball_height)
    ball_speed_x = random.choice([-3, 3])
    ball_speed_y = -3

    # Определение блоков
    block_width = 60
    block_height = 20
    num_blocks = 40
    blocks = []

    for i in range(num_blocks):
        block_x = 85 + (i % 10) * (block_width + 10)
        block_y = 50 + (i // 10) * (block_height + 10)
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        blocks.append(block)

    # Функция для отображения сообщения об окончании игры
    def game_over():
        font = pygame.font.Font(None, 36)
        text1 = font.render("Игра окончена", True, WHITE)
        text2 = font.render("Нажмите Q чтобы выйти или C чтобы начать новую игру", True, WHITE)
        text_rect1 = text1.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        text_rect2 = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        pygame.display.flip()

    # Основной игровой цикл
    running = True
    game_over_flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.x -= 6
        if keys[pygame.K_RIGHT]:
            paddle.x += 6

        if paddle.x < 0:
            paddle.x = 0
        if paddle.x > screen_width - paddle.width:
            paddle.x = screen_width - paddle.width

        if not game_over_flag:
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.x < 0 or ball.x > screen_width - ball.width:
                ball_speed_x *= -1
            if ball.y < 0:
                ball_speed_y *= -1

            if ball.colliderect(paddle):
                ball_speed_y *= -1

            for block in blocks[:]:
                if ball.colliderect(block):
                    ball_speed_y *= -1
                    blocks.remove(block)

            if ball.y > screen_height:
                game_over_flag = True

        screen.fill(BLACK)

        pygame.draw.rect(screen, BLUE, paddle)

        # Отображение шарика
        pygame.draw.circle(screen, RED, (ball.x + ball.width // 2, ball.y + ball.height // 2), ball.width // 2)

        for block in blocks:
            pygame.draw.rect(screen, WHITE, block)

        if game_over_flag:
            game_over()

        pygame.display.flip()
        clock.tick(60)

        # Новая игра
        if game_over_flag:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                running = False
                try:
                    window_game_menu.deiconify()
                except NameError:
                    window.deiconify()
            elif keys[pygame.K_c]:
                game_over_flag = False
                paddle.x = screen_width // 2 - paddle_width // 2
                ball.x = screen_width // 2 - ball_width // 2
                ball.y = screen_height // 2 - ball_height // 2
                ball_speed_x = random.choice([-3, 3])
                ball_speed_y = -3
                blocks = []
                for i in range(num_blocks):
                    block_x = 85 + (i % 10) * (block_width + 10)
                    block_y = 50 + (i // 10) * (block_height + 10)
                    block = pygame.Rect(block_x, block_y, block_width, block_height)
                    blocks.append(block)

    pygame.quit()