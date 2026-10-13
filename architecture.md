# 🗺️ Architecture Map (Claude Clone)

## 1. Sơ đồ kết nối thư mục

```text
claude_clone_ver_3/
├── main.py                 # Điểm khởi chạy ứng dụng (Entry Point)   
│
└── client/                 # Tầng giao tiếp LLM 
    ├── llm_client.py       # Kết nối AsyncOpenAI & đóng gói request/tool
    └── response.py         # Định nghĩa cấu trúc dữ liệu phản hồi từ AI 

```
-----------------------------------
## 2. Luồng dữ liệu (Data Flow)
```text
[ main.py ] 
   │ (Khởi tạo & gọi yêu cầu)
   ▼
[ client/llm_client.py ] 
   │ (Đóng gói prompt/tool + Gửi request API qua AsyncOpenAI)
   ▼
[ OpenRouter API ] 
   │ (Trả kết quả stream/text)
   ▼
[ client/response.py ] (Chuẩn hóa dữ liệu trả về)
```