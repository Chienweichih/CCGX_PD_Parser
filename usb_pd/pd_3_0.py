from . import utils

# Message Header
def table6_1(data):
    Extended = utils.bit(data, 15, 15)
    ObjCnt = utils.bit(data, 14, 12)
    # MessageID = utils.bit(data, 11, 9)
    PortPowerRole = utils.bit(data, 8, 8)
    # Revision = utils.bit(data, 7, 6)
    PortDataRole = utils.bit(data, 5, 5)
    MessageType = utils.bit(data, 4, 0)
    return (Extended, ObjCnt, PortPowerRole, PortDataRole, MessageType)

# Control Message Types
def table6_5(MessageType):
    if MessageType == 0b0000 or\
       (MessageType >= 0b1110 and MessageType <= 0b1111) or\
       (MessageType >= 0b10111 and MessageType <= 0b11111):
        print("All values not explicitly defined are Reserved and Shall Not be used.")
        return ""
    else:
        return {
            0b00001: "GoodCRC",
            0b00010: "GotoMin",
            0b00011: "Accept",
            0b00100: "Reject",
            0b00101: "Ping",
            0b00110: "PS_RDY",
            0b00111: "Get_Source_Cap",
            0b01000: "Get_Sink_Cap",
            0b01001: "DR_Swap",
            0b01010: "PR_Swap",
            0b01011: "VCONN_Swap",
            0b01100: "Wait",
            0b01101: "Soft_Reset",
            0b10000: "Not_Supported",
            0b10001: "Get_Source_Cap_Extended",
            0b10010: "Get_Status",
            0b10011: "FR_Swap",
            0b10100: "Get_PPS_Status",
            0b10101: "Get_Country_Codes",
            0b10110: "Get_Sink_Cap_Extended"
        }[MessageType]

# Data Message Types
def table6_6(MessageType):
    if MessageType == 0b0000 or\
       (MessageType >= 0b1000 and MessageType <= 0b1110) or\
       MessageType >= 0b10000:
        print("All values not explicitly defined are Reserved and Shall Not be used.")
        return ""
    else:
        return {
            0b0001: "Source_Cap      ",
            0b0010: "Request         ",
            0b0011: "BIST            ",
            0b0100: "Sink_Cap        ",
            0b0101: "Battery_Status  ",
            0b0110: "Alert           ",
            0b0111: "Get_Country_Info",
            0b1111: "Vendor_Defined  "
        }[MessageType]

# Fixed Supply PDO - Source
# Fixed Supply PDO - Sink
def table6_9_14(dataList, isSink):
    output = "[Fixed supply]" + utils.ONE_OBJ_NEWLINE
    for data in dataList:
        output += "===========================================" + utils.ONE_OBJ_NEWLINE

        voltage = utils.bit(data, 19, 10) * 50 / 1000
        current = utils.bit(data, 9 , 0 ) * 10 / 1000

        if not isSink and voltage != 5:
            # Table 10-4 Fixed Supply PDO – Source 9V
            utils.checkRSV0(data, 29, 22)
            output += "Peak Current: " + str(utils.bit(data, 21, 20)) + " (check table 6-10)" + utils.ONE_OBJ_NEWLINE
        else:
            output += "[Dual-Role Power]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 29, 29) == 1 else ""
            output += (("[Higher Capability]" if isSink else "[USB Suspend Supported]") + utils.ONE_OBJ_NEWLINE)\
                      if utils.bit(data, 28, 28) == 1 else ""
            output += "[Unconstrained Power]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 27, 27) == 1 else ""
            output += "[USB Communications Capable]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 26, 26) == 1 else ""
            output += "[Dual-Role Data]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 25, 25) == 1 else ""

            if isSink:
                output += "Fast Role Swap required USB Type-C Current: "
                output += {
                    0b00: "Fast Swap not supported",
                    0b01: "Default USB Power",
                    0b10: "1.5A @ 5V",
                    0b11: "3.0A @ 5V"
                }[utils.bit(data, 24, 23)]
                output += utils.ONE_OBJ_NEWLINE
                utils.checkRSV0(data, 22, 20)
            else:
                output += "[Unchunked Extended Messages Supported]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 24, 24) == 1 else ""
                utils.checkRSV0(data, 23, 22)
                output += "Peak Current: " + str(utils.bit(data, 21, 20)) + " (check table 6-10)" + utils.ONE_OBJ_NEWLINE

        output += str(voltage) + " V" + utils.ONE_OBJ_NEWLINE
        output += str(current) + " A" + utils.ONE_OBJ_NEWLINE
    output += "===========================================" + utils.ONE_OBJ_NEWLINE
    return output

# Variable Supply (non-Battery) PDO - Source
# Variable Supply (non-Battery) PDO - Sink
def table6_11_15(data, isSink):
    output = "[Variable Supply]" + utils.ONE_OBJ_NEWLINE
    output += "Maximum Voltage: " + str(utils.bit(data, 29, 20) * 50 / 1000) + " V" + utils.ONE_OBJ_NEWLINE
    output += "Minimum Voltage: " + str(utils.bit(data, 19, 10) * 50 / 1000) + " V" + utils.ONE_OBJ_NEWLINE
    output += ("Operational" if isSink else "Maximum") + " Current: "\
              + str(utils.bit(data, 9, 0) * 10 / 1000) + " A"
    return output

# Battery Supply PDO - Source
# Battery Supply PDO - Sink
def table6_12_16(data, isSink):
    output = "[Battery]" + utils.ONE_OBJ_NEWLINE
    output += "Maximum Voltage: " + str(utils.bit(data, 29, 20) * 50 / 1000) + " V" + utils.ONE_OBJ_NEWLINE
    output += "Minimum Voltage: " + str(utils.bit(data, 19, 10) * 50 / 1000) + " V" + utils.ONE_OBJ_NEWLINE
    output += ("Operational" if isSink else "Maximum Allowable") + " Power: "\
              + str(utils.bit(data, 9, 0) * 250 / 1000) + " W"
    return output

# Programmable Power Supply APDO - Source
# Programmable Power Supply APDO - Sink
def table6_13_17(data, isSink):
    output = "[Augmented Power Data Object]" + utils.ONE_OBJ_NEWLINE

    if (utils.bit(data, 29, 28) == 0):
        output += "[Programmable Power Supply]" + utils.ONE_OBJ_NEWLINE
    elif not isSink:
        print("Table 6-13, B29-28, Reserved - Shall Not be used.")

    if isSink:
        utils.checkRSV0(data, 27, 25)
    else:
        output += "[PPS Power Limited]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 27, 27) == 1 else ""
        utils.checkRSV0(data, 26, 25)

    output += "Maximum Voltage in 100mV increments: " + str(utils.bit(data, 24, 17)) + utils.ONE_OBJ_NEWLINE
    utils.checkRSV0(data, 16, 16)
    output += "Minimum Voltage in 100mV increments: " + str(utils.bit(data, 15, 8 )) + utils.ONE_OBJ_NEWLINE
    utils.checkRSV0(data, 7 , 7 )
    output += "Maximum Current in 50mA  increments: " + str(utils.bit(data, 6 , 0 ))
    return output

# Fixed and Variable Request Data Object
# The request takes a different form depending on the kind of power requested. 
# Need to check
def table6_18(data):
    utils.checkRSV0(data, 31, 31)
    utils.checkRSV0(data, 22, 20)

    objPos = utils.bit(data, 30, 28)
    if objPos == 0:
        print("Table 6-18, B30..28, 000b is Reserved and Shall Not be used.")

    output = "Object position: " + str(objPos) + utils.ONE_OBJ_NEWLINE
    output += "[GiveBack]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 27, 27) == 1 else ""
    output += "[Capability Mismatch]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 26, 26) == 1 else ""
    output += "[USB Communications Capable]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 25, 25) == 1 else ""
    output += "[No USB Suspend]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 24, 24) == 1 else ""
    output += "[Unchunked Extended Messages Supported]" + utils.ONE_OBJ_NEWLINE if utils.bit(data, 23, 23) == 1 else ""
    output += "Operating current: " + str(utils.bit(data, 19, 10) * 10 / 1000) + " A" + utils.ONE_OBJ_NEWLINE
    output += "Maximum Operating Current: " + str(utils.bit(data, 9, 0) * 10 / 1000) + " A"
    return output

# BIST Data Object
def table6_23(data):
    utils.checkRSV0(data, 27, 0)

    output = ""
    B31_28 = utils.bit(data, 31, 28)
    if B31_28 == 0b0101:
        output += "[BIST Carrier Mode]"
    elif B31_28 == 0b1000:
        output += "[BIST Test Data]"
    else:
        print("Shall Not be used")
    return output

# ID Header VDO
def table6_25(data, isUFP):
    CapableHost = utils.bit(data[0], 31, 31)
    CapableDev  = utils.bit(data[0], 30, 30)
    ProductType_U_C = utils.bit(data[0], 29, 27)
    MO_sup = utils.bit(data[0], 26, 26)
    ProductTypeDFP = utils.bit(data[0], 25, 23)
    utils.checkRSV0(data[0], 22, 16)
    USBVID = utils.bit(data[0], 15, 0)

    # Table C-3 Discover Identity Command response from Hub Responder Example
    USBXID = data[1]
    USBPID = utils.bit(data[2], 31, 16)
    bcdDevice = utils.bit(data[2], 15, 0)

    output = "Data Capable: "
    if CapableHost == 1 and CapableDev == 1:
        output += "Host and Device, "
    elif CapableHost == 1:
        output += "Host, "
    elif CapableDev == 1:
        output += "Device, "
    else:
        output += "N/A, "

    output += utils.VDM_NEWLINE
    if isUFP:
        output += "Product Type UFP / Cable Plug: "
        output += hex(ProductType_U_C) + ", "
    else:
        if (ProductTypeDFP > 4):
            print("Table 6-29, B25..23, Reserved, Shall Not be used.")
        else:
            output += "Product Type DFP: "
            output += {
                0b000: "Undefined,", 
                0b001: "PDUSB Hub,",
                0b010: "PDUSB Hub,",
                0b011: "Power Brick,",
                0b100: "Alternate Mode Controller (AMC),"
            }[ProductTypeDFP]

    output += utils.VDM_NEWLINE
    output += "Modal Operation: " + ("Yes" if MO_sup == 1 else "No") + ", "
    output += utils.VDM_NEWLINE
    output += "USB VID: " + '0x{:0>4X}'.format(USBVID) + ", "
    output += utils.VDM_NEWLINE
    output += "USB XID: " + '0x{:0>4X}'.format(USBXID) + ", "
    output += "USB PID: " + '0x{:0>4X}'.format(USBPID) + ", "
    output += utils.VDM_NEWLINE
    output += "Device version: " + '0x{:0>4X}'.format(bcdDevice) + ", "
    output += utils.VDM_NEWLINE
    # TODO: check this value
    output += '( 0x{:0>8X} ) <- ??'.format(data[3])
    return output

# Discover SVIDs Responder VDO
def table6_40(data):
    output = "SVIDs:"
    for i in range(len(data)):
        SVID  = ['0x{:0>4X}'.format(utils.bit(data[i], 31, 16))]
        SVID += ['0x{:0>4X}'.format(utils.bit(data[i], 15, 0 ))]
        output += utils.VDM_NEWLINE + str(SVID)
    return output

# Battery Status Data Object (BSDO)
def table6_41(data):
    utils.checkRSV0(data, 7, 0)

    output = "Battery Present Capacity: 0x{:0>4X}".format(utils.bit(data, 31, 16)) + utils.ONE_OBJ_NEWLINE
    output += "Battery Info: "
    info = utils.bit(data, 15, 8)
    utils.checkRSV0(info, 7, 4)
    output += "[Invalid Battery reference] " if utils.bit(info, 0, 0) == 1 else ""
    if utils.bit(info, 1, 1) == 1:
        output += {
            0b00: "[Battery is Charging]",
            0b01: "[Battery is Discharging]",
            0b10: "[Battery is Idle]",
            0b11: "[Reserved, Shall Not be used]"
        }[utils.bit(info, 3, 2)]
    else:
        utils.checkRSV0(info, 3, 2)
    return output

# Alert Data Object
def table6_42(data):
    utils.checkRSV0(data, 15, 0)
    AlertType = utils.bit(data, 31, 24)

    output = "AlertType: 0x{:0>2X} (check Table 6-42)".format(AlertType) + utils.ONE_OBJ_NEWLINE

    output += "Fixed Batteries: [ "
    for idx, val in enumerate(reversed([int(x) for x in bin(utils.bit(data, 23, 20))[2:]])):
        if val == 1:
            output += "B" + str(idx) + " "
    output += "]" + utils.ONE_OBJ_NEWLINE
    output += "Hot Swappable Batteries: [ "
    for idx, val in enumerate(reversed([int(x) for x in bin(utils.bit(data, 19, 16))[2:]])):
        if val == 1:
            output += "B" + str(idx + 4) + " "
    output += "]"
    return output

# Country Code Data Object
def table6_43(data):
    utils.checkRSV0(data, 15, 0)
    return "Country Code: 0x{:0>2X} ".format(utils.bit(data, 31, 24)) + "0x{:0>2X}".format(utils.bit(data, 23, 16))

# Extended Message Types
def table6_44(MessageType):
    if MessageType == 0b0000 or\
       (MessageType >= 0b10000 and MessageType <= 0b11111):
        print("All values not explicitly defined are Reserved and Shall Not be used.")
        return ""
    else:
        return {
            0b00001: "Source_Capabilities_Extended",
            0b00010: "Status",
            0b00011: "Get_Battery_Cap",
            0b00100: "Get_Battery_Status",
            0b00101: "Battery_Capabilities",
            0b00110: "Get_Manufacturer_Info",
            0b00111: "Manufacturer_Info",
            0b01000: "Security_Request",
            0b01001: "Security_Response",
            0b01010: "Firmware_Update_Request",
            0b01011: "Firmware_Update_Response",
            0b01100: "PPS_Status",
            0b01101: "Country_Info",
            0b01110: "Country_Codes",
            0b01111: "Sink_Capabilities_Extended",
        }[MessageType]

# TODO: find table in spec
def d_mode(data):
    return '0x{:0>8X}'.format(data)

# TODO: find table in spec
def attention(data):
    return '0x{:0>8X}'.format(data)

def capacity(data, isSink):
    PDOTypes = utils.bit(data[0], 31, 30)
    output = ""

    if (PDOTypes == 0b00):
        # Fixed Supply PDO
        output += table6_9_14(data[0:], isSink)
    elif (PDOTypes == 0b01):
        # Battery Supply PDO
        output += table6_12_16(data[0], isSink)
    elif (PDOTypes == 0b10):
        # Variable Supply (non-Battery) PDO
        output += table6_11_15(data[0], isSink)
    else:
        # Augmented PDO
        output += table6_13_17(data[0], isSink)
    return output
