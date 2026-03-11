import requests
import time
import threading
from sqlalchemy.orm import Session
from app.models.sync_queue import SyncQueue
from app.core.database import SessionLocal

API_URL = "http://localhost:8000/sync"  # cambiar después

def sync_with_server():

    db = SessionLocal()

    pending = db.query(SyncQueue).filter(SyncQueue.synced == 0).all()

    for event in pending:
        try:
            response = requests.post(API_URL, json={
                "entity": event.entity,
                "operation": event.operation,
                "payload": event.payload
            })

            if response.status_code == 200:
                event.synced = 1
                db.commit()

        except:
            pass

    db.close()


def start_sync_loop():

    def loop():
        while True:
            sync_with_server()
            time.sleep(30)  # cada 30 segundos

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()