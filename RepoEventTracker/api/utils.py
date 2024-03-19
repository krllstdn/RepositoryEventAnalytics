import os
from datetime import datetime, timedelta

import requests
from django.utils import timezone

from .models import Events, Repositories


def fetch_repository_events(
    owner: str, repo: str, token: str = os.environ.get("GITHUB_TOKEN")
):
    """
    Fetches repository events from the GitHub API.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        token (str, optional): The GitHub API token. Defaults to the value of the "GITHUB_TOKEN" environment variable.

    Returns:
        list: A list of repository events.

    Raises:
        Exception: If there is an error fetching the events.

    """
    events = []
    page = 1
    per_page = 100
    url = f"https://api.github.com/repos/{owner}/{repo}/events"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    while True:
        try:
            params = {"per_page": per_page, "page": page}
            response = requests.get(url, params=params, headers=headers)

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
    """
    Fetches repository events for all repositories and saves them to the database.

    This function retrieves all repositories from the database and fetches their events
    using the GitHub API. It then saves the fetched events to the database if they don't
    already exist.

    Note: The function requires the 'GITHUB_TOKEN' environment variable to be set with a valid
    GitHub personal access token.

    Returns:
        None
    """
    repositories = Repositories.objects.all()

    for repository in repositories:
        events = fetch_repository_events(repository.owner, repository.name)
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
    """
    Retrieves statistics for each repository's unique events.

    Returns:
        dict: A dictionary containing the statistics for each repository's unique events.
              The keys of the dictionary are in the format "{owner}/{name}" of the repository,
              and the values are dictionaries containing the event types and their average time
              between timestamps.
    """
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
                #  get sorted list of all timestamps for each event type
                filtered_events = Events.objects.filter(
                    repository=repository,
                    event_type=event,
                    timestamp__gte=timezone.now() - timedelta(days=210),
                ).order_by("timestamp")[:500]

                timestamps = [e.timestamp for e in filtered_events]

                output[f"{repository.owner}/{repository.name}"][event] = (
                    average_time_between_timestamps(timestamps)
                )
    except Exception as e:
        print(f"Error calculating the statistics: {e}")

    return output


def average_time_between_timestamps(datetime_timestamps: list[datetime]):
    """
    Calculates the average time difference between a list of datetime timestamps.

    Args:
        datetime_timestamps (list[datetime]): A list of datetime timestamps.

    Returns:
        float: The average time difference between the timestamps in seconds, rounded to the nearest integer.

    Raises:
        None

    Notes:
        - The function requires at least two timestamps to calculate the average time difference.
        - The average time difference is calculated by taking the difference between each pair of consecutive timestamps,
          converting it to seconds, and then calculating the average of all the differences.
    """
    if len(datetime_timestamps) < 2:
        return None  # Need at least two timestamps to calculate the average time between them

    time_diffs = [
        (datetime_timestamps[i + 1] - datetime_timestamps[i]).total_seconds()
        for i in range(len(datetime_timestamps) - 1)
    ]

    avg_time_diff = sum(time_diffs) / len(time_diffs)

    return round(avg_time_diff)
