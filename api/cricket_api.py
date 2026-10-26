"""
Optional External Cricket API Client
Provides integration helpers to sync live match data, scorecards, or player bios
from external cricket data providers (e.g., CricAPI, Sportradar, or rapidapi).
"""

import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError

class CricketAPIClient:
    def __init__(self, api_key=None, base_url="https://api.cricapi.com/v1"):
        self.api_key = api_key or os.getenv("CRICKET_API_KEY", "")
        self.base_url = base_url

    def get_live_scores(self):
        """Fetches live matches or returns mock fallback data if API key is not configured."""
        if not self.api_key:
            return {
                "status": "mock",
                "message": "CRICKET_API_KEY not configured. Returning sample live data.",
                "data": [
                    {
                        "id": "mock_live_1",
                        "name": "India vs Australia - 2nd ODI",
                        "status": "India won toss and elected to bat",
                        "venue": "Eden Gardens, Kolkata",
                        "score": "142/2 (24.4 ov)"
                    }
                ]
            }

        url = f"{self.base_url}/currentMatches?apikey={self.api_key}"
        try:
            req = Request(url, headers={"User-Agent": "CricketStatsApp/1.0"})
            with urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except URLError as e:
            return {"status": "error", "message": str(e)}

    def search_player(self, player_name):
        """Searches external player records by name."""
        if not self.api_key:
            return {
                "status": "mock",
                "message": "CRICKET_API_KEY not set. Using local database search.",
                "data": []
            }

        url = f"{self.base_url}/players?apikey={self.api_key}&search={player_name}"
        try:
            req = Request(url, headers={"User-Agent": "CricketStatsApp/1.0"})
            with urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except URLError as e:
            return {"status": "error", "message": str(e)}

# Singleton instance
cricket_api = CricketAPIClient()
