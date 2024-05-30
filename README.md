# Yale-Assignment
## Description
A simple web application to search for and retrieve data from the PubMed database maintained by the National Library of Medicine. The app retrieves relevant information such as PMIDs, number of records, etc based on the search term provided by the user. \
The back-end was developed using the following technologies: \
Flask: \
Used as the primary web framework for creating the API endpoints and handling HTTP requests and responses. \
Celery: \
Used for managing background tasks, such as making requests to the PubMed API and processing the results. \
Redis: \
Used as the message broker and result backend for Celery to handle task queueing and storing task results.

The front-end technologies include: HTML, CSS, JavaScript (with the Fetch API).

## Usage
Install Dependencies: \
Install the necessary Python packages: Flask, Celery, requests, and redis. \
$ git clone https://github.com/PreetiSubbiah/Yale-Assignment.git \
$ cd Yale-Assigment $ pip install -r requirements.txt \
Set Environment Variables: \
Set the environment variables REDIS_URL and NCBI_API_KEY. \
Run Redis Server:
Start a Redis server, which is required for Celery to work. \
Run Flask App: \
Start the Flask app by running: python app.py. \
Ctrl + C will stop the process and close the connection to the app.
