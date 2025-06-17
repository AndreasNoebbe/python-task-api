# Task Manager API

A simple yet powerful REST API for managing tasks, built with FastAPI and deployed using GitHub Actions.

## 🚀 Features

- **Full CRUD operations** for tasks
- **Status-based filtering** (pending, in_progress, completed)
- **Input validation** with Pydantic models
- **Comprehensive testing** with pytest
- **Docker containerization**
- **CI/CD pipeline** with GitHub Actions
- **Automatic deployment** to Azure
- **Health check endpoint** for monitoring

## 📋 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /tasks/status/{status}` - Get tasks by status

## 🛠️ Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/python-task-api.git
cd python-task-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application
uvicorn app.main:app --reload

# The API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run linting
flake8 app tests
black --check app tests

# Security scan
bandit -r app
```

### Docker
```bash
# Build image
docker build -t task-api .

# Run container
docker run -p 8000:8000 task-api
```

## 🚀 Deployment

This project uses GitHub Actions for CI/CD:

1. **Push to main branch** triggers the pipeline
2. **Tests run** on multiple Python versions
3. **Code quality checks** (linting, formatting, security)
4. **Docker image built** and pushed
5. **Automatic deployment** to Azure App Service

## 📊 Project Structure

```
python-task-api/
├── .github/workflows/     # GitHub Actions CI/CD
├── app/                   # Application code
│   ├── main.py           # FastAPI app
│   ├── models.py         # Pydantic models
│   └── database.py       # Database layer
├── tests/                # Test suite
├── requirements.txt      # Dependencies
├── Dockerfile           # Container definition
└── README.md           # This file
```

## 🔧 Configuration

Set these secrets in your GitHub repository:
- `AZURE_WEBAPP_PUBLISH_PROFILE` - For Azure deployment

## 📈 Monitoring

- Health check: `GET /health`
- Logs available in Azure App Service
- Test coverage reports in GitHub Actions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.