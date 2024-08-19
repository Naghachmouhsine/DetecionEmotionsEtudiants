from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import modelYolo
from pydantic import BaseModel
import uvicorn
from typing import List, Dict
from dataBase import auth,gestionSeance
import asyncio
# Initialisation de FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Autoriser les origines frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser les connexions et les objets
yolo = modelYolo.FaceDetector()

import mysql.connector.pooling

# Configurer le pool de connexions
dbconfig = {
    "host": "localhost",
    "database": "emotionDetectionDB",
    "user": "root",
    "password": ""
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

def get_db_connection():
    return cnxpool.get_connection()


authentification = auth.Authentification(get_db_connection())
ges = gestionSeance.GestionSeance(get_db_connection())

class UserImage(BaseModel):
    image: str
    user: int
    isStop : bool

class Seance(BaseModel):
    user_id: int
    module: str
    date: str
    heure: str
    emotion: Dict[str, float] = {}

@app.get("/")
async def root():
    return {"message": "Welcome to the Emotion Detection API"}


@app.get("/tstCnx")
async def tstCnx():
    return {"cnx": True}

@app.post("/detect")
async def detect(data: UserImage):
    print(data.isStop)
    if data.isStop : 
        return {"class_name" : [],"frame" : data.image}
    else : 
        try:
            image_data = data.image.split(",")[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Exécuter la fonction de détection dans un thread séparé
            resultat =yolo.detect_faces(image, data.user)
            _, buffer = cv2.imencode('.jpg', resultat[1])
            frame_encoded = base64.b64encode(buffer).decode('utf-8')
            return {"class_names": resultat[0], "frame": frame_encoded}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/register")
async def register(data: dict):
    res = authentification.register(data)
    return {"res": res}


@app.post("/auth/login")
async def login(data : dict) :
    resultat=authentification.auth(data)
    return JSONResponse(content=resultat)


@app.post("/insertNewSeance")
async def insertNewSeance(seance: Seance):
    tabEmotions = yolo.faces_detected_total[seance.user_id]
    r = {}
    for e in set(tabEmotions):
        r[e] = round((tabEmotions.count(e) / len(tabEmotions)) * 100, 2)
    for i in ["surprise", "anger", "disgust", "fear", "happiness", "neutral", "sadness"]:
        r[i] = r[i] if i in r.keys() else 0
    seance.emotion = r
    ges.insertSeance(seance.dict())
    print(yolo.faces_detected_total)
    yolo.faces_detected_total[seance.user_id] = []
    return JSONResponse(content=r)

@app.post("/getStatistique")
async def getStatistique(data: dict):
    idUser = data["user"]
    resultat = {}
    for res in ges.getStatistique(idUser):
        resultat[res[0]] = [round(res[1], 2), round(res[2], 2), round(res[3], 2), round(res[4], 2), round(res[5], 2), round(res[6], 2), round(res[7], 2)]
    return JSONResponse(content=resultat)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
