# -*- coding: utf-8 -*-
from . import pd_3_0

def parser(MessageType, PortDataRole, PortPowerRole, Extended, data):
    output = ""
    if Extended == 1:
        output += pd_3_0.table6_44(MessageType) + " "
        output += '  '.join(data[1:])
        # TODO: Finish Extended Type
    else:
        output += pd_3_0.table6_6(MessageType) + " "

        if MessageType == 0b0001 or MessageType == 0b0100:
            # Source_Cap or Sink_Cap
            output += pd_3_0.capacity([int(x, 16) for x in data], (PortPowerRole == 0))
        elif MessageType == 0b0010:
            # Request
            output += pd_3_0.table6_18(int(data[0], 16))
        elif MessageType == 0b0011:
            # BIST
            output += pd_3_0.table6_23(int(data[0], 16))
        elif MessageType == 0b0101:
            # Battery_Status
            output += pd_3_0.table6_41(int(data[0], 16))
        elif MessageType == 0b0110:
            # Alert
            output += pd_3_0.table6_42(int(data[0], 16))
        elif MessageType == 0b0111:
            # Get_Country_Info
            output += pd_3_0.table6_43(int(data[0], 16))
        elif MessageType == 0b1111:
            # Vendor_Defined
            output += '  '.join(data[1:])
    return output

def csvReader(fileName, magicPassword):
    import csv
    with open(fileName, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        print("PD Parser Result:")
        for row in rows:
        # for idx, row in enumerate(rows):
            dataList = row['Data'].split()
            (Extended, ObjCnt, PortPowerRole, PortDataRole, MessageType) = pd_3_0.table6_1(int(dataList[0], 16))
            if (magicPassword.lower() != 'GoodCRC'.lower()) and (ObjCnt == 0) and (MessageType == 1):
                # Hide GoodCRC if no magicPassword
                continue
            outputString = "{:0>4d}".format(int(row['SL#'])) + ' | '
            # outputString = "{:0>4d}".format(idx + 1) + ' | '
            if row['SOP'] == 'SOP':
                outputString += 'DR: ' + ('UFP' if PortDataRole == 0 else 'DFP') + ' | '
                outputString += 'PR: ' + ('Sink   ' if PortPowerRole == 0 else 'Source ') + ' | '
            else:
                outputString += 'DR: RSV | '
                outputString += 'PR: ' + ('DFP/UFP' if PortPowerRole == 0 else 'C_P/VPD') + ' | '
            outputString += parser(MessageType, PortDataRole, PortPowerRole, Extended, dataList[1:])\
                            if ObjCnt > 0 else\
                            pd_3_0.table6_5(MessageType)
            print(outputString)

def parse_cc_log():
    import sys
    if len(sys.argv) < 2:
        print("Need CSV File Name (argv[1])")
    else:
        csvReader(sys.argv[1], sys.argv[-1])
