"""
JobsLib exceptions.
"""

__all__ = ['JobsLibError', 'TaskError', 'Terminate']


class JobsLibError(Exception):
    """
    Base error, ancestor for all other JobsLib errors.
    """

    pass


class TaskError(JobsLibError):
    """
    Task error.
    """

    pass


class Terminate(BaseException):
    """
    Indicates that terminate signal has been reached.
    """

    pass
