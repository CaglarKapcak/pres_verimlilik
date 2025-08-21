from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
from datetime import datetime

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.machine_data_cache: Dict[int, Dict] = {}
    
    async def connect(self, websocket: WebSocket, machine_id: int):
        await websocket.accept()
        if machine_id not in self.active_connections:
            self.active_connections[machine_id] = []
        self.active_connections[machine_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, machine_id: int):
        if machine_id in self.active_connections:
            self.active_connections[machine_id].remove(websocket)
            if not self.active_connections[machine_id]:
                del self.active_connections[machine_id]
    
    async def broadcast_machine_update(self, machine_id: int, data: Dict):
        """Makine verilerini tüm bağlı istemcilere gönder"""
        if machine_id in self.active_connections:
            message = {
                "type": "machine_update",
                "machine_id": machine_id,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            
            disconnected = []
            for connection in self.active_connections[machine_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            # Bağlantısı kopanları temizle
            for connection in disconnected:
                self.disconnect(connection, machine_id)
    
    async def broadcast_oee_update(self, machine_id: int, oee_data: Dict):
        """OEE verilerini gönder"""
        if machine_id in self.active_connections:
            message = {
                "type": "oee_update",
                "machine_id": machine_id,
                "oee": oee_data,
                "timestamp": datetime.now().isoformat()
            }
            
            disconnected = []
            for connection in self.active_connections[machine_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            for connection in disconnected:
                self.disconnect(connection, machine_id)
    
    def update_machine_cache(self, machine_id: int, data: Dict):
        """Makine verilerini önbellekte güncelle"""
        self.machine_data_cache[machine_id] = {
            **data,
            "last_update": datetime.now().isoformat()
        }
    
    def get_machine_cache(self, machine_id: int) -> Dict:
        """Önbellekten makine verilerini getir"""
        return self.machine_data_cache.get(machine_id, {})

# Global WebSocket manager instance
websocket_manager = WebSocketManager()
