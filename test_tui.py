import time
from ui.tui import TUI

def main():
    # Khởi tạo đối tượng TUI
    terminal_ui = TUI()
    
    print("--- Bắt đầu test TUI ---")
    
    # 1. Bắt đầu phiên trợ lý (In dòng kẻ ngang "Assistance")
    terminal_ui.begin_assistance()
    
    # 2. Giả lập streaming nội dung từ LLM (từng từ một)
    sample_response = (
        "Chào bạn! Đây là một đoạn văn bản giả lập được stream "
        "trực tiếp qua giao diện dòng lệnh sử dụng thư viện Rich. "
        "Mọi thứ đang hiển thị rất mượt mà và đúng định dạng!"
    )
    
    for word in sample_response.split(" "):
        terminal_ui._stream_assistance_delta(word + " ")
        time.sleep(0.06)  # Tạo độ trễ nhỏ để quan sát hiệu ứng chữ chạy
        
    # 3. Kết thúc phiên trợ lý (Xuống dòng ngắt phiên)
    terminal_ui.end_assistance()
    
    print("--- Kết thúc test TUI ---")

if __name__ == "__main__":
    main()