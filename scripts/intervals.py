

# intervals.icu api docs
# https://intervals.icu/api/v1/docs

import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

from activity import Activity

oldest = (date.today() - timedelta(days=30)).isoformat()
newest = date.today().isoformat()







class IntervalsClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ["INTERVALS_API_KEY"]
        self.athlete_id = os.environ["INTERVALS_ATHLETE_ID"]
        self._auth = ("API_KEY", self.api_key)

    def _url(self, path: str) -> str:
        BASE_URL = "https://intervals.icu/api/v1"
        return f"{BASE_URL}/athlete/{self.athlete_id}/{path}"

    def list_activities(self, oldest: str | None = None, newest: str | None = None) -> list[str]:
        """Return a list of activity ids in the given time range."""
        params = {}
        if oldest:
            params["oldest"] = oldest
        if newest:
            params["newest"] = newest
        resp = requests.get(self._url("activities"), auth=self._auth, params=params)
        resp.raise_for_status()
        return [a["id"] for a in resp.json()]

    def pull_activity(self, id: str) -> Activity:
        """Fetch a single activity by id and return it as an Activity instance."""
        resp = requests.get(self._url(f"activities/{id}"), auth=self._auth)
        resp.raise_for_status()
        data = resp.json()[0]
        return Activity(
            id=data["id"],
            date=data["start_date_local"][:10],
            name=data["name"],
            type=data["type"],
        )


    # def create_event(self, event: dict) -> dict:
    #     """Create a single planned workout event. Returns the created event.
    #
    #     Required fields:
    #       category         "WORKOUT"
    #       start_date_local "2026-06-05T07:00:00"
    #       type             "Ride" | "Run" | "WeightTraining" | ...
    #       name             str
    #
    #     Useful optional fields:
    #       description      workout steps in intervals.icu text format (see below)
    #       moving_time      planned duration in seconds
    #       icu_training_load estimated load
    #       external_id      stable id from your system; enables upsert
    #
    #     Description syntax:
    #       - 15m 55%          15 minutes at 55% FTP (or pace zone for runs)
    #       3x                 repeat block (implicit close)
    #       - 5m 110%
    #       - 5m 50%
    #       - 10m 65% Cooldown
    #     """
    #     resp = requests.post(self._url("events"), auth=self._auth, json=event)
    #     resp.raise_for_status()
    #     return resp.json()

    # def create_events_bulk(self, events: list[dict], upsert: bool = True) -> list[dict]:
    #     """Create multiple planned workout events in one call.
    #
    #     With upsert=True, existing events matching external_id are updated instead
    #     of duplicated — safe to call repeatedly from the Sunday plan script.
    #     """
    #     params = {"upsert": "true" if upsert else "false"}
    #     resp = requests.post(self._url("events/bulk"), auth=self._auth, json=events, params=params)
    #     resp.raise_for_status()
    #     return resp.json()


