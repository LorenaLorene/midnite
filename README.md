# FastAPI Event Server

This is a simple FastAPI project with a single endpoint: `/event`.
Endpoint takes payload representing users action and returns alert.


## Requirements

Python 3.7 or higher

## Setup Instructions

Follow the steps below to set up and run the FastAPI server.

### 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/LorenaLorene/midnite.git
cd midnite
```


### 2. Install requirements & run server

```bash
pip install -r requirements.txt

uvicorn app.main:app --reload
```

### 3. Database

Local dabatabase will be populated when application is built.

### 3. Test event endpoint 

```bash
curl -XPOST http://127.0.0.1:8000/event -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "50.00", "user_id": 2, "t": 0}'
```

