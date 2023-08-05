import collections
import sys

import six

if six.PY3 and not sys.version_info.minor == 5:  # All python 3 expect for 3.5
    from .results_py3 import *
else:
    NetflixFastMeasurementResult = collections.namedtuple(
        "NetflixFastMeasurementResult",
        "id errors download_rate download_rate_unit download_size download_size_unit"
        " asn ip isp city country urlcount reason_terminated ",
    )

    NetflixFastThreadResult = collections.namedtuple(
        "NetflixFastThreadResult",
        "id errors host download_size download_size_unit download_rate download_rate_unit city country minimum_latency average_latency maximum_latency median_deviation"
        " packets_transmitted packets_received packets_lost packets_lost_unit time time_unit",
    )
