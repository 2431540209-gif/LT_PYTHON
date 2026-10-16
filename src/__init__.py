"""
Gói mã nguồn trò chơi Mê Cung (Maze Game)
Gom và tái xuất khẩu (Re-export) toàn bộ tài nguyên để các file khác import ngắn gọn.
"""

# 1. Cấu hình & Bảng màu
from src.config import (
    WIDTH, HEIGHT, FPS, PLAYER_SPEED,
    CELL, WALL_THICK, HUD_H,
    MAZE_COLS, MAZE_ROWS, START_CELL, FINISH_CELL,
    COLOR_BG, COLOR_WALL, COLOR_WALL_EDGE,
    COLOR_PLAYER, COLOR_PLAYER_EDGE, COLOR_START,
    COLOR_FINISH, COLOR_FINISH_GLOW, COLOR_TEXT,
    COLOR_TEXT_SHADOW, COLOR_OVERLAY, COLOR_PATH, COLOR_HUD_BG
)

# 2. Thuật toán sinh mê cung & tạo tường
from src.maze import (
    generate_maze,
    build_walls_from_maze,
    cell_center,
    cell_rect
)

# 3. Xử lý di chuyển & va chạm
from src.player import try_move

# 4. Giao diện & Vẽ đồ họa
from src.ui import (
    draw_game,
    draw_text_centered,
    get_hud_restart_btn_rect,
    get_overlay_restart_btn_rect
)

__all__ = [
    "WIDTH", "HEIGHT", "FPS", "PLAYER_SPEED",
    "CELL", "WALL_THICK", "HUD_H",
    "MAZE_COLS", "MAZE_ROWS", "START_CELL", "FINISH_CELL",
    "COLOR_BG", "COLOR_WALL", "COLOR_WALL_EDGE",
    "COLOR_PLAYER", "COLOR_PLAYER_EDGE", "COLOR_START",
    "COLOR_FINISH", "COLOR_FINISH_GLOW", "COLOR_TEXT",
    "COLOR_TEXT_SHADOW", "COLOR_OVERLAY", "COLOR_PATH", "COLOR_HUD_BG",
    "generate_maze", "build_walls_from_maze", "cell_center", "cell_rect",
    "try_move",
    "draw_game", "draw_text_centered",
    "get_hud_restart_btn_rect", "get_overlay_restart_btn_rect"
]
