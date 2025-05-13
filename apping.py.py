from flask import Flask, render_template, Response, url_for
from ultralytics import YOLO
import cv2
import datetime
import os

app = Flask(__name__)

# 경로 설정
SAVE_DIR = '흡연자'
STATIC_SAVE_DIR = 'static/detected'
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(STATIC_SAVE_DIR, exist_ok=True)

# 모델 불러오기
model = YOLO('C:\\Users\\STC\\Documents\\KTH_python\\yolov8_project\\runs\\detect\\final_pt\\weights\\best.pt')

# 라벨 정의
person_label = 'person'
cigarette_label = 'cigarette'

# 카메라
cap = cv2.VideoCapture(0)


smoke_count = 0

smoke_count = 0
smoke_frame_count = 0
SMOKE_DETECT_THRESHOLD = 30
is_counted = False

def generate_frames():
    global smoke_count, smoke_frame_count, is_counted
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        boxes = results.boxes
        names = results.names

        persons = []
        cigarettes = []

        for box in boxes:
            cls_id = int(box.cls[0].item())
            label = names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            if label == person_label:
                persons.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame, 'person', (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            elif label == cigarette_label:
                cigarettes.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, 'cigarette', (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        smoking_detected = False

        for (px1, py1, px2, py2) in persons:
            for (cx1, cy1, cx2, cy2) in cigarettes:
                if px1 <= cx1 and py1 <= cy1 and px2 >= cx2 and py2 >= cy2:
                    smoking_detected = True
                    break

        if smoking_detected:
            smoke_frame_count += 1

            # 항상 빨간 화면과 텍스트 출력
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), -1)
            alpha = 0.4
            frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
            cv2.putText(frame, "Stop Smoking Please.", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

            # 단 1회 카운팅 및 저장
            if smoke_frame_count >= SMOKE_DETECT_THRESHOLD and not is_counted:
                is_counted = True
                smoke_count += 1

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'detected_{timestamp}.jpg'
                cv2.imwrite(os.path.join(SAVE_DIR, filename), frame)
                cv2.imwrite(os.path.join(STATIC_SAVE_DIR, filename), frame)

        else:
            smoke_frame_count = 0
            is_counted = False

        # Flask 영상 스트리밍용
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    image_list = sorted(os.listdir(STATIC_SAVE_DIR), reverse=True)[:6]  # 최근 이미지 6장 표시
    return render_template('index.html', count=smoke_count, images=image_list)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)