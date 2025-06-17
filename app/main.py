from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from .models import Task, TaskCreate, TaskUpdate
from .database import TaskDatabase

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API built with FastAPI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = TaskDatabase()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Task Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "task-manager-api"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return db.get_all_tasks()

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task"""
    return db.create_task(task)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    task = db.update_task(task_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    if not db.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return {"message": f"Task {task_id} deleted successfully"}

@app.get("/tasks/status/{task_status}")
async def get_tasks_by_status(task_status: str):
    """Get tasks filtered by status"""
    valid_statuses = ["pending", "in_progress", "completed"]
    if task_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    return db.get_tasks_by_status(task_status)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)