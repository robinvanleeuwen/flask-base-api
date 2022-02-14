import datetime
import inspect
import os

from flask import g


class ColorTypes(object):
    HEADER = "\033[95m"
    INFOBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


log_level_definitions = {
    "DEBUG": 6,
    "INFO": 5,
    "NORMAL": 4,
    "WARNING": 3,
    "ERROR": 2,
    "SILENT": 1,
}

ENVIRONMENT = "config.Development"

if ENVIRONMENT == "config.Development":
    LOG_TO_SCREEN = True
    LOG_TO_FILE = False
    LOG_TO_DATABASE = False
    LOG_LEVEL = "DEBUG"

elif ENVIRONMENT == "config.Staging":
    LOG_TO_SCREEN = False
    LOG_TO_FILE = False
    LOG_TO_DATABASE = False
    LOG_LEVEL = "INFO"

elif ENVIRONMENT == "config.Production":
    LOG_TO_SCREEN = False
    LOG_TO_FILE = False
    LOG_TO_DATABASE = False
    LOG_LEVEL = "WARNING"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CustomLogger(object, metaclass=Singleton):
    def __init__(
            self,
            log_level=LOG_LEVEL,
            log_to_screen=LOG_TO_SCREEN,
            log_to_database=LOG_TO_DATABASE,
            log_to_file=LOG_TO_FILE,
            max_length=60000,
    ):
        self.log_level = log_level
        self.log_to_screen = log_to_screen
        self.log_to_file = log_to_file
        self.log_to_database = log_to_database
        self.max_length = max_length

    def debug(self, message: any, timestamp: datetime.datetime = None, **kwargs):

        if log_level_definitions[self.log_level] < 6:
            return

        message = str(message)
        if len(message) > self.max_length:
            message = (
                    message[0: int(self.max_length / 2)]
                    + " { ... ... ... truncated ... ... ... } "
                    + message[int(-1 * (self.max_length / 2)):]
            )

        if timestamp is None:
            timestamp = datetime.datetime.now()

        stack_info = inspect.stack()[1][3]

        formatted_message = (
                ColorTypes.BOLD
                + f"[{str(timestamp)}]"
                + " "
                + f"[{g.get('email', '- not logged in -')}]"
                + " "
                + f"[{stack_info}]"
                + " "
                + str(message)
                + ColorTypes.ENDC
        )

        self.do_logging(
            formatted_message=formatted_message,
            timestamp=timestamp,
            log_level="DEBUG",
            stack_info=stack_info,
            message=message,
            user=g.get("email", "- not logged in -"),
            **kwargs,
        )

    def header(self, message: str, timestamp: datetime.datetime = None, **kwargs):

        if log_level_definitions[self.log_level] < 5:
            return

        message = str(message)
        if len(message) > self.max_length:
            message = (
                    message[0: int(self.max_length / 2)]
                    + " { ... ... ... truncated ... ... ... } "
                    + message[int(-1 * (self.max_length / 2)):]
            )
        if timestamp is None:
            timestamp = datetime.datetime.now()

        stack_info = inspect.stack()[1][3]

        formatted_message = (
                ColorTypes.HEADER
                + f"[{str(timestamp)}]"
                + " "
                + f"[{g.get('email', '- not logged in -')}]"
                + " "
                + f"[{stack_info}]"
                + " "
                + str(message)
                + ColorTypes.ENDC
        )

        self.do_logging(
            formatted_message=formatted_message,
            timestamp=timestamp,
            log_level="HEADER",
            stack_info=stack_info,
            message=message,
            user=g.get("email", "- not logged in -"),
            **kwargs,
        )

    def info(
            self,
            message: str,
            timestamp: datetime.datetime = None,
            **kwargs: object,
    ) -> object:
        if log_level_definitions[self.log_level] < 5:
            return

        if timestamp is None:
            timestamp = datetime.datetime.now()

        message = str(message)
        if len(message) > self.max_length:
            message = (
                    message[0: int(self.max_length / 2)]
                    + " { ... ... ... truncated ... ... ... } "
                    + message[int(-1 * (self.max_length / 2)):]
            )

        stack_info = inspect.stack()[1][3]

        formatted_message = (
                ColorTypes.INFOBLUE
                + f"[{str(timestamp)}]"
                + " "
                + f"[{g.get('email', '- not logged in -')}]"
                + " "
                + f"[{stack_info}]"
                + " "
                + str(message)
                + ColorTypes.ENDC
        )

        self.do_logging(
            formatted_message=formatted_message,
            timestamp=timestamp,
            log_level="INFO",
            stack_info=stack_info,
            message=message,
            user=g.get("email", "- not logged in -"),
            **kwargs,
        )

    def ok(self, message: str, timestamp: datetime.datetime = None, **kwargs):

        if log_level_definitions[self.log_level] < 4:
            return

        message = str(message)
        if len(message) > self.max_length:
            message = (
                    message[0: int(self.max_length / 2)]
                    + " { ... ... ... truncated ... ... ... } "
                    + message[int(-1 * (self.max_length / 2)):]
            )

        if timestamp is None:
            timestamp = datetime.datetime.now()

        stack_info = inspect.stack()[1][3]

        formatted_message = (
                ColorTypes.OKGREEN
                + f"[{str(timestamp)}]"
                + " "
                + f"[{g.get('email', '- not logged in -')}]"
                + " "
                + f"[{stack_info}]"
                + " "
                + str(message)
                + ColorTypes.ENDC
        )

        self.do_logging(
            formatted_message=formatted_message,
            timestamp=timestamp,
            log_level="OK",
            stack_info=stack_info,
            message=message,
            user=g.get("email", "- not logged in -"),
            **kwargs,
        )

    def warning(self, message, timestamp: datetime.datetime = None, **kwargs):
        if log_level_definitions[self.log_level] < 3:
            return

        message = str(message)
        if len(message) > self.max_length:
            message = (
                    message[0: int(self.max_length / 2)]
                    + " { ... ... ... truncated ... ... ... } "
                    + message[int(-1 * (self.max_length / 2)):]
            )

        if timestamp is None:
            timestamp = datetime.datetime.now()

        stack_info = inspect.stack()[1][3]

        formatted_message = (
                ColorTypes.WARNING
                + f"[{str(timestamp)}]"
                + " "
                + f"[{g.get('email', '- not logged in -')}]"
                + " "
                + f"[{stack_info}]"
                + " "
                + str(message)
                + ColorTypes.ENDC
        )

        self.do_logging(
            formatted_message=formatted_message,
            timestamp=timestamp,
            log_level="WARNING",
            stack_info=stack_info,
            message=message,
            user=g.get("email", "- not logged in -"),
            **kwargs,
        )

    def fail(
            self,
            message: str,
            timestamp: datetime.datetime = None,
            stop=False,
            **kwargs,
    ):
        if log_level_definitions[self.log_level] < 2:
            return

        message = str(message)
        if len(message) > self.max_length:
            message = (
                    message[0: int(self.max_length / 2)]
                    + " { ... ... ... truncated ... ... ... } "
                    + message[int(-1 * (self.max_length / 2)):]
            )

        if timestamp is None:
            timestamp = datetime.datetime.now()

        stack_info = inspect.stack()[1][3]

        formatted_message = (
                ColorTypes.FAIL
                + f"[{str(timestamp)}]"
                + " "
                + f"[{g.get('email', '- not logged in -')}]"
                + " "
                + f"[{stack_info}]"
                + " "
                + str(message)
                + ColorTypes.ENDC
        )

        self.do_logging(
            formatted_message=formatted_message,
            timestamp=timestamp,
            log_level="FAIL",
            stack_info=stack_info,
            message=message,
            user=g.get("email", "- not logged in -"),
            **kwargs,
        )

    def write_to_database(self, timestamp, level, function, message, user):

        if not self.log_to_database:
            return

        from db.base import db_session_manager
        from db.models.log import Log

        with db_session_manager() as session:
            log_line = Log()
            log_line.timestamp = timestamp
            log_line.level = str(level)
            log_line.function = str(function)
            log_line.message = str(message)
            log_line.user = str(user)
            session.add(log_line)
            session.commit()

    def write_to_logfile(self, message: str = None):
        from init_app import app

        if message:
            try:
                f = open(app.config.get("LOGFILE", "./ticketmatrix.log"), "a")
                f.write(message + "\n")
            except Exception as e:
                self.fail(f"Could not write to logfile: {str(e)}", stop=True)

    def do_logging(
            self,
            formatted_message,
            timestamp,
            log_level,
            stack_info,
            message,
            user,
            **kwargs,
    ):

        if self.log_to_screen:
            print(formatted_message, **kwargs)

        if self.log_to_file:
            self.write_to_logfile(message=message)

        if self.log_to_database:
            self.write_to_database(timestamp, log_level, stack_info, message, user=user)
