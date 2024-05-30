from flask import Flask
from celery import Celery
from flask import jsonify, request, render_template
from requests.exceptions import HTTPError
import requests
import os
import time
from flask_cors import CORS
from datetime import datetime
# from views import fetch

# initializes flask app:
app = Flask(__name__)
CORS(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])  # tells Celery where the redis broker service is running
celery.conf.update(app.config)


PUBMED_BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
NCBI_API_KEY = os.environ.get('NCBI_API_KEY')  # to allow sites to make more than 3 requests per second


# Execute pubmed search function in the background using celery decorator
@celery.task(bind=True)
def pubmed_search(self, search_term):
    connect_timeout, read_timeout = 5.0, 15.0
    start_time = time.time()
    url = PUBMED_BASE_URL+'?term={term}&retmode=json&api_key={api_key}'.format(term=search_term, api_key=NCBI_API_KEY)
    # response = requests.get(url, timeout=(connect_timeout, read_timeout))
    # if response.status_code != 200:
    #     return jsonify({'error': 'Failed to fetch the data from PubMed'}), 500
    try:
        response = requests.get(url, timeout=(connect_timeout, read_timeout))
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        print("Success")
    
        response_json = response.json()
        pmids = response_json.get('esearchresult', {}).get('idlist', [])  # esearchresult is a nested dict with actual pmids in a list: {'esearchresult': {'pmids': [1,2,3]}}
        record_count = int(response_json.get('esearchresult', {}).get('count', 0))
        end_time = time.time()
        run_time = end_time - start_time
        print(response_json)
        return {
            'status': 'completed',
            'result': {'pmids': pmids},
            'created_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'run_seconds': run_time, 
            'records': record_count
        }


@app.route('/')
def initScreen():
    return render_template(
            'index.html'
        )


@app.route('/search', methods=['GET'])
def search():
    term = request.args.get('term')
    print(term)
    if not term:
        return jsonify({'error': 'No search term provided'}), 500
    
    async_task = pubmed_search.apply_async(args=[term]) # returns an AsyncResult object (dict)
    print(async_task.id)
    # initial response from search will include only 'query' and 'task_id'; once the task is completed and fetched 'records' is added
    data = {
         "query": term,
        "task_id": async_task.id
    }
    return jsonify(data)
    

@app.route('/fetch/<task_id>', methods=['GET'])
def fetch(task_id):
    task = pubmed_search.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'task_id': task_id, 
            'status': task.status,
            'created_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        # fetch(task_id) # CAUSES RecursionError: maximum recursion depth exceeded while calling a Python object
    elif task.state == 'FAILURE':
        response = {
            'task_id': task_id, 
            'status': task.status, 
            'message': str(task.info)
        }
    else:
        response = task.result
        response['task_id'] = task_id
        print(response)
    return jsonify(response)

    