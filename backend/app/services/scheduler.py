import logging
from datetime import datetime, timedelta, time
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.standup import StandupConfig, StandupSession, StandupResponse
from app.models.project import Project

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def create_daily_sessions():
    """Check all configs and create sessions if it's the right time and day."""
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        configs = db.query(StandupConfig).all()
        
        for config in configs:
            # Check if session already exists for today in config's timezone
            tz = pytz.timezone(config.timezone)
            local_now = datetime.now(tz)
            today_date = local_now.date()
            
            # Check if it's a working day
            day_name = local_now.strftime("%a")
            if day_name not in config.working_days:
                continue
                
            # Check if session exists
            existing = db.query(StandupSession).filter(
                StandupSession.config_id == config.id,
                StandupSession.date == today_date
            ).first()
            
            if existing:
                continue
            
            # Check if current time is >= config time
            config_h, config_m = map(int, config.time.split(':'))
            if local_now.time() >= time(config_h, config_m):
                # Create session
                closes_at = local_now + timedelta(hours=config.response_window_hours)
                session = StandupSession(
                    config_id=config.id,
                    date=today_date,
                    status="active",
                    closes_at=closes_at.astimezone(pytz.UTC).replace(tzinfo=None)
                )
                db.add(session)
                logger.info(f"Created standup session for project {config.project_id}")
        
        db.commit()
    except Exception as e:
        logger.error(f"Error in create_daily_sessions: {e}")
    finally:
        db.close()

def close_expired_sessions():
    """Close sessions that have passed their response window."""
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        expired = db.query(StandupSession).filter(
            StandupSession.status == "active",
            StandupSession.closes_at <= now
        ).all()
        
        for session in expired:
            session.status = "closed"
            logger.info(f"Closed standup session {session.id}")
            
        db.commit()
    except Exception as e:
        logger.error(f"Error in close_expired_sessions: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Check every 15 minutes
        scheduler.add_job(create_daily_sessions, CronTrigger(minute="*/15"), id="create_sessions")
        scheduler.add_job(close_expired_sessions, CronTrigger(minute="*/15"), id="close_sessions")
        scheduler.start()
        logger.info("APScheduler started.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("APScheduler stopped.")
