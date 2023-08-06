"""
Use of this source code is governed by the MIT license found in the LICENSE file.

General node object to control associated plugwise nodes like: Circle+, Circle, Scan, Stealth
"""
from datetime import datetime
from plugwise.constants import (
    HA_SWITCH,
    MAX_TIME_DRIFT,
    NODE_TYPE_CIRCLE,
    NODE_TYPE_CIRCLE_PLUS,
    NODE_TYPE_SCAN,
    NODE_TYPE_SENSE,
    NODE_TYPE_STEALTH,
    NODE_TYPE_SWITCH,
    NODE_TYPE_STICK,
    SENSOR_AVAILABLE,
    SENSOR_RSSI_IN,
    SENSOR_RSSI_OUT,
    SENSOR_PING,
    SWITCH_RELAY,
)
from plugwise.message import PlugwiseMessage
from plugwise.messages.responses import (
    NodeClockResponse,
    NodeInfoResponse,
    NodePingResponse,
)
from plugwise.messages.requests import (
    NodeClockGetRequest,
    NodeClockSetRequest,
    NodeInfoRequest,
    NodePingRequest,
)
from plugwise.util import validate_mac


class PlugwiseNode(object):
    """provides interface to the Plugwise node devices
    """

    def __init__(self, mac, address, stick):
        mac = mac.upper()
        if validate_mac(mac) == False:
            self.stick.logger.debug(
                "MAC address is in unexpected format: %s", str(mac),
            )
        self.mac = bytes(mac, encoding="ascii")
        self.stick = stick
        self.categories = ()
        self.sensors = ()
        self.switches = ()
        self._address = address
        self._callbacks = {}
        self.last_update = None
        self.last_request = None
        self._available = False
        self.in_RSSI = None
        self.out_RSSI = None
        self.ping_ms = None
        self._node_type = None
        self._hardware_version = None
        self._firmware_version = None
        self._relay_state = False
        self._last_log_address = None
        self._last_log_collected = False
        self._last_info_message = None
        self._clock_offset = None
        self.get_clock(self.sync_clock)

    def get_categories(self) -> tuple:
        """ Return Home Assistant catagories supported by plugwise node """
        return self.categories

    def get_sensors(self) -> tuple:
        """ Return sensors supported by plugwise node """
        return self.sensors

    def get_switches(self) -> tuple:
        """ Return switches supported by plugwise node """
        return self.switches

    def get_available(self) -> bool:
        """ Return current network state of plugwise node """
        return self._available

    def set_available(self, state, request_info=False):
        """ Set current network state of plugwise node """
        if state == True:
            if self._available == False:
                self._available = True
                self.stick.logger.debug(
                    "Mark node %s available", self.get_mac(),
                )
                self.do_callback(SENSOR_AVAILABLE["id"])
                if request_info:
                    self._request_info()
        else:
            if self._available == True:
                self._available = False
                self.stick.logger.debug(
                    "Mark node %s unavailable", self.get_mac(),
                )
                self.do_callback(SENSOR_AVAILABLE["id"])

    def get_mac(self) -> str:
        """Return mac address"""
        return self.mac.decode("ascii")

    def get_name(self) -> str:
        """Return unique name"""
        return self.get_node_type() + " (" + str(self._address) + ")"

    def get_node_type(self) -> str:
        """Return Circle type"""
        if self._node_type == NODE_TYPE_CIRCLE:
            return "Circle"
        elif self._node_type == NODE_TYPE_CIRCLE_PLUS:
            return "Circle+"
        elif self._node_type == NODE_TYPE_SCAN:
            return "Scan"
        elif self._node_type == NODE_TYPE_SENSE:
            return "Sense"
        elif self._node_type == NODE_TYPE_STEALTH:
            return "Stealth"
        elif self._node_type == NODE_TYPE_SWITCH:
            return "Switch"
        elif self._node_type == NODE_TYPE_STICK:
            return "Stick"
        return "Unknown"

    def get_hardware_version(self) -> str:
        """Return hardware version"""
        if self._hardware_version != None:
            return self._hardware_version
        return "Unknown"

    def get_firmware_version(self) -> str:
        """Return firmware version"""
        if self._firmware_version != None:
            return str(self._firmware_version)
        return "Unknown"

    def get_last_update(self) -> datetime:
        """Return  version"""
        return self.last_update

    def get_in_RSSI(self) -> int:
        """Return inbound RSSI level"""
        if self.in_RSSI != None:
            return self.in_RSSI
        return 0

    def get_out_RSSI(self) -> int:
        """Return outbound RSSI level"""
        if self.out_RSSI != None:
            return self.out_RSSI
        return 0

    def get_ping(self) -> int:
        """Return ping roundtrip"""
        if self.ping_ms != None:
            return self.ping_ms
        return 0

    def _request_info(self, callback=None):
        """ Request info from node"""
        self.stick.send(
            NodeInfoRequest(self.mac), callback,
        )

    def ping(self, callback=None):
        """ Ping node"""
        self.stick.send(
            NodePingRequest(self.mac), callback,
        )

    def on_message(self, message):
        """
        Process received message
        """
        assert isinstance(message, PlugwiseMessage)
        if message.mac == self.mac:
            if message.timestamp != None:
                self.stick.logger.debug(
                    "Last update %s of node %s, last message %s",
                    str(self.last_update),
                    self.get_mac(),
                    str(message.timestamp),
                )
                self.last_update = message.timestamp
            if isinstance(message, NodePingResponse):
                self._process_ping_response(message)
                self.stick.message_processed(message.seq_id)
            elif isinstance(message, NodeInfoResponse):
                self._process_info_response(message)
                self.stick.message_processed(message.seq_id)
            elif isinstance(message, NodeClockResponse):
                self._response_clock(message)
                self.stick.message_processed(message.seq_id)
            else:
                self.set_available(True)
                self._on_message(message)
        else:
            self.stick.logger.debug(
                "Skip message, mac of node (%s) != mac at message (%s)",
                message.mac.decode("ascii"),
                self.get_mac(),
            )

    def _on_message(self, message):
        pass

    def subscribe_callback(self, callback, sensor):
        """ Subscribe callback to execute when state change happens """
        if sensor not in self._callbacks:
            self._callbacks[sensor] = []
        self._callbacks[sensor].append(callback)

    def unsubscribe_callback(self, callback, sensor):
        """ Register callback to execute when state change happens """
        if sensor in self._callbacks:
            self._callbacks[sensor].remove(callback)

    def do_callback(self, sensor):
        """ Execute callbacks registered for specified callback type """
        if sensor in self._callbacks:
            for callback in self._callbacks[sensor]:
                try:
                    callback(None)
                except Exception as e:
                    self.stick.logger.error(
                        "Error while executing all callback : %s", e,
                    )

    def _process_ping_response(self, message):
        """ Process ping response message"""
        self.set_available(True, True)
        if self.in_RSSI != message.in_RSSI.value:
            self.in_RSSI = message.in_RSSI.value
            self.do_callback(SENSOR_RSSI_IN["id"])
        if self.out_RSSI != message.out_RSSI.value:
            self.out_RSSI = message.out_RSSI.value
            self.do_callback(SENSOR_RSSI_OUT["id"])
        if self.ping_ms != message.ping_ms.value:
            self.ping_ms = message.ping_ms.value
            self.do_callback(SENSOR_PING["id"])

    def _process_info_response(self, message):
        """ Process info response message"""
        self.stick.logger.debug("Response info message for plug %s", self.get_mac())
        self.set_available(True)
        if message.relay_state.serialize() == b"01":
            if not self._relay_state:
                self._relay_state = True
                self.do_callback(SWITCH_RELAY["id"])
        else:
            if self._relay_state:
                self._relay_state = False
                self.do_callback(SWITCH_RELAY["id"])
        self._hardware_version = int(message.hw_ver.value)
        self._firmware_version = message.fw_ver.value
        self._node_type = message.node_type.value
        self._last_info_message = message.timestamp
        if self._last_log_address != message.last_logaddr.value:
            self._last_log_address = message.last_logaddr.value
            self._last_log_collected = False
        self.stick.logger.debug("Node type        = %s", self.get_node_type())
        self.stick.logger.debug("Relay state      = %s", str(self._relay_state))
        self.stick.logger.debug("Hardware version = %s", str(self._hardware_version))
        self.stick.logger.debug("Firmware version = %s", str(self._firmware_version))

    def _request_power_buffer(self, log_address=None, callback=None):
        pass

    def get_clock(self, callback=None):
        """ get current datetime of internal clock of CirclePlus """
        self.stick.send(
            NodeClockGetRequest(self.mac), callback,
        )

    def _response_clock(self, message):
        dt = datetime(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
            message.time.value.hour,
            message.time.value.minute,
            message.time.value.second,
        )
        clock_offset = message.timestamp.replace(microsecond=0) - (
            dt + self.stick.timezone_delta
        )
        if clock_offset.days == -1:
            self._clock_offset = clock_offset.seconds - 86400
        else:
            self._clock_offset = clock_offset.seconds
        self.stick.logger.debug(
            "Clock of node %s has drifted %s sec",
            self.get_mac(),
            str(self._clock_offset),
        )

    def set_clock(self, callback=None):
        """ set internal clock of CirclePlus """
        self.stick.send(
            NodeClockSetRequest(self.mac, datetime.utcnow()), callback,
        )

    def sync_clock(self, max_drift=0):
        """ Resync clock of node if time has drifted more than MAX_TIME_DRIFT
        """
        if self._clock_offset != None:
            if max_drift == 0:
                max_drift = MAX_TIME_DRIFT
            if (self._clock_offset > max_drift) or (self._clock_offset < -(max_drift)):
                self.stick.logger.info(
                    "Reset clock of node %s because time has drifted %s sec",
                    self.get_mac(),
                    str(self._clock_offset),
                )
                self.set_clock()
