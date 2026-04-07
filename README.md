# APS System 🚀

## 📌 Overview

APS System is an AI-powered assistant built using FastAPI and Google Generative AI, designed to automate user interactions and deliver intelligent real-time responses.

The system integrates modular agents, tools, and database components to create a scalable and production-ready backend, deployed on Google Cloud Run.

---

## ⚙️ Tech Stack

* 🐍 Python
* ⚡ FastAPI
* 🤖 Google Generative AI
* 🍃 MongoDB
* 🐳 Docker
* ☁️ Google Cloud Run

---

## ✨ Features

* ✅ AI-powered intelligent response generation
* ✅ Modular architecture using agents and tools
* ✅ FastAPI-based high-performance backend
* ✅ Cloud deployment using Docker & Cloud Run
* ✅ Scalable and extensible system design
* ✅ REST API endpoints for integration

---

## 🏗️ Project Structure

```
aps-system/
│── agents/          # AI logic and workflows
│── tools/           # Utility/helper functions
│── db/              # Database connection & operations
│── templates/       # Frontend UI (HTML)
│── app.py           # Main FastAPI application
│── requirements.txt # Dependencies
│── Dockerfile       # Container setup
│── .env.example     # Environment variables template
│── README.md
```

---

## ⚡ System Architecture

User → FastAPI Backend → AI Agent → Google Generative AI → Response → UI

---

## 📡 API Endpoints

* `/` → Root endpoint
* `/ui` → User interface
* `/predict` → AI response generation

---

## 🌐 Live Demo

👉 https://aps-ai-assistant-360951018596.asia-south1.run.app/ui

---

## 📸 Screenshots

<img width="1917" height="950" alt="Screenshot 2026-04-06 212332" src="https://github.com/user-attachments/assets/5e42cba4-6df7-4576-8c06-52aa51d758f2" />


---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/HariRam2172/aps-system.git
cd aps-system
```

### 2️⃣ Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create a `.env` file based on `.env.example`

---

### 5️⃣ Run the application

```bash
uvicorn app:app --reload
```

---

### 6️⃣ Open in browser

```
http://127.0.0.1:8000/ui
```

---

## 🚀 Deployment

This project is containerized using Docker and deployed on Google Cloud Run, ensuring scalability and high availability.

---

## 💡 Future Improvements

* 🔹 Voice-based interaction
* 🔹 Multi-language support
* 🔹 Persistent conversation memory
* 🔹 Enhanced UI/UX

---

## 👨‍💻 Author

**Hari Ram**
GitHub: https://github.com/HariRam2172
