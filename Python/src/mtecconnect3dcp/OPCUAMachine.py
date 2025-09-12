from asyncua.sync import Client #https://github.com/FreeOpcUa/asyncua
from asyncua import ua #https://github.com/FreeOpcUa/asyncua

import inspect
from typing import Optional, Callable, Any, Union
import threading

class OPCUAMachine:
    """
    Base class for OPC-UA machine communication.

    Args:
        ip (str): IP address of the machine.
        baseNode (str): Base node of the machine.
    """
    def __init__(self, baseNode = "ns=4;s=|var|B-Fortis CC-Slim S04.Application.GVL_OPC.", livebitNode = "Livebit2machine"):
        self._baseNode = baseNode
        self._liveBitNode = livebitNode
        self._connected = False

    def connect(self, ip: str):
        """
        Connects to the machine using the provided IP address.

        Args:
            ip (str): IP address of the machine.
        """
        self._ip = ip
        if not self._ip:
            raise ValueError("No IP address provided.")
        
        # check if ip address starts with opc.tcp://, if not add it
        if not self._ip.startswith("opc.tcp://"):
            self._ip = "opc.tcp://" + self._ip

        # check if ip address has port, if not add default port 4840
        if ":" not in self._ip.split("//")[1]:
            self._ip += ":4840"
        
        self._reader = Client(url=self._ip)
        self._writer = Client(url=self._ip)
        self._reader.connect()
        self._writer.connect()
        self._reader.load_data_type_definitions()
        self._writer.load_data_type_definitions()

        self._connected = True

        # check if Livebit2machine exists, otherwise use Livebit2DuoMix
        try:
            self.read(self._liveBitNode)
        except ua.UaError:
            self._liveBitNode = "Livebit2DuoMix"
        # check if Livebit2DuoMix exists, otherwise throw error
        try:
            self.read(self._liveBitNode)
        except ua.UaError:
            raise ValueError("Livebit node not found. Machine not supported.")

        self.subscribe("Livebit2extern", self.changeLivebit, 500)
        
    
    def disconnect(self):
        """
        Disconnects from the machine.
        """
        self._reader.disconnect()
        self._writer.disconnect()
        self._connected = False

    def _status_change_callback(self, status):
        """
        Callback for subscription status changes.

        Args:
            status: The new status.
        """
        print("Connection status changed:", status)
        self._connected = status == ua.StatusCode(0)

    def safe_change(self, parameter: str, value: Any, typ: str) -> bool:
        """
        Changes the value of an OPC-UA variable, with feature-not-supported feedback.

        Args:
            parameter (str): Variable to change.
            value (Any): Value to change the variable to.
            typ (str): String of variable type ("bool", "uint16", "int32", "float").

        Returns:
            bool: True if successful, False if not supported.
        """
        try:
            self.change(parameter, value, typ)
            return True
        except KeyError:
            print(f"Feature '{parameter}' is not supported on this machine.")
            return False
    
    def safe_read(self, parameter: str, default: Any) -> Any:
        """
        Reads the value of an OPC-UA variable, with feature-not-supported feedback.

        Args:
            parameter (str): Variable to read.
            default: Value to return if parameter is not available.

        Returns:
            Any: Value of the variable or default if not available.
        """
        try:
            return self.read(parameter)
        except KeyError:
            print(f"Feature '{parameter}' is not supported on this machine.")
            return default
    
    def change(self, parameter: str, value: Any, typ: str):
        """
        Changes the value of an OPC-UA variable.

        Args:
            parameter (str): Variable to change.
            value (Any): Value to change the variable to.
            typ (str): String of variable type ("bool", "uint16", "int32", "float").
        """
        if not self._connected:
            raise ua.UaError("Not connected to machine.")
        
        if callable(value):
            self.easy_subscribe(parameter, value)
            return

        if typ == "bool":
            t = ua.VariantType.Boolean
            value = bool(value)
        elif typ == "uint16":
            t = ua.VariantType.UInt16
            value = int(abs(value))
        elif typ == "int32":
            t = ua.VariantType.Int32
            value = int(value)
        elif typ == "float":
            t = ua.VariantType.Float
            value = float(value)
        else:
            return
        node = self._writer.get_node(self._baseNode + parameter)
        node.set_value(ua.Variant(value, t))

    def read(self, parameter: str) -> Any:
        """
        Reads the value of an OPC-UA variable.

        Args:
            parameter (str): Variable to read.

        Returns:
            Any: Value of the variable.
        """
        node = self._reader.get_node(self._baseNode + parameter)
        return node.get_value()

    def easy_subscribe(self, parameter: Union[str, list], callback: Callable, wrap: bool = True, interval: int = 500):
        """
        Easy subscription method for a given OPC-UA parameter.

        Args:
            parameter (Union[str, list]): The OPC-UA parameter(s) to subscribe to.
            callback (Callable): Callback function receiving value and parameter.
            wrap (bool): Whether to wrap the callback to filter arguments. Default is True.
            interval (int): Interval in ms for checking the parameter.

        Returns:
            list: List of subscriptions created.
        """
                
        subscriptions = []
        handler = None
        if wrap:
            sw = SubscriptionWrapper(callback)
        # check if parameter is a string or an array of strings
        if isinstance(parameter, str):
            if wrap:
                subscription, handler = self.subscribe(parameter, sw.trigger)
                sw.subscription(subscription)
            else:
                subscription, handler = self.subscribe(parameter, callback)
                subscriptions.append(subscription)
        elif isinstance(parameter, list):
            for param in parameter:
                if isinstance(param, str):
                    if wrap:
                        subscription, handler = self.subscribe(param, sw.trigger)
                        sw.subscription(subscription)
                    else:
                        subscription, handler = self.subscribe(param, callback)
                        subscriptions.append(subscription)
        return subscriptions

    def subscribe(self, parameter: str, callback: Callable, interval: int = 500):
        """
        Subscribes to a given OPC-UA parameter.

        Args:
            parameter (str): The OPC-UA parameter to subscribe to.
            callback (Callable): Callback function receiving value and parameter.
            interval (int): Interval in ms for checking the parameter.

        Returns:
            list: [subscription, handler]
        """
        if not self._connected:
            raise ua.UaError("Not connected to machine.")
        
        subscriptionHandler = OpcuaSubscriptionHandler(parameter, callback, self._status_change_callback)
        subscription = self._reader.create_subscription(interval, subscriptionHandler)
        handler = subscription.subscribe_data_change(self._reader.get_node(self._baseNode + parameter))
        return [subscription, handler]

    def changeLivebit(self, value: bool, parameter=None):
        """
        Changes the Livebit value.

        Args:
            value (bool): The value to change the Livebit to.
            parameter: Unused, for callback compatibility.
        """
        if not self._connected:
            raise ua.UaError("Not connected to machine.")
        
        self.change(self._liveBitNode, value, "bool")

class SubscriptionWrapper:
    def __init__(self, callback: Callable, subscription=[]):
        self._callback = callback
        self._subscriptions = subscription

    def subscription(self, subscription):
        self._subscriptions.append(subscription)

    def delete(self):
        for subscription in self._subscriptions:
            subscription.delete()
        self._subscriptions = []

    def trigger(self, value, parameter):
        self.exec(value=value, parameter=parameter, subscription=self)

    def exec(self, **kwargs):
        sig = inspect.signature(self._callback)
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
        # execute the callback in a new thread to avoid blocking
        threading.Thread(target=self._callback, kwargs=filtered_kwargs).start()

class OpcuaSubscriptionHandler:
    """
    Handler for OPC-UA subscription data changes.
    """
    def __init__(self, parameter, callback, status_change_callback=None):
        """
        Args:
            parameter (str): The parameter being subscribed to.
            callback (Callable): Callback function for data changes.
            status_change_callback (Callable, optional): Callback for status changes. Defaults to None.
        """
        self.parameter = parameter
        self.callback = callback
        self.status_change_callback = status_change_callback

    def datachange_notification(self, node, value, data):
        """
        Called when a data change notification is received.

        Args:
            node: The OPC-UA node.
            value: The new value.
            data: Additional data.
        """
        self.callback(value, self.parameter)

    def status_change_notification(self, status):
        """
        Called when a status change notification is received.

        Args:
            status: The new status.
        """
        if self.status_change_callback:
            self.status_change_callback(status)