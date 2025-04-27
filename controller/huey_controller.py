from huey import RedisHuey
from huey.signals import (
    SIGNAL_CANCELED,
    SIGNAL_COMPLETE,
    SIGNAL_ENQUEUED,
    SIGNAL_EXECUTING,
    SIGNAL_INTERRUPTED,
)

huey = RedisHuey("my-app")


@huey.signal(SIGNAL_EXECUTING)
def signal_executing(signal, task, exc=None):
    print("I'm executing")


@huey.signal(SIGNAL_CANCELED)
def signal_canceled(signal, task, exc=None):
    print("I'm canceled")


@huey.signal(SIGNAL_COMPLETE)
def signal_complete(signal, task, exc=None):
    print("I'm complete")


@huey.signal(SIGNAL_ENQUEUED)
def signal_enqueued(signal, task, exc=None):
    print("I'm enqueued")


@huey.signal(SIGNAL_INTERRUPTED)
def signal_interrupted(signal, task, exc=None):
    print("I'm SIGNAL_INTERRUPTED")
