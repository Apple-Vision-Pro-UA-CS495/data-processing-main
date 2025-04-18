from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from transformers import pipeline
from PIL import Image, UnidentifiedImageError
import io
import base64
import json

app = FastAPI()
MAX_MB = 25
MAX_IMAGE_SIZE_BYTES = MAX_MB * 1024 * 1024

# Load Hugging Face model 
model = pipeline("image-classification", model="google/vit-base-patch16-224")

@app.websocket("/ws")
async def process_image(websocket: WebSocket):
    #Establish connection
    await websocket.accept()
    try:
        while True:
            try:
                #Get data
                raw_data = await websocket.receive_text()
                try:
                    json_data = json.loads(raw_data)
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "error": "Invalid JSON format"
                    })
                    continue
                
                size_in_bytes = len(json_data.encode('utf-8'))
                if size_in_bytes > MAX_IMAGE_SIZE_BYTES:
                    error_message = f"Image size exceeds the maximum allowed limit of {MAX_MB} MB."
                    await websocket.send_json({"error": error_message})
                    raise ValueError(error_message)
                
                # Validate message structure
                if "type" not in json_data or "data" not in json_data:
                    await websocket.send_json({
                        "error": "Missing required fields: 'type' and 'data'"
                    })
                    continue

                if json_data["type"] != "image":
                    await websocket.send_json({"error": f"Unsupported message type: {json_data['type']}"})
                    continue  # Keep connection open for further messages

                try: 
                    #Decode from base64
                    image_data = base64.b64decode(json_data["data"])
                except base64.binascii.Error:
                    await websocket.send_json({"error": "Invalid base64 encoding"})
                    continue

                try:
                    #Convert to image
                    image = Image.open(io.BytesIO(image_data))
                except UnidentifiedImageError:
                    await websocket.send_json({"error": "Unsupported image format"})
                    continue

                #Run inference
                try:
                    result = model(image)  
                except Exception as e:
                    await websocket.send_json({"error": f"Model error: {str(e)}"})
                    continue

                #Return result
                await websocket.send_json({"result": result})  
    
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"error: {e}")
                await websocket.send_json({"error": "Websocket error"})
    finally:
        await websocket.close()
