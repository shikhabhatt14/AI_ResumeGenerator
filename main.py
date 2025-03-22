from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from resumeGenerator import generate_resume_content, render_resume

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-resume")
async def generate_resume(
        request: Request,
        name: str = Form(...),
        email: str = Form(...),
        experience: str = Form(...),
        skills: str = Form(...),
        job_description: str = Form(None)
):
    ai_content = generate_resume_content(name, experience, skills, job_description)
    pdf_path = render_resume(name, email, ai_content)
    return FileResponse(pdf_path, media_type='application/pdf', filename="resume.pdf")
