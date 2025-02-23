# 🚀 **Resume Enhancer with AI**  
_A cutting-edge AI-powered tool to enhance resumes, built with **Angular** (Frontend) and **Flask** (Backend)._

![Resume Enhancer Banner](https://img.shields.io/badge/Angular-Standalone-blue?style=flat&logo=angular) ![Flask Backend](https://img.shields.io/badge/Flask-Backend-green?style=flat&logo=flask) ![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat&logo=postgresql)

---

## 🌟 **Overview**  
Resume Enhancer with AI is a **modern web application** that allows users to **upload resumes and enhance them using AI**. This tool leverages **Flask for backend** API processing, **Angular for an interactive UI**, and **PostgreSQL** for database storage.

### **Key Features** 🎯
✅ **AI-powered resume enhancement** 🧠  
✅ **Secure authentication (JWT)** 🔒  
✅ **Responsive UI with Angular standalone components** 🎨  
✅ **Database integration using PostgreSQL** 🗄️  
✅ **RESTful API with Flask** 🚀  
✅ **Cloud-hosted backend (Render / GCP)** ☁️  

---

## 🏗️ **Tech Stack**
### **Frontend (Angular)**
- **Angular 18+**
- Standalone Components
- Bootstrap / SCSS Styling
- **HttpClient (Flask API Calls)**

### **Backend (Flask)**
- Flask + Flask-CORS  
- Flask-JWT-Extended (Authentication)  
- SQLAlchemy (Database ORM)  
- Flask-Migrate (Database Migrations)  

### **Database**
- **PostgreSQL** (Hosted on Render Cloud)  
- SQLAlchemy ORM for database interactions  

---

## 📸 **Screenshots**
### 🔵 **Login Page**
![Screenshot](https://private-user-images.githubusercontent.com/12083176/415963862-1809b261-672a-4550-916d-c0caf8b5b138.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDAyOTMzMzUsIm5iZiI6MTc0MDI5MzAzNSwicGF0aCI6Ii8xMjA4MzE3Ni80MTU5NjM4NjItMTgwOWIyNjEtNjcyYS00NTUwLTkxNmQtYzBjYWY4YjViMTM4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMjMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjIzVDA2NDM1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTg0NDZhNjYyOWZiOTc2MzE3MzQ0OTE0MjUzMmQwMDA2Y2FhOThhODMzN2FiZWNhZjRkYmJhZjVmN2Q0MmFlZWImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.3t9T8cG0zPn8FTmayMHkzXkkp-nbG6F-kaNMrGupUY0)

### 🟣 **AI Resume Enhancement**
![Screenshot](https://private-user-images.githubusercontent.com/12083176/415964040-6d703236-a453-4667-909d-d87d6f23983d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDAyOTM1MTYsIm5iZiI6MTc0MDI5MzIxNiwicGF0aCI6Ii8xMjA4MzE3Ni80MTU5NjQwNDAtNmQ3MDMyMzYtYTQ1My00NjY3LTkwOWQtZDg3ZDZmMjM5ODNkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMjMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjIzVDA2NDY1NlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTA3MWY1MTY2NTQ4MWI0YjcyZmQyMDQ1MDczNTYwNjgwZTU1NDA0YzYwZDYxNmVhMjQ3YmI3MjRlOTVhMGUxN2ImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.sZxtLOpT1iyzqhBQsD8sJiNnDeCs-jlKlCzi42Gx0Tc)

---

## ⚙️ **Installation & Setup**
### **Prerequisites**
✔️ Node.js & Angular CLI  
✔️ Python 3.10+  
✔️ PostgreSQL  
✔️ MS-Office 

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/resume-enhancer.git
cd resume-enhancer

Backend Setup (Flask)
cd backend
python -m venv venv
source venv/bin/activate  # (On Windows: venv\Scripts\activate)
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask run


Frontend Setup (Angular)

cd frontend
npm install
ng serve
🚀 Deployment
Frontend (Angular)
bash
Copy
Edit
ng build --configuration production
Host the dist/ folder on Firebase, Vercel, or Netlify.

Backend (Flask)
bash
Copy
Edit
gunicorn --bind 0.0.0.0:8000 wsgi:app
Deploy on Render, GCP App Engine, or AWS Lambda.

🛠 Contributing
Fork the repository 🍴
Create a branch (feature-new-ui) 🌿
Commit changes (git commit -m "Improved UI responsiveness") ✅
Push the branch (git push origin feature-new-ui) 🚀
Create a PR 🎉
