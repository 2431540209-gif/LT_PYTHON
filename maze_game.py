"""
Điểm chuyển tiếp tương thích (Backward Compatibility Entry Point)
Giúp bạn vẫn có thể chạy `python maze_game.py` hoặc `python main.py`.
Toàn bộ logic đã được tái cấu trúc thành các module trong thư mục src/:
- main.py: Vòng lặp chính và xử lý sự kiện
- src/config.py: Cấu hình và bảng màu
- src/maze.py: Thuật toán sinh mê cung
- src/player.py: Xử lý di chuyển & va chạm
- src/ui.py: Vẽ giao diện & nút bấm
"""
from main import main

if __name__ == "__main__":
    main()
