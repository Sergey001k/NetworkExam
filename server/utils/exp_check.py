import asyncio
from datetime import datetime, timedelta, timezone
from db.db_models import Session


async def check_session_expire(session_id: int, end_time):
    now = datetime.now(timezone.utc)
    end_time = end_time.replace(tzinfo=timezone.utc)

    if end_time > now:
        sleep_time = (end_time - now).total_seconds()
        await asyncio.sleep(sleep_time)

    await Session.filter(id=session_id).update(finished=True)
    