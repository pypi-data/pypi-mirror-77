"""
Module :mod:`jobslib.metrics.dummy` provides :class:`DummyMetrics`
writer.
"""

from . import BaseMetrics

__all__ = ['DummyMetrics']


class DummyMetrics(BaseMetrics):
    """
    Dummy metrics implementation. Doesn't provide real functionality.
    It is useful for development or if it is not necessary metrics. For
    use of :class:`DummyMetrics` write into :mod:`settings`:

    .. code-block:: python

        METRICS = {
            'backend': 'jobslib.metrics.dummy.DummyMetrics',
        }
    """

    def push(self, metrics):
        pass
