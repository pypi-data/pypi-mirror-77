def read_coils_serialize(start_addr, no_of_coils, unit_addr, tid):
    """ This function serializes the input data into a request that will be sent and saves the serialization information
        into a dictionary.

    Args:
        start_addr: The starting address from which the coils are being read.
        no_of_coils: Number of coils to be read.
        unit_addr:  The unit address on the device.
        tid: The transaction id that will be used in the request.

    Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.

    """
    func_code = "01"
    protocol = _get_protocol_str()
    tid = _get_tid_str(tid)
    unit_addr = _get_unit_addr_str(unit_addr)
    start_addr = _get_start_addr_str(start_addr)

    no_of_coils = str(hex(no_of_coils))[2:].rjust(4, '0')
    modbus_request = func_code + start_addr + no_of_coils

    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)
    communication_dict = _make_com_dict(tid, unit_addr, func_code, "Read Coils.", start_addr, no_of_coils, bytes_req)
    return bytes_req, communication_dict


def read_discrete_inputs_serialize(start_addr, input_count, unit_addr, tid):
    """ This function serializes the input data into a request that will be sent and saves the serialization information
        into dictionary.

    Args:
        start_addr: The starting address from which the coils are being read.
        input_count: Number of discrete inputs to be read.
        unit_addr:  The unit address on the device.
        tid: The transaction id that will be used in the request.

     Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.

    """
    func_code = "02"
    protocol = _get_protocol_str()
    tid = _get_tid_str(tid)
    unit_addr = _get_unit_addr_str(unit_addr)
    start_addr = _get_start_addr_str(start_addr)

    input_count = str(hex(input_count))[2:].rjust(4, '0')
    modbus_request = func_code + start_addr + input_count

    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Read Discrete Inputs."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, input_count, bytes_req)
    return bytes_req, communication_dict


def read_holding_registers_serialize(start_addr, h_regs_count, unit_addr, tid):
    """ This function serializes the input data into a request that will be sent and saves the serialization information
        into dictionary.

    Args:
        start_addr: The starting address from which the coils are being read.
        h_regs_count: Number of holding registers to be read.
        unit_addr:  The unit address on the device.
        tid: The transaction id that will be used in the request.

    Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.

    """
    func_code = "03"
    protocol = _get_protocol_str()
    tid = _get_tid_str(tid)
    unit_addr = _get_unit_addr_str(unit_addr)
    start_addr = _get_start_addr_str(start_addr)

    h_regs_count = str(hex(h_regs_count))[2:].rjust(4, '0')
    modbus_request = func_code + start_addr + h_regs_count

    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Read Holding Registers."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, h_regs_count, bytes_req)
    return bytes_req, communication_dict


def read_input_registers_serialize(start_addr, in_regs_count, unit_addr, tid):
    """ This function serializes the input data into a request that will be sent and saves the serialization information
        into dictionary.

    Args:
        start_addr: The starting address from which the coils are being read.
        in_regs_count: Number of input registers to be read.
        unit_addr:  The unit address on the device.
        tid: The transaction id that will be used in the request.

    Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.

    """
    func_code = "04"
    protocol = _get_protocol_str()
    tid = _get_tid_str(tid)
    unit_addr = _get_unit_addr_str(unit_addr)
    start_addr = _get_start_addr_str(start_addr)
    in_regs_count = str(hex(in_regs_count))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + in_regs_count
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Read Input Registers."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, in_regs_count, bytes_req)
    return bytes_req, communication_dict


def write_single_coil_serialize(start_addr, coil_state, unit_addr, tid):
    """ This function serializes the input data into a request that will be sent and saves the serialization information
        into dictionary.

    Args:
        start_addr: The starting address from which the coils are being read.
        coil_state: The value to be written into a coil. It can only be 1 or 0.
        unit_addr:  The unit address on the device.
        tid: The transaction id that will be used in the request.

    Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.

    """
    func_code = "05"
    protocol = _get_protocol_str()
    tid = _get_tid_str(tid)
    unit_addr = _get_unit_addr_str(unit_addr)
    start_addr = _get_start_addr_str(start_addr)

    if coil_state == 1:
        modbus_request = func_code + start_addr + "ff" + "00"
    else:
        modbus_request = func_code + start_addr + "00" + "00"

    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Write Single Coil."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, str(coil_state), bytes_req)
    return bytes_req, communication_dict


def write_single_register_serialize(start_addr, reg_value, unit_addr, tid):
    """ This function serializes the input data into a request that will be sent and saves the serialization information
        into dictionary.

    Args:
        start_addr: The starting address from which the coils are being read.
        reg_value: The value to be written into a register.
        unit_addr:  The unit address on the device.
        tid: The transaction id that will be used in the request.

    Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.

    """
    func_code = "06"
    protocol = _get_protocol_str()
    tid = _get_tid_str(tid)
    unit_addr = _get_unit_addr_str(unit_addr)
    start_addr = _get_start_addr_str(start_addr)
    reg_value = str(hex(reg_value))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + reg_value
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Write Single Register."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, reg_value, bytes_req)
    return bytes_req, communication_dict


def _make_com_dict(tid, unit_addr, func_code, req_name, start_addr, no_of_el, bytes_req):
    communication_dict = {
        "current_tid": int(tid, 16),
        "current_unit_address": str(int(unit_addr, 16)),
        "current_function_code": func_code,
        "current_request_name": req_name,
        "current_request_from_gui": [int(start_addr, 16) + 1, int(no_of_el, 16), int(unit_addr, 16), int(func_code)],
        "current_request_from_gui_is_valid": True,
        "current_request_from_gui_error_msg": "-",
        "current_request_serialized": bytes_req
    }
    return communication_dict


def _get_protocol_str():
    protocol = "0000"
    return protocol


def _get_tid_str(tid):
    tid = str(hex(tid))[2:].rjust(4, '0')
    return tid


def _get_unit_addr_str(unit_addr):
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    return unit_addr


def _get_start_addr_str(start_addr):
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')
    return start_addr
