import asyncio

from typing import Optional, Any, Dict

class TwitterScraper():
    secret = vault.read('clients', task['slug'], task['credentials'])  # This can be switched to env variables file