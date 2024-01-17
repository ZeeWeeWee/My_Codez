import websocket
import threading

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run():
        while True:
            message = input("Enter your message: ")
            ws.send(message)
    threading.Thread(target=run).start()

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://172.232.21.168:3000",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
