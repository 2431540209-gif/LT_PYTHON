"""
Module hiển thị giao diện người dùng (UI), các nút bấm và vẽ đồ họa game.
"""

import time
import pygame
from src.config import (
    WIDTH, HEIGHT, HUD_H, CELL, WALL_THICK, MAZE_COLS, MAZE_ROWS,
    COLOR_BG, COLOR_WALL, COLOR_WALL_EDGE, COLOR_PLAYER, COLOR_PLAYER_EDGE,
    COLOR_START, COLOR_FINISH, COLOR_FINISH_GLOW, COLOR_TEXT, COLOR_TEXT_SHADOW,
    COLOR_OVERLAY, COLOR_PATH, COLOR_HUD_BG
)


def draw_text_centered(surface, font, text, center, color, shadow=True):
    """Vẽ text căn giữa có hiệu ứng bóng đổ."""
    if shadow:
        s = font.render(text, True, COLOR_TEXT_SHADOW)
        surface.blit(s, s.get_rect(center=(center[0] + 2, center[1] + 2)))
    t = font.render(text, True, color)
    surface.blit(t, t.get_rect(center=center))


def get_hud_restart_btn_rect():
    """Tọa độ nút Chơi lại trên thanh HUD."""
    btn_w, btn_h = 130, 28
    return pygame.Rect(WIDTH - btn_w - 10, (HUD_H - btn_h) // 2, btn_w, btn_h)


def get_overlay_restart_btn_rect():
    """Tọa độ nút Chơi lại trên màn hình Hoàn thành."""
    btn_w, btn_h = 240, 44
    return pygame.Rect((WIDTH - btn_w) // 2, HEIGHT // 2 + 55, btn_w, btn_h)


def draw_game(screen, walls, player_rect, elapsed, finished,
              font_big, font_small, font_btn, start_r, finish_r, mouse_pos):
    """Vẽ toàn bộ khung hình màn chơi game."""
    screen.fill(COLOR_BG)

    # 1. Thanh HUD background
    pygame.draw.rect(screen, COLOR_HUD_BG, (0, 0, WIDTH, HUD_H))
    pygame.draw.line(screen, COLOR_WALL, (0, HUD_H), (WIDTH, HUD_H), 2)

    # 2. Nền lưới ô trống (path)
    off_x = WALL_THICK // 2
    off_y = HUD_H + WALL_THICK // 2
    for r in range(MAZE_ROWS):
        for c in range(MAZE_COLS):
            rect = pygame.Rect(off_x + c * CELL, off_y + r * CELL, CELL, CELL)
            pygame.draw.rect(screen, COLOR_PATH, rect)

    # 3. Điểm START
    pygame.draw.rect(screen, COLOR_START, start_r, border_radius=4)
    draw_text_centered(screen, font_small, "S", start_r.center,
                       COLOR_BG, shadow=False)

    # 4. Điểm FINISH (có hiệu ứng nhấp nháy phát sáng)
    pulse = int(time.time() * 3) % 2
    fc = COLOR_FINISH if pulse == 0 else COLOR_FINISH_GLOW
    pygame.draw.rect(screen, fc, finish_r, border_radius=4)
    draw_text_centered(screen, font_small, "F", finish_r.center,
                       (255, 255, 255), shadow=False)

    # 5. Các bức tường
    for wall in walls:
        pygame.draw.rect(screen, COLOR_WALL, wall)
        pygame.draw.rect(screen, COLOR_WALL_EDGE, wall, 1)

    # 6. Nhân vật (Player)
    pygame.draw.rect(screen, COLOR_PLAYER, player_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_PLAYER_EDGE, player_rect, 2, border_radius=6)

    # 7. Thông tin thời gian trên HUD
    if not finished:
        time_text = f"Thời gian: {elapsed:.1f}s"
    else:
        time_text = f"Hoàn thành: {elapsed:.1f}s"
    time_surf = font_small.render(time_text, True, COLOR_TEXT)
    screen.blit(time_surf, (15, (HUD_H - time_surf.get_height()) // 2))

    # 8. Nút "Chơi lại (R)" trên thanh HUD
    hud_btn = get_hud_restart_btn_rect()
    hud_hover = hud_btn.collidepoint(mouse_pos)
    hud_btn_col = (55, 75, 120) if hud_hover else (38, 48, 75)
    pygame.draw.rect(screen, hud_btn_col, hud_btn, border_radius=5)
    pygame.draw.rect(screen, COLOR_WALL, hud_btn, 1, border_radius=5)
    draw_text_centered(screen, font_btn, "Chơi lại (R)", hud_btn.center,
                       (220, 230, 255), shadow=False)

    # 9. Màn hình chiến thắng (Overlay khi hoàn thành)
    if finished:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        screen.blit(overlay, (0, 0))

        draw_text_centered(screen, font_big,
                           "HOÀN THÀNH!",
                           (WIDTH // 2, HEIGHT // 2 - 45),
                           COLOR_PLAYER)
        draw_text_centered(screen, font_big,
                           f"Thời gian: {elapsed:.2f} giây",
                           (WIDTH // 2, HEIGHT // 2 + 5),
                           COLOR_TEXT)

        # Nút chơi lại lớn
        over_btn = get_overlay_restart_btn_rect()
        over_hover = over_btn.collidepoint(mouse_pos)
        over_btn_col = (45, 140, 90) if over_hover else (35, 110, 70)
        pygame.draw.rect(screen, over_btn_col, over_btn, border_radius=8)
        pygame.draw.rect(screen, COLOR_PLAYER, over_btn, 2, border_radius=8)
        draw_text_centered(screen, font_small, "Chơi lại (R / Click)", over_btn.center,
                           (255, 255, 255), shadow=False)

        draw_text_centered(screen, font_btn,
                           "Nhấn ESC để thoát",
                           (WIDTH // 2, HEIGHT // 2 + 115),
                           (160, 160, 175))

    pygame.display.flip()
