from fastapi import FastAPI
from app.database import engine, SessionLocal
from app.models import user
from datetime import datetime
from app.api import event

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(event.router)

user.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        db.query(user.User).delete()
        db.query(user.UserActivity).delete()
        db.commit()

        user_ids = [1, 2, 3]
        for id in user_ids:
            db_user = user.User(user_id=id)
            db.add(db_user)
        db.commit()

        for user_id in [1, 2, 3]:
            db_user = db.query(user.User).filter(user.User.user_id == user_id).first()
            if not db_user:
                db_user = user.User(user_id=user_id)
                db.add(db_user)
                db.commit()
                db.refresh(db_user)

        activity_data = [
            {"user_id": 1, "action": "withdraw", "amount": 150.0},
            {"user_id": 1, "action": "withdraw", "amount": 100.0},
            {"user_id": 2, "action": "deposit", "amount": 200.0},
            {"user_id": 2, "action": "deposit", "amount": 50.0},
            {"user_id": 3, "action": "withdraw", "amount": 50.0}
        ]

        for data in activity_data:
            db_activity = user.UserActivity(
                action=data["action"],
                amount=data["amount"],
                user_id=data["user_id"],
                timestamp=datetime.utcnow()
            )
            db.add(db_activity)

        db.commit()

    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with SQLite"}
