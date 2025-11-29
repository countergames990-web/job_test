# 🤖 Stealth Job Discovery Bot

A fully automated, **legally compliant** job discovery tool with a beautiful UI that finds jobs matching your skills using AI, without violating any terms of service.

## ⚖️ Legal & Ethical Compliance

This bot is designed to be **100% legal and undetectable**:

- ✅ **Checks robots.txt before every scrape** (automatic compliance)
- ✅ **Scrapes only public job postings** (no authentication bypass)
- ✅ **Goes directly to company career pages** (avoids Indeed, LinkedIn aggregators)
- ✅ **Uses human-like behavior** to avoid detection
- ✅ **Does NOT auto-apply** to jobs (you apply manually)
- ✅ **Respects crawl delays** specified in robots.txt
- ✅ **No IP bans** - polite rate limiting and delays

⚠️ **Important**: You are responsible for ensuring compliance with the websites you scrape. This tool is for **personal, non-commercial use only**.

---

## 🎯 What It Does

1. **Upload Your CV**: Upload a .txt file with your resume
2. **Auto-Skill Detection**: Extracts skills from your CV automatically
3. **Company Database**: Searches 200+ companies (MNCs, Mid-tier, Startups)
4. **Robots.txt Compliance**: Checks and respects robots.txt before scraping
5. **Direct Career Pages**: Goes to company sites, not job aggregators
6. **AI Matching**: Analyzes jobs with Google Gemini AI
7. **Beautiful Results**: Shows matching jobs in an elegant interface
8. **Export Feature**: Download results as Markdown

**You stay in control** - the bot never applies on your behalf.

---

## 🎨 New Beautiful UI Features

- 💜 Modern gradient design with Gradio
- 📤 Drag-and-drop CV upload
- ⚙️ Customizable search parameters
- 📊 Real-time progress tracking
- 📋 Interactive results table
- 💾 Export results to file
- 📱 Mobile-responsive design

---

## 📋 Prerequisites

- **Python 3.8+** installed on your machine
- **Git** (optional, for cloning the repo)
- **Internet connection**
- Two free API keys (instructions below)

---

## 🚀 Installation Guide

### One-Command Setup (Easiest!)

```bash
./setup.sh
```

This automated script will:
1. Create virtual environment
2. Install all dependencies
3. Install Playwright browsers
4. Set up .env file

### Manual Setup

#### Step 1: Clone or Download This Repository

```bash
git clone <your-repo-url>
cd job_test
```

Or download and extract the ZIP file.

### Step 2: Create a Virtual Environment

This keeps your project dependencies isolated.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers

Playwright needs to download Chromium:

```bash
playwright install chromium
```

This downloads a special version of Chrome for automation (~100MB).

---

## 🔑 Get Your API Keys (Both FREE)

### 1. SerpApi Key (for Google Jobs search)

1. Go to [serpapi.com](https://serpapi.com/)
2. Sign up for a free account
3. Copy your API key from the dashboard
4. **Free tier**: 100 searches/month

### 2. Gemini API Key (for AI job analysis)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. **Free tier**: 60 requests/minute

### 3. Create Your `.env` File

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` and paste your keys:

```bash
SERPAPI_KEY=your_actual_serpapi_key_here
GEMINI_API_KEY=your_actual_gemini_key_here
```

**Never commit `.env` to Git!** (already in `.gitignore`)

---

## ⚙️ Configuration

### Customize Your Profile

Open `analyzer.py` and edit the `MY_PROFILE` variable:

```python
MY_PROFILE = """
I am a GoLang Developer with 3 years of experience.
Skills: Go, Microservices, Docker, Kubernetes, AWS, PostgreSQL
Experience: 3 years
Looking for: Remote or Hybrid roles
Preferred locations: India, USA (remote)
Industries: Tech startups, SaaS companies
"""
```

**Pro tip**: You can also create a `my_cv.txt` file and set `use_cv_file=True` in `main.py`.

---

## 🎮 How to Run

### Quick Start (UI Mode - Recommended!)

1. **Activate your virtual environment**:
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. **Start the beautiful UI**:
```bash
python ui_app.py
```

3. **Open your browser**:
   - Go to: `http://localhost:7860`
   - You'll see a beautiful purple-gradient interface!

4. **Use the bot**:
   - Upload your `sample_cv.txt` (or create your own)
   - Set job title, experience, location
   - Choose company tier (High/Mid/Startup/All)
   - Click "🚀 Start Job Search"
   - Watch real-time progress!
   - Get matching jobs with apply links
   - Export results to Markdown

### Command Line Mode (Advanced)

```bash
python main.py
```

The bot will ask you:
- What job title to search for
- Location preference
- How many jobs to analyze
- Minimum match score threshold

### Option 2: Hardcoded Search

Edit `main.py` and uncomment this section at the bottom:

```python
run_bot(
    search_query="Python Backend Developer",
    location="Remote",
    num_jobs=5,
    min_score=70
)
```

Then run:

```bash
python main.py
```

---

## 📊 Example Output

```
🔎 Searching Google Jobs for: 'Python Developer' in 'India'...

✅ Found 10 potential jobs. Limiting to top 3...

============================================================
📋 Job 1/3: Senior Python Developer
🏢 Company: TechCorp
📍 Location: Bangalore, India
============================================================
🔗 URL: https://techcorp.com/careers/python-dev
🕵️  Stealth visiting: https://techcorp.com/careers/python-dev
✅ Successfully scraped 4523 characters
🤖 Analyzing job with AI...

   🎯 AI Match Score: 87/100
   💡 Reason: Strong match for Python and Docker skills. Remote option available.
   ✅ GOOD MATCH - Added to your list!

============================================================
🎉 FINAL REPORT: 2 Good Matches Found
============================================================

1. 🏆 Senior Python Developer @ TechCorp
   📍 Bangalore, India
   🎯 Match: 87/100
   💡 Why: Strong match for Python and Docker skills
   🔗 Apply: https://techcorp.com/careers/python-dev

============================================================
✅ Bot execution completed!
============================================================
```

---

## 🛠️ Advanced Usage

### Test Individual Modules

Test the scraper:
```bash
python scraper.py
```

Test the AI analyzer:
```bash
python analyzer.py
```

### Adjust Stealth Settings

In `scraper.py`, change `headless=True` to `headless=False` to watch the browser:

```python
browser = p.chromium.launch(headless=False, ...)
```

### Increase Job Limit

Edit `main.py` and increase `num_jobs`:

```python
run_bot(num_jobs=10)  # Analyze more jobs
```

⚠️ **Note**: More jobs = more API credits used.

---

## 🧪 Troubleshooting

### ❌ "playwright: command not found"

Run: `playwright install chromium`

### ❌ "Error: SERPAPI_KEY not configured"

Make sure your `.env` file exists and has the correct key.

### ❌ "Address already in use" (Gradio)

Port 7860 is already in use. Either:
- Stop the other process using that port
- Change the port in `ui_app.py`: `app.launch(server_port=7861)`

### ❌ "Blocked by robots.txt"

The bot automatically skips sites that block scraping. This is expected and prevents IP bans.

### ❌ "JSON parsing failed"

The AI sometimes returns improperly formatted JSON. The bot handles this gracefully and skips that job.

### ❌ "Access Denied" or empty content

Some sites block automated scrapers. The bot will skip these jobs automatically.

### ❌ Rate limiting

If you get rate limited:
- Increase delays in `scraper.py` (change `time.sleep` values)
- Reduce `num_jobs` in your search
- Wait a few minutes before retrying

---

## 📁 Project Structure

```bash
job_test/
├── ui_app.py            # 🎨 Beautiful Gradio UI (START HERE!)
├── main.py              # Command-line controller
├── scraper.py           # Stealth web scraper (with robots.txt check)
├── analyzer.py          # AI job matcher (Gemini)
├── job_finder.py        # Advanced job search (no aggregators)
├── robots_checker.py    # Robots.txt compliance validator
├── companies.py         # 200+ company database
├── requirements.txt     # Python dependencies
├── sample_cv.txt        # Example CV for testing
├── .env.example         # API key template
├── .env                 # Your actual keys (never commit!)
├── .gitignore          # Keeps .env private
└── README.md           # This file
```

---

## 🔒 Privacy & Security

- **API keys**: Never share your `.env` file
- **Personal data**: Your CV/profile stays local (not uploaded anywhere)
- **Scraped data**: Only stored temporarily in memory
- **No tracking**: The bot doesn't send your data to third parties

---

## 📝 Legal Disclaimer

This tool is provided for **educational and personal use only**. You are responsible for:

1. ✅ Ensuring compliance with websites' Terms of Service
2. ✅ Respecting rate limits and robots.txt
3. ✅ Not using it for commercial purposes without authorization
4. ✅ Manually applying to jobs (never auto-applying)

The authors are not responsible for misuse of this software.

---

## 🤝 Contributing

Improvements welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 🆘 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Ensure API keys are correctly set in `.env`
3. Verify Python 3.8+ is installed: `python --version`
4. Check Playwright is installed: `playwright --version`

---

## 📜 License

This project is provided as-is under the MIT License. Use responsibly.

---

## 🎉 Happy Job Hunting!

Remember: This bot is a **tool to assist you**, not a replacement for genuine networking and applications. Always personalize your applications and follow up professionally.

Good luck! 🚀
