from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import pymupdf
import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
TOKEN = os.getenv("TOKEN")
JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

def calculate_match_score(job, resume_skills):
    total_skills = len(resume_skills)

    if total_skills == 0:
        return 0

    matched_skills = job.get("matched_skills", [])

    score = (len(matched_skills) / total_skills) * 100

    return round(score)

def role_matches(job_title, job_role):
    job_title = job_title.lower()
    job_role = job_role.lower()

    role_words = job_role.split()

    matched_words = 0

    for word in role_words:
        if word in job_title:
            matched_words += 1

    return matched_words == len(role_words)

def search_jobs(job_role, location):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": job_role,
        "where": location,
        "results_per_page": 20
    }

    response = requests.get(url, params=params)

    print("Adzuna status:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        print("Adzuna Error:", response.status_code)
        print(response.text)
        return None


def search_himalayas_jobs(job_role):
    url = "https://himalayas.app/jobs/api/search"

    params = {
        "q": job_role,
        "page": 1
    }

    response = requests.get(url, params=params)

    print("Himalayas status:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        print("Himalayas Error:", response.status_code)
        print(response.text)
        return None
    

def search_jooble_jobs(job_role, location):
    url = f"https://in.jooble.org/api/{JOOBLE_API_KEY}"

    data = {
        "keywords": job_role,
        "location": location,
        "page": 1
    }

    response = requests.post(url, json=data)

    print("Jooble status:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        print("Jooble Error:", response.status_code)
        print(response.text)
        return None

def experience_matches(job_text, experience):
    ranges = re.findall(
        r'(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*years?',
        job_text
    )

    plus_years = re.findall(
        r'(\d+(?:\.\d+)?)\s*\+?\s*years?',
        job_text
    )

    if "fresher" in experience or "entry" in experience:
        if any(word in job_text for word in [
            "senior",
            "sr.",
            "lead",
            "manager",
            "principal",
            "director"
        ]):
            return False

        if ranges:
            for start, end in ranges:
                if float(start) >= 2:
                    return False

        for years in plus_years:
            if float(years) >= 2:
                return False

        return True

    if "1-3 years" in experience:
        for start, end in ranges:
            if float(start) > 3:
                return False

        for years in plus_years:
            if float(years) > 3:
                return False

    if "3-5 years" in experience:
        for start, end in ranges:
            if float(start) > 5 or float(end) < 3:
                return False

    for years in plus_years:
        if float(years) > 5:
            return False

    if "5+ years" in experience:
        for start, end in ranges:
            if float(end) < 5:
                return False

        for years in plus_years:
            if float(years) < 5:
                return False

    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "👋 Welcome to AI Job Hunter!\n\n"
        "🎯 What type of opportunity are you looking for?\n\n"
        "1️⃣ Internship\n"
        "2️⃣ Fresher / Entry-Level Role\n"
        "3️⃣ Experienced Role — 1–3 years\n"
        "4️⃣ Experienced Role — 3–5 years\n"
        "5️⃣ Experienced Role — 5+ years"
    )

    context.user_data["waiting_for_opportunity"] = True


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("waiting_for_opportunity"):
        if text == "1":
            context.user_data["opportunity_type"] = "Internship"
            context.user_data["experience"] = "Internship"

        elif text == "2":
            context.user_data["opportunity_type"] = "Fresher / Entry-Level"
            context.user_data["experience"] = "Fresher"

        elif text == "3":
            context.user_data["opportunity_type"] = "Experienced 1-3 years"
            context.user_data["experience"] = "1-3 years"

        elif text == "4":
            context.user_data["opportunity_type"] = "Experienced 3-5 years"
            context.user_data["experience"] = "3-5 years"

        elif text == "5":
            context.user_data["opportunity_type"] = "Experienced 5+ years"
            context.user_data["experience"] = "5+ years"

        else:
            await update.message.reply_text(
                "❌ Please choose 1, 2, 3, 4, or 5."
            )
            return

        context.user_data["waiting_for_opportunity"] = False
        context.user_data["waiting_for_job_role"] = True

        await update.message.reply_text(
            "💼 What job role are you looking for?"
        )
        return

    if context.user_data.get("waiting_for_job_role"):
        context.user_data["job_role"] = text
        context.user_data["waiting_for_job_role"] = False
        context.user_data["waiting_for_location"] = True

        await update.message.reply_text(
            "📍 What is your preferred location?"
        )
        return

    if context.user_data.get("waiting_for_location"):
        context.user_data["location"] = text
        context.user_data["waiting_for_location"] = False
        context.user_data["waiting_for_resume"] = True

        await update.message.reply_text(
            "📄 Please upload your resume as a PDF."
        )
        return

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_resume"):
        return

    document = update.message.document

    if document.mime_type != "application/pdf":
        await update.message.reply_text("❌ Please upload your resume as a PDF file.")
        return

    file = await document.get_file()

    file_path = f"resume_{update.effective_user.id}.pdf"

    await file.download_to_drive(file_path)
    doc = pymupdf.open(file_path)

    resume_text = ""

    for page in doc:

        resume_text += page.get_text()

    doc.close()

    context.user_data["resume_path"] = file_path
    context.user_data["waiting_for_resume"] = False
    await update.message.reply_text("📄 Resume text extracted successfully!")
    await update.message.reply_text("📄 Resume received successfully!")
    print(resume_text)

    skills = []
    common_skills = ["Python", "SQL", "Excel", "Power BI", "Tableau", "R", "Java", "C++", "JavaScript"]

    for skill in common_skills:
        if skill.lower() in resume_text.lower():
            skills.append(skill)

    context.user_data["skills"] = skills

    print("Job role:", context.user_data.get("job_role"))
    print("Detected skills:", context.user_data.get("skills"))

    job_role = context.user_data.get("job_role")
    location = context.user_data.get("location")

    print("Location:", location)

    await update.message.reply_text(
        "🔎 Searching for the best jobs for you..."
    )

    jobs_data = search_jobs(job_role, location)
    himalayas_data = search_himalayas_jobs(job_role)

    print("Himalayas jobs:", len(himalayas_data.get("jobs", []) if himalayas_data else []))

    jooble_data = search_jooble_jobs(job_role, location)

    print("Jooble jobs:", len(jooble_data.get("jobs", []) if jooble_data else []))

    resume_skills = context.user_data.get("skills", [])

    if jobs_data or himalayas_data or jooble_data:
        
        jobs = jobs_data.get("results", []) if jobs_data else []

        himalayas_jobs = himalayas_data.get("jobs", [])
        jobs.extend(himalayas_jobs)

        jooble_jobs = jooble_data.get("jobs", [])

        for job in jooble_jobs:
            job["title"] = job.get("title", "")
            job["description"] = job.get("snippet", "")
            job["company"] = {
                "display_name": job.get("company", "Unknown company")
            }
            job["redirect_url"] = job.get("link", "")

        jobs.extend(jooble_jobs)

        print("Total jobs before filtering:", len(jobs))

        experience = context.user_data.get("experience", "").lower()
        opportunity_type = context.user_data.get("opportunity_type", "").lower()

        filtered_jobs = []

        for job in jobs:
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()

            job_text = title + " " + description

            job_requirements = []

            for skill in common_skills:
                 if skill.lower() in job_text:
                    job_requirements.append(skill)

            resume_match = []

            for skill in job_requirements:
                if skill in resume_skills:
                    resume_match.append(skill)

            job["resume_matched_skills"] = resume_match

            resume_match_score = 0

            if len(job_requirements) > 0:
                resume_match_score = round(
                    (len(resume_match) / len(job_requirements)) * 100
                )

            job["resume_match_score"] = resume_match_score

            missing_requirements = [
                skill for skill in job_requirements
                if skill not in resume_match
            ]

            job["missing_requirements"] = missing_requirements

            if not role_matches(title, job_role):
                continue

            if "internship" in opportunity_type:
                if "intern" not in job_text and "internship" not in job_text:
                    continue    

            if not experience_matches(job_text, experience):
                continue

        
            filtered_jobs.append(job)

        jobs = filtered_jobs

        resume_skills = context.user_data.get("skills", [])

        matched_jobs = []

        for job in jobs:
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()

            job_text = title + " " + description

            matched_skills = []

            for skill in resume_skills:
                if skill.lower() in job_text:
                    matched_skills.append(skill)

            job["matched_skills"] = matched_skills
            job["match_count"] = len(matched_skills)

            job["match_score"] = calculate_match_score(
                job,
                resume_skills
            )

            matched_jobs.append(job)

        jobs = matched_jobs

        jobs = [
            job for job in jobs
            if job.get("match_score", 0) >= 30
        ]

        unique_jobs = []
        seen_urls = set()

        for job in jobs:
            job_url = job.get("redirect_url", "")

            if job_url and job_url in seen_urls:
                continue

            if job_url:
                seen_urls.add(job_url)

            unique_jobs.append(job)

        jobs = unique_jobs

        jobs.sort(
            key=lambda job: job.get("match_score", 0),
            reverse=True
)


        if jobs:
            await update.message.reply_text(
                f"🔎 Found {len(jobs)} jobs for {job_role} in {location}."
            )

            for job in jobs:
                title = job.get("title", "No title")
                company = job.get("company", {}).get("display_name", "Unknown company")
                description = job.get("description", "No description available")
                job_url = job.get("redirect_url", "")

                await update.message.reply_text(
                    f"💼 {title}\n"
                    f"🏢 {company}\n"
                    f"📍 {location}\n\n"
                    f"🎯 Overall Match: {job.get('match_score', 0)}%\n"
                    f"📄 Resume Match: {job.get('resume_match_score', 0)}%\n"
                    f"🛠️ Skills Matched: {job.get('match_count', 0)}/{len(resume_skills)}\n"
                    f"📄 Resume Skills Matching Job: {', '.join(job.get('resume_matched_skills', [])) or 'None'}\n"
                    f"⚠️ Missing Requirements: {', '.join(job.get('missing_requirements', [])) or 'None'}\n"
                    f"✅ Matching Skills: {', '.join(job.get('matched_skills', [])) or 'None'}\n"
                    f"📝 Job Description:\n"
                    f"{description[:500]}\n\n"
                    f"🔗 Apply Here:\n"
                    f"{job_url}"

                    )

        else:
            await update.message.reply_text(
                f"❌ No suitable jobs found for {job_role} at the selected experience level."
            )
            await start(update, context)

    else:
        await update.message.reply_text(
            "❌ Unable to find jobs from the available job sources right now. Please try again later."
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("❌ Unexpected error:", context.error)

    if update and getattr(update, "effective_message", None):
        await update.effective_message.reply_text(
            "⚠️ Something went wrong. Please try again."
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.add_handler(MessageHandler(filters.Document.PDF, resume))

app.add_error_handler(error_handler)

app.run_polling()
