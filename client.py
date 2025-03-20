import websocket
import base64

#WebSocket server URL
ws_url = "wss://127.0.0.1:8000/ws"

#Convert image to base64
with open("temp.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

#Establish connection
ws = websocket.create_connection(ws_url)

#Send message
ws.send(encoded_image)

#Receive the response
result = ws.recv()
print("Server response:", result)

# Close connection
ws.close()
