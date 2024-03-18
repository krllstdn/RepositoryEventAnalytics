import requests

from .models import Events, Repositories
import os
from datetime import datetime, timedelta
from django.utils import timezone


def fetch_repository_events(
    owner: str, repo: str, token: str = os.environ.get("GITHUB_TOKEN")
):
    # fetch events as many as possible (as limits are small) and save them to the database
    events = []
    page = 1
    per_page = 100
    url = f"https://api.github.com/repos/{owner}/{repo}/events"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    print("token:", token)

    while True:
        try:
            params = {"per_page": per_page, "page": page}
            response = requests.get(url, params=params, headers=headers)

            print(f"Fetching events for {owner}/{repo} (page {page})...")

            if response.status_code == 200:
                events_page = response.json()
                events.extend(events_page)

                # Check if there are more pages
                links = response.headers.get("Link")
                if not links or f'rel="next"' not in links:
                    break  # No more pages
                else:
                    page += 1
            else:
                raise Exception(
                    f"Error fetching events: {response.status_code} - {response.text}"
                )
        except Exception as e:
            print(f"Error fetching events for {owner}/{repo}: {e}")
            break

    return events


def fetch_and_save_repository_events():
    repositories = Repositories.objects.all()

    for repository in repositories:

        events = fetch_repository_events(
            repository.owner, repository.name, token=os.environ.get("GITHUB_TOKEN")
        )
        print(f"Fetched {len(events)} events for {repository.owner}/{repository.name}")

        for event in events:
            event_id = event.get("id")
            if (
                event_id is not None
                and not Events.objects.filter(event_id=event_id).exists()
            ):
                Events.objects.create(
                    event_id=event["id"],
                    event_type=event["type"],
                    timestamp=event["created_at"],
                    repository=repository,
                )


def get_statistics():
    repositories = Repositories.objects.all()
    output = {}

    try:
        for repository in repositories:
            output[f"{repository.owner}/{repository.name}"] = {}

            unique_events = (
                Events.objects.filter(repository=repository)
                .values_list("event_type", flat=True)
                .distinct()
            )
            for event in unique_events:
                # get list of all timestamps for each event
                filtered_events = Events.objects.filter(
                    repository=repository,
                    event_type=event,
                    timestamp__gte=timezone.now() - timedelta(days=210),
                ).order_by("timestamp")[:500]

                # get list of all timestamps for each event and sort them
                timestamps = [e.timestamp for e in filtered_events]

                output[f"{repository.owner}/{repository.name}"][event] = (
                    average_time_between_timestamps(timestamps)
                )
    except Exception as e:
        print(f"Error calculating the statistics: {e}")

    return output


def average_time_between_timestamps(datetime_timestamps: list[datetime]):
    if len(datetime_timestamps) < 2:
        return None  # Need at least two timestamps to calculate the average time between them

    time_diffs = [
        (datetime_timestamps[i + 1] - datetime_timestamps[i]).total_seconds()
        for i in range(len(datetime_timestamps) - 1)
    ]

    avg_time_diff = sum(time_diffs) / len(time_diffs)

    return round(avg_time_diff)
