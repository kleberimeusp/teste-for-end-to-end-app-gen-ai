
# Debt Manager - Backend (FastAPI) & Frontend (Next.js)

## Description
Debt Manager is an application for managing debts, including authentication, listing, and creation of debts. The project is divided into two main services:
- Backend in **Python (FastAPI)**.
- Frontend in **Next.js** with **TypeScript**.

---

## Project Structure

### Backend (FastAPI)
The backend follows a modular architecture with the following layers:
- **Configurations (`config/`)**: Configuration for the database and environment variables.
- **Models (`models/`)**: Represent the database tables.
- **Repositories (`repositories/`)**: Data access layer.
- **Services (`services/`)**: Business logic implementation.
- **Controllers (`controllers/`)**: Manages endpoints.
- **Routers (`routers/`)**: Organizes the API routes.
- **Middlewares (`middlewares/`)**: Handles request interception, such as JWT authentication.
- **Tests (`tests/`)**: Includes unit and integration tests.

### Frontend (Next.js)
The frontend is developed using **Next.js** and follows these layers:
- **Pages (`pages/`)**: Manages frontend routes.
- **Components (`components/`)**: Contains reusable components.
- **Contexts (`contexts/`)**: Manages global state.
- **Services (`services/`)**: Handles API communication.
- **Styles (`styles/`)**: TailwindCSS configuration.
- **Utils (`utils/`)**: Includes utility functions.

---

## Technologies Used

### Backend
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Docker**: Backend and database deployment

### Frontend
- **Language**: TypeScript
- **Framework**: Next.js
- **Styling**: TailwindCSS
- **State Management**: Context API

---

## How to Run the Project

### Prerequisites
- Docker and Docker Compose
- Node.js (>= 16.x)

### Running the Backend
1. Navigate to the backend directory:
   ```bash
   cd debt_manager_backend_fastapi
   ```
2. Configure the `.env` file with the required variables.
3. Start the backend and the PostgreSQL database with Docker:
   ```bash
   docker-compose up --build
   ```

### Running the Frontend
1. Navigate to the frontend directory:
   ```bash
   cd debt_manager_frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Accessing the Application
- **Backend**: `http://localhost:8000/docs` (Swagger UI)
- **Frontend**: `http://localhost:3000`

---

## Folder Structure

```plaintext
debt_manager_backend_fastapi/
  ├── app/
  │   ├── config/
  │   ├── controllers/
  │   ├── middlewares/
  │   ├── migrations/
  │   ├── models/
  │   ├── repositories/
  │   ├── routers/
  │   ├── services/
  │   └── tests/
  ├── Dockerfile
  ├── docker-compose.yml
  └── requirements.txt

debt_manager_frontend/
  ├── src/
  │   ├── app/
  │   ├── components/
  │   ├── contexts/
  │   ├── pages/
  │   ├── services/
  │   ├── styles/
  │   ├── utils/
  │   └── tests/
  ├── package.json
  ├── tsconfig.json
  └── tailwind.config.ts
```

---

## Contact
For questions or suggestions, please contact via email: [kleber.ime.usp@gmail.com](mailto:kleber.ime.usp@gmail.com).
