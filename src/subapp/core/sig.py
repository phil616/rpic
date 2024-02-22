from fastapi import FastAPI
import uvicorn
import signal

app = FastAPI()
server = None

def signal_handler(sig, frame):
    print("程序被终止")
    if server is not None:
        server.should_exit = True

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/stop")
def stop_server():
    signal_handler(signal.SIGINT, None)
    return {"message": "Server stopped"}

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    server = uvicorn.Server(uvicorn.Config(app, host="0.0.0.0", port=8000))
    server.run()
