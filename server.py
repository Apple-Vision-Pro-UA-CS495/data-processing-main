from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
from PIL import Image
import io

app = FastAPI()

# Load a Hugging Face model 
model = pipeline("image-classification", model="google/vit-base-patch16-224")

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        # Read the image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Run inference
        result = model(image)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
