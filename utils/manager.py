from jobs import get_job_by_name
from datetime import time
from telegram.ext import JobQueue
import pytz

class JobManager:
    

    DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

    @staticmethod
    def configure_jobs_scheduler(job_queue: JobQueue, scheduler: dict):
        """_summary_

        Args:
            job_queue (JobQueue): _description_
            scheduler (dict): _description_
        """
        for job_config in scheduler["daily"]:
            JobManager.configure_daily_job(job_queue, job_config)
        for job_config in scheduler["monthly"]:
            JobManager.configure_monthly_job(job_queue, job_config)

    @staticmethod
    def configure_daily_job(job_queue: JobQueue, job_config: dict) -> None:
        """Configure job queue to setup job to run and how

        Args:
            job_queue (JobQueue): queue
            job (BaseJob): job to execute
        """
        job = get_job_by_name(job_config["job"])
        t = time(*job_config["time"], tzinfo=JobManager.DEFAULT_TIMEZONE)
        job_queue.run_daily(job, time=t, days=job_config["days"])

    @staticmethod
    def configure_monthly_job(job_queue: JobQueue, job_config: dict) -> None:
        """Configure job queue to setup job to run and how

        Args:
            job_queue (JobQueue): queue
            job (BaseJob): job to execute
        """
        job = get_job_by_name(job_config["job"])
        t = time(*job_config["time"], tzinfo=JobManager.DEFAULT_TIMEZONE)
        job_queue.run_monthly(job, when=t, day=job_config["day"])
