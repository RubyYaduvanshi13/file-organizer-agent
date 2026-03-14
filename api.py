# api.py - Make sure this is running
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from agent import FileOrganizerAgent
import os

app = FastAPI(title="AI File Organizer Agent")
agent = FileOrganizerAgent()

class OrganizeRequest(BaseModel):
    files: Optional[List[str]] = None

@app.get("/")
async def root():
    return {
        "message": "🤖 AI File Organizer API",
        "docs": "/docs",
        "endpoints": ["/status", "/organize", "/memory", "/learn"]
    }

@app.get("/status")
async def get_status():
    return agent.get_status()

@app.post("/organize")
async def organize_files(request: OrganizeRequest = None):
    print("\n📢 API received organize request!")
    files = request.files if request else None
    results = agent.organize(files)
    print(f"✅ Organized {len(results)} files")
    return {
        "success": True,
        "results": results,
        "total": len(results)
    }

@app.get("/memory")
async def get_memory():
    return {
        "learned": agent.memory.get('learned', {}),
        "history": agent.memory.get('history', [])[-10:]
    }

@app.post("/learn/{extension}/{folder}")
async def learn(extension: str, folder: str):
    if not extension.startswith('.'):
        extension = '.' + extension
    agent.memory['learned'][extension] = folder
    agent.save_memory()
    return {"message": f"Learned: {extension} -> {folder}"}

@app.get("/files")
async def list_files():
    """List all files in workspace with their locations"""
    files = []
    workspace = Path("agent_workspace")
    
    for item in workspace.rglob("*"):
        if item.is_file() and item.name != "memory.json":
            files.append({
                "name": item.name,
                "path": str(item),
                "folder": item.parent.name,
                "size": item.stat().st_size
            })
    return files

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 STARTING AI AGENT API")
    print("="*50)
    print(f"📁 Workspace: agent_workspace")
    print("🌐 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
