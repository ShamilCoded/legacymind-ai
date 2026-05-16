# Vercel entrypoint
import sys
from pathlib import Path

# Add the backend directory itself to the path
sys.path.insert(0, str(Path(__file__).parent))

from src.api.app import app

# Vercel looks for 'app' variable in this file
