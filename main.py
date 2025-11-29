"""
Stealth Job Discovery Bot - Main Controller
Orchestrates job search, scraping, and AI analysis.
"""

import os
import time
from serpapi import GoogleSearch
from scraper import get_page_content
from analyzer import analyze_job
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def find_jobs(query="Software Developer", location="India", num_results=5):
    """
    Search for jobs using SerpApi's Google Jobs engine.
    
    Args:
        query (str): Job search query (e.g., "Python Developer", "Backend Engineer")
        location (str): Location filter (e.g., "India", "Remote", "San Francisco")
        num_results (int): Maximum number of jobs to return
        
    Returns:
        list: List of job postings with details
    """
    print(f"🔎 Searching Google Jobs for: '{query}' in '{location}'...\n")
    
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "in",  # Google country code (in = India)
        "api_key": os.getenv("SERPAPI_KEY")
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        jobs = results.get("jobs_results", [])
        
        if not jobs:
            print("⚠️  No jobs found. Try a different search query.")
            return []
        
        print(f"✅ Found {len(jobs)} potential jobs. Limiting to top {num_results}...\n")
        return jobs[:num_results]
        
    except Exception as e:
        print(f"❌ Error searching jobs: {e}")
        print("Make sure your SERPAPI_KEY is set correctly in .env file")
        return []


def extract_job_url(job):
    """
    Extract the best URL to scrape from a job result.
    Prioritizes company career pages over aggregator sites.
    
    Args:
        job (dict): Job posting from SerpApi
        
    Returns:
        str: URL to scrape, or None if no suitable URL found
    """
    # Try to get related links (company career pages)
    related_links = job.get('related_links', [])
    
    if related_links:
        # Filter out job boards - prefer direct company links
        excluded_domains = ['linkedin.com', 'indeed.com', 'glassdoor.com', 
                           'naukri.com', 'monster.com', 'ziprecruiter.com']
        
        for link in related_links:
            url = link.get('link', '')
            if not any(domain in url for domain in excluded_domains):
                return url
        
        # If no direct company link, use the first one
        return related_links[0].get('link')
    
    # Fallback: Try share_url or job_id-based link
    if 'share_url' in job:
        return job['share_url']
    
    return None


def run_bot(search_query="Python Developer", location="India", num_jobs=3, min_score=70):
    """
    Main bot execution function.
    
    Args:
        search_query (str): What kind of jobs to search for
        location (str): Where to search
        num_jobs (int): How many jobs to analyze (default 3 to save API credits)
        min_score (int): Minimum AI match score to be considered a good match (0-100)
    """
    print("="*60)
    print("🤖 STEALTH JOB DISCOVERY BOT - Starting...")
    print("="*60)
    print(f"Search: {search_query}")
    print(f"Location: {location}")
    print(f"Analyzing: Top {num_jobs} results")
    print(f"Minimum Score: {min_score}/100")
    print("="*60 + "\n")
    
    # Step 1: Find jobs using SerpApi
    jobs = find_jobs(query=search_query, location=location, num_results=num_jobs)
    
    if not jobs:
        print("\n❌ No jobs to analyze. Exiting.")
        return
    
    good_matches = []
    
    # Step 2: Analyze each job
    for idx, job in enumerate(jobs, 1):
        print(f"\n{'='*60}")
        print(f"📋 Job {idx}/{len(jobs)}: {job.get('title', 'Unknown Title')}")
        print(f"🏢 Company: {job.get('company_name', 'Unknown')}")
        print(f"📍 Location: {job.get('location', 'Unknown')}")
        print(f"{'='*60}")
        
        # Extract the URL to scrape
        target_url = extract_job_url(job)
        
        if not target_url:
            print("   ⚠️  No direct link found, skipping this job.")
            continue
        
        print(f"🔗 URL: {target_url}")
        
        # Step 3: Stealth scrape the job page
        content = get_page_content(target_url)
        
        if not content:
            print("   ❌ Failed to scrape content, moving to next job.")
            continue
        
        if len(content) < 100:
            print("   ⚠️  Content too short (likely access denied or paywall), skipping.")
            continue
        
        # Step 4: Analyze with AI
        analysis = analyze_job(content)
        
        score = analysis['match_score']
        reason = analysis['reason']
        apply_link = analysis.get('apply_link') or target_url
        
        print(f"\n   🎯 AI Match Score: {score}/100")
        print(f"   💡 Reason: {reason}")
        
        # Step 5: Save good matches
        if score >= min_score:
            print(f"   ✅ GOOD MATCH - Added to your list!")
            good_matches.append({
                "title": job.get('title'),
                "company": job.get('company_name'),
                "location": job.get('location'),
                "score": score,
                "reason": reason,
                "link": apply_link
            })
        else:
            print(f"   ⏭️  Score too low - Skipping")
        
        # Be nice to servers - small delay between requests
        if idx < len(jobs):
            time.sleep(2)
    
    # Step 6: Final report
    print("\n" + "="*60)
    print(f"🎉 FINAL REPORT: {len(good_matches)} Good Matches Found")
    print("="*60 + "\n")
    
    if not good_matches:
        print("😕 No jobs met your criteria. Try:")
        print("   - Lowering the min_score threshold")
        print("   - Using different search keywords")
        print("   - Expanding location preferences")
    else:
        for idx, match in enumerate(good_matches, 1):
            print(f"{idx}. 🏆 {match['title']} @ {match['company']}")
            print(f"   📍 {match['location']}")
            print(f"   🎯 Match: {match['score']}/100")
            print(f"   💡 Why: {match['reason']}")
            print(f"   🔗 Apply: {match['link']}")
            print()
    
    print("="*60)
    print("✅ Bot execution completed!")
    print("="*60)


def interactive_mode():
    """
    Interactive CLI mode - prompts user for search parameters.
    """
    print("\n" + "="*60)
    print("🤖 STEALTH JOB DISCOVERY BOT - Interactive Mode")
    print("="*60 + "\n")
    
    # Get user input
    search_query = input("What job are you looking for? (e.g., 'Python Developer'): ").strip()
    if not search_query:
        search_query = "Software Developer"
    
    location = input("Preferred location? (e.g., 'India', 'Remote', 'San Francisco'): ").strip()
    if not location:
        location = "India"
    
    try:
        num_jobs = int(input("How many jobs to analyze? (1-10, default 3): ").strip() or "3")
        num_jobs = max(1, min(num_jobs, 10))  # Clamp between 1-10
    except ValueError:
        num_jobs = 3
    
    try:
        min_score = int(input("Minimum match score? (0-100, default 70): ").strip() or "70")
        min_score = max(0, min(min_score, 100))  # Clamp between 0-100
    except ValueError:
        min_score = 70
    
    print("\n🚀 Starting search...\n")
    run_bot(search_query=search_query, location=location, num_jobs=num_jobs, min_score=min_score)


if __name__ == "__main__":
    # Check if API keys are configured
    if not os.getenv("SERPAPI_KEY") or os.getenv("SERPAPI_KEY") == "your_serpapi_key_here":
        print("\n❌ ERROR: SERPAPI_KEY not configured!")
        print("Please create a .env file and add your API keys.")
        print("See .env.example for the required format.\n")
        exit(1)
    
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_gemini_api_key_here":
        print("\n❌ ERROR: GEMINI_API_KEY not configured!")
        print("Please create a .env file and add your API keys.")
        print("See .env.example for the required format.\n")
        exit(1)
    
    # You can either use interactive mode or hardcode your preferences:
    
    # OPTION 1: Interactive mode (recommended for beginners)
    interactive_mode()
    
    # OPTION 2: Hardcoded search (uncomment below and comment out interactive_mode())
    # run_bot(
    #     search_query="GoLang Backend Developer",
    #     location="Remote",
    #     num_jobs=5,
    #     min_score=70
    # )
