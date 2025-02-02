import requests

# Simulate sending an image from the Vision Pro to the local server
def send_image_to_server(image_path):
    url = "http://localhost:8000/process"
    with open(image_path, "rb") as file:
        files = {"file": (image_path, file, "image/jpeg")}
        response = requests.post(url, files=files)
    return response.json()

# Test with a sample image (replace "test_image.jpg" with your image)
result = send_image_to_server("temp.jpg")
print("AI Result:", result)
