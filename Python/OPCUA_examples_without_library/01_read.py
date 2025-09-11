from opcua import Client, ua      

# connect
reader = Client("opc.tcp://10.129.4.73:4840")
reader.connect()
reader.load_type_definitions()

# read variable
node = reader.get_node("ns=4;s=|var|B-Fortis CC-Slim S04.Application.GVL_OPC.reserve_AI_2")
print("AI_2:", node.get_value())