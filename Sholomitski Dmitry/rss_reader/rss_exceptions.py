class RssReaderException(Exception):
    pass


class DateTimeError(RssReaderException):
    pass


class EmptyUrlError(RssReaderException):
    pass


class BadUrlError(RssReaderException):
    pass



# class NoDataInCache(RssReaderException):
    # pass


if __name__ == '__main__':
    pass
