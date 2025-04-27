from time import sleep

from controller.huey_controller import huey


@huey.task()
def add_numbers(a, b):
    sleep(5)
    return a + b
