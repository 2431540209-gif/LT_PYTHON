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

# Import siêu ngắn gọn nhờ re-export từ src/__init__.py
from src import (
    WIDTH, HEIGHT, FPS, PLAYER_SPEED,
    CELL, MAZE_COLS, MAZE_ROWS, START_CELL, FINISH_CELL,
    generate_maze, build_walls_from_maze, cell_center, cell_rect,
    try_move, draw_game,
    get_hud_restart_btn_rect, get_overlay_restart_btn_rect
)


class MazeGame:
    """Lớp quản lý trạng thái và vòng lặp trò chơi Mê Cung."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Game - Mê Cung")
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("segoeui", 34, bold=True)
        self.font_small = pygame.font.SysFont("segoeui", 19, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 14)

        # Khởi tạo ván chơi đầu tiên
        self.restart()

    def restart(self):
        """Khởi tạo màn chơi mới (không cần dùng nonlocal)."""
        passages = generate_maze(MAZE_COLS, MAZE_ROWS)
        self.walls = build_walls_from_maze(passages, MAZE_COLS, MAZE_ROWS)

        player_size = int(CELL - 20)
        self.player_rect = pygame.Rect(0, 0, player_size, player_size)
        self.player_rect.center = cell_center(*START_CELL)

        self.start_r = cell_rect(*START_CELL)
        self.finish_r = cell_rect(*FINISH_CELL)

        self.start_time = time.time()
        self.finished = False
        self.finish_time = 0.0

    def run(self):
        """Vòng lặp chính của trò chơi."""
        running = True
        while running:
            self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()

            # 1. Xử lý sự kiện (phím / chuột)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Xử lý click chuột
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if get_hud_restart_btn_rect().collidepoint(event.pos):
                        self.restart()
                    elif self.finished and get_overlay_restart_btn_rect().collidepoint(event.pos):
                        self.restart()

                # Xử lý nhấn phím
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # Kiểm tra phím R toàn diện (scancode phần cứng, keycode, unicode, space/enter khi win)
                    is_r_key = (
                        getattr(event, "scancode", None) == pygame.KSCAN_R or
                        event.key == pygame.K_r or
                        getattr(event, "unicode", "").lower() == "r" or
                        (self.finished and event.key in (pygame.K_SPACE, pygame.K_RETURN))
                    )

                    if is_r_key:
                        self.restart()

            # 2. Cập nhật di chuyển nếu chưa hoàn thành
            if not self.finished:
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

                self.player_rect = try_move(self.player_rect, dx, dy, self.walls)

                if self.player_rect.colliderect(self.finish_r):
                    self.finished = True
                    self.finish_time = time.time() - self.start_time

                elapsed = time.time() - self.start_time
            else:
                elapsed = self.finish_time

            # 3. Vẽ toàn bộ giao diện màn hình
            draw_game(
                self.screen, self.walls, self.player_rect, elapsed, self.finished,
                self.font_big, self.font_small, self.font_btn,
                self.start_r, self.finish_r, mouse_pos
            )

        pygame.quit()
        sys.exit()


def main():
    """Hàm khởi chạy game."""
    game = MazeGame()
    game.run()


if __name__ == "__main__":
    main()
