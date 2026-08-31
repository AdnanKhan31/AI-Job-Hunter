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
