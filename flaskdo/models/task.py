# Class Task

from priority import Priority
from status import Status


class Task:

    def __init__(self, title, priority):

        # attibutes
        self.id = id(self)
        self.title = title
        self.description = ""
        self.priority = Priority.LOW
        self.status = Status.NOT_STARTED
