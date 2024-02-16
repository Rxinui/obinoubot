from commands.base import BaseCommand
from commands import get_command_by_classname
from jobs import get_job_by_name
from utils.botconfig import BotConfig
from datetime import time
from telegram.ext import JobQueue, Application
import pytz
import logging


class CommandManager:
    @staticmethod
    def init_commands_from_botconfig(botconfig: BotConfig) -> list[BaseCommand]:
        """Initialise all commands declared in botconfig.

        Args:
            botconfig (BotConfig): bot configuration

        Returns:
            list[BaseCommand]: list of generated commands
        """
        return [
            get_command_by_classname(cmd_info["instance_of"])(
                botconfig, cmd_name, **cmd_info["args"]
            )
            for cmd_name, cmd_info in botconfig.commands.items()
        ]

    @staticmethod
    def add_command(application: Application, command: BaseCommand):
        """Add a command to Telegram bot

        Args:
            application (Application): Telegram app
            command (BaseCommand): Command to configure
        """
        logging.info(f"CommandManager: add handler {command.command_name}")
        application.add_handler(command.handler)

    @staticmethod
    def add_commands(application: Application, commands: list[BaseCommand]):
        """Add multiple commands at once to Telegram bot

        Args:
            application (Application): Telegram app
            commands (list[BaseCommand]): Commands to configure
        """
        for command in commands:
            CommandManager.add_command(application, command)


class JobManager:
    DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

    @staticmethod
    def configure_jobs_scheduler(job_queue: JobQueue, botconfig: BotConfig):
        """_summary_

        Args:
            job_queue (JobQueue): _description_
            botconfig (dict): _description_
        """
        JobManager.configure_daily_job(job_queue, botconfig)
        JobManager.configure_monthly_job(job_queue, botconfig)

    def configure_daily_job(job_queue: JobQueue, botconfig: BotConfig) -> None:
        """Configure job queue to setup job to run and how

        Args:
            job_queue (JobQueue): queue
            job (BaseJob): job to execute
        """
        for job_config in botconfig.scheduler["daily"]:
            job_class = get_job_by_name(job_config["job"])
            job = job_class(botconfig, **job_config["args"])
            t = time(*job_config["time"], tzinfo=JobManager.DEFAULT_TIMEZONE)
            job_queue.run_daily(job, time=t, days=job_config["days"])

    @staticmethod
    def configure_monthly_job(job_queue: JobQueue, botconfig: BotConfig) -> None:
        """Configure job queue to setup job to run and how

        Args:
            job_queue (JobQueue): queue
            job (BaseJob): job to execute
        """
        for job_config in botconfig.scheduler["monthly"]:
            job_class = get_job_by_name(job_config["job"])
            job = job_class(botconfig, **job_config["args"])
            t = time(*job_config["time"], tzinfo=JobManager.DEFAULT_TIMEZONE)
            job_queue.run_monthly(job, when=t, day=job_config["day"])
