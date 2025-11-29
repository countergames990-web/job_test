"""
Beautiful Gradio UI for Stealth Job Discovery Bot
Professional, modern interface with CV upload and customization.
"""

import gradio as gr
import os
import time
from dotenv import load_dotenv

# Import our modules
from companies import get_companies_by_tier, get_all_companies
from job_finder import search_by_skills_and_experience, search_multiple_companies
from scraper import get_page_content
from analyzer import analyze_job
from robots_checker import is_url_scrapable

load_dotenv()

# Global state to store results
search_results = []


def read_cv_file(cv_file):
    """Read CV from uploaded file"""
    if cv_file is None:
        return "No CV uploaded. Please upload your CV.txt file."
    
    try:
        with open(cv_file.name, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading CV: {str(e)}"


def extract_skills_from_text(text):
    """Extract key skills from CV text (simple keyword extraction)"""
    common_skills = [
        'Python', 'Java', 'JavaScript', 'Go', 'Golang', 'C++', 'C#', 'Ruby', 'PHP',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
        'Machine Learning', 'AI', 'Deep Learning', 'TensorFlow', 'PyTorch',
        'REST API', 'GraphQL', 'Microservices', 'Git', 'Linux'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills[:10]  # Return top 10


def run_job_search(
    cv_file,
    job_title,
    years_exp,
    location,
    company_tier,
    max_companies,
    min_match_score,
    progress=gr.Progress()
):
    """Main job search function with progress tracking"""
    
    global search_results
    search_results = []
    
    # Initialize detailed logging
    detailed_logs = []
    
    def log(msg, level="INFO"):
        """Helper to log messages"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {msg}"
        detailed_logs.append(log_entry)
        print(log_entry)  # Also print to console
    
    log("=" * 80)
    log("JOB SEARCH SESSION STARTED")
    log("=" * 80)
    log(f"Search Parameters: Title={job_title}, Location={location}, Tier={company_tier}")
    log(f"Settings: Max Companies={max_companies}, Min Score={min_match_score}")
    
    # Step 1: Read CV
    progress(0.1, desc="📄 Reading your CV...")
    log("STEP 1: Reading CV file...")
    cv_content = read_cv_file(cv_file)
    log(f"CV loaded: {len(cv_content)} characters")
    
    if "Error" in cv_content or "No CV" in cv_content:
        log(f"ERROR: CV read failed - {cv_content}", "ERROR")
        return cv_content, "❌ Cannot proceed without CV", [], "\n".join(detailed_logs)
    
    # Extract skills
    progress(0.2, desc="🔍 Extracting skills from CV...")
    log("STEP 2: Extracting skills from CV...")
    skills = extract_skills_from_text(cv_content)
    log(f"Skills detected: {', '.join(skills) if skills else 'None'}")
    
    if not skills:
        skills = ["Software Development"]  # Fallback
    
    skills_display = f"**Detected Skills:** {', '.join(skills)}\n\n"
    
    # Step 2: Get companies to search
    progress(0.3, desc="🏢 Loading company database...")
    log("STEP 3: Loading company database...")
    
    if company_tier == "All Tiers":
        companies = get_all_companies()
        log(f"Loaded all companies: {len(companies)} total")
    else:
        tier_map = {
            "High-Tier (MNCs)": "high",
            "Mid-Tier (Established)": "mid",
            "Startups (Unicorns)": "startup"
        }
        companies = get_companies_by_tier(tier_map[company_tier])
        log(f"Loaded {company_tier}: {len(companies)} companies")
    
    total_companies = min(max_companies, len(companies))
    log(f"Will search {total_companies} companies")
    
    # Step 3: Search for jobs
    progress(0.4, desc=f"🔎 Searching jobs at {total_companies} companies...")
    log("STEP 4: Searching for jobs via SerpApi...")
    log("-" * 80)
    
    found_jobs = search_multiple_companies(
        companies=companies,
        job_title=job_title,
        location=location,
        max_companies=max_companies,
        jobs_per_company=2,
        logger=log  # Pass our log function
    )
    
    log("-" * 80)
    log(f"Search complete: Found {len(found_jobs)} total job postings")
    
    if not found_jobs:
        log("WARNING: No jobs found from search", "WARN")
        return (
            skills_display + "❌ No jobs found. Try different search criteria.",
            "No jobs to analyze",
            [],
            "\n".join(detailed_logs)
        )
    
    progress_msg = f"{skills_display}✅ Found {len(found_jobs)} potential jobs\n\n"
    progress_msg += "🤖 Starting AI analysis...\n\n"
    
    log("STEP 5: Starting AI job analysis...")
    log("-" * 80)
    
    # Step 4: Analyze each job
    good_matches = []
    
    for idx, job in enumerate(found_jobs):
        progress(
            0.4 + (0.5 * (idx / len(found_jobs))),
            desc=f"🤖 Analyzing job {idx+1}/{len(found_jobs)}..."
        )
        
        job_title_text = job.get('title', 'Unknown')
        company_name = job.get('company_name', 'Unknown')
        job_url = job.get('career_page_url', '')
        url_source = job.get('url_source', 'unknown')
        
        log(f"Job {idx+1}/{len(found_jobs)}: {job_title_text} @ {company_name}")
        log(f"  URL: {job_url or 'No URL'}")
        log(f"  URL Source: {url_source}")
        
        # Check robots.txt
        if job_url:
            log(f"  Checking robots.txt for {job_url}...")
            allowed, reason = is_url_scrapable(job_url)
            log(f"  robots.txt result: Allowed={allowed}, Reason={reason}")
            if not allowed:
                progress_msg += f"⏭️  Skipped: {job_title_text} @ {company_name} (robots.txt blocked)\n"
                log(f"  SKIPPED due to robots.txt", "WARN")
                continue
        
        # Scrape job details
        progress_msg += f"🕵️  Analyzing: {job_title_text} @ {company_name}\n"
        
        content = None
        content_source = ""
        
        if job_url:
            log(f"  Attempting to scrape job page...")
            content = get_page_content(job_url, respect_robots=True)
            if content and len(content) >= 100:
                log(f"  ✅ Scraped {len(content)} characters from job page")
                content_source = "scraped"
            else:
                log(f"  ⚠️  Scraping returned insufficient content ({len(content) if content else 0} chars)")
        
        # Use SerpApi description as fallback (often has good details)
        if not content or len(content) < 100:
            description = job.get('description', '')
            if description:
                log(f"  Using SerpApi description: {len(description)} characters")
                content = f"Job Title: {job_title_text}\\n\\n{description}"
                content_source = "serpapi_description"
            else:
                log(f"  No description available from SerpApi")
        
        if not content or len(content) < 50:
            progress_msg += f"   ⚠️  Could not fetch details, skipping\\n\\n"
            log(f"  SKIPPED: Content too short ({len(content) if content else 0} chars)", "WARN")
            continue
        
        log(f"  Content source: {content_source}, length: {len(content)}")
        
        # AI Analysis
        log(f"  Sending to Gemini AI for analysis...")
        analysis = analyze_job(content, logger=log)
        score = analysis['match_score']
        log(f"  AI returned score: {score}/100")
        
        progress_msg += f"   🎯 Score: {score}/100 - {analysis['reason']}\n"
        
        if score >= min_match_score:
            log(f"  ✅ GOOD MATCH! (score {score} >= threshold {min_match_score})")
            good_matches.append({
                'title': job_title_text,
                'company': company_name,
                'location': job.get('location', 'Unknown'),
                'score': score,
                'reason': analysis['reason'],
                'url': job_url or job.get('share_url', '#'),
                'apply_link': analysis.get('apply_link') or job_url
            })
            progress_msg += f"   ✅ GOOD MATCH!\n\n"
        else:
            log(f"  ⏭️ Score too low ({score} < {min_match_score})")
            progress_msg += f"   ⏭️  Score too low\n\n"
        
        log("")  # Empty line for readability
        time.sleep(1)  # Rate limiting
    
    log("-" * 80)
    log(f"Analysis complete: {len(good_matches)} jobs matched criteria")
    
    # Step 5: Final results
    progress(1.0, desc="✅ Search complete!")
    log("STEP 6: Preparing final results...")
    
    if not good_matches:
        final_msg = f"\n\n{'='*50}\n😕 No jobs matched your criteria (min score: {min_match_score})\n"
        final_msg += "Try lowering the minimum match score or broadening your search.\n"
        final_msg += f"{'='*50}"
        log("No matches found meeting criteria", "WARN")
        log("=" * 80)
        log("SESSION ENDED - NO MATCHES")
        log("=" * 80)
        return skills_display + progress_msg + final_msg, "No matches found", [], "\n".join(detailed_logs)
    
    # Format results
    results_table = []
    final_summary = f"\n\n{'='*50}\n🎉 Found {len(good_matches)} Excellent Matches!\n{'='*50}\n\n"
    
    for idx, match in enumerate(good_matches, 1):
        final_summary += f"{idx}. **{match['title']}** @ **{match['company']}**\n"
        final_summary += f"   📍 {match['location']}\n"
        final_summary += f"   🎯 Match Score: {match['score']}/100\n"
        final_summary += f"   💡 {match['reason']}\n"
        final_summary += f"   🔗 [Apply Here]({match['apply_link']})\n\n"
        
        # Table format
        results_table.append([
            match['title'],
            match['company'],
            match['location'],
            f"{match['score']}/100",
            match['apply_link']
        ])
    
    search_results = good_matches
    
    log(f"Formatted {len(good_matches)} results for display")
    log("=" * 80)
    log("SESSION ENDED - SUCCESS")
    log("=" * 80)
    
    return (
        skills_display + progress_msg + final_summary,
        f"✅ Analysis complete! Found {len(good_matches)} matching jobs.",
        results_table,
        "\n".join(detailed_logs)  # Return logs as 4th value
    )


def export_results():
    """Export results to a file"""
    if not search_results:
        return None
    
    output = "# Job Search Results\n\n"
    output += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    output += f"Total Matches: {len(search_results)}\n\n"
    output += "="*60 + "\n\n"
    
    for idx, job in enumerate(search_results, 1):
        output += f"## {idx}. {job['title']}\n"
        output += f"- **Company:** {job['company']}\n"
        output += f"- **Location:** {job['location']}\n"
        output += f"- **Match Score:** {job['score']}/100\n"
        output += f"- **Why:** {job['reason']}\n"
        output += f"- **Apply:** {job['apply_link']}\n\n"
    
    # Save to file
    filename = f"job_results_{int(time.time())}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return filename


# Create Gradio Interface
with gr.Blocks(
    title="🤖 Stealth Job Discovery Bot",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="purple",
    ),
    css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            padding: 10px;
            color: #666;
            font-size: 0.9em;
        }
    """
) as app:
    
    # Header
    gr.HTML("""
        <div class="header">
            <h1>🤖 Stealth Job Discovery Bot</h1>
            <p>AI-Powered Job Matching with Robots.txt Compliance</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📝 Your Profile")
            
            cv_file = gr.File(
                label="Upload CV (TXT file)",
                file_types=[".txt"],
                type="filepath"
            )
            
            cv_preview = gr.Textbox(
                label="CV Preview",
                lines=5,
                placeholder="CV content will appear here...",
                interactive=False
            )
            
            cv_file.change(
                fn=read_cv_file,
                inputs=[cv_file],
                outputs=[cv_preview]
            )
            
            gr.Markdown("---")
            gr.Markdown("## 🎯 Search Parameters")
            
            job_title = gr.Textbox(
                label="Job Title",
                placeholder="e.g., Backend Developer, Data Scientist",
                value="Software Engineer"
            )
            
            years_exp = gr.Slider(
                label="Years of Experience",
                minimum=0,
                maximum=20,
                step=1,
                value=3
            )
            
            location = gr.Textbox(
                label="Location",
                placeholder="e.g., Bangalore, Remote, India",
                value="India"
            )
            
            company_tier = gr.Radio(
                label="Company Tier",
                choices=[
                    "High-Tier (MNCs)",
                    "Mid-Tier (Established)",
                    "Startups (Unicorns)",
                    "All Tiers"
                ],
                value="All Tiers"
            )
            
            max_companies = gr.Slider(
                label="Max Companies to Search",
                minimum=1,
                maximum=50,
                step=1,
                value=10,
                info="More companies = longer search time"
            )
            
            min_match_score = gr.Slider(
                label="Minimum Match Score",
                minimum=0,
                maximum=100,
                step=5,
                value=70,
                info="Jobs scoring below this will be filtered out"
            )
            
            search_btn = gr.Button(
                "🚀 Start Job Search",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=2):
            gr.Markdown("## 📊 Search Results")
            
            status_box = gr.Textbox(
                label="Status",
                lines=1,
                interactive=False
            )
            
            results_box = gr.Markdown(
                value="Click 'Start Job Search' to begin...",
                label="Analysis Log"
            )
            
            gr.Markdown("### 🔍 Detailed Logs (Debug)")
            
            logs_box = gr.Textbox(
                label="System Logs",
                lines=15,
                max_lines=30,
                interactive=False,
                placeholder="Detailed logs will appear here...",
                show_label=True
            )
            
            gr.Markdown("### 📋 Matching Jobs")
            
            results_table = gr.Dataframe(
                headers=["Job Title", "Company", "Location", "Score", "Apply Link"],
                datatype=["str", "str", "str", "str", "str"],
                label="Top Matches",
                wrap=True
            )
            
            export_btn = gr.Button("💾 Export Results", variant="secondary")
            export_file = gr.File(label="Download Results")
    
    # Event handlers
    search_btn.click(
        fn=run_job_search,
        inputs=[
            cv_file,
            job_title,
            years_exp,
            location,
            company_tier,
            max_companies,
            min_match_score
        ],
        outputs=[results_box, status_box, results_table, logs_box]  # Added logs_box as 4th output
    )
    
    export_btn.click(
        fn=export_results,
        outputs=[export_file]
    )
    
    # Footer
    gr.HTML("""
        <div class="footer">
            <p>⚖️ <strong>Legal & Ethical Use:</strong> This bot respects robots.txt, only scrapes public data, and never auto-applies to jobs.</p>
            <p>🔒 Your CV stays local. No data is uploaded to external servers.</p>
        </div>
    """)


if __name__ == "__main__":
    # Check API keys
    if not os.getenv("SERPAPI_KEY") or not os.getenv("GEMINI_API_KEY"):
        print("\n❌ ERROR: API keys not configured!")
        print("Please set SERPAPI_KEY and GEMINI_API_KEY in your .env file\n")
        exit(1)
    
    print("\n" + "="*60)
    print("🚀 Starting Gradio UI Server...")
    print("="*60)
    print("\n📌 Features:")
    print("  ✅ Beautiful modern interface")
    print("  ✅ CV upload and skill extraction")
    print("  ✅ Robots.txt compliance checking")
    print("  ✅ Direct company career pages only")
    print("  ✅ AI-powered job matching")
    print("  ✅ Export results to Markdown")
    print("\n" + "="*60 + "\n")
    
    # Launch the app
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to create a public link
        show_error=True
    )
