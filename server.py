from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from transformers import pipeline
from PIL import Image
import io
import base64
import json

app = FastAPI()

# Load Hugging Face model 
model = pipeline("image-classification", model="google/vit-base-patch16-224")

@app.websocket("/ws")
async def process_image(websocket: WebSocket):
    #Establish connection
    await websocket.accept()
    try:
        while True:
            #Get data
            raw_data = await websocket.receive_text()
            json_data = json.loads(raw_data)
            
            if json_data["type"] == "image": 
                #Decode from base64
                image_data = base64.b64decode(json_data["data"])
                
                #Convert to image
                image = Image.open(io.BytesIO(image_data))
                
                #Run inference
                result = model(image)  

                #Return result
                await websocket.send_json({"result": result})  
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed")

    

    