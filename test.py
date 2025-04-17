from fastapi.testclient import TestClient
from server import app  # Import FastAPI app instance
from unittest.mock import patch
import base64
from PIL import Image
import io

client = TestClient(app)

# Test WebSocket connection establishment
def test_websocket_connection():
    with client.websocket_connect("/wss") as websocket:
        assert websocket

# Test invalid JSON data handling
def test_invalid_json():
    with client.websocket_connect("/wss") as websocket:
        websocket.send_text("invalid_json")
        response = websocket.receive_json()
        assert response["error"] == "Invalid JSON format"

# Test missing fields in message handling
def test_missing_fields():
    with client.websocket_connect("/wss") as websocket:
        websocket.send_json({"type": "image"})  # Missing 'data' field
        response = websocket.receive_json()
        assert "Missing required fields" in response["error"]

# Test unsupported message type handling
def test_invalid_message_type():
    with client.websocket_connect("/wss") as ws:
        ws.send_json({"type": "text", "data": "hello"})
        response = ws.receive_json()
        assert "Unsupported message type" in response["error"]

# Test invalid base64 data handling
def test_invalid_base64():
    with client.websocket_connect("/wss") as websocket:
        websocket.send_json({"type": "image", "data": "invalid_b64"})
        response = websocket.receive_json()
        assert "Invalid base64 encoding" in response["error"]

# Test unsupported image format handling
def test_invalid_image_format():
    with client.websocket_connect("/wss") as ws:
        ws.send_json({"type": "image", "data": base64.b64encode(b"not an image").decode()})
        response = ws.receive_json()
        assert "Unsupported image format" in response["error"]  # Connection stays open

# Test successful image processing
@patch("server.model")
def test_successful_image_processing(mock_model):
    mock_model.return_value = [{"label": "test", "score": 0.95}]
    
    with client.websocket_connect("/wss") as websocket:
        # Create valid test image
        image = Image.new("RGB", (224, 224), color="red")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        test_image = base64.b64encode(buffered.getvalue()).decode()
        
        websocket.send_json({
            "type": "image",
            "data": test_image
        })
        response = websocket.receive_json()
        assert "result" in response
        assert response["result"][0]["label"] == "test"

# Test client disconnection
def test_client_disconnect():
    with client.websocket_connect("/wss") as websocket:
        websocket.close()
