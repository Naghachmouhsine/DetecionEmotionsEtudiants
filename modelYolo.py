# import os
import cv2
from ultralytics import YOLO
from modelClassification import Classifieur
class FaceDetector:
    def __init__(self):
        self.model = YOLO("yolov8n-face.pt")
        self.classifieur=Classifieur()
        self.faces_detected_total={}
    def detect_faces(self, frame,user):
        # frame=cv2.imread(path)
        faces_detected=[]
        results = self.model(frame)
        for info in results:
            parameters = info.boxes
            for box in parameters:
                xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
                if float(box.conf[0])>0.5 : #confiance
                    # Dessiner le rectangle autour du visage
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)                    
                    class_name=self.classifieur.prediction(frame[ymin:ymax, xmin:xmax])
                    faces_detected.append(class_name)
        userExist=user in self.faces_detected_total.keys()
        self.faces_detected_total[user]=(self.faces_detected_total[user] if userExist else [])+faces_detected
        return faces_detected,frame
