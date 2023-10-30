from fastapi import FastAPI, HTTPException, WebSocket
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import time
from database import engine,Base,StoneActivationStatus,SessionLocal
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from schema import StoneActivationRequest
import asyncio
import json
from celery import Celery
app = FastAPI()


# Celery setup
celery = Celery('myapp', broker='pyamqp://guest@localhost//', result_backend='rpc://')
# Configure Celery
celery.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

@celery.task
def simulate_stone_activation(stone_id, user_id, power_duration):
    # Simulate activation by waiting for power_duration seconds.
    time.sleep(power_duration)
    return f"Stone {stone_id} activated for user {user_id}"


# Part 1 - Stone Power Activation Endpoint

@app.post("/activate_stone_power")
async def activate_stone_power(request: StoneActivationRequest):
    stone_id = request.stone_id
    user_id = request.user_id
    power_duration = request.power_duration

    # Trigger Celery task to handle the activation
    task_id = simulate_stone_activation.apply_async((stone_id, user_id, power_duration))
    
    # Store activation record in the database
    db = SessionLocal()
    activation_status = StoneActivationStatus(
        stone_id=stone_id,
        user_id=user_id,
        task_id = task_id.id,
        activation_start_time=datetime.now(),
        activation_end_time=datetime.now() + timedelta(seconds=power_duration)
    )
    db.add(activation_status)
    db.commit()
    db.close()

    return {"message": "Stone power activation request received", "task_id": task_id.id}

# Real-time Updates with WebSockets
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    print(f"WebSocket Connection Opened for user {user_id}")
    try:
        while True:
            # Simulated real-time update message
            message = f"Update for user {user_id}: Something happened!"
            await websocket.send_text(message)

            # Simulate an update every 1 second (adjust as needed)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"WebSocket Connection Closed for user {user_id}")
