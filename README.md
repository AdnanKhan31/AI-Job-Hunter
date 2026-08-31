## Problem Statement

Job seekers often have to monitor multiple job portals to discover relevant opportunities. Repeatedly searching across different platforms can be time-consuming and may result in duplicated listings, irrelevant opportunities, and difficulty identifying which positions genuinely align with their skills and experience.

Even after finding a suitable opportunity, candidates often need to manually compare the job description with their resume to understand how well their skills match the requirements.

## Solution

**AI Job Hunter** is a Python-based Telegram bot designed to streamline the job-search and job-matching process through a single interface.

The bot collects the candidate's opportunity preference, job role, preferred location, experience level, and resume. It then retrieves job listings from multiple job sources and applies role, location, opportunity-type, and experience-based filtering.

The bot also extracts relevant skills from the candidate's resume and compares them with the skills and requirements identified in each job description. It calculates an overall match score, displays matching skills, highlights missing requirements, removes duplicate listings, and ranks relevant opportunities based on their match score.

This provides candidates with a more structured way to discover relevant opportunities and assess their suitability before applying.

## Key Features
* 🔎 **Multi-Source Job Search** — Retrieves job opportunities from Adzuna, Himalayas, and Jooble.
* 🎯 **Opportunity & Experience Filtering** — Supports internships, fresher/entry-level roles, and experienced roles across different experience ranges.
* 📍 **Location-Based Search** — Searches for opportunities based on the candidate's preferred location.
* 📄 **Resume PDF Processing** — Extracts text from an uploaded resume and identifies relevant skills.
* 🧩 **Resume–Job Matching** — Compares skills identified in the resume with skills and requirements found in job descriptions.
* 📊 **Match Scoring** — Calculates an overall percentage match for each job opportunity.
* ⚠️ **Missing Requirement Detection** — Highlights job requirements that are not identified in the candidate's resume.
* ♻️ **Duplicate Removal** — Removes duplicate job listings based on their URLs.
* 📈 **Relevance Ranking** — Ranks filtered opportunities from highest to lowest match score.
* 🔗 **Job Application Links** — Provides direct links to the available job listings.
* 🛡️ **Error Handling** — Provides user-friendly feedback when unexpected errors occur.

## Technology Stack
* **Python** — Core programming language and application logic
* **Python-Telegram-Bot** — Telegram bot development and user interaction
* **PyMuPDF** — PDF resume text extraction
* **Requests** — API requests and job data retrieval
* **Adzuna API** — Job listing source
* **Himalayas Jobs API** — Job listing source
* **Jooble API** — Job listing source
* **python-dotenv** — Secure management of API credentials and environment variables
* **Regular Expressions (Regex)** — Experience and requirement pattern detection

## How It Works
1. **Select Opportunity Type** — Choose an internship, fresher/entry-level role, or experienced role based on experience level.
2. **Enter Job Role** — Specify the type of job you are looking for.
3. **Specify Location** — Enter the preferred job location.
4. **Upload Resume** — Upload the resume as a PDF file.
5. **Extract Resume Skills** — The bot extracts text from the resume and identifies relevant skills.
6. **Search Multiple Job Sources** — Retrieves job listings from Adzuna, Himalayas, and Jooble.
7. **Filter Opportunities** — Filters listings based on job role, opportunity type, location, and experience requirements.
8. **Match Resume with Jobs** — Compares skills identified in the resume with relevant skills found in each job description.
9. **Calculate Match Scores** — Calculates an overall percentage match based on the identified skill overlap.
10. **Identify Missing Requirements** — Highlights relevant requirements that are not identified in the resume.
11. **Remove Duplicates** — Removes duplicate listings using job URLs.
12. **Rank Results** — Sorts opportunities from highest to lowest match score.
13. **Display Results** — Presents the job title, company, location, match scores, matching skills, missing requirements, job description, and application link.

## Project Structure
```text
AI-Job-Hunter/
│
├── bot.py          # Main Telegram bot application
├── .gitignore      # Prevents sensitive and unnecessary files from being committed
├── .env            # Local environment variables (not committed to GitHub)
├── README.md       # Project documentation
└── requirements.txt # Python dependencies
```

## Project Demo

https://github.com/user-attachments/assets/963d1b25-292c-42d7-bfe4-a1d6434a0b52

## Limitations & Future Improvements

### Current Limitations

* 🌐 **External Job-Source Dependency** — Job availability and data quality depend on the external job sources and APIs used by the application.
* 📝 **Job Description Formatting** — Some job descriptions may contain HTML elements from the source, which can occasionally affect how the description is displayed.
* 🧩 **Skill-Based Matching** — Resume–job matching primarily relies on identifiable skills and requirements extracted from the resume and job description, so some contextual qualifications may not be captured.
* 🔄 **Local Execution** — The current version is designed to run locally and requires the application environment and API credentials to be available.

### Future Improvements

* 🧹 Improve HTML sanitization and job-description formatting.
* 🤖 Implement more advanced NLP/AI-based resume–job matching.
* 📊 Introduce more detailed match explanations and ranking factors.
* 🔔 Add automated job alerts and scheduled searches.
* ☁️ Deploy the bot to a cloud environment for continuous availability.
* 🗂️ Add additional job sources and improve duplicate detection.





  
