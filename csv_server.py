import asyncio
import websockets
import os
import time

# Path to the CSV file to be sent
CSV_FILE_PATH = "data.csv"

async def send_csv(websocket, path):
    """Continuously send the CSV file to the connected client."""
    try:
        while True:
            if os.path.exists(CSV_FILE_PATH):
                with open(CSV_FILE_PATH, "r") as file:
                    csv_content = file.read()
                    await websocket.send(csv_content)
                    print(f"Sent CSV file to {websocket.remote_address}")
            else:
                print(f"CSV file not found: {CSV_FILE_PATH}")

            # Wait for a specified interval before sending the file again
            await asyncio.sleep(5)  # Send every 5 seconds
    except websockets.ConnectionClosed:
        print(f"Connection closed with {websocket.remote_address}")

async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(send_csv, "0.0.0.0", 8765)
    print("WebSocket server started on ws://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Server stopped.")
