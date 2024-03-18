create a venv 
`python -m venv datamole`

activate env
`source datamole/bin/activate`

install requirements
`pip install -r requirements.txt`

Go to RepoEventTracker directory.

create `.env` file from the `.env-example` in the RepoEventTracker directory. add your github token there.
the gh token must have the permissions for the metadata read

run migrations 
`python manage.py migrate`

Run the django app
`python manage.py runserver`

The API schema can be looked at `http://127.0.0.1:8000/swagger/`.

Navigate to `localhost:8000/repositories/` in your browser and add your desired repositories. Please make sure that the values are correct.

Navigate to `localhost:8000/fetch-events/` in your browser or send request via Postman or any other api client of choice. This will fetch available data from the Github API and save it to the database if records are not already there. Please note that Github API allows only 122 records fetched (at least with my repository).
Ideally we would want to run this API, or the function behind it, every once in a while (e.g. once a day, every 12 hours, every 6 hours. Fetching it more often is not ideal as it does not save requests and the API itself has a latency of up to 6 hours). This can be done with `django-apscheduler`. 

Finally, navigate (or send request) to `localhost:8000/statistics/` to get the required statistics. Resulting numbers are average number of seconds between the events.  `None` means that in the last 7 days there were not enough data to calculate the statistics.

### Future work
- Simple front end application that will allow us to add a validation to the input of repositories data. (or just an endpoint that will add and check if such a repository exist)
- Thorough testing, automated unit tests
- Logging
- More thorough API documentation: the response data structures; response codes explained.

