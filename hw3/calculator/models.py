from django.db import models

# Create your models here.


class CalculateInfo(object):
    def __init__(self, stack: list, output, entering, errmsg=None):
        self.stack = stack
        self.output = output
        self.entering = entering
        self.errmsg = errmsg
        self.op = None

    def to_dict(self):
        return {
            "output": self.output,
            "entering": self.entering,
            "op": self.op,
            "stack": ",".join([str(i) for i in self.stack])
        }

    def save_output(self):
        self.stack.pop()
        self.stack.pop()
        self.stack.append(self.output)
        self.entering = False
        self.op = 'cal'
