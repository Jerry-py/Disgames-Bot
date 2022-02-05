from dotenv import load_dotenv
import os


class Config:
    """Access the environment variables"""
    def __init__(self):
        self.env = load_dotenv()
        
    def __getitem__(self, item):
        """Get an environment variable"""
        return os.getenv(item)
    
    @property
    def _env(self):
        """Get the env"""
        return self.env
