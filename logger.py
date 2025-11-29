"""
Logging utility for the Job Discovery Bot
Provides detailed logging for debugging and transparency
"""

import time
from typing import List

class JobBotLogger:
    """Centralized logger for all bot operations"""
    
    def __init__(self):
        self.logs: List[str] = []
        self.session_start = time.time()
    
    def log(self, message: str, level: str = "INFO"):
        """Add a log entry with timestamp and level"""
        timestamp = time.strftime("%H:%M:%S")
        elapsed = time.time() - self.session_start
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)  # Also print to console
        return log_entry
    
    def get_all_logs(self) -> str:
        """Get all logs as a single string"""
        return "\n".join(self.logs)
    
    def clear(self):
        """Clear all logs"""
        self.logs = []
        self.session_start = time.time()
    
    def section(self, title: str):
        """Add a section header"""
        separator = "=" * 60
        self.log(separator)
        self.log(title)
        self.log(separator)

# Global logger instance
global_logger = JobBotLogger()
