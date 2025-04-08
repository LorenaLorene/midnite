# FastAPI Event Server

This is a simple FastAPI project with a single endpoint: `/event`.
Endpoint takes payload representing users action and returns alert.


## Setup Instructions

Follow the steps below to set up and run the FastAPI server.

### 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/LorenaLorene/midnite.git
```


### 2. Install requirements & run the server

```bash
pip install -r requirements.txt

uvicorn app.main:app --reload
```

### 3. Database

Local dabatabase will be populated when application is built.

### 3. Test event endpoint 

Test db will be populated with 3 users. 3 different POST will return different codes.

##### This will return code - 123 for user - 2 if it's run less than 30 sec after the built 
```bash
curl -XPOST http://127.0.0.1:8000/event -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "50.00", "user_id": 2, "t": 0}'
```

##### This will return code - 30 for user -1 
```bash
curl -XPOST http://127.0.0.1:8000/event -H 'Content-Type: application/json' \
-d '{"type": "withdraw", "amount": "50.00", "user_id": 1, "t": 0}'
```

##### This will return no code for user - 3
```bash
curl -XPOST http://127.0.0.1:8000/event -H 'Content-Type: application/json' \
-d '{"type": "withdraw", "amount": "50.00", "user_id": 3, "t": 0}'
```
