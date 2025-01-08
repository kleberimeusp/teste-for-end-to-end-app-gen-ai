
# Debt Manager - Backend (FastAPI) & Frontend (Next.js)

## Description
Debt Manager is an application for managing debts, including authentication, listing, and creation of debts. The project is divided into two main services:
- Backend in **Python (FastAPI)**.
- Frontend in **Next.js** with **TypeScript**.

---

## Main Technologies Used - API (Backend Microservices)

![Git](https://img.shields.io/badge/Git-2.40.0-%237159c1?style=for-the-badge&logo=git)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-%237159c1?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.3-%237159c1?style=for-the-badge&logo=postgresql)
![MongoDB](https://img.shields.io/badge/MongoDB-1.14.1-%237159c1?style=for-the-badge&logo=mongodb)
![Docker](https://img.shields.io/badge/Docker-4.1.8-%237159c1?style=for-the-badge&logo=docker)
![Swagger](https://img.shields.io/badge/Swagger-2.10.5-%237159c1?style=for-the-badge&logo=swagger)
![Python](https://img.shields.io/badge/Python-3.10-%237159c1?style=for-the-badge&logo=python)
![VSCode](https://img.shields.io/badge/VSCode-1.77.3-%237159c1?style=for-the-badge&logo=visualstudiocode)

---

## Main Technologies Used - Frontend

![Git](https://img.shields.io/badge/Git-2.40.0-%237159c1?style=for-the-badge&logo=git)
![React](https://img.shields.io/badge/React-18.2.0-%237159c1?style=for-the-badge&logo=react)
![Next.js](https://img.shields.io/badge/Next.js-13.4-%237159c1?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-4.9-%237159c1?style=for-the-badge&logo=typescript)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3.2-%237159c1?style=for-the-badge&logo=tailwindcss)
![Postman](https://img.shields.io/badge/Postman-10.13.10-%237159c1?style=for-the-badge&logo=postman)
![Insomnia](https://img.shields.io/badge/Insomnia-2023.1.0-%237159c1?style=for-the-badge&logo=insomnia)
![VSCode](https://img.shields.io/badge/VSCode-1.77.3-%237159c1?style=for-the-badge&logo=visualstudiocode)

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
