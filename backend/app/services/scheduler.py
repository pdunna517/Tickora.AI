import logging
import pytz
from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.standup import StandupConfig, StandupSession, SessionStatus
from app.services.standup_service import standup_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def create_daily_sessions():
    """Check all active configs and create sessions if it's the right time and day."""
    db: Session = SessionLocal()
    try:
        configs = db.query(StandupConfig).filter(StandupConfig.is_active == True).all()
        
        for config in configs:
            tz = pytz.timezone(config.timezone)
            local_now = datetime.now(tz)
            day_name = local_now.strftime("%a")
            
            if day_name not in (config.working_days or []):
                continue
                
            config_h, config_m = map(int, config.time.split(':'))
            # If current local time matches the config time (within the minute)
            if local_now.hour == config_h and local_now.minute == config_m:
                standup_service.create_session(db, config.id)
                
    except Exception as e:
        logger.error(f"Error in create_daily_sessions: {e}")
    finally:
        db.close()

def close_expired_sessions():
    """Close sessions that have passed their response window and generate summary."""
    db: Session = SessionLocal()
    try:
        now_utc = datetime.utcnow()
        expired = db.query(StandupSession).filter(
            StandupSession.status == SessionStatus.ACTIVE,
            StandupSession.ends_at <= now_utc
        ).all()
        
        for session in expired:
            standup_service.close_session(db, session.id)
            
    except Exception as e:
        logger.error(f"Error in close_expired_sessions: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Runs every minute as requested
        scheduler.add_job(create_daily_sessions, CronTrigger(second="0"), id="create_sessions")
        scheduler.add_job(close_expired_sessions, CronTrigger(second="30"), id="close_sessions")
        scheduler.start()
        logger.info("APScheduler started.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("APScheduler stopped.")
