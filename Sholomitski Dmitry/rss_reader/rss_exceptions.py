class RssReaderException(Exception):
    pass


class DateTimeError(RssReaderException):
    pass


class EmptyUrlError(RssReaderException):
    pass


class BadUrlError(RssReaderException):
    pass


class NoNewsinInCache(RssReaderException):
    pass


class RssURLError(RssReaderException):
    pass
