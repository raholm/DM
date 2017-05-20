import datetime


def timestamp_to_readable(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


def is_within_time(time, time_interval):
    if not len(time_interval) == 2:
        raise ValueError("A time interval requires 2 times: %s" % (time_interval,))
    return time_interval[0] <= time <= time_interval[1]
