# 🎨 UI User Guide

## Overview

The Stealth Job Discovery Bot now features a beautiful, professional Gradio-based web interface that makes job hunting easy and enjoyable!

## 🚀 Quick Start

### 1. Launch the UI

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Start the UI
python ui_app.py
```

### 2. Open Your Browser

Go to: **http://localhost:7860**

You'll see a beautiful purple-gradient interface!

---

## 📋 Using the Interface

### Left Panel: Your Profile & Settings

#### 📝 CV Upload
- Click "Upload CV (TXT file)" or drag & drop
- Use the provided `sample_cv.txt` or create your own
- CV preview appears automatically
- Skills are extracted automatically

#### 🎯 Search Parameters

**Job Title**
- What role you're looking for
- Examples: "Backend Developer", "Data Scientist", "Product Manager"

**Years of Experience**
- Slider from 0-20 years
- Affects job level (entry/mid/senior)

**Location**
- Where you want to work
- Examples: "Bangalore", "Remote", "India", "Mumbai"

**Company Tier**
- **High-Tier (MNCs)**: Google, Microsoft, Amazon, etc.
- **Mid-Tier (Established)**: TCS, Infosys, Flipkart, etc.
- **Startups (Unicorns)**: Razorpay, CRED, Polygon, etc.
- **All Tiers**: Search all 200+ companies

**Max Companies to Search**
- How many companies to check
- More companies = longer search time
- Recommended: 10-20 for quick results

**Minimum Match Score**
- Filter threshold (0-100)
- Jobs below this score are hidden
- Recommended: 70 for good matches

---

### Right Panel: Results

#### Status Box
Shows current operation status in real-time

#### Analysis Log
Detailed progress of the search:
- Skills detected from CV
- Companies being searched
- Jobs being analyzed
- AI match scores
- Final summary

#### Matching Jobs Table
Interactive table showing:
- Job Title
- Company Name
- Location
- Match Score
- Apply Link (clickable!)

#### Export Results
Click "💾 Export Results" to download a Markdown file with all matches

---

## 🎯 Search Process Explained

### Step 1: CV Analysis (10%)
- Reads your uploaded CV
- Extracts technical skills automatically
- Identifies programming languages, frameworks, tools

### Step 2: Company Selection (30%)
- Loads company database based on tier selection
- Prioritizes by tier: High → Mid → Startup

### Step 3: Job Search (40%)
- Searches Google Jobs via SerpApi
- Filters out job aggregators (Indeed, LinkedIn)
- Gets direct company career page links

### Step 4: Robots.txt Check (50%)
- **CRITICAL FOR LEGAL COMPLIANCE**
- Checks robots.txt for each company site
- Skips blocked URLs automatically
- Respects crawl delays

### Step 5: Stealth Scraping (60-90%)
- Visits job pages in stealth mode
- Mimics human behavior
- Extracts job descriptions
- Multiple layers of anti-detection

### Step 6: AI Analysis (90-100%)
- Sends job description to Gemini AI
- Compares against your CV
- Generates match score (0-100)
- Provides reasoning

### Step 7: Results Display (100%)
- Filters by minimum score
- Displays in beautiful table
- Provides direct apply links

---

## 💡 Pro Tips

### Get Better Results

1. **Use a Detailed CV**
   - Include all your skills
   - Mention specific technologies
   - Add years of experience for each

2. **Start Small**
   - Try 5-10 companies first
   - Adjust minimum score based on results
   - Then expand to more companies

3. **Be Specific with Job Title**
   - "Python Backend Developer" > "Developer"
   - "Senior Data Scientist" > "Analyst"
   - Include level (Junior/Mid/Senior)

4. **Adjust Match Score**
   - High score (80-100): Very selective
   - Medium score (60-79): Balanced
   - Low score (40-59): Exploratory

5. **Use "All Tiers" for Diversity**
   - Gets jobs from MNCs, mid-sized, and startups
   - More variety in culture and opportunities

### Avoid Common Mistakes

❌ **Don't upload PDF/Word files** - Convert to TXT first
❌ **Don't search 50+ companies initially** - Start small
❌ **Don't set minimum score below 50** - Too many false positives
❌ **Don't ignore robots.txt blocks** - They're there for a reason

---

## 🔧 Advanced Features

### Custom Company List

Edit `companies.py` to add your own companies:

```python
# Add to HIGH_TIER_COMPANIES, MID_TIER_COMPANIES, or STARTUP_COMPANIES
"YourCompany": "https://yourcompany.com/careers/"
```

### Skill Detection

The bot looks for these skills automatically:
- Programming: Python, Java, Go, JavaScript, C++, etc.
- Frameworks: React, Django, Spring, Node.js, etc.
- Cloud: AWS, Azure, GCP
- DevOps: Docker, Kubernetes, Jenkins
- Databases: PostgreSQL, MongoDB, Redis
- AI/ML: TensorFlow, PyTorch, Machine Learning

### Export Format

Exported files include:
- Timestamp
- All matching jobs
- Full details (title, company, location, score, reason, link)
- Markdown formatting for easy reading

---

## 🎨 UI Customization

### Change Theme Colors

Edit `ui_app.py`:

```python
theme=gr.themes.Soft(
    primary_hue="blue",      # Change to: green, red, purple, etc.
    secondary_hue="purple",   # Change to: blue, orange, etc.
)
```

### Change Port

Edit `ui_app.py`:

```python
app.launch(
    server_port=7861,  # Change from 7860
)
```

### Enable Public Sharing

Edit `ui_app.py`:

```python
app.launch(
    share=True,  # Creates a public gradio.live link
)
```

⚠️ **Warning**: Only enable public sharing if you trust who will access it!

---

## 📊 Understanding Match Scores

### 90-100: Excellent Match 🏆
- All key skills match
- Experience level perfect
- Location preferences align
- Highly recommended to apply!

### 70-89: Good Match ✅
- Most skills match
- Experience level appropriate
- Worth applying
- May need to highlight specific skills

### 50-69: Moderate Match ⚠️
- Some skills match
- Could be a stretch role
- Apply if interested in learning
- Prepare to explain gaps

### 0-49: Poor Match ❌
- Few matching skills
- Experience mismatch
- Not recommended unless you're pivoting careers

---

## 🛡️ Safety & Compliance

### What the Bot Does for Safety

✅ **Checks robots.txt** before every scrape
✅ **Respects crawl delays** specified by websites
✅ **Uses realistic delays** between requests
✅ **Avoids job aggregators** (no Indeed, LinkedIn scraping)
✅ **No auto-applying** (you're in control)
✅ **Rate limiting** to avoid overwhelming servers

### What You Should Do

✅ Only use for personal job searching
✅ Don't run searches too frequently (wait 1+ hour between runs)
✅ Respect company privacy policies
✅ Apply manually to jobs (never auto-apply)
✅ Don't share your API keys

---

## 📞 Troubleshooting UI Issues

### UI Won't Load

1. Check if port 7860 is available: `lsof -i :7860`
2. Try a different port (edit `ui_app.py`)
3. Check firewall settings

### Slow Performance

1. Reduce "Max Companies to Search"
2. Increase "Minimum Match Score" (fewer results to process)
3. Check internet connection
4. Verify API quotas not exceeded

### CV Not Uploading

1. Make sure file is .txt format (not .pdf or .docx)
2. Check file size < 10MB
3. Try copying content and pasting into a new .txt file

### No Results Found

1. Lower minimum match score
2. Try different job title
3. Expand company tier to "All Tiers"
4. Check if CV has enough skills listed

---

## 🎉 Happy Job Hunting!

Remember:
- This is a tool to **assist** you, not replace genuine networking
- Always **personalize** your applications
- **Follow up** professionally after applying
- Be **patient** - good jobs take time to find

Good luck! 🚀
