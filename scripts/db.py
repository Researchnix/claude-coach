from pathlib import Path
from dataclasses import fields
from activity import Activity

a = Activity(id="i154867202", date="2026-06-07", name="Morning Ride", type="Ride")
b = Activity(id="i154867203", date="2026-06-08", name="Easy Run", type="Run")
c = Activity(id="i154867204", date="2026-06-09", name="Long Ride", type="Ride")

LOG_DIR = Path(__file__).parent.parent / "log"


def _filepath(id: str) -> Path:
    return LOG_DIR / f"{id}.md"


def _read_frontmatter(id: str) -> dict:
    parts = _filepath(id).read_text().split("---")
    data = {}
    for line in parts[1].strip().splitlines():
        if ": " in line:
            key, _, value = line.partition(": ")
            data[key.strip()] = value.strip()
        elif line.endswith(":"):
            data[line[:-1].strip()] = None
    return data


def save_activity(activity: Activity) -> None:
    """Write an activity object to a markdown file with YAML frontmatter in log/."""
    lines = ["---\n"]
    for f in fields(activity):
        value = getattr(activity, f.name)
        lines.append(f"{f.name}:\n" if value is None else f"{f.name}: {value}\n")
    lines.append("---\n")
    _filepath(activity.id).write_text("".join(lines))


def load_activity(id: str) -> Activity:
    """Load an activity from log/ by its id."""
    data = _read_frontmatter(id)
    return Activity(
        id=data["id"],
        date=data["date"],
        name=data["name"],
        type=data["type"],
    )


def load_all() -> list[Activity]:
    """Load all activities from log/."""
    activities = []
    for filepath in LOG_DIR.glob("*.md"):
            activities.append(load_activity(filepath.stem))
    return activities


def activity_exists(id: str) -> bool:
    """Check if an activity file exists in log/."""
    return _filepath(id).exists()


def has_field(id: str, field: str) -> bool:
    """Check if a saved activity has a non-null value for the given field."""
    data = _read_frontmatter(id)
    return field in data and data[field] is not None


def update_field(id: str, field: str, value) -> None:
    """Update a single field in an existing activity file."""
    new_line = f"{field}: {value}\n"
    output = []
    found = False
    for line in _filepath(id).read_text().splitlines(keepends=True):
        if line.startswith(f"{field}:"):
            output.append(new_line)
            found = True
        elif line.strip() == "---" and not found and output:
            output.append(new_line)
            output.append(line)
            found = True
        else:
            output.append(line)
    _filepath(id).write_text("".join(output))
