# 🚀 **Resume Enhancer with AI**  
_A cutting-edge AI-powered tool to enhance resumes, built with **Angular** (Frontend) and **Flask** (Backend)._

![Resume Enhancer Banner](https://img.shields.io/badge/Angular-Standalone-blue?style=flat&logo=angular) ![Flask Backend](https://img.shields.io/badge/Flask-Backend-green?style=flat&logo=flask) ![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat&logo=postgresql)

---

## 🌟 **Overview**  
Resume Enhancer with AI is a **modern web application** that allows users to **upload resumes and enhance them using AI**. This tool leverages **Flask for backend** API processing, **Angular for an interactive UI**, and **PostgreSQL** for database storage.

### **Key Features** 🎯
 **AI-powered resume enhancement** 🧠  
 **Secure authentication (JWT)** 🔒  
 **Responsive UI with Angular standalone components** 🎨  
 **Database integration using PostgreSQL** 🗄️  
 **RESTful API with Flask** 🚀  


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
Commit changes (git commit -m "Improved UI responsiveness") 
Push the branch (git push origin feature-new-ui) 🚀
Create a PR 🎉
