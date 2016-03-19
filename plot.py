#!/usr/bin/env python
'''
Read log file and plot presence for a day
'''
import sys
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

def linspace(start, stop, step):
    return [v * step for v in range(start, int(stop / step))]

def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, DATETIME_FORMAT)

def days_ago(days_in_past):
    return date.today() - timedelta(days=days_in_past)

def read_log_file(log_file, log_day):
    '''
    Parse the log file from the arduino serial
    '''
    events = []
    with open(log_file) as f:
        for line in f:
            cols = line.strip().split(' ')
            if cols[0] == '1':
                timestamp = cols[1]
                dt = parse_timestamp(timestamp)
                if dt.date() == log_day:
                    hour, minute = dt.hour, dt.minute
                    events.append((hour, minute))
    return events

def plot(events):
    '''
    plot histogram of movement for 24 hour period
    (48 bins with half-hours)
    '''
    inbins = linspace(0, 24, 0.5)

    # add half hours
    hours = []
    for hour, minutes in events:
        hour = 2 * hour
        if minutes > 30:
            hour = hour + 1
        hour = hour / 2.0
        hours.append(hour)

    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(hours, bins=inbins, align='left', orientation='vertical')
    ax.set_xticks(range(24))

    plt.show()

def main():
    if len(sys.argv) not in [2, 3]:
        print 'Usage: %s LOG_FILE [N]' % sys.argv[0]
        sys.exit(1)

    LOG_FILE = sys.argv[1]

    days_in_past = 0 if len(sys.argv) == 2 else int(sys.argv[2])

    log_day = days_ago(days_in_past)

    events = read_log_file(LOG_FILE, log_day)
    if len(events) > 0:
        plot(events)
    else:
        print 'No data available from %s days ago' % days_in_past

if __name__ == '__main__':
    main()
