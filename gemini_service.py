import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

def ask_gemini(prompt: str, image=None) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return "❌ ไม่พบ API Key กรุณาตรวจสอบไฟล์ .env"
        
    client = genai.Client(api_key=key)
    
    # เตรียมโมเดลไว้ 2 ตัว ตัวหลัก (flash) และ ตัวสำรอง (pro) เผื่อคิวเต็ม
    models = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    for model_name in models:
        for attempt in range(3): # ลองส่งคิว 3 รอบต่อโมเดล
            try:
                if image:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[image, prompt]
                    )
                else:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                return response.text or "Gemini ไม่ได้ส่งข้อความตอบกลับ"
                
            except Exception as e:
                error_msg = str(e)
                # ถ้าคิวเต็ม (503) หรือส่งถี่ไป (429) ให้โปรแกรมแอบรอ 2 วินาทีแล้วลองใหม่เงียบๆ
                if "503" in error_msg or "429" in error_msg:
                    time.sleep(2)
                    continue 
                else:
                    return f"❌ เกิดข้อผิดพลาดจาก Gemini API: {error_msg}"
                    
    return "❌ 503 เซิร์ฟเวอร์ AI ของ Google เต็มทุกช่องทางในขณะนี้ ระบบพยายามสลับคิวให้แล้วแต่ไม่สำเร็จ กรุณาลองกดใหม่อีกครั้งครับ"