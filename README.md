```markdown
# Mini Trello/Kanban Board Application

Simple implementation of a Trello/Kanban-like board with drag-and-drop functionality for task management. It consists of a React frontend, a Python FastAPI backend, and uses DynamoDB Local as the database.

### Prerequisites

- Docker
- Python 3.8+
- Node.js and npm
- AWS CLI (optional, for DynamoDB Local)

### Setting Up the Database (DynamoDB Local)

1. **Run DynamoDB Local with Docker**:
   ```sh
   docker pull amazon/dynamodb-local
   docker run -p 8000:8000 amazon/dynamodb-local
   ```

2. **Create DynamoDB Tables**:
   You can use the AWS CLI to create tables, or run a script if provided in the backend application.

   Example AWS CLI command to create a table:
   ```sh
   aws dynamodb create-table --table-name Tasks --attribute-definitions AttributeName=task_id,AttributeType=S --key-schema AttributeName=task_id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000
   ```

### Setting Up the Backend (FastAPI)

1. **Navigate to the Backend Directory**:
   ```sh
   cd path/to/back
   ```

2. **Install Dependencies and create venv**:
   ```sh
    python3 -m venv venv
   pip install -r requirements.txt
   ```

3. **Run the FastAPI Server**:
   ```sh
   uvicorn main:app --reload
   ```

### Setting Up the Frontend (React)

1. **Navigate to the Frontend Directory**:
   ```sh
   cd path/to/frontend
   ```

2. **Install Dependencies**:
   ```sh
   npm install
   ```

3. **Run the React Development Server**:
   ```sh
   npm start
   ```

### Accessing the Application

- The frontend can be accessed at `http://localhost:3000`.
- The backend GraphQL endpoint is available at `http://localhost:8000/graphql`.
- DynamoDB Local is running at `http://localhost:8000`.
