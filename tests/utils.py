from functools import wraps
import signal


class TimeoutException(Exception):
    pass


class TestTimeout:
    """
    Environment for tests timeout.
    """

    def __init__(self, seconds, error_message=None):
        if error_message is None:
            error_message = 'test timed out after {}s.'.format(seconds)
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutException(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


def async_timeout_test(f):
    """
    Decorator to create asyncio context for asyncio methods or functions.
    """

    @wraps(f)
    def g(*args, **kwargs):
        with TestTimeout(5):
            args[0].loop.run_until_complete(f(*args, **kwargs))

    return g
