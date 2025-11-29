"""
Advanced Job Finder Module
Searches company career pages directly using SerpApi, avoiding job aggregators.
"""

import os
import time
from serpapi import GoogleSearch
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Domains to AVOID (job aggregators)
BLOCKED_DOMAINS = [
    'indeed.com',
    'linkedin.com',
    'naukri.com',
    'monster.com',
    'glassdoor.com',
    'ziprecruiter.com',
    'shine.com',
    'timesjobs.com',
    'instahyre.com',
    'hirist.com',
    'foundit.in',
    'apna.co',
]


def is_company_career_page(url: str) -> bool:
    """
    Check if URL is a direct company career page (not a job aggregator).
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if it's a company career page, False if it's an aggregator
    """
    url_lower = url.lower()
    
    # Block known aggregators
    for domain in BLOCKED_DOMAINS:
        if domain in url_lower:
            return False
    
    # Prefer URLs with career-related keywords
    career_keywords = ['career', 'job', 'hiring', 'work-with-us', 'join', 'opportunity']
    return any(keyword in url_lower for keyword in career_keywords)


def search_jobs_at_company(company_name: str, job_title: str = "", location: str = "India", logger=None):
    """
    Search for jobs at a specific company using SerpApi with logging.
    
    Args:
        company_name (str): Company to search at
        job_title (str): Optional job title filter
        location (str): Location filter
        logger: Logger function
        
    Returns:
        list: Job postings from that company
    """
    def log(msg, level="INFO"):
        if logger:
            logger(msg, level)
        else:
            print(f"[{level}] {msg}")
    
    if job_title:
        query = f"{job_title} at {company_name} {location}"
    else:
        query = f"jobs at {company_name} {location}"
    
    log(f"SerpApi Query: '{query}'")
    
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "in",
        "api_key": os.getenv("SERPAPI_KEY")
    }
    
    log(f"SerpApi Parameters: {params}")
    
    try:
        log("Sending request to SerpApi...")
        search = GoogleSearch(params)
        results = search.get_dict()
        
        log(f"SerpApi Response received")
        log(f"Response keys: {list(results.keys())}")
        
        jobs = results.get("jobs_results", [])
        log(f"Raw jobs found: {len(jobs)}")
        
        # Log the first job's structure for debugging
        if jobs:
            first_job = jobs[0]
            log(f"First job structure - Available fields: {list(first_job.keys())}")
            log(f"  - title: {first_job.get('title', 'N/A')}")
            log(f"  - company_name: {first_job.get('company_name', 'N/A')}")
            log(f"  - job_id: {first_job.get('job_id', 'N/A')}")
            
            # Check all available URL fields
            for key in ['apply_link', 'share_url', 'apply_options', 'related_links']:
                if key in first_job:
                    log(f"  - {key}: {first_job[key]}")
        
        # Filter to only include jobs from the target company
        company_jobs = [
            job for job in jobs 
            if company_name.lower() in job.get('company_name', '').lower()
        ]
        
        log(f"Filtered jobs (matching {company_name}): {len(company_jobs)}")
        
        return company_jobs
        
    except Exception as e:
        log(f"SerpApi Error: {str(e)}", "ERROR")
        return []


def extract_job_posting_url(job, logger=None):
    """
    Extract the ACTUAL job posting URL from SerpApi response.
    Prioritizes direct application links over generic career pages.
    
    Priority order:
    1. apply_link (direct job posting URL)
    2. apply_options (if contains direct link)
    3. related_links with job/career keywords
    4. share_url (fallback, usually aggregator)
    
    Args:
        job (dict): Job posting from SerpApi
        logger: Logger function (optional)
        
    Returns:
        tuple: (url, source) - URL and where it came from
    """
    def log(msg, level="INFO"):
        if logger:
            logger(f"    {msg}", level)
    
    # Priority 1: Direct apply_link (best option - actual job posting)
    if 'apply_link' in job:
        url = job['apply_link']
        if url and is_company_career_page(url):
            if log:
                log(f"✅ Found apply_link: {url}")
            return url, "apply_link"
    
    # Priority 2: apply_options (sometimes has direct links)
    apply_options = job.get('apply_options', [])
    if apply_options:
        for option in apply_options:
            url = option.get('link', '')
            if url and is_company_career_page(url):
                if log:
                    log(f"✅ Found apply_options link: {url}")
                return url, "apply_options"
    
    # Priority 3: related_links with career/job keywords
    related_links = job.get('related_links', [])
    for link in related_links:
        url = link.get('link', '')
        if url and is_company_career_page(url):
            # Prefer URLs with specific job indicators
            if any(x in url.lower() for x in ['job', 'position', 'opening', 'jid=', 'jobid=']):
                if log:
                    log(f"✅ Found related_link (specific job): {url}")
                return url, "related_links"
    
    # Priority 4: share_url (last resort, often aggregator)
    share_url = job.get('share_url', '')
    if share_url:
        # Only use if it's NOT an aggregator
        if is_company_career_page(share_url):
            if log:
                log(f"⚠️  Using share_url (fallback): {share_url}")
            return share_url, "share_url"
        else:
            if log:
                log(f"❌ share_url is aggregator, skipping: {share_url}")
    
    # No valid URL found
    if log:
        log(f"❌ No valid job URL found", "WARN")
    return None, "none"


def search_multiple_companies(
    companies: dict,
    job_title: str = "",
    location: str = "India",
    max_companies: int = 10,
    jobs_per_company: int = 3,
    logger=None
):
    """
    Search for jobs across multiple companies with detailed logging.
    
    Args:
        companies (dict): Company name -> career URL mapping
        job_title (str): Job title to search for
        location (str): Location filter
        max_companies (int): Maximum companies to search
        jobs_per_company (int): Max jobs to return per company
        logger: Logger function (optional)
        
    Returns:
        list: All job postings found
    """
    def log(msg, level="INFO"):
        if logger:
            logger(msg, level)
        else:
            print(f"[{level}] {msg}")
    
    all_jobs = []
    companies_searched = 0
    
    log(f"Starting search across {min(max_companies, len(companies))} companies")
    log(f"Search query: '{job_title}' in '{location}'")
    
    for company_name, career_url in list(companies.items())[:max_companies]:
        if companies_searched >= max_companies:
            break
        
        log(f"\\n{'='*60}")
        log(f"Company {companies_searched + 1}/{max_companies}: {company_name}")
        log(f"Career URL: {career_url}")
        log(f"{'='*60}")
        
        jobs = search_jobs_at_company(company_name, job_title, location, logger=log)
        
        if jobs:
            log(f"✅ Found {len(jobs)} jobs at {company_name}", "SUCCESS")
            
            # Add company career URL to each job
            for idx, job in enumerate(jobs[:jobs_per_company], 1):
                job['company_career_url'] = career_url
                
                log(f"  Job {idx}: {job.get('title', 'Unknown')}")
                log(f"    Location: {job.get('location', 'Unknown')}")
                
                # Extract actual job posting URL
                extracted_url, source = extract_job_posting_url(job, logger=log)
                job['career_page_url'] = extracted_url or career_url
                job['url_source'] = source
                
                log(f"    Final URL ({source}): {job['career_page_url']}")
                all_jobs.append(job)
        else:
            log(f"ℹ️  No jobs found at {company_name}", "WARN")
        
        companies_searched += 1
        
        # Rate limiting - be nice to SerpApi
        if companies_searched < max_companies:
            log("  Waiting 2s (rate limiting)...")
            time.sleep(2)
    
    log(f"\\nSearch complete: {len(all_jobs)} total jobs from {companies_searched} companies")
    return all_jobs


def search_by_skills_and_experience(
    job_title: str,
    skills: list,
    years_experience: int,
    location: str = "India",
    companies: dict = None,
    max_results: int = 20
):
    """
    Advanced search combining job title, skills, and experience.
    
    Args:
        job_title (str): Job title (e.g., "Backend Developer")
        skills (list): List of key skills (e.g., ["Python", "Go", "AWS"])
        years_experience (int): Years of experience
        location (str): Location preference
        companies (dict): Optional specific companies to search
        max_results (int): Maximum jobs to return
        
    Returns:
        list: Matching job postings
    """
    # Build search query
    skills_str = " ".join(skills[:3])  # Use top 3 skills
    
    if years_experience < 2:
        level = "entry level"
    elif years_experience < 5:
        level = "mid level"
    else:
        level = "senior"
    
    query = f"{level} {job_title} {skills_str} {location}"
    
    print(f"\n🎯 Advanced Search Query: {query}\n")
    
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "in",
        "api_key": os.getenv("SERPAPI_KEY")
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        jobs = results.get("jobs_results", [])[:max_results]
        
        # Filter out aggregators and add career URLs
        filtered_jobs = []
        for job in jobs:
            career_url, source = extract_job_posting_url(job)
            if career_url:  # Only include if we found a company career page
                job['career_page_url'] = career_url
                job['url_source'] = source
                filtered_jobs.append(job)
        
        print(f"✅ Found {len(filtered_jobs)} jobs from company career pages")
        print(f"❌ Filtered out {len(jobs) - len(filtered_jobs)} aggregator links")
        
        return filtered_jobs
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []


if __name__ == "__main__":
    # Test the job finder
    print("🧪 Testing Job Finder\n")
    
    # Test 1: Search at a specific company
    jobs = search_jobs_at_company("Google", "Software Engineer", "India")
    print(f"\nFound {len(jobs)} Google jobs")
    
    if jobs:
        job = jobs[0]
        print(f"\nSample Job:")
        print(f"  Title: {job.get('title')}")
        print(f"  Company: {job.get('company_name')}")
        print(f"  Location: {job.get('location')}")
        career_url, source = extract_job_posting_url(job)
        print(f"  Career URL ({source}): {career_url}")
