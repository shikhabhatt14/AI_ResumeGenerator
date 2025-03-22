from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
import pdfkit

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_resume_content(name, experience, skills, job_desc):
    prompt = f"""
    Create a professional resume summary and work experience bullets for:
    Name: {name}
    Experience: {experience}
    Skills: {skills}
    Job Description: {job_desc if job_desc else 'N/A'}
    """
    #response = client.chat.completions.create(
    #    model="gemini-2.0-flash",
    #    messages=[{"role": "user", "content": prompt}]
    #)
    #return response.choices[0].message.content
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def render_resume(name, email, content):

    env = Environment(loader=FileSystemLoader("resumeTemplates"))
    template = env.get_template("resumeTemplate.html")
    html_out = template.render(name=name, email=email, content=content)

    output_path = f"{name.replace(' ', '_')}_resume.pdf"
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(html_out, output_path)
    return output_path
