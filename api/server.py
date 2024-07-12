from typing import Union, List
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from random import random
import os
import glob
import logging
from datetime import datetime, timedelta
import time
import schedule
import threading
import subprocess

# Setup Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup store for global state
class Store():
    imgUrls = []
    lastUrl = ""
    counter = 1
store = Store()

# Ensure the directory exists
dir = "../dist/img"
if not os.path.exists(dir):
    os.makedirs(dir)

# Populate the list of imgUrls
file_pattern = "*_*_*.jpg"
store.imgUrls = glob.glob(f"{dir}/{file_pattern}")
store.imgUrls = [url.replace('../dist/img/', '') for url in store.imgUrls]

def capture(name):
    filename = f"{name}_{store.counter:04d}.jpg"
    pathname = os.path.join(dir, filename)
    command = f"libcamera-still -t 1 -v 0 -o {pathname}"
    logging.info(f"Capturing {pathname}")    
    def take_picture():
        try:
            subprocess.run(command.split(), check=True)
            logging.info(f"Picture {pathname} taken successfully.")
            store.lastUrl = filename
            store.imgUrls.append(filename)
            store.counter += 1
            if name=="Test" and store.counter>10 :
                store.counter = 1
        except subprocess.CalledProcessError as e:
            logging.error(f"An error occurred while taking {pathname}: {e.stderr}")
    run_in_background(take_picture)

app = FastAPI(docs_url="/api/docs", openapi_url="/api/v1/openapi.json")

class StatusResponse(BaseModel):
    IP: str = Field(title="IP Address of the server")
    Port: int = Field(title="TCP/IP Port of the server")
    isRecording: bool = Field(title="Flag to indicate whether images are being captured")
    idleSeconds: Union[float, None] = Field(title="Number of seconds to next capture")
    imgUrls: List[str] = Field(title="Array of filenames of captured images")
    lastUrl: str = Field(title="Filename of the last captured image")
    Magic: float = Field(title="Random number between 0 and 1")
@app.get("/api/status")
def read_status(request: Request)  -> StatusResponse:
    return {
        "IP": request.client.host, 
        "Port": request.client.port, 
        "isRecording": len(schedule.get_jobs("capture"))>0,
        "idleSeconds": schedule.idle_seconds(),
        "imgUrls": store.imgUrls,
        "lastUrl": store.lastUrl,
        "Magic": random(), 
    }

@app.put("/api/test")
def test_capture():
    store.counter = 1
    name_date = "Test"
    schedule.every(5).seconds.until(timedelta(minutes=360)).do(capture, name=name_date).tag("capture")
    schedule.run_all()     # This runs the capture immediately 
    return {"message": "Capture test" }

class StartRequest(BaseModel):
    name: str = Field(min_length=1, title="Recording name")
    interval: int = Field(ge=1, title="Interval between photos in seconds")
    duration: int = Field(ge=1, title="Duration of recording in minutes")
@app.put("/api/start")
def start_capture(data: StartRequest):
    store.counter = 1
    name_date = f"{data.name}_{datetime.now().strftime('%Y-%m-%d-%Hh%Mm')}"
    schedule.every(data.interval).seconds.until(timedelta(minutes=data.duration)).do(capture, name=name_date).tag("capture")
    schedule.run_all()     # This runs the capture immediately 
    return {"message": "Capture started", "request": data }

@app.put("/api/stop")
def stop_capture():
    schedule.clear('capture')
    return {"message": "Capture stopped" }

@app.put("/api/reset")
def reset_capture():
    imgUrls.clear()
    return {"message": "Capture reset" }

app.mount("/img", StaticFiles(directory="../dist/img", html=True), name="img")
app.mount("/", StaticFiles(directory="../dist/spa", html=True), name="spa")

def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_in_background(fnToRun):
    schedule_thread = threading.Thread(target=fnToRun)
    schedule_thread.daemon = True
    schedule_thread.start()

run_in_background(run_scheduled_jobs)