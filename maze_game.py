"""
Game Mê Cung - Maze Game
=========================
Di chuyển nhân vật (ô xanh lá) từ START đến FINISH.
Dùng phím mũi tên hoặc WASD để di chuyển.
Nhấn R để chơi lại (mê cung mới), ESC để thoát.
"""

import pygame
import sys
import time
import random

# ---------------------------------------------------------------------------
# Cấu hình
# ---------------------------------------------------------------------------
CELL = 40                       # kích thước 1 ô logic
WALL_THICK = 6                  # độ dày tường (pixel)
MAZE_COLS, MAZE_ROWS = 15, 11   # số ô trong mê cung (lẻ để dễ nhìn)
# Kích thước cửa sổ = lưới ô + viền
WIDTH  = MAZE_COLS * CELL + WALL_THICK
HEIGHT = MAZE_ROWS * CELL + WALL_THICK + 40   # +40 cho HUD trên cùng
HUD_H  = 40                    # chiều cao vùng HUD
FPS = 60
PLAYER_SPEED = 3                # pixel/frame

# Màu sắc
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

# ---------------------------------------------------------------------------
# Sinh mê cung bằng Recursive Backtracking
# ---------------------------------------------------------------------------
def generate_maze(cols, rows):
    """
    Sinh mê cung cols x rows ô bằng DFS (Recursive Backtracking).
    Trả về tập hợp các cạnh đã MỞ (passages) giữa 2 ô kề nhau.
    Mỗi ô: (col, row).  Mỗi cạnh: frozenset({(c1,r1), (c2,r2)}).
    Đảm bảo mọi ô đều đến được từ mọi ô khác (perfect maze).
    """
    visited = set()
    passages = set()  # tập cạnh đã phá tường

    def dfs(c, r):
        visited.add((c, r))
        # Xáo trộn 4 hướng
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(dirs)
        for dc, dr in dirs:
            nc, nr = c + dc, r + dr
            if 0 <= nc < cols and 0 <= nr < rows and (nc, nr) not in visited:
                passages.add(frozenset({(c, r), (nc, nr)}))
                dfs(nc, nr)

    # Dùng stack thay vì đệ quy để tránh tràn stack với mê cung lớn
    stack = [(0, 0)]
    visited.add((0, 0))
    while stack:
        c, r = stack[-1]
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
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
    off_x = W // 2       # offset x cho lưới
    off_y = HUD_H + W // 2  # offset y (dưới HUD)

    # --- Viền ngoài (4 cạnh) ---
    # Trên
    walls.append(pygame.Rect(off_x - W // 2, off_y - W // 2,
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
                # Tường dọc giữa ô (c,r) và (c+1,r)
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


# ---------------------------------------------------------------------------
# Vị trí Start / Finish (tính theo ô lưới)
# ---------------------------------------------------------------------------
START_CELL  = (0, 0)
FINISH_CELL = (MAZE_COLS - 1, MAZE_ROWS - 1)


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


# ---------------------------------------------------------------------------
# Hàm kiểm tra va chạm — chặn di chuyển
# ---------------------------------------------------------------------------
def try_move(player_rect, dx, dy, walls):
    """
    Thử di chuyển player theo (dx, dy).
    Kiểm tra va chạm với TẤT CẢ các tường trên từng trục riêng.
    Nếu va chạm → đẩy player ra khỏi tường.
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


# ---------------------------------------------------------------------------
# Vẽ
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Vẽ & Giao diện
# ---------------------------------------------------------------------------
def draw_text_centered(surface, font, text, center, color, shadow=True):
    """Vẽ text có bóng đổ."""
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
    """Vẽ toàn bộ màn hình game."""
    screen.fill(COLOR_BG)

    # HUD background
    pygame.draw.rect(screen, COLOR_HUD_BG, (0, 0, WIDTH, HUD_H))
    pygame.draw.line(screen, COLOR_WALL, (0, HUD_H), (WIDTH, HUD_H), 2)

    # Vẽ nền ô trống
    off_x = WALL_THICK // 2
    off_y = HUD_H + WALL_THICK // 2
    for r in range(MAZE_ROWS):
        for c in range(MAZE_COLS):
            rect = pygame.Rect(off_x + c * CELL, off_y + r * CELL, CELL, CELL)
            pygame.draw.rect(screen, COLOR_PATH, rect)

    # Vẽ START
    pygame.draw.rect(screen, COLOR_START, start_r, border_radius=4)
    draw_text_centered(screen, font_small, "S", start_r.center,
                       COLOR_BG, shadow=False)

    # Vẽ FINISH (nhấp nháy)
    pulse = int(time.time() * 3) % 2
    fc = COLOR_FINISH if pulse == 0 else COLOR_FINISH_GLOW
    pygame.draw.rect(screen, fc, finish_r, border_radius=4)
    draw_text_centered(screen, font_small, "F", finish_r.center,
                       (255, 255, 255), shadow=False)

    # Vẽ tường
    for wall in walls:
        pygame.draw.rect(screen, COLOR_WALL, wall)
        pygame.draw.rect(screen, COLOR_WALL_EDGE, wall, 1)

    # Vẽ player
    pygame.draw.rect(screen, COLOR_PLAYER, player_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_PLAYER_EDGE, player_rect, 2, border_radius=6)

    # HUD text (thời gian bên trái/giữa)
    if not finished:
        time_text = f"Thời gian: {elapsed:.1f}s"
    else:
        time_text = f"Hoàn thành: {elapsed:.1f}s"
    time_surf = font_small.render(time_text, True, COLOR_TEXT)
    screen.blit(time_surf, (15, (HUD_H - time_surf.get_height()) // 2))

    # Nút "Chơi lại (R)" trên thanh HUD
    hud_btn = get_hud_restart_btn_rect()
    hud_hover = hud_btn.collidepoint(mouse_pos)
    hud_btn_col = (55, 75, 120) if hud_hover else (38, 48, 75)
    pygame.draw.rect(screen, hud_btn_col, hud_btn, border_radius=5)
    pygame.draw.rect(screen, COLOR_WALL, hud_btn, 1, border_radius=5)
    draw_text_centered(screen, font_btn, "Chơi lại (R)", hud_btn.center,
                       (220, 230, 255), shadow=False)

    # Overlay khi hoàn thành
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

        # Nút lớn chơi lại trên overlay
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


# ---------------------------------------------------------------------------
# Khởi tạo / Reset game
# ---------------------------------------------------------------------------
def new_game():
    """Tạo mê cung mới, trả về (walls, player_rect, start_rect, finish_rect)."""
    passages = generate_maze(MAZE_COLS, MAZE_ROWS)
    walls = build_walls_from_maze(passages, MAZE_COLS, MAZE_ROWS)

    player_size = int(CELL * 0.55)
    player_rect = pygame.Rect(0, 0, player_size, player_size)
    player_rect.center = cell_center(*START_CELL)

    start_r  = cell_rect(*START_CELL)
    finish_r = cell_rect(*FINISH_CELL)

    return walls, player_rect, start_r, finish_r


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game - Mê Cung")
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("segoeui", 34, bold=True)
    font_small = pygame.font.SysFont("segoeui", 19, bold=True)
    font_btn   = pygame.font.SysFont("segoeui", 14)

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

            # Click chuột để chơi lại
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if get_hud_restart_btn_rect().collidepoint(event.pos):
                    restart()
                elif finished and get_overlay_restart_btn_rect().collidepoint(event.pos):
                    restart()

            # Bàn phím
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Kiểm tra phím R toàn diện:
                # 1. Mã scancode phần cứng KSCAN_R (không bao giờ bị lỗi do Unikey/EVKey)
                # 2. Mã phím K_r
                # 3. Ký tự unicode 'r' / 'R'
                # 4. Phím Space hoặc Enter khi đã chiến thắng
                is_r_key = (
                    getattr(event, "scancode", None) == pygame.KSCAN_R or
                    event.key == pygame.K_r or
                    getattr(event, "unicode", "").lower() == "r" or
                    (finished and event.key in (pygame.K_SPACE, pygame.K_RETURN))
                )

                if is_r_key:
                    restart()

        if not finished:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
                dx = -PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = PLAYER_SPEED
            if keys[pygame.K_UP]    or keys[pygame.K_w]:
                dy = -PLAYER_SPEED
            if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
                dy = PLAYER_SPEED

            player_rect = try_move(player_rect, dx, dy, walls)

            if player_rect.colliderect(finish_r):
                finished = True
                finish_time = time.time() - start_time

            elapsed = time.time() - start_time
        else:
            elapsed = finish_time

        draw_game(screen, walls, player_rect, elapsed, finished,
                  font_big, font_small, font_btn, start_r, finish_r, mouse_pos)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
