import abc
import six
import multiprocessing as mp


class IContext(six.with_metaclass(abc.ABCMeta)):
    """Provides RPC-related information and action."""

    @abc.abstractmethod
    def is_active(self):
        """Describes whether the RPC is active or has terminated.

        Returns:
          bool:
          True if RPC is active, False otherwise.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def time_remaining(self):
        """Describes the length of allowed time remaining for the RPC.

        Returns:
          A nonnegative float indicating the length of allowed time in seconds
          remaining for the RPC to complete before it is considered to have
          timed out, or None if no deadline was specified for the RPC.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self):
        """Cancels the RPC.

        Idempotent and has no effect if the RPC has already terminated.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def add_callback(self, callback):
        """Registers a callback to be called on RPC termination.

        Args:
          callback: A no-parameter callable to be called on RPC termination.

        Returns:
          True if the callback was added and will be called later; False if
            the callback was not added and will not be called (because the RPC
            already terminated or some other reason).
        """
        raise NotImplementedError()


class Context(IContext):

    def __init__(self, stop_event: mp.Event):
        self.stop_event = stop_event
        self.metadata = {}

    def is_active(self):
        return self.stop_event.is_set()

    def time_remaining(self):
        raise NotImplementedError()

    def cancel(self):
        raise NotImplementedError()

    def add_callback(self, callback):
        raise NotImplementedError()
