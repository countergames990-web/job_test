"""
Robots.txt Compliance Checker
Ensures we respect website robots.txt rules to avoid IP bans and legal issues.
"""

import urllib.robotparser
import urllib.parse
from urllib.parse import urlparse
import requests
from typing import Optional
import time

class RobotsChecker:
    """
    Checks if a URL can be scraped according to robots.txt rules.
    Caches robots.txt to avoid repeated requests.
    """
    
    def __init__(self, user_agent="Mozilla/5.0 (compatible; JobBot/1.0)"):
        self.user_agent = user_agent
        self.cache = {}  # Cache robots.txt parsers by domain
        self.cache_timeout = 3600  # 1 hour cache
        self.cache_timestamps = {}
    
    def can_fetch(self, url: str) -> tuple[bool, str]:
        """
        Check if we're allowed to scrape this URL.
        
        Args:
            url (str): The URL to check
            
        Returns:
            tuple: (can_fetch: bool, reason: str)
        """
        try:
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            robots_url = f"{domain}/robots.txt"
            
            # Check cache
            current_time = time.time()
            if domain in self.cache:
                if current_time - self.cache_timestamps.get(domain, 0) < self.cache_timeout:
                    rp = self.cache[domain]
                    if rp is None:
                        # Previously failed to fetch robots.txt - allow by default
                        return True, "No robots.txt found (allowed by default)"
                    
                    if rp.can_fetch(self.user_agent, url):
                        return True, "✅ Allowed by robots.txt"
                    else:
                        return False, "❌ Blocked by robots.txt"
            
            # Fetch and parse robots.txt
            print(f"📋 Checking robots.txt: {robots_url}")
            
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            
            try:
                rp.read()
                self.cache[domain] = rp
                self.cache_timestamps[domain] = current_time
                
                if rp.can_fetch(self.user_agent, url):
                    return True, "✅ Allowed by robots.txt"
                else:
                    # Check crawl delay
                    crawl_delay = rp.crawl_delay(self.user_agent)
                    if crawl_delay:
                        return False, f"❌ Blocked by robots.txt (crawl-delay: {crawl_delay}s)"
                    return False, "❌ Blocked by robots.txt"
                    
            except Exception as e:
                # If robots.txt doesn't exist or can't be read, allow by default
                print(f"   ⚠️  Could not read robots.txt: {e}")
                self.cache[domain] = None
                self.cache_timestamps[domain] = current_time
                return True, "No robots.txt found (allowed by default)"
                
        except Exception as e:
            print(f"⚠️  Error checking robots.txt: {e}")
            return True, f"Error checking robots.txt (proceeding cautiously)"
    
    def get_crawl_delay(self, url: str) -> Optional[float]:
        """
        Get the crawl delay specified in robots.txt for this domain.
        
        Args:
            url (str): The URL to check
            
        Returns:
            float: Crawl delay in seconds, or None if not specified
        """
        try:
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            
            if domain in self.cache and self.cache[domain] is not None:
                rp = self.cache[domain]
                return rp.crawl_delay(self.user_agent)
            
            return None
            
        except Exception:
            return None
    
    def clear_cache(self):
        """Clear the robots.txt cache."""
        self.cache.clear()
        self.cache_timestamps.clear()


# Global instance for easy access
robots_checker = RobotsChecker()


def is_url_scrapable(url: str) -> tuple[bool, str]:
    """
    Convenience function to check if a URL is scrapable.
    
    Args:
        url (str): The URL to check
        
    Returns:
        tuple: (allowed: bool, reason: str)
    """
    return robots_checker.can_fetch(url)


if __name__ == "__main__":
    # Test the robots checker
    test_urls = [
        "https://careers.google.com/jobs/results/",
        "https://www.microsoft.com/en-us/careers",
        "https://amazon.jobs/en/",
        "https://careers.flipkart.com/",
    ]
    
    print("🧪 Testing Robots.txt Checker\n")
    
    for url in test_urls:
        allowed, reason = is_url_scrapable(url)
        status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
        print(f"{status}: {url}")
        print(f"   Reason: {reason}\n")
