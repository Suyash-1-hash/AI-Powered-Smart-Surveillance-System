import cv2
from ultralytics import YOLO
import winsound
from datetime import datetime
import smtplib
from email.message import EmailMessage


face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

model = YOLO(r"C:\\Users\\suyash\\runs\\detect\\train5\\weights\\best.pt")

cap = cv2.VideoCapture(0)

def send_email_alert(image_name, time_text):
    sender_email = "SENDER'S MAIL"
    receiver_email = "RECIEVER'S MAIL"
    app_password = "GMAIL APP PASSWORD"

    msg = EmailMessage()
    msg["Subject"] = "🚨 WEAPON DETECTED"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(f"Weapon detected at {time_text}")

    with open(image_name, "rb") as f:
        msg.add_attachment(f.read(),
                           maintype="image",
                           subtype="jpeg",
                           filename=image_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)


image_saved = False

while True:
    now = datetime.now()
    time_text = now.strftime("%d-%m-%Y %H:%M:%S")

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    faces = face_cascade.detectMultiScale(frame1, 1.1, 5)
            
    for (x,y,w,h) in faces:
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame1, "Face Detected", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 0, 255), 2)

    motion = False

    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        
        x, y, w, h = cv2.boundingRect(c)
        
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        motion = True

    if motion:

        cv2.putText(frame1, "MOTION DETECTED", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,0,255),2)

        results = model(frame1, conf=0.1)

        weapon_detected = False

        for r in results:
            for box in r.boxes:

                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]

                if label == "senjata_api":
                    label = "Gun"
                    weapon_detected = True
                elif label == "senjata_tajam":
                    label = "Knife"
                    weapon_detected = True

                cv2.rectangle(frame1,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame1,label,(x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

        if weapon_detected:

            cv2.putText(frame1,"WARNING: WEAPON DETECTED",(50,80),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

            now = datetime.now()
            time_text = now.strftime("%d-%m-%Y %H:%M:%S")

            if not image_saved:

                filename = f"weapon_{now.strftime('%d%m%Y_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame1)

                send_email_alert(filename, time_text)

                winsound.Beep(2000,1000)

                image_saved = True

        else:
            image_saved = False

    cv2.imshow("AI Security System", frame1)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()