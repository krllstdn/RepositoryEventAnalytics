create a venv 
`python -m venv datamole`

activate env
`source datamole/bin/activate`

install requirements
`pip install -r requirements.txt`

Go to the RepoEventTracker directory.

Create `.env` file from the `.env-example` in the RepoEventTracker directory. Add your GitHub token there.
The GH token must have the `metadata:read` permissions

Run migrations.
`python manage.py migrate`

Run the django app.
`python manage.py runserver`

The API schema can be looked at `http://127.0.0.1:8000/swagger/`.

Navigate to `localhost:8000/repositories/` in your browser and add your desired repositories. Please make sure that the input values are correct.

Navigate to `localhost:8000/fetch-events/` in your browser or send a request via Postman or any other API client of choice. This will fetch available data from the GitHub API and save it to the database if records are not already there. Please note that GitHub API allows only 122 records fetched (at least with my repository).
Ideally, we would want to run this API, or the function behind it, every once in a while (e.g. once a day, every 12 hours, every 6 hours. Fetching it more often is not ideal as it does not save requests and the API itself has a latency of up to 6 hours). This can be done with `django-apscheduler`. 

Finally, navigate (or send a request) to `localhost:8000/statistics/` to get the required statistics. The resulting numbers are the average number of seconds between the events.   `None` means that in the last 7 days, there was not enough data to calculate the statistics.

### Future work
- `/fetch-events` task scheduling with `django-apscheduler`. Explained [here](https://stackoverflow.com/questions/62525295/how-to-use-python-to-schedule-tasks-in-a-django-application) in detail.
- Simple front-end application that will allow us to add a validation to the input of repository data (or just an endpoint that will add a repository to the db and check if it exists).
- Thorough testing, automated unit tests.
- Logging.
- More thorough API documentation: the response data structures; and response codes explained.

