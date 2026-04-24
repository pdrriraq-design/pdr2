import cv2
import requests
import os
from ultralytics import YOLO

# إعدادات تليجرام (يجب الحصول على Token و ID من BotFather)
TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)
    except:
        print("خطأ في الاتصال بتليجرام")

def alert_sound():
    # أمر لينكس لإصدار صوت تنبيه بسيط
    os.system('spd-say "Warning: Drone Detected" &')

# تحميل النموذج
model = YOLO('yolov8m.pt')
last_alert_time = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    results = model.predict(frame, conf=0.5, verbose=False)
    drone_detected = False

    for det in results[0].boxes:
        label = model.names[int(det.cls[0])]
        if label in ['airplane', 'bird', 'drone']:
            drone_detected = True
            # رسم مربع أحمر للتحذير
            x1, y1, x2, y2 = map(int, det.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, "ALARM: OBJECT DETECTED", (x1, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # إطلاق الإنذار إذا تم رصد هدف
    if drone_detected:
        alert_sound()
        # إرسال رسالة تليجرام (مرة كل دقيقة لتجنب الإزعاج)
        # يمكنك إضافة منطق زمني هنا باستخدام time.time()
        # send_telegram_msg("⚠️ تنبيه: تم رصد أجسام مشبوهة في المنطقة!")

    cv2.imshow('AI Early Warning System', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
