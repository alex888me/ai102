"""Develop AI agents on Azure
https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-on-azure/"""

from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path.home() / ".msfoundry"
if not dotenv_path.is_file():
    raise FileNotFoundError(f"Missing environment file: {dotenv_path}. Copy .msfoundry.example to your home directory as .msfoundry, and populate it with the appropriate values.")

load_dotenv(dotenv_path)