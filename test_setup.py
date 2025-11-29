"""
Test script to verify all modules work correctly
Run this before launching the UI to ensure everything is set up properly
"""

import os
import sys

print("\n" + "="*60)
print("🧪 TESTING STEALTH JOB DISCOVERY BOT")
print("="*60 + "\n")

# Test 1: Check API Keys
print("1️⃣  Checking API Keys...")
from dotenv import load_dotenv
load_dotenv()

serpapi_key = os.getenv("SERPAPI_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not serpapi_key or serpapi_key == "your_serpapi_key_here":
    print("   ❌ SERPAPI_KEY not configured!")
    print("   → Add your key to .env file")
    sys.exit(1)
else:
    print(f"   ✅ SERPAPI_KEY found ({serpapi_key[:10]}...)")

if not gemini_key or gemini_key == "your_gemini_api_key_here":
    print("   ❌ GEMINI_API_KEY not configured!")
    print("   → Add your key to .env file")
    sys.exit(1)
else:
    print(f"   ✅ GEMINI_API_KEY found ({gemini_key[:10]}...)")

# Test 2: Check Dependencies
print("\n2️⃣  Checking Dependencies...")
try:
    import gradio
    print(f"   ✅ Gradio {gradio.__version__}")
except ImportError:
    print("   ❌ Gradio not installed")
    print("   → Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from playwright.sync_api import sync_playwright
    print("   ✅ Playwright installed")
except ImportError:
    print("   ❌ Playwright not installed")
    print("   → Run: pip install playwright")
    sys.exit(1)

try:
    from serpapi import GoogleSearch
    print("   ✅ SerpApi installed")
except ImportError:
    print("   ❌ SerpApi not installed")
    print("   → Run: pip install google-search-results")
    sys.exit(1)

try:
    import google.generativeai as genai
    print("   ✅ Gemini AI installed")
except ImportError:
    print("   ❌ Gemini AI not installed")
    print("   → Run: pip install google-generativeai")
    sys.exit(1)

# Test 3: Check Custom Modules
print("\n3️⃣  Checking Custom Modules...")
try:
    from companies import get_all_companies
    companies = get_all_companies()
    print(f"   ✅ companies.py loaded ({len(companies)} companies)")
except Exception as e:
    print(f"   ❌ Error loading companies.py: {e}")
    sys.exit(1)

try:
    from robots_checker import is_url_scrapable
    print("   ✅ robots_checker.py loaded")
except Exception as e:
    print(f"   ❌ Error loading robots_checker.py: {e}")
    sys.exit(1)

try:
    from job_finder import search_jobs_at_company
    print("   ✅ job_finder.py loaded")
except Exception as e:
    print(f"   ❌ Error loading job_finder.py: {e}")
    sys.exit(1)

try:
    from analyzer import analyze_job
    print("   ✅ analyzer.py loaded")
except Exception as e:
    print(f"   ❌ Error loading analyzer.py: {e}")
    sys.exit(1)

try:
    from scraper import get_page_content
    print("   ✅ scraper.py loaded")
except Exception as e:
    print(f"   ❌ Error loading scraper.py: {e}")
    sys.exit(1)

# Test 4: Test Robots.txt Checker
print("\n4️⃣  Testing Robots.txt Checker...")
test_url = "https://careers.google.com/jobs/results/"
try:
    allowed, reason = is_url_scrapable(test_url)
    print(f"   ✅ Test URL: {test_url}")
    print(f"   ✅ Result: {reason}")
except Exception as e:
    print(f"   ⚠️  Warning: {e}")
    print("   This might be okay if you're offline")

# Test 5: Test Company Database
print("\n5️⃣  Testing Company Database...")
from companies import HIGH_TIER_COMPANIES, MID_TIER_COMPANIES, STARTUP_COMPANIES

print(f"   ✅ High-Tier: {len(HIGH_TIER_COMPANIES)} companies")
print(f"   ✅ Mid-Tier: {len(MID_TIER_COMPANIES)} companies")
print(f"   ✅ Startups: {len(STARTUP_COMPANIES)} companies")
print(f"   ✅ Total: {len(companies)} companies")

# Test 6: Check Sample CV
print("\n6️⃣  Checking Sample CV...")
if os.path.exists("sample_cv.txt"):
    with open("sample_cv.txt", 'r') as f:
        cv_lines = len(f.readlines())
    print(f"   ✅ sample_cv.txt exists ({cv_lines} lines)")
else:
    print("   ⚠️  sample_cv.txt not found (optional)")

# Test 7: Check Playwright Browsers
print("\n7️⃣  Checking Playwright Browsers...")
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        browser.close()
    print("   ✅ Playwright Chromium browser installed")
except Exception as e:
    print(f"   ❌ Playwright browser not installed: {e}")
    print("   → Run: playwright install chromium")
    sys.exit(1)

# All tests passed!
print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\n🚀 You're ready to run the bot!")
print("\nNext steps:")
print("  1. Run UI: python ui_app.py")
print("  2. Open browser: http://localhost:7860")
print("  3. Upload your CV and start searching!")
print("\n" + "="*60 + "\n")
