"""
Module thuật toán sinh mê cung và chuyển đổi thành tường trong game.
"""

import random
import pygame
from src.config import CELL, WALL_THICK, HUD_H


def generate_maze(cols, rows):
    """
    Sinh mê cung cols x rows ô bằng DFS (Recursive Backtracking với Stack).
    Trả về tập hợp các cạnh đã MỞ (passages) giữa 2 ô kề nhau.
    Mỗi ô: (col, row). Mỗi cạnh: frozenset({(c1,r1), (c2,r2)}).
    Đảm bảo mọi ô đều đến được từ mọi ô khác (perfect maze).
    """
    visited = set()
    passages = set()

    # Dùng stack thay vì đệ quy để tránh tràn stack với mê cung lớn
    stack = [(0, 0)]
    visited.add((0, 0))

    while stack:
        c, r = stack[-1] # Lấy ô mới nhất vừa được thêm vào
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)] #⬆️⬇️⬅️➡️
        random.shuffle(dirs)
        found = False

        for dc, dr in dirs:
            nc, nr = c + dc, r + dr
            if 0 <= nc < cols and 0 <= nr < rows and (nc, nr) not in visited:
                visited.add((nc, nr))
                passages.add(frozenset({(c, r), (nc, nr)}))
                stack.append((nc, nr))
                found = True
                break

        if not found:
            stack.pop()

    return passages


def build_walls_from_maze(passages, cols, rows):
    """
    Chuyển đổi mê cung (tập passages) thành danh sách pygame.Rect (tường).
    Mỗi tường là 1 hình chữ nhật mỏng nằm giữa 2 ô hoặc ở viền ngoài.
    """
    walls = []
    T = CELL
    W = WALL_THICK
    off_x = W // 2           # offset x cho lưới
    off_y = HUD_H + W // 2   # offset y (dưới HUD)

    # --- Viền ngoài (4 cạnh) ---
    # Trên
    walls.append(pygame.Rect(off_x - W // 2, off_y - W // 2, # // là chia lấy nguyên
                             cols * T + W, W))
    # Dưới
    walls.append(pygame.Rect(off_x - W // 2, off_y + rows * T - W // 2,
                             cols * T + W, W))
    # Trái
    walls.append(pygame.Rect(off_x - W // 2, off_y - W // 2,
                             W, rows * T + W))
    # Phải
    walls.append(pygame.Rect(off_x + cols * T - W // 2, off_y - W // 2,
                             W, rows * T + W))

    # --- Tường bên trong ---
    # Tường dọc: giữa cột c và c+1, hàng r
    for c in range(cols - 1):
        for r in range(rows):
            edge = frozenset({(c, r), (c + 1, r)})
            if edge not in passages:
                wx = off_x + (c + 1) * T - W // 2
                wy = off_y + r * T - W // 2
                walls.append(pygame.Rect(wx, wy, W, T + W))

    # Tường ngang: giữa hàng r và r+1, cột c
    for r in range(rows - 1):
        for c in range(cols):
            edge = frozenset({(c, r), (c, r + 1)})
            if edge not in passages:
                wx = off_x + c * T - W // 2
                wy = off_y + (r + 1) * T - W // 2
                walls.append(pygame.Rect(wx, wy, T + W, W))

    return walls


def cell_center(col, row):
    """Trả về tọa độ pixel trung tâm của ô (col, row)."""
    off_x = WALL_THICK // 2
    off_y = HUD_H + WALL_THICK // 2
    return (off_x + col * CELL + CELL // 2,
            off_y + row * CELL + CELL // 2)


def cell_rect(col, row):
    """Trả về pygame.Rect của ô (col, row)."""
    off_x = WALL_THICK // 2
    off_y = HUD_H + WALL_THICK // 2
    return pygame.Rect(off_x + col * CELL, off_y + row * CELL, CELL, CELL)
