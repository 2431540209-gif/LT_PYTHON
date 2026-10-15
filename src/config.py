"""
Cấu hình và hằng số cho Game Mê Cung (Maze Game)
"""

# ---------------------------------------------------------------------------
# Kích thước & thông số lưới
# ---------------------------------------------------------------------------
CELL = 40                       # kích thước 1 ô logic (pixel)
WALL_THICK = 6                  # độ dày tường (pixel)
MAZE_COLS, MAZE_ROWS = 15, 11   # số ô trong mê cung (lẻ để dễ nhìn)

# Kích thước cửa sổ = lưới ô + viền
WIDTH  = MAZE_COLS * CELL + WALL_THICK
HEIGHT = MAZE_ROWS * CELL + WALL_THICK + 40   # +40 cho thanh HUD trên cùng
HUD_H  = 40                                    # chiều cao vùng HUD
FPS = 60
PLAYER_SPEED = 3                               # pixel/frame

# ---------------------------------------------------------------------------
# Vị trí Start / Finish (tính theo ô lưới)
# ---------------------------------------------------------------------------
START_CELL  = (0, 0)
FINISH_CELL = (MAZE_COLS - 1, MAZE_ROWS - 1)

# ---------------------------------------------------------------------------
# Bảng màu sắc
# ---------------------------------------------------------------------------
COLOR_BG          = (22,  24,  35)
COLOR_WALL        = (70,  90, 135)
COLOR_WALL_EDGE   = (50,  65, 100)
COLOR_PLAYER      = (80, 220, 120)
COLOR_PLAYER_EDGE = (40, 160,  70)
COLOR_START       = (60, 180, 240)
COLOR_FINISH      = (255, 80,  90)
COLOR_FINISH_GLOW = (255, 140, 140)
COLOR_TEXT         = (220, 220, 230)
COLOR_TEXT_SHADOW  = (0,   0,   0)
COLOR_OVERLAY      = (0,   0,   0, 180)
COLOR_PATH         = (35,  38,  52)
COLOR_HUD_BG       = (28,  30,  42)
