import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import TaskDatabase

client = TestClient(app)

# Test fixtures
@pytest.fixture
def clean_database():
    """Reset database before each test"""
    app.db.clear_all_tasks()
    yield
    app.db.clear_all_tasks()

class TestRootEndpoints:
    """Test basic endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "task-manager-api"

class TestTaskCRUD:
    """Test task CRUD operations"""
    
    def test_get_all_tasks(self):
        """Test getting all tasks"""
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_task(self):
        """Test creating a new task"""
        new_task = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending"
        }
        response = client.post("/tasks", json=new_task)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == new_task["title"]
        assert data["description"] == new_task["description"]
        assert data["status"] == new_task["status"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_task_minimal(self):
        """Test creating a task with minimal data"""
        new_task = {"title": "Minimal Task"}
        response = client.post("/tasks", json=new_task)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == new_task["title"]
        assert data["status"] == "pending"  # default status
    
    def test_create_task_invalid_data(self):
        """Test creating a task with invalid data"""
        invalid_task = {"title": ""}  # empty title
        response = client.post("/tasks", json=invalid_task)
        assert response.status_code == 422  # Validation error
    
    def test_get_task_by_id(self):
        """Test getting a specific task"""
        # First create a task
        new_task = {"title": "Get Test Task", "description": "For testing get endpoint"}
        create_response = client.post("/tasks", json=new_task)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Then get it
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == new_task["title"]
    
    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist"""
        response = client.get("/tasks/999999")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_update_task(self):
        """Test updating a task"""
        # Create a task first
        new_task = {"title": "Update Test Task"}
        create_response = client.post("/tasks", json=new_task)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Update it
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "completed"
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]
        assert data["updated_at"] != data["created_at"]
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist"""
        update_data = {"title": "Updated Title"}
        response = client.put("/tasks/999999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_task(self):
        """Test deleting a task"""
        # Create a task first
        new_task = {"title": "Delete Test Task"}
        create_response = client.post("/tasks", json=new_task)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Delete it
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data["message"]
        
        # Verify it's gone
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist"""
        response = client.delete("/tasks/999999")
        assert response.status_code == 404

class TestTaskFiltering:
    """Test task filtering functionality"""
    
    def test_get_tasks_by_status_valid(self):
        """Test getting tasks by valid status"""
        # Test each valid status
        valid_statuses = ["pending", "in_progress", "completed"]
        for status in valid_statuses:
            response = client.get(f"/tasks/status/{status}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            # All returned tasks should have the requested status
            for task in data:
                assert task["status"] == status
    
    def test_get_tasks_by_status_invalid(self):
        """Test getting tasks by invalid status"""
        response = client.get("/tasks/status/invalid_status")
        assert response.status_code == 400
        data = response.json()
        assert "Invalid status" in data["detail"]

class TestTaskValidation:
    """Test input validation"""
    
    def test_task_title_too_long(self):
        """Test task with title too long"""
        long_title = "x" * 101  # Max is 100 chars
        new_task = {"title": long_title}
        response = client.post("/tasks", json=new_task)
        assert response.status_code == 422
    
    def test_task_description_too_long(self):
        """Test task with description too long"""
        long_description = "x" * 501  # Max is 500 chars
        new_task = {
            "title": "Valid Title",
            "description": long_description
        }
        response = client.post("/tasks", json=new_task)
        assert response.status_code == 422
    
    def test_invalid_status(self):
        """Test task with invalid status"""
        new_task = {
            "title": "Valid Title",
            "status": "invalid_status"
        }
        response = client.post("/tasks", json=new_task)
        assert response.status_code == 422

# Integration test
def test_full_task_lifecycle():
    """Test complete task lifecycle"""
    # 1. Create a task
    new_task = {
        "title": "Lifecycle Test Task",
        "description": "Testing full lifecycle",
        "status": "pending"
    }
    create_response = client.post("/tasks", json=new_task)
    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # 2. Get the task
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    
    # 3. Update the task
    update_data = {"status": "in_progress"}
    update_response = client.put(f"/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200
    
    # 4. Verify update
    get_updated_response = client.get(f"/tasks/{task_id}")
    updated_task = get_updated_response.json()
    assert updated_task["status"] == "in_progress"
    
    # 5. Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    
    # 6. Verify deletion
    get_deleted_response = client.get(f"/tasks/{task_id}")
    assert get_deleted_response.status_code == 404