"""
Game Mê Cung - Maze Game
=========================
File chính (Entry point) điều khiển vòng lặp và logic game.
- Di chuyển nhân vật (ô xanh lá) từ START đến FINISH.
- Dùng phím mũi tên hoặc WASD để di chuyển.
- Nhấn R để chơi lại (mê cung mới), ESC để thoát.
"""

import sys
import time
import pygame

from src.config import (
    WIDTH, HEIGHT, FPS, PLAYER_SPEED,
    CELL, MAZE_COLS, MAZE_ROWS, START_CELL, FINISH_CELL
)
from src.maze import (
    generate_maze,
    build_walls_from_maze,
    cell_center,
    cell_rect
)
from src.player import try_move
from src.ui import (
    draw_game,
    get_hud_restart_btn_rect,
    get_overlay_restart_btn_rect
)


def new_game():
    """Tạo màn chơi mới: sinh mê cung, tính vị trí player và start/finish."""
    passages = generate_maze(MAZE_COLS, MAZE_ROWS)
    walls = build_walls_from_maze(passages, MAZE_COLS, MAZE_ROWS)

    player_size = int(CELL * 0.55)
    player_rect = pygame.Rect(0, 0, player_size, player_size)
    player_rect.center = cell_center(*START_CELL)

    start_r = cell_rect(*START_CELL)
    finish_r = cell_rect(*FINISH_CELL)

    return walls, player_rect, start_r, finish_r


def main():
    """Vòng lặp chính của trò chơi."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game - Mê Cung")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("segoeui", 34, bold=True)
    font_small = pygame.font.SysFont("segoeui", 19, bold=True)
    font_btn = pygame.font.SysFont("segoeui", 14)

    walls, player_rect, start_r, finish_r = new_game()
    start_time = time.time()
    finished = False
    finish_time = 0.0

    def restart():
        nonlocal walls, player_rect, start_r, finish_r, start_time, finished, finish_time
        walls, player_rect, start_r, finish_r = new_game()
        start_time = time.time()
        finished = False
        finish_time = 0.0

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Xử lý click chuột
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if get_hud_restart_btn_rect().collidepoint(event.pos):
                    restart()
                elif finished and get_overlay_restart_btn_rect().collidepoint(event.pos):
                    restart()

            # Xử lý nhấn phím
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Kiểm tra phím R toàn diện (scancode phần cứng, keycode, unicode, space/enter khi win)
                is_r_key = (
                    getattr(event, "scancode", None) == pygame.KSCAN_R or
                    event.key == pygame.K_r or
                    getattr(event, "unicode", "").lower() == "r" or
                    (finished and event.key in (pygame.K_SPACE, pygame.K_RETURN))
                )

                if is_r_key:
                    restart()

        # Cập nhật di chuyển nếu chưa hoàn thành
        if not finished:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = PLAYER_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = PLAYER_SPEED

            player_rect = try_move(player_rect, dx, dy, walls)

            if player_rect.colliderect(finish_r):
                finished = True
                finish_time = time.time() - start_time

            elapsed = time.time() - start_time
        else:
            elapsed = finish_time

        # Vẽ giao diện
        draw_game(screen, walls, player_rect, elapsed, finished,
                  font_big, font_small, font_btn, start_r, finish_r, mouse_pos)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
