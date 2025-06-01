from deepface import DeepFace
import cv2

def detect_facial_mood():
    cap = cv2.VideoCapture(0)
    try:
        ret, frame = cap.read()
        if not ret:
            return "neutral"
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(result, list):
                return result[0].get('dominant_emotion', 'neutral')
            elif isinstance(result, dict):
                return result.get('dominant_emotion', 'neutral')
        except Exception:
            return "neutral"
    finally:
        cap.release()