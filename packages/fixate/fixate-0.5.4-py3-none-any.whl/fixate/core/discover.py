import re
from pubsub import pub
import visa
import fixate.config
from fixate.drivers import ftdi
from fixate.core.exceptions import InstrumentNotConnected


def open_instrument(instr_type):
    """open_visa_instrument implements the  public api for each of the drivers for discovering and opening a connection
    :param instr_type:
    The abstract base class to implement
    A dictionary containing the technical specifications of the required equipment
    :return:
    A instantiated class connected to a valid dmm
    """
    instruments = filter_connected(
        fixate.config.INSTRUMENTS, fixate.config.DRIVERS.get(instr_type, {})
    )
    try:
        instrument = list(instruments.values())[0]

    except IndexError:
        raise InstrumentNotConnected("No valid {} found".format(instr_type))
    else:
        instrument_name = type(instrument).__name__
        pub.sendMessage(
            "driver_open",
            instr_type=instrument_name,
            identity=instrument.get_identity(),
        )
        return instrument


def discover_ftdi():
    ftdi.create_device_info_list()
    return list(ftdi.get_device_info_list())


def filter_connected(instruments, classes):
    """Iterates through a list of connected equipment and attempts to detect if they are matched to the given classes
    :return:
    """
    rm = (
        visa.ResourceManager()
    )  # TODO remove this and place onus on instrument to know about visa
    result = {}
    for cls_name, cls in classes:
        if cls.INSTR_TYPE == "VISA":
            for instr_id, instr_interface in instruments.get("visa", []):
                # In future make it a proper regex search rather than a straight string search
                if re.search(cls.REGEX_ID, instr_id):
                    try:
                        result[cls_name] = cls(rm.open_resource(instr_interface))
                    except visa.VisaIOError:
                        pass
        if cls.INSTR_TYPE == "SERIAL":
            for com_port, info in instruments.get("serial", {}).items():
                instr_id, baud_rate = info
                if re.search(cls.REGEX_ID, instr_id):
                    try:
                        result[cls_name] = cls(com_port)
                        result[cls_name].baud_rate = baud_rate
                    except Exception as e:
                        pass
    return result
