import logging
from os import path
from glob import glob
from time import sleep

from influxdb import InfluxDBClient
from pyirclogs import parse_file

from irc_client import IRCClient

sleep(5)

logger = logging.getLogger('feeder')

influx = InfluxDBClient('influxdb', 8086)
influx.create_database('irclogs')
influx.switch_database('irclogs')

def to_measurement(msg):
    return dict(
        time=msg.time,
        measurement="message",
        fields={
            "words": len(msg.text.split()),
            "text_length": len(msg.text),
            "text": msg.text,
        },
        tags={"by": msg.nick, "chan": msg.chan, "is_action": msg.action}
    )


def main():
    chans = set()

    for logfile in glob('irclogs/#*'):
        path, file_format = logfile.split('.')
        prefix, chan_name = path.rsplit('/', 1)
        chans.add(chan_name)
        logs = parse_file(logfile, parser=file_format, chan=chan_name)
        influx.write_points(map(to_measurement, logs))
        print("INSERTED CHAN %s" % chan_name)

    irc = IRCClient("iTitest", "Titou testing things")
    for msg in irc.lines(list(chans)):
        influx.write_points([to_measurement(msg)])
        print(msg)

if __name__ == "__main__":
    main()
