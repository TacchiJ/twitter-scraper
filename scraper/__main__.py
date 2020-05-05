import os
import asyncio
import requests

from typing import Optional, Any, Dict

class TwitterScraper():
    foo = os.environ['VAULT_TOKEN']
    bar = os.environ['TWITTER_CREDS'] 
    # secret = vault.read('clients', task['slug'], task['credentials'])  # This can be switched to env variables file

    # # Async method 1
    # async def get_tweets(self):
    #     url = 'https://api.github.com/repos/psf/requests'
    #     data = {
    #         'username': 'username',
    #         'password': 'password'
    #     }

    #     async with requests.get(url, json=data) as resp:
    #         resp.raise_for_status()
    #         resp_data = resp.json()

    #     print(resp_data["description"])


if __name__ == "__main__":
    scraper = TwitterScraper()
    
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(scraper.get_tweets())
    # loop.close()
