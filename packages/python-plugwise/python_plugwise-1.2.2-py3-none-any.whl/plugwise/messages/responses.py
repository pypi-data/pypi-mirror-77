"""
Use of this source code is governed by the MIT license found in the LICENSE file.

All (known) response messages to be received from plugwise plugs
"""
from datetime import datetime
import struct
from plugwise.constants import (
    MESSAGE_FOOTER,
    MESSAGE_HEADER,
)
from plugwise.message import PlugwiseMessage
from plugwise.util import (
    DateTime,
    Float,
    Int,
    LogAddr,
    RealClockDate,
    RealClockTime,
    String,
    UnixTimestamp,
    Time,
)


class NodeResponse(PlugwiseMessage):
    def __init__(self):
        super().__init__()
        self.params = []
        self.mac = None
        self.timestamp = datetime.now()
        self.seq_id = None

    def unserialize(self, response):
        if len(response) != len(self):
            raise ProtocolError(
                "message doesn't have expected length. expected %d bytes got %d"
                % (len(self), len(response))
            )
        header, function_code, self.seq_id, self.mac = struct.unpack(
            "4s4s4s16s", response[:28]
        )

        # FIXME: check function code match
        if header != MESSAGE_HEADER:
            raise ProtocolError("broken header!")
        # FIXME: avoid magic numbers
        response = response[28:]
        response = self._parse_params(response)
        crc = response[:4]

        if response[4:] != MESSAGE_FOOTER:
            raise ProtocolError("broken footer!")

    def _parse_params(self, response):
        for p in self.params:
            myval = response[: len(p)]
            p.unserialize(myval)
            response = response[len(myval) :]
        return response

    def __len__(self):
        arglen = sum(len(x) for x in self.params)
        return 34 + arglen


class CircleCalibrationResponse(NodeResponse):
    ID = b"0027"

    def __init__(self):
        super().__init__()
        self.gain_a = Float(0, 8)
        self.gain_b = Float(0, 8)
        self.off_tot = Float(0, 8)
        self.off_noise = Float(0, 8)
        self.params += [self.gain_a, self.gain_b, self.off_tot, self.off_noise]


class CirclePlusRealTimeClockResponse(NodeResponse):
    """returns the real time clock of CirclePlus node
    """

    ID = b"003A"

    def __init__(self):
        super().__init__()

        self.time = RealClockTime()
        self.day_of_week = Int(0, length=2)
        self.date = RealClockDate()
        self.params += [self.time, self.day_of_week, self.date]


class CirclePowerUsageResponse(NodeResponse):
    """returns power usage as impulse counters for several different timeframes
    """

    ID = b"0013"

    def __init__(self):
        super().__init__()
        self.pulse_1s = Int(0, 4)
        self.pulse_8s = Int(0, 4)
        self.pulse_hour_consumed = Int(0, 8)
        self.pulse_hour_produced = Int(0, 8)
        self.nanosecond_offset = Int(0, 4)
        self.params += [
            self.pulse_1s,
            self.pulse_8s,
            self.pulse_hour_consumed,
            self.pulse_hour_produced,
            self.nanosecond_offset,
        ]


class CirclePowerBufferResponse(NodeResponse):
    """returns information about historical power usage
    each response contains 4 log buffers and each log buffer contains data for 1 hour
    """

    ID = b"0049"

    def __init__(self):
        super().__init__()
        self.logdate1 = DateTime()
        self.pulses1 = Int(0, 8)
        self.logdate2 = DateTime()
        self.pulses2 = Int(0, 8)
        self.logdate3 = DateTime()
        self.pulses3 = Int(0, 8)
        self.logdate4 = DateTime()
        self.pulses4 = Int(0, 8)
        self.logaddr = LogAddr(0, length=8)
        self.params += [
            self.logdate1,
            self.pulses1,
            self.logdate2,
            self.pulses2,
            self.logdate3,
            self.pulses3,
            self.logdate4,
            self.pulses4,
            self.logaddr,
        ]


class CircleScanResponse(NodeResponse):
    ID = b"0019"

    def __init__(self):
        super().__init__()
        self.node_mac = String(None, length=16)
        self.node_address = Int(0, length=2)
        self.params += [self.node_mac, self.node_address]


class CircleSwitchResponse(NodeResponse):
    ID = b"0099"

    def __init__(self):
        super().__init__()
        self.unknown = None
        self.relay_state = None

    # overule unserialize because of different message format (relay before mac)
    def unserialize(self, response):
        if len(response) != len(self):
            raise ProtocolError(
                "message doesn't have expected length. expected %d bytes got %d"
                % (len(self), len(response))
            )
        (
            header,
            function_code,
            self.seq_id,
            self.unknown,
            self.relay_state,
            self.mac,
        ) = struct.unpack("4s4s4s2s2s16s", response[:32])

        # FIXME: check function code match
        if header != MESSAGE_HEADER:
            raise ProtocolError("broken header!")
        # FIXME: avoid magic numbers
        response = response[32:]
        crc = response[:4]

        if response[4:] != MESSAGE_FOOTER:
            raise ProtocolError("broken footer!")

    def __len__(self):
        return 38


class NodeClockResponse(NodeResponse):
    ID = b"003F"

    def __init__(self):
        super().__init__()
        self.time = Time()
        self.day_of_week = Int(0, 2)
        self.unknown = Int(0, 2)
        self.unknown2 = Int(0, 4)
        self.params += [self.time, self.day_of_week, self.unknown, self.unknown2]


class NodeInfoResponse(NodeResponse):
    ID = b"0024"

    def __init__(self):
        super().__init__()
        self.datetime = DateTime()
        self.last_logaddr = LogAddr(0, length=8)
        self.relay_state = Int(0, length=2)
        self.hz = Int(0, length=2)
        self.hw_ver = String(None, length=12)
        self.fw_ver = UnixTimestamp(0)
        self.node_type = Int(0, length=2)
        self.params += [
            self.datetime,
            self.last_logaddr,
            self.relay_state,
            self.hz,
            self.hw_ver,
            self.fw_ver,
            self.node_type,
        ]


class NodePingResponse(NodeResponse):
    ID = b"000E"

    def __init__(self):
        super().__init__()
        self.in_RSSI = Int(0, length=2)
        self.out_RSSI = Int(0, length=2)
        self.ping_ms = Int(0, length=4)
        self.params += [
            self.in_RSSI,
            self.out_RSSI,
            self.ping_ms,
        ]


class StickInitResponse(NodeResponse):
    ID = b"0011"

    def __init__(self):
        super().__init__()
        self.unknown1 = Int(0, length=2)
        self.network_is_online = Int(0, length=2)
        self.circle_plus_mac = String(None, length=16)
        self.network_id = Int(0, length=4)
        self.unknown2 = Int(0, length=2)
        self.params += [
            self.unknown1,
            self.network_is_online,
            self.circle_plus_mac,
            self.network_id,
            self.unknown2,
        ]
