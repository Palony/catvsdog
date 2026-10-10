import io
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import tensorflow as tf
from keras.utils import load_img, img_to_array
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catvsdogs_model.keras')
model = tf.keras.models.load_model(MODEL_PATH)


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/animal")
async def receive_animal(file: UploadFile):

    contents = await file.read()

    img = load_img(io.BytesIO(contents), target_size=(180, 180))

    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    # Model zwraca 2 logity (Dense(2) bez aktywacji) -> softmax daje prawdopodobieństwa
    probabilities = tf.nn.softmax(predictions[0]).numpy()
    predicted_class = int(np.argmax(probabilities))
    score = float(probabilities[predicted_class])

    # Kolejność klas z image_dataset_from_directory jest alfabetyczna: 0 = cats, 1 = dogs
    class_names = ["Kot", "Pies"]
    class_name = class_names[predicted_class]

    print(f"Prawdopodobieństwa [Kot, Pies]: {probabilities}")
    print(f"Model uważa, że to: {class_name} (Indeks: {predicted_class})")
    return {
        "filename": file.filename,
        "class": class_name,
        "score": score,
    }