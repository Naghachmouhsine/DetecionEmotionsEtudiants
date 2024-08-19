import joblib

from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import cv2
class Classifieur : 
    def __init__(self):
        self.model = joblib.load("randomForest91%.joblib")
        self.modelVGG16 = VGG16(weights='imagenet', include_top=False, input_shape=(100, 100, 3))
    # def extract_features(self, image_matrix):
    #     x = np.expand_dims(image_matrix, axis=0)
    #     x = preprocess_input(x)
    #     features = self.modelVGG16.predict(x)
    #     return features.flatten()
    def extract_features(self, images_matrix):
        # Assurez-vous que les images ont la bonne forme et sont normalisées
        x = np.array([preprocess_input(img) for img in images_matrix])
        features = self.modelVGG16.predict(x)
        return features.reshape(len(images_matrix), -1)


    def prediction(self, imgs):
        mats = [image.img_to_array(img) for img in imgs]
        features = self.extract_features(mats)
        return self.model.predict(features)




