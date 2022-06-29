from flask import request


class Context:
    def __init__(self):
        self.request = request
