"""
Module xử lý di chuyển và kiểm tra va chạm của nhân vật với các bức tường.
"""

import pygame


def try_move(player_rect, dx, dy, walls):
    """
    Thử di chuyển player theo (dx, dy).
    Kiểm tra va chạm với TẤT CẢ các tường trên từng trục riêng biệt (X, Y).
    Nếu va chạm → đẩy player dừng ngay sát mép tường.
    """
    new_rect = player_rect.copy()

    # --- Trục X ---
    if dx != 0:
        new_rect.x += dx
        for wall in walls:
            if new_rect.colliderect(wall):
                if dx > 0:
                    new_rect.right = wall.left
                else:
                    new_rect.left = wall.right

    # --- Trục Y ---
    if dy != 0:
        new_rect.y += dy
        for wall in walls:
            if new_rect.colliderect(wall):
                if dy > 0:
                    new_rect.bottom = wall.top
                else:
                    new_rect.top = wall.bottom

    return new_rect
