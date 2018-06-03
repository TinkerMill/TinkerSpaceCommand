#
# This file contains constants for various functionality in TinkerSpaceCommand.
#

# How often to scan for offline sensors.
#
# The time is in seconds.
SENSOR_OFFLINE_CHECK_DELAY = 60

#
# The format for date times.
#
SENSOR_TIMESTAMP_DATE_TIME_FORMAT = '%H:%M:%S %b %d, %Y'

INFLUXDB_MEASUREMENT_NAME_SENSORS = "sensors"

INFLUXDB_TAG_NAME_SENSED = "sensed"
INFLUXDB_TAG_NAME_SENSOR = "sensor"
INFLUXDB_TAG_NAME_CHANNEL = "channel"

