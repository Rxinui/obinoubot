from jobs import get_job_by_name
from datetime import time
from telegram.ext import JobQueue
import pytz


class JobManager:
    DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

    @staticmethod
    def configure_jobs_scheduler(job_queue: JobQueue, botconfig: dict):
        """_summary_

        Args:
            job_queue (JobQueue): _description_
            botconfig (dict): _description_
        """
        JobManager.configure_daily_job(job_queue, botconfig)
        JobManager.configure_monthly_job(job_queue, botconfig)

    @staticmethod
    def configure_daily_job(job_queue: JobQueue, botconfig: dict) -> None:
        """Configure job queue to setup job to run and how

        Args:
            job_queue (JobQueue): queue
            job (BaseJob): job to execute
        """
        for job_config in botconfig["scheduler"]["daily"]:
            job_class = get_job_by_name(job_config["job"])
            job = job_class.__init__(**job_config["args"])
            t = time(*job_config["time"], tzinfo=JobManager.DEFAULT_TIMEZONE)
            job_queue.run_daily(job, time=t, days=job_config["days"])

    @staticmethod
    def configure_monthly_job(job_queue: JobQueue, botconfig: dict) -> None:
        """Configure job queue to setup job to run and how

        Args:
            job_queue (JobQueue): queue
            job (BaseJob): job to execute
        """
        for job_config in botconfig["scheduler"]["monthly"]:
            job_class = get_job_by_name(job_config["job"])
            job = job_class.__init__(**job_config["args"])
            t = time(*job_config["time"], tzinfo=JobManager.DEFAULT_TIMEZONE)
            job_queue.run_monthly(job, when=t, day=job_config["day"])
