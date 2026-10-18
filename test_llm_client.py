import asyncio
import os
from dotenv import load_dotenv
from client.llm_client import LLMClient  # Thay đổi đường dẫn import nếu file LLMClient của bạn nằm ở thư mục khác
from client.response import StreamEventType

load_dotenv()


async def test_chat_completion():
    client = LLMClient()

    messages = [
        {"role": "user", "content": "Hãy chào tôi bằng một câu ngắn gọn."}
    ]

    print("=" * 50)
    print("1. ĐANG KIỂM TRA TRƯỜNG HỢP: stream = True")
    print("=" * 50)
    try:
        async for event in client.chat_completion(
            messages, stream=True
        ):
            print(f"[Stream Event Type]: {event.type}")
            if event.type == StreamEventType.TEXT_DELTA:
                print(f"Delta content: {event.text_delta}")
            elif event.type == StreamEventType.TEXT_COMPLETE:
                print(f"Complete finish_reason: {event.finish_reason}")
                print(f"Usage: {event.usage}")
            elif event.type == StreamEventType.TEXT_ERROR:
                print(f"❌ Lỗi nhận được: {event.error}")
    except Exception as e:
        print(f"❌ Ngoại lệ không mong muốn khi stream: {e}")

    print("\n" + "=" * 50)
    print("2. ĐANG KIỂM TRA TRƯỜNG HỢP: stream = False")
    print("=" * 50)
    try:
        async for event in client.chat_completion(
            messages, stream=False
        ):
            print(f"[Non-Stream Event Type]: {event.type}")
            if event.type == StreamEventType.TEXT_COMPLETE:
                print(f"Complete finish_reason: {event.finish_reason}")
                print(f"Content message: {event.text_delta}")
                print(f"Usage: {event.usage}")
            elif event.type == StreamEventType.TEXT_ERROR:
                print(f"❌ Lỗi nhận được: {event.error}")
    except Exception as e:
        print(f"❌ Ngoại lệ không mong muốn khi non-stream: {e}")

    print("\n" + "=" * 50)
    print("3. ĐANG KIỂM TRA CƠ CHẾ RETRY (GIẢ LẬP LỖI KẾT NỐI)")
    print("=" * 50)
    
    # Lưu lại base_url cũ
    original_client = client._client
    
    # Cố tình đổi base_url thành một địa chỉ sai để kích hoạt APIConnectionError hoặc lỗi kết nối
    if client._client:
        await client.close()
    
    # Gán tạm một cấu hình kết nối lỗi để test retry
    from openai import AsyncOpenAI
    client._client = AsyncOpenAI(
        api_key="invalid_key",
        base_url="https://api.nonexistent-domain-xyz123.com/v1"
    )

    print("Đang gọi API với base_url lỗi (Sẽ thử lại 3 lần theo _MAX_RETRIES_)...")
    start_time = asyncio.get_event_loop().time()
    
    try:
        async for event in client.chat_completion(messages, stream=False):
            print(f"Event nhận được sau các lần retry: {event.type}")
            if event.type == StreamEventType.TEXT_ERROR:
                print(f"Thông báo lỗi cuối cùng: {event.error}")
    except Exception as e:
        print(f"Ngoại lệ phát sinh: {e}")
        
    end_time = asyncio.get_event_loop().time()
    print(f"Thời gian hoàn tất quá trình retry: {end_time - start_time:.2f} giây")

    # Đóng kết nối cuối cùng
    await client.close()
    print("\n✅ Hoàn tất toàn bộ kịch bản test!")


if __name__ == "__main__":
    asyncio.run(test_chat_completion())