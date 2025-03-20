from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from transformers import pipeline
from PIL import Image
import io
import base64

app = FastAPI()

# Load Hugging Face model 
model = pipeline("image-classification", model="google/vit-base-patch16-224")

@app.websocket("/wss")
async def process_image(websocket: WebSocket):
    #Establish connection
    await websocket.accept()

    #Get data
    base64_image = await websocket.receive_text()

    #Decode from base64
    image_data = base64.b64decode(base64_image)
    
    #Convert to image
    image = Image.open(io.BytesIO(image_data))
    
    #Run inference
    result = model(image)  

    #Return result
    await websocket.send_json({"result": result})  
