from .athlete_log_reminder import AthleteLogReminderJob
from .base import BaseJob

def get_job_by_name(job_name: str) -> BaseJob:
    print("DEBUG:",globals()[job_name])
    return globals().get(job_name)()