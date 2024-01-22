#!/var/www/html/Base_Flask/venv/bin/python3
import sys
sys.path.insert(0, '/var/www/html/Base_Flask')

from app import create_app

application = create_app()