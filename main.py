
import pygame as pg
import playsound as ps
from random import randrange

WINDOW = 1000
FPS = 60
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: (randrange(*RANGE), randrange(*RANGE))
pg.init()
pg.mixer.init()
death_sound = pg.mixer.Sound('snake_death.mp3')
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_direction = (0, 0)
time, time_to_move = 0, 110
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode((WINDOW, WINDOW))
clock = pg.time.Clock()
banned_dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            ps.playsound('snake_death.mp3')
            exit()
        if event.type == pg.KEYDOWN:
            if length == 1:
                if event.key == pg.K_UP:
                    snake_direction = (0, -TILE_SIZE)
                if event.key == pg.K_DOWN:
                    snake_direction = (0, TILE_SIZE)
                if event.key == pg.K_LEFT:
                    snake_direction = (-TILE_SIZE, 0)
                if event.key == pg.K_RIGHT:
                    snake_direction = (TILE_SIZE, 0)
            else:
                if event.key == pg.K_UP and banned_dirs[pg.K_UP]:
                    snake_direction = (0, -TILE_SIZE)
                    banned_dirs = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                if event.key == pg.K_DOWN and banned_dirs[pg.K_DOWN]:
                    snake_direction = (0, TILE_SIZE)
                    banned_dirs = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                if event.key == pg.K_LEFT and banned_dirs[pg.K_LEFT]:
                    snake_direction = (-TILE_SIZE, 0)
                    banned_dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
                if event.key == pg.K_RIGHT and banned_dirs[pg.K_RIGHT]:
                    snake_direction = (TILE_SIZE, 0)
                    banned_dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

            if event.key == pg.K_ESCAPE:
                death_sound.play()
                exit()
            if event.key == pg.K_SPACE:
                death_sound.play()
                print('You lost!')
    screen.fill((0, 0, 0))
    # check if snake is out of screen
    if not snake.colliderect(screen.get_rect()):
        ps.playsound('snake_death.mp3')
        exit()
    # check if snake eats food
    if snake.colliderect(food):
        length += 1
        food.center = get_random_position()
    # check if snake eats itself
    if snake.collidelist(segments[:-1]) != -1:
        ps.playsound('snake_death.mp3')
        exit()
    # draw food
    pg.draw.rect(screen, (255, 0, 0), food)
    # draw snake
    [pg.draw.rect(screen, (255, 255, 255), segment) for segment in segments]
    # move snake
    time_now= pg.time.get_ticks()
    if time_now - time > time_to_move:
        time = time_now
        snake.move_ip(snake_direction)
        segments.append(snake.copy())
        segments = segments[-length:]

    pg.display.flip()
    clock.tick(FPS)

