from asyncua.sync import Client #https://github.com/FreeOpcUa/asyncua
from asyncua import ua #https://github.com/FreeOpcUa/asyncua

class Machine:
    """
    Base class for OPC-UA machine communication.

    Args:
        baseNode (str): Base node of the machine.
    """
    def __init__(self, baseNode = "ns=4;s=|var|B-Fortis CC-Slim S04.Application.GVL_OPC."):
        self.baseNode = baseNode
        self.liveBitNode = "Livebit2machine"
        self.connected = False

    def connect(self, ip: str):
        """
        Connects to the machine using the provided IP address.

        Args:
            ip (str): IP address of the machine.
        """
        self.reader = Client(url=ip)
        self.writer = Client(url=ip)
        self.reader.connect()
        self.writer.connect()
        self.reader.load_data_type_definitions()
        self.writer.load_data_type_definitions()

        self.connected = True

        # check if Livebit2machine exists, otherwise use Livebit2DuoMix
        try:
            self.read(self.liveBitNode)
        except ua.UaError:
            self.liveBitNode = "Livebit2DuoMix"
        # check if Livebit2DuoMix exists, otherwise throw error
        try:
            self.read(self.liveBitNode)
        except ua.UaError:
            raise ua.UaError("Livebit node not found. Machine not supported.")

        self.subscribe("Livebit2extern", self.changeLivebit, 500)
        
    
    def disconnect(self):
        """
        Disconnects from the machine.
        """
        self.reader.disconnect()
        self.writer.disconnect()
        self.connected = False

    def _status_change_callback(self, status):
        """
        Callback for subscription status changes.

        Args:
            status: The new status.
        """
        print("Connection status changed:", status)
        self.connected = status == ua.StatusCode(0)

    def change(self, parameter: str, value: any, typ: str):
        """
        Changes the value of an OPC-UA variable.

        Args:
            parameter (str): Variable to change.
            value (any): Value to change the variable to.
            typ (str): String of variable type ("bool", "uint16", "int32", "float").
        """
        if not self.connected:
            raise ua.UaError("Not connected to machine.")

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
        node = self.writer.get_node(self.baseNode + parameter)
        node.set_value(ua.Variant(value, t))

    def read(self, parameter: str) -> any:
        """
        Reads the value of an OPC-UA variable.

        Args:
            parameter (str): Variable to read.

        Returns:
            any: Value of the variable.
        """
        node = self.reader.get_node(self.baseNode + parameter)
        return node.get_value()

    def subscribe(self, parameter: str, callback: callable, interval: int):
        """
        Subscribes to a given OPC-UA parameter.

        Args:
            parameter (str): The OPC-UA parameter to subscribe to.
            callback (callable): Callback function receiving value and parameter.
            interval (int): Interval in ms for checking the parameter.

        Returns:
            list: [subscription, handler]
        """
        if not self.connected:
            raise ua.UaError("Not connected to machine.")
        
        subscriptionHandler = OpcuaSubscriptionHandler(parameter, callback, self._status_change_callback)
        subscription = self.reader.create_subscription(interval, subscriptionHandler)
        handler = subscription.subscribe_data_change(self.reader.get_node(self.baseNode + parameter))
        return [subscription, handler]

    def changeLivebit(self, value: bool, parameter=None):
        """
        Changes the Livebit value.

        Args:
            value (bool): The value to change the Livebit to.
            parameter: Unused, for callback compatibility.
        """
        if not self.connected:
            raise ua.UaError("Not connected to machine.")
        
        self.change(self.liveBitNode, value, "bool")



class OpcuaSubscriptionHandler:
    """
    Handler for OPC-UA subscription data changes.
    """
    def __init__(self, parameter, callback, status_change_callback=None):
        """
        Args:
            parameter (str): The parameter being subscribed to.
            callback (callable): Callback function for data changes.
            status_change_callback (callable, optional): Callback for status changes. Defaults to None.
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