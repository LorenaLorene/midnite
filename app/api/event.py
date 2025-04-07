from fastapi import APIRouter, status, Depends
from app.schemas.event_schema import Event, EventResponse, EventCode
from sqlalchemy.orm import Session
from app.models.user import UserActivity
from datetime import datetime, timedelta
from app.database import get_db

router = APIRouter()


def save_user_activity(db: Session, event: Event):
    db_activity = UserActivity(
        action=event.type,
        amount=str(event.amount),
        user_id=event.user_id,
        timestamp=datetime.utcnow()
    )
    db.add(db_activity)
    db.commit()


@router.post(
    "/event",
    status_code=status.HTTP_201_CREATED,
    response_model=EventResponse)
def alert_event(event: Event, db: Session = Depends(get_db)):
    alert_codes = []
    if float(event.amount) > 100:
        alert_codes.append(EventCode.WITHDRAW_OVER_100)

    user_activities = db.query(UserActivity).filter(
        UserActivity.user_id == event.user_id).order_by(
        UserActivity.timestamp.desc()).limit(2).all()

    if len(user_activities) >= 2:
        consecutive_withdraws = 0
        consecutive_deposits = 0
        deposits = []
        for activity in user_activities:
            if activity.action == "withdraw":
                consecutive_withdraws += 1
            if activity.action == "deposit":
                consecutive_deposits += 1
                deposits.append(float(activity.amount))

        if event.type == "withdraw" and consecutive_withdraws == 2:
            alert_codes.append(EventCode.CONSECUTIVE_3_WITHDRAWS)

        if event.type == "deposit" and consecutive_deposits == 2:
            deposits.append(float(event.amount))
            deposits = sorted(deposits, reverse=True)
            if deposits[0] > deposits[1] > deposits[2]:
                alert_codes.append(EventCode.CONSECUTIVE_3_INCREASING_DEPOSITS)

        if event.type == "deposit":
            time_window = datetime.utcnow() - timedelta(seconds=30)
            recent_deposits = db.query(UserActivity).filter(
                UserActivity.user_id == event.user_id,
                UserActivity.timestamp >= time_window,
                UserActivity.action == "deposit"
            ).all()

            total_deposit = sum(
                float(deposit.amount) for deposit in recent_deposits) + float(event.amount)
            if total_deposit > 200:
                alert_codes.append(EventCode.ACCUMULATIVE_DEPOSITS_200_IN_30_SECONDS)

    alert = True if alert_codes else False

    save_user_activity(db=db, event=event)

    return EventResponse(alert=alert, alert_codes=alert_codes, user_id=event.user_id)
