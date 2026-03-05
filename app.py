"""
FastAPI Portfolio Application
"""
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import resend

# Load environment variables
load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")

# Static Data
SKILLS = [
    {"name": "Python", "category": "Language", "level": 90},
    {"name": "C", "category": "Language", "level": 85},
    {"name": "C++", "category": "Language", "level": 80},
    {"name": "C#", "category": "Language", "level": 75},
    {"name": "Mobile App Dev", "category": "Framework", "level": 85},
    {"name": "OOP", "category": "Concept", "level": 90},
    {"name": "Advanced DB", "category": "Database", "level": 80},
    {"name": "DIP", "category": "Specialization", "level": 75}
]

PROJECTS = [
    {
        "name": "Daily Dua & Azkar App",
        "desc": "Mobile app for daily prayers and remembrances",
        "url": "https://github.com/Rubina-Bibi/Rubina-Bibi-Rubina-Bibi-RollNo-100069-DailyDua-AzkarApp-MobileApplicationDevelopment-TermProject01",
        "image": "/static/images/project1.jpg"
    },
    {
        "name": "Document Scanner",
        "desc": "Digital image processing for document digitization",
        "url": "https://github.com/Rubina-Bibi/DIP-Project-Document-Scanner-100069-5th-Semester",
        "image": "/static/images/project2.jpg"
    }
]

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Server Started!")
    yield
    # Shutdown logic
    print("Server Stopped!")

# Create App
app = FastAPI(title="Rubina Bibi - Portfolio", version="1.0.0", lifespan=lifespan)

# Mount Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "skills": SKILLS,
        "projects": PROJECTS,
        "name": "Rubina Bibi",
        "role": "Aspiring Fullstack Developer | Computer Operator",
        "email": "rubinabibi.khr.tech1144@gmail.com",
        "linkedin": "https://www.linkedin.com/in/rubina-bibi-b87578359",
        "github": "https://github.com/Rubina-Bibi",
        "facebook": "https://www.facebook.com/share/1CJQfwRh4c/"
    })

# API: Skills
@app.get("/api/skills")
async def api_skills():
    return JSONResponse({"success": True, "data": SKILLS})

# API: Projects
@app.get("/api/projects")
async def api_projects():
    return JSONResponse({"success": True, "data": PROJECTS})

# API: Contact
@app.post("/api/contact")
async def contact(request: Request):
    try:
        data = await request.json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()
        print(f"DEBUG: Received contact request - Name: {name}, Email: {email}")
        print(f"DEBUG: RESEND_API_KEY set: {'Yes' if resend.api_key else 'No'}")
        print(f"DEBUG: CONTACT_EMAIL: {CONTACT_EMAIL}")
        
        if not (name and email and message):
            return JSONResponse({"success": False, "message": "Fill all fields!"}, status_code=400)

        # Send Email via Resend
        if resend.api_key and CONTACT_EMAIL:
            params = {
                "from": "Portfolio Contact <onboarding@resend.dev>",
                "to": [CONTACT_EMAIL],
                "subject": f"New Message from {name}",
                "html": f"<strong>Name:</strong> {name}<br><strong>Email:</strong> {email}<br><strong>Message:</strong><p>{message}</p>",
            }
            print(f"DEBUG: Sending email from onboarding@resend.dev to {CONTACT_EMAIL}")
            resend.Emails.send(params)
            print("DEBUG: Email sent successfully")
            return JSONResponse({"success": True, "message": "Message sent to email! Correct"})
        else:
            return JSONResponse({"success": False, "message": "Email service not configured. Check .env!"}, status_code=500)

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"DEBUG: Exception in contact API:\n{error_trace}")
        return JSONResponse({"success": False, "message": f"Error: {str(e)}", "trace": error_trace}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)