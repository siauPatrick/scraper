"""
Scraper core exceptions
"""


class UsageError(Exception):
    def __init__(self, *args, **kwargs):
        self.print_help = kwargs.pop('print_help', True)
        super(UsageError, self).__init__(*args, **kwargs)
