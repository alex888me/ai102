"""
OLD
Develop computer vision solutions in Azure (deprecated)
https://learn.microsoft.com/en-us/training/paths/create-computer-vision-solutions-azure-ai/

NEW
Develop computer vision solutions with Microsoft Foundry
https://learn.microsoft.com/en-us/training/paths/develop-computer-vision-with-foundry/
"""

from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path.home() / ".msfoundry"
if not dotenv_path.is_file():
    raise FileNotFoundError(f"Missing environment file: {dotenv_path}. Copy .msfoundry.example to your home directory as .msfoundry, and populate it with the appropriate values.")

load_dotenv(dotenv_path)