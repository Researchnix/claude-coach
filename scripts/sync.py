from datetime import date, timedelta
from db import save_activity, activity_exists, update_field
from intervals import IntervalsClient


# Pull recent activities from Intervals.icu and save any new ones to log/.
# Skips activities that already have a file in log/.
def sync(days: int = 30) -> None:
    """Download and save all activities from the past days unless already present."""
    client = IntervalsClient()
    oldest = (date.today() - timedelta(days=days)).isoformat()
    for id in client.list_activities(oldest=oldest):
        if not activity_exists(id):
            activity = client.pull_activity(id)
            save_activity(activity)


# Fetch a specific field from Intervals.icu and write it to the saved activity file.
def fetch_field(id: str, field: str) -> None:
    """Fetch a field value from Intervals.icu and update the local activity file."""
    client = IntervalsClient()
    activity = client.pull_activity(id)
    value = getattr(activity, field)
    update_field(id, field, value)


# if __name__ == "__main__":
#     sync()
