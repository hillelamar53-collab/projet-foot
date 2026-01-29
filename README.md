# ⚽ Football Player Manager API

## 📖 Description

Football Player Manager is a **Python REST API** built with **FastAPI** that allows users to manage football players using a **CRUD system** (Create, Read, Update, Delete).

The application follows **Object-Oriented Programming (OOP)** principles and stores data in a **JSON file** for persistence.

This project was developed as part of a **Hackathon at Developers Institute**.

---

## 🛠 Technologies Used

- Python 3
- FastAPI
- Object-Oriented Programming (OOP)
- JSON
- Uvicorn
- Swagger / OpenAPI
- Git & GitHub

---

## 📂 Project Structure

```bash
project_foot/
│
├── api.py              # FastAPI routes
├── app.py              # FastAPI app instance
├── main.py             # Application entry point
├── manager.py          # CRUD logic
├── models.py           # Player model (OOP)
├── storage.py          # JSON persistence layer
├── players.json        # Stored players data
├── requirements.txt
└── README.md