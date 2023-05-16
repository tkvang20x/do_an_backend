import logging
from datetime import datetime, timedelta
import time

DATETIME_PATTERN = '%Y-%m-%d-%H:%M:%S'


def get_utc_time_now():
    """ Get current date time - format UTC
        ex: 2011-08-12T20:17:46.384Z
    """
    d = datetime.utcnow()
    return d.isoformat("T") + "Z"


def get_string_datetime_now():
    """ Get current date time
        return: Datetime yyyy-mm-dd HH:mm:ss <string>
    """
    return datetime.today().strftime(DATETIME_PATTERN)


def get_month_before_month_now(month):
    date_end = '28'
    if month == '01' or month == '03' or month == '05' or month == '07' or month == '08' or month == '10' or month == '12':
        date_end = '31'
        return date_end
    elif month == '04' or month == '06' or month == '09' or month == '11':
        date_end = '30'
        return date_end
    else:
        return date_end


def get_timestamp_now():
    """ Get current date time - format timestamp
        ex: 12343545
    """
    timestamp = datetime.timestamp(datetime.today())
    return int(timestamp)


def get_milisecond_time():
    return round(time.time() * 1000)


def get_duration_second_time(target_time: str):
    """
        Difference in minute time
    """
    try:
        fmt = DATETIME_PATTERN
        target = datetime.strptime(target_time, fmt)
        current = datetime.strptime(get_string_datetime_now(), fmt)
        # Calculate second diff
        seconds_diff = (current - target).seconds
        return seconds_diff
    except Exception as e:
        logging.info(f"[datetime-utils] Get duration second time error  -- caused by: {e.__str__()}")
        return 0


def get_second_between_moment_time(begin_time: str, last_time: str):
    """
        Difference in minute time
    """
    try:
        fmt = DATETIME_PATTERN
        target = datetime.strptime(begin_time, fmt)
        current = datetime.strptime(last_time, fmt)
        # Calculate second diff
        seconds_diff = (current - target).seconds
        return seconds_diff
    except Exception as e:
        logging.info(f"[datetime-utils] Get_second_between_moment_time error  -- caused by: {e.__str__()}")
        return 0


def get_duration_minute_time(target_time: str):
    """
        Difference in minute time
    """
    try:
        # Calculate second diff
        seconds_diff = get_duration_second_time(target_time)
        minutes_diff = (seconds_diff / 60)
        return minutes_diff
    except Exception as e:
        logging.info(f"[datetime-utils] Get duration minute time error -- caused by: {e.__str__()}")
        return None


def check_datetime_yyyymmdd_format(datetime_str: str):
    """
        Check datetime format yyyy-mm-dd
    :param datetime_str:
    :return:
    """
    try:
        datetime_valid = datetime.strptime(datetime_str, '%Y-%m-%d')
        return datetime_valid
    except ValueError:
        logging.error(f"[datetime-utils] Incorrect data format, should be YYYY-MM-DD")
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    except Exception as e:
        logging.error(f"[datetime-utils] Get check_datetime_format error -- caused by: {e.__str__()}")
        return None


def add_days_to_date_yyyymmdd_format(datetime_str: str,
                                     num_of_days: int):
    """
        add n days to date string
    :param num_of_days:
    :param datetime_str:
    :return: datetime next num of days
    """
    try:
        datetime_value = check_datetime_yyyymmdd_format(datetime_str)
        if not datetime_value:
            return None
        modified_date = datetime_value + timedelta(days=num_of_days)
        return modified_date.strftime('%Y-%m-%d')
    except Exception as e:
        logging.error(f"[datetime-utils] add_days_to_date_yyyymmdd_format() error -- caused by: {e.__str__()}")
        return None
