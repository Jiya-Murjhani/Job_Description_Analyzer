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

STRICT RULES(Read all of these carefully before responding and follow them exactly):
1. Return valid JSON only. No explanation. No preamble. No markdown. Only raw JSON.
2. Only extract skills explicitly stated in the Job Description. Never invent or infer.
3. If fewer than 10 skills are present in the JD, extract only what exists — do not pad the list.
4. Matched_skills and Missing_skills must only contain skills from Required_skills. No exceptions.
5. Match_score calculation:
   - Strong match = 1 full point
   - Partial match = 0.5 points  
   - Missing = 0 points
   Score = (total points / total skills extracted) x 100. Round to nearest integer.
6. For skill matching, accept clear semantic equivalents 
   (e.g. "ML" = "Machine Learning") as strong matches. 
   If the skill is implied or indirectly related, mark it partial. 
   Only mark missing if there is no reference whatsoever.
7. Treat this as a fresher or early-career candidate unless the resume clearly shows 
   2+ years of experience. Calibrate suggestions to beginner-to-intermediate level.
8. For each missing skill suggestion:
   - If the skill can be inferred from existing resume experience → 
     Start with "Rewrite:" and provide the exact rewritten resume bullet.
   - If the skill is completely absent → 
     Start with "Project:" and give a specific 1-2 line project idea 
     showing exactly how the skill is demonstrated and what the output is.
    -For "Rewrite:" suggestions, only reference skills, techniques, 
and experiences that are explicitly present in the resume. 
Never invent or assume specific methods the candidate used 
that are not stated in the resume.
9. When extracting skills, only extract:
- Technical skills (Python, Pandas, machine learning, etc.)
- Tools and frameworks (Scikit-learn, NumPy, Tableau, etc.)
- Domain knowledge areas (predictive modeling, data analysis, etc.)

Do NOT extract:
- Soft skills (analytical thinking, problem-solving, communication)
- Attitude or interest statements ("interest in X", "passion for Y")
- Remote work capability statements
- Generic professional traits
10. If the same skill appears multiple times in different phrasings, 
extract it only once using the most concise technical form. 
For example: "Python" not "Knowledge of Python programming fundamentals".
11. Detect the seniority level of the role from the Job Description 
(internship / entry-level / mid-level / senior-level).
Calibrate your skill matching and suggestions accordingly:
- Internship/Entry-level: academic projects and coursework count as valid experience
- Mid-level: personal projects count but professional experience is weighted higher
- Senior-level: only professional experience counts, not academic projects
For internship/entry-level roles, certifications and 
relevant coursework listed under Education count as 
valid evidence of a skill. Do not mark a skill missing 
if it appears in certifications or academic coursework.
12. For each matched skill, assign a confidence level:
   - "strong": skill is explicitly and clearly stated in the resume
   - "partial": skill is implied, related, or mentioned indirectly
   Never assign strong confidence unless the skill is directly and 
   explicitly present in the resume.
13. Overall_tip must be:
    - A single sentence only
    - Specific to this candidate's resume and this JD
    - The single most impactful thing they can do to improve their chances
    - Actionable — not generic advice like "keep learning"
    -The tip must reference something specific from the candidate's 
     actual resume — a project, skill, or experience already present — 
     and connect it directly to a gap or requirement in this JD.
    Example: "Add Scikit-learn model training examples to your GitHub 
    to directly demonstrate the hands-on ML experience this role requires."
12. Match_summary must reflect both strong and partial matches separately, 
not just a single count.

Return ONLY this JSON format:
{{
  "Required_skills": ["skill1", "skill2", ...],
  "Matched_skills": [
    {{"skill": "skill1", "confidence": "strong"}},
    {{"skill": "skill2", "confidence": "partial"}}
  ],
  "Missing_skills": ["skill3", ...],
  "Total_skills_extracted": 10,
  "Match_score": 60,
  "Match_summary": "5 strong matches, 2 partial matches out of 10 required skills",
  "Overall_tip": "One sentence of the most important advice for this candidate.",
  "Suggestions": {{
    "skill3": "Rewrite: ... OR Project: ..."
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