"""
Stealth Web Scraper Module
Uses Playwright with stealth techniques to scrape job postings undetectably.
NOW INCLUDES ROBOTS.TXT COMPLIANCE CHECK!
"""

import time
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from robots_checker import is_url_scrapable, robots_checker


def get_page_content(url, respect_robots=True):
    """
    Visits a URL in stealth mode and returns the text content.
    
    This function mimics human behavior to avoid detection:
    - Uses realistic Chrome user agent
    - Disables automation flags
    - Implements random delays
    - Simulates mouse movements and scrolling
    - CHECKS ROBOTS.TXT BEFORE SCRAPING (if respect_robots=True)
    
    Args:
        url (str): The URL to scrape
        respect_robots (bool): Whether to check robots.txt compliance
        
    Returns:
        str: The extracted text content, or None if scraping fails or blocked
    """
    # Check robots.txt compliance first
    if respect_robots:
        allowed, reason = is_url_scrapable(url)
        print(f"   {reason}")
        
        if not allowed:
            print(f"⛔ Skipping {url} - Blocked by robots.txt")
            return None
        
        # Respect crawl delay if specified
        crawl_delay = robots_checker.get_crawl_delay(url)
        if crawl_delay:
            print(f"   ⏱️  Respecting crawl-delay: {crawl_delay}s")
            time.sleep(crawl_delay)
    
    print(f"🕵️  Stealth visiting: {url}")
    
    with sync_playwright() as p:
        # Launch browser with anti-detection settings
        browser = p.chromium.launch(
            headless=True,  # Set to False to watch the browser in action
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Create context with realistic browser fingerprint
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            geolocation={'latitude': 28.6139, 'longitude': 77.2090},  # Delhi coordinates
            color_scheme='light'
        )
        
        # Add realistic headers
        context.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        page = context.new_page()
        
        # Apply stealth techniques to hide automation
        stealth_sync(page)

        try:
            # Navigate with realistic timeout
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            
            # Human-like behavior: Random sleep (2-5 seconds)
            time.sleep(random.uniform(2, 5))
            
            # Simulate reading behavior - scroll slowly
            page.mouse.wheel(0, random.randint(300, 700))
            time.sleep(random.uniform(1, 2))
            
            # Optionally scroll down further (mimics reading)
            if random.random() > 0.5:
                page.mouse.wheel(0, random.randint(400, 800))
                time.sleep(random.uniform(0.5, 1.5))
            
            # Extract all visible text content
            content = page.evaluate("document.body.innerText")
            
            print(f"✅ Successfully scraped {len(content)} characters")
            return content
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return None
            
        finally:
            browser.close()


def get_page_html(url):
    """
    Alternative method: Returns raw HTML instead of just text.
    Use this if you need to parse specific HTML elements.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: The HTML content, or None if scraping fails
    """
    print(f"🕵️  Stealth visiting (HTML mode): {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        stealth_sync(page)

        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(random.uniform(2, 4))
            
            # Get full HTML
            html_content = page.content()
            return html_content
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return None
            
        finally:
            browser.close()


if __name__ == "__main__":
    # Test the scraper
    test_url = "https://www.python.org"
    content = get_page_content(test_url)
    if content:
        print(f"\n📄 Preview (first 500 chars):\n{content[:500]}")
