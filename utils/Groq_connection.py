from groq import Groq
import os
from dotenv import load_dotenv
import json  

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

def resume_and_jd_comparison(resume_text, job_description):
    prompt = f"""
You are a senior technical recruiter with 10+ years of experience at top tech companies, 
combined with an AI/ML career coach who has helped hundreds of candidates land roles. 
You think like a hiring manager — you know exactly what gets a resume shortlisted 
and what gets it rejected in the first 10 seconds.

Below is a Job Description and a Resume. Your job is to:

1. Extract the top 10 MOST IMPORTANT required skills from the Job Description
2. Check which of those skills are present in the Resume
3. List the skills that are missing
4. Give a match score out of 100 based on matched skills
5. For each missing skill, give one specific, actionable suggestion

STRICT RULES:
1. Return valid JSON only. No explanation. No preamble. No markdown. Only raw JSON.
2. Only extract skills explicitly stated in the Job Description. Never invent or infer.
3. If fewer than 10 skills are present in the JD, extract only what exists — do not pad the list.
4. Matched_skills and Missing_skills must only contain skills from Required_skills. No exceptions.
5. Match_score = (number of matched skills / total skills extracted) x 100. Round to nearest integer.
6. For skill matching, accept clear semantic equivalents (e.g. "ML" = "Machine Learning") 
   but do not stretch — if it requires assumption, mark it missing.
7. Treat this as a fresher or early-career candidate unless the resume clearly shows 
   2+ years of experience. Calibrate suggestions to beginner-to-intermediate level.
8. For each missing skill suggestion:
   - If the skill can be inferred from existing resume experience → 
     Start with "Rewrite:" and provide the exact rewritten resume bullet.
   - If the skill is completely absent → 
     Start with "Project:" and give a specific 1-2 line project idea 
     showing exactly how the skill is demonstrated and what the output is.

Return ONLY this JSON format:
{{
  "Required_skills": ["skill1", "skill2", ...],
  "Matched_skills": ["skill1", ...],
  "Missing_skills": ["skill2", ...],
  "Total_skills_extracted": 10,
  "Match_score": 60,
  "Match_summary": "6 out of 10 required skills found in resume",
  "Suggestions": {{
    "skill2": "Rewrite: ... OR Project: ..."
  }}
}}

Job Description:
{job_description}

Resume:
{resume_text}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        # Parse and return dictionary directly
        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response was: {raw}")
        return None

    except Exception as e:
        print(f"Groq API error: {e}")
        return None