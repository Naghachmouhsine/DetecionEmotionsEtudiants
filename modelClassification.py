import joblib

from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import cv2
class Classifieur : 
    def __init__(self) :
        self.model=joblib.load("randomForest91%.joblib")
        self.modelVGG16 = VGG16(  # Instancie le modèle VGG16
            weights='imagenet',  # Précise que les poids pré-entraînés sur le jeu de données ImageNet doivent être utilisés
            include_top=False,  # Indique que la couche fully connected (top) du modèle VGG16 ne doit pas être incluse
            input_shape=(100, 100, 3)  # Spécifie la forme des images en entrée du modèle (hauteur, largeur, nombre de canaux)
        )

    # # Extraire les caractéristiques des images à partir du modèle CNN pré-entraîné
    # def extract_features_path(self,img_path):
    #     img = image.load_img(img_path, target_size=(100, 100)) # Charge l'image depuis le chemin d'accès spécifié et redimensionne à la taille attendue par le modèle (100x100 pixels)
    #     x = image.img_to_array(img)# Convertit l'image en tableau numpy
    #     x = np.expand_dims(x, axis=0)  # Ajoute une dimension supplémentaire pour correspondre à la forme attendue par le modèle
    #     x = preprocess_input(x) # Prétraite l'image pour la rendre compatible avec le modèle VGG16 (normalisation)
    #     features = self.modelVGG16.predict(x) # Utilise le modèle VGG16 pour prédire les caractéristiques de l'image
    #     return features.flatten()
    def extract_features(self,image_matrix):
        x = np.expand_dims(image_matrix, axis=0)
        x = preprocess_input(x)
        features =self.modelVGG16.predict(x)
        return features.flatten()
    def prediction(self,img) : 
        # img = image.load_img(path, target_size=(100, 100))
        img=cv2.resize(img,(100,100))
        mat=image.img_to_array(img)
        extr=self.extract_features(mat)
        resultat=self.model.predict([extr])
        return resultat[0]