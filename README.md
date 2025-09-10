
# mtecconnect3dcp

This repository contains tools and libraries for connecting to m-tec machines using OPC UA.

For the Python client library, see the [Python package README](Python/README.md).

## Supported Machines

The duo-mix connect and SMP connect use OPC UA as communication protocol. ([The P20 connect and P50 connect use Modbus RTU instead.](https://github.com/m-tec-com/m-tecConnectModbus))

## Connection

Connect the machine with the control unit (or your PC) with an ethernet cable.

You might have to change the IP-Range of your control unit (or PC).

The default IP-Adress of the OPC UA server in the m-tec connect duo-mix 3DCP, 3DCP+, SMP 3DCP, and flow-matic control unit is `10.129.4.73`.

