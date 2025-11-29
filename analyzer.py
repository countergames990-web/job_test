"""
AI Job Analyzer Module
Uses Google Gemini AI to match job descriptions against your profile.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# ============================================
# 🎯 CUSTOMIZE YOUR PROFILE HERE
# ============================================
MY_PROFILE = """
I am a Software Developer with experience in backend development.
Skills: Python, Go, JavaScript, React, Node.js, Docker, Kubernetes, AWS, PostgreSQL, MongoDB
Experience: 3 years
Looking for: Full-time remote or hybrid roles in software engineering
Preferred locations: India, USA, Europe (remote)
Industries: Tech startups, SaaS companies, fintech
"""

# You can also load your CV from a file instead:
def load_cv_from_file(filepath="my_cv.txt"):
    """
    Optional: Load your CV/profile from a text file instead of hardcoding it.
    Create a file called 'my_cv.txt' in the same directory.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  CV file '{filepath}' not found. Using default profile.")
        return MY_PROFILE


def analyze_job(job_text, use_cv_file=False, logger=None):
    """
    Analyzes a job description using AI to determine match quality with logging.
    
    Args:
        job_text (str): The full text content of the job posting
        use_cv_file (bool): If True, loads profile from 'my_cv.txt'
        logger: Logger function for detailed logging
        
    Returns:
        dict: Contains match_score (0-100), reason, and apply_link
    """
    def log(msg, level="INFO"):
        if logger:
            logger(msg, level)
        else:
            print(f"[{level}] {msg}")
    
    profile = load_cv_from_file() if use_cv_file else MY_PROFILE
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Truncate job text to avoid token limits (keep first 10,000 chars)
    truncated_job_text = job_text[:10000]
    
    log(f"Preparing AI analysis...")
    log(f"  Job text length: {len(job_text)} chars (truncated to {len(truncated_job_text)})")
    log(f"  Using model: gemini-2.5-flash")
    
    prompt = f"""
You are an expert career advisor and recruiter. Your job is to analyze whether a job posting matches a candidate's profile.

CANDIDATE PROFILE:
{profile}

JOB DESCRIPTION TEXT:
{truncated_job_text}

INSTRUCTIONS:
1. Analyze how well this job matches the candidate's skills, experience, and preferences.
2. Assign a match score from 0-100:
   - 90-100: Excellent match, highly recommended
   - 70-89: Good match, worth applying
   - 50-69: Moderate match, could apply if interested
   - 0-49: Poor match, not recommended
3. Extract the direct application URL from the text if present (look for "Apply at:", "Click here:", job portal links, etc.)
4. Provide a concise 1-2 sentence explanation for the score.

IMPORTANT: Return ONLY valid JSON with no additional text, markdown formatting, or code blocks.

Required JSON format:
{{
    "match_score": 85,
    "reason": "Strong match for backend skills with Go and Python. Remote position aligns with preferences.",
    "apply_link": "https://company.com/careers/apply/12345"
}}

If no apply link is found in the text, set apply_link to null.
"""
    
    try:
        log("Sending request to Gemini AI...")
        response = model.generate_content(prompt)
        log("Received AI response")
        
        # Clean up response - remove markdown code blocks if present
        clean_json = response.text.strip()
        log(f"  Raw response preview: {clean_json[:150]}...")
        clean_json = clean_json.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        log("Parsing AI response as JSON...")
        result = json.loads(clean_json)
        
        # Validate structure
        if not all(key in result for key in ['match_score', 'reason']):
            raise ValueError("Invalid JSON structure")
            
        # Ensure apply_link exists (even if null)
        if 'apply_link' not in result:
            result['apply_link'] = None
        
        log(f"✅ AI analysis successful", "SUCCESS")
        log(f"  Match score: {result['match_score']}/100")
        log(f"  Reason: {result['reason'][:100]}...")
            
        return result
        
    except json.JSONDecodeError as e:
        log(f"JSON parsing failed: {e}", "ERROR")
        log(f"Raw AI response: {response.text[:200]}", "ERROR")
        return {
            "match_score": 0,
            "reason": "AI response format error - could not parse analysis",
            "apply_link": None
        }
        
    except Exception as e:
        log(f"AI Analysis failed: {str(e)}", "ERROR")
        return {
            "match_score": 0,
            "reason": f"Error during analysis: {str(e)}",
            "apply_link": None
        }


def batch_analyze_jobs(job_list):
    """
    Analyze multiple jobs in sequence.
    
    Args:
        job_list (list): List of dicts with 'title', 'company', and 'text' keys
        
    Returns:
        list: List of results with original job data plus analysis
    """
    results = []
    
    for idx, job in enumerate(job_list, 1):
        print(f"\n📊 Analyzing job {idx}/{len(job_list)}: {job.get('title', 'Unknown')}")
        
        analysis = analyze_job(job.get('text', ''))
        
        results.append({
            'title': job.get('title'),
            'company': job.get('company'),
            'url': job.get('url'),
            'match_score': analysis['match_score'],
            'reason': analysis['reason'],
            'apply_link': analysis.get('apply_link')
        })
        
    return results


if __name__ == "__main__":
    # Test the analyzer
    print("🧪 Testing AI Analyzer...\n")
    
    sample_job_text = """
    Senior Backend Engineer - Go & Python
    
    Company: TechCorp Inc.
    Location: Remote (India)
    
    We are looking for an experienced backend engineer with strong skills in:
    - Go (Golang) and Python
    - Microservices architecture
    - Docker and Kubernetes
    - AWS cloud services
    - 3+ years of experience
    
    This is a full-time remote position.
    
    Apply at: https://techcorp.com/careers/apply/backend-123
    """
    
    result = analyze_job(sample_job_text)
    
    print(f"✅ Match Score: {result['match_score']}/100")
    print(f"📝 Reason: {result['reason']}")
    print(f"🔗 Apply Link: {result['apply_link']}")
