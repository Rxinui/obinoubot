from .message import MessageJob
from .base import BaseJob

def get_job_by_name(job_name: str) -> BaseJob | MessageJob:
    print("DEBUG:", globals()[job_name])
    return globals().get(job_name)
