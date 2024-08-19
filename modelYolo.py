# import os
import cv2
from ultralytics import YOLO
from modelClassification import Classifieur
class FaceDetector:
    def __init__(self):
            self.model = YOLO("yolov8n-face.pt")
            self.classifieur = Classifieur()
            self.faces_detected_total = {}
    def detect_faces(self, frame, user):
            results = self.model(frame)
            faces_detected = []
            for info in results:
                parameters = info.boxes
                for box in parameters:
                    xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
                    if float(box.conf[0]) > 0.5:
                        face_img = frame[ymin:ymax, xmin:xmax]
                        face_img_resized = cv2.resize(face_img, (100, 100))
                        faces_detected.append(face_img_resized)
                        # Dessiner le rectangle autour du visage
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)    

            predictions=self.classifieur.prediction(faces_detected).tolist()
            if user in self.faces_detected_total:
                self.faces_detected_total[user].extend(predictions)
            else:
                self.faces_detected_total[user] = predictions
            return predictions, frame





