
async function startSearch() {
    try {
        const search_term = document.getElementById('search-term').value;
        const method = "GET"
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        };
        const options = {
            method,
            headers
        };
    
        const response = await fetch(`http://127.0.0.1:5000/search?term=${search_term}`, options);
        const data = await response.json();
        console.log(data);
        // document.getElementById('records').innerText = `Records: ${data.records}`;
        document.getElementById('query').innerText = `Query: ${data.query}`;
        document.getElementById('taskId').innerText = `Task ID: ${data.task_id}`;
        document.getElementById('status').innerText = 'Searching...';
    }
    catch(err) {
        console.log(err);
    }
    checkStatus(taskId)
}

async function checkStatus(taskId) {
    const response = await fetch(`/fetch/${taskId}`);
    const data = response.json();

    if (data.status === 'processing') {
        // Expected output:
        // "task_id": "7fd381bf3cbe28e892e163db81b9e2cd"
        // "status": "processing",
        // "created_time": "2024-03-12 13:51:02"
        document.getElementById('taskId').innerText = `Task ID: ${data.task_id}`;
        document.getElementById('status').innerText = `Status: ${data.status}`;
        document.getElementById('createdTime').innerText = `Created Time: ${data.created_time}`;
        setTimeout(() => checkStatus(taskId), 2000);
    } else if (data.status === 'completed') {
        // Expected output:
        // {
        //     "task_id": "7fd381bf3cbe28e892e163db81b9e2cd"
        //     "status":"completed",
        //     "result":{
        //     "pmids":[7952237,37506310,32397415,...]
        //     },
        //     "created_time":"2024-03-12 13:51:02",
        //     "run_seconds": 75
        // }  
        document.getElementById('taskId').innerText = `Task ID: ${data.task_id}`;
        document.getElementById('status').innerText = `Status: ${data.status}`;
        document.getElementById('results').innerText = `Result: ${data.result.pmids.join(', ')}`
        document.getElementById('createdTime').innerText = `Created Time: ${data.created_time}`;
        document.getElementById('runtime').innerText = `Status: ${data.run_seconds}`;
    }  else {
        document.getElementById('status').innerText = 'Helloooo';
        document.getElementById('status').innerText = `Status: ${data.status}`;
    }
}

const initPage = () => {
    startSearch();
}