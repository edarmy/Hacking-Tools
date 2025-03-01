

def openLogFile(path):
    with (path) as log_file:
        for logline in log_file:
            yield logline
        