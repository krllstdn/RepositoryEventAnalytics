import requests

from .models import Events, Repositories
import os


def fetch_repository_events(owner, repo, token=os.environ.get("GITHUB_TOKEN")):
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

    # get all repositories
    repositories = Repositories.objects.all()

    for repository in repositories:

        events = fetch_repository_events(
            repository.owner, repository.name, token=os.environ.get("GITHUB_TOKEN")
        )
        print(f"Fetched {len(events)} events for {repository.owner}/{repository.name}")
        # Save the events to the database
        for event in events:
            # print("event:", type(event))
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
