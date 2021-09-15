import logging

import sdm_modbus
from sdm_modbus import registerType, registerDataType

class GARO(sdm_modbus.SDM):
    def _encode_value(self, data, dtype):
        if dtype == registerDataType.INT32:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            builder.add_32bit_int(data)
            return builder.to_registers()
        elif dtype == registerDataType.INT16:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            builder.add_16bit_int(data)
            return builder.to_registers()
        return super()._encode_value(data, dtype)

    def _bigbig_to_biglittle(self, value):
        # Hack because base class doesn't allow defining a different endianness.
        b = value.to_bytes(4, byteorder='big', signed=False)
        return int.from_bytes(b[2:4]+b[0:2], byteorder='big', signed=True)

    def _decode_value(self, data, length, dtype, vtype):
        if dtype == registerDataType.INT32:
            return vtype(self._bigbig_to_biglittle(data.decode_32bit_uint()))
        elif dtype == registerDataType.INT16:
            return vtype(data.decode_16bit_int())
        return super()._decode_value(data, length, dtype, vtype)


class GNM3D(GARO):
    def __init__(self, *args, **kwargs):
        self.model = "GNM3D"
        super().__init__(*args, **kwargs)

        self.register_description = {
            "p1n_voltage": { "register": (0x0000, 2, registerType.INPUT, registerDataType.INT32, int, "V L1-N", "", 1), "scaling": 1/10 },
            "p2n_voltage": { "register": (0x0002, 2, registerType.INPUT, registerDataType.INT32, int, "V L2-N", "", 1), "scaling": 1/10 },
            "p3n_voltage": { "register": (0x0004, 2, registerType.INPUT, registerDataType.INT32, int, "V L3-N", "", 1), "scaling": 1/10 },
            "p12_voltage": { "register": (0x0006, 2, registerType.INPUT, registerDataType.INT32, int, "V L1-L2", "", 1), "scaling": 1/10 },
            "p23_voltage": { "register": (0x0008, 2, registerType.INPUT, registerDataType.INT32, int, "V L2-L3", "", 1), "scaling": 1/10 },
            "p31_voltage": { "register": (0x000A, 2, registerType.INPUT, registerDataType.INT32, int, "V L3-L1", "", 1), "scaling": 1/10 },
            "p1_current": { "register": (0x000C, 2, registerType.INPUT, registerDataType.INT32, int, "A L1", "", 1), "scaling": 1/1000 },
            "p2_current": { "register": (0x000E, 2, registerType.INPUT, registerDataType.INT32, int, "A L2", "", 1), "scaling": 1/1000 },
            "p3_current": { "register": (0x0010, 2, registerType.INPUT, registerDataType.INT32, int, "A L3", "", 1), "scaling": 1/1000 },
            "p1_power_active": { "register": (0x0012, 2, registerType.INPUT, registerDataType.INT32, int, "W L1", "", 1), "scaling": 1/10 },
            "p2_power_active": { "register": (0x0014, 2, registerType.INPUT, registerDataType.INT32, int, "W L2", "", 1), "scaling": 1/10 },
            "p3_power_active": { "register": (0x0016, 2, registerType.INPUT, registerDataType.INT32, int, "W L3", "", 1), "scaling": 1/10 },
            "p1_energy_apparent": { "register": (0x0018, 2, registerType.INPUT, registerDataType.INT32, int, "kVA L1", "kVA", 1), "scaling": 1/10000 },
            "p2_energy_apparent": { "register": (0x001A, 2, registerType.INPUT, registerDataType.INT32, int, "kVA L2", "kVA", 1), "scaling": 1/10000 },
            "p3_energy_apparent": { "register": (0x001C, 2, registerType.INPUT, registerDataType.INT32, int, "kVA L3", "kVA", 1), "scaling": 1/10000 },
            "p1_energy_reactive": { "register": (0x001E, 2, registerType.INPUT, registerDataType.INT32, int, "kVAr L1", "kVAr", 1), "scaling": 1/10000 },
            "p2_energy_reactive": { "register": (0x0020, 2, registerType.INPUT, registerDataType.INT32, int, "kVAr L2", "kVAr", 1), "scaling": 1/10000 },
            "p3_energy_reactive": { "register": (0x0022, 2, registerType.INPUT, registerDataType.INT32, int, "kVAr L3", "kVAr", 1), "scaling": 1/10000 },
            "voltage_ln": { "register": (0x0024, 2, registerType.INPUT, registerDataType.INT32, int, "V L-N sys", "V", 2), "scaling": 1/10 },
            "voltage_ll": { "register": (0x0026, 2, registerType.INPUT, registerDataType.INT32, int, "V L-L sys", "V", 2), "scaling": 1/10 },
            "power_active": { "register": (0x0028, 2, registerType.INPUT, registerDataType.INT32, int, "kW sys", "kW", 2), "scaling": 1/10000 },
            "power_apparent": { "register": (0x002A, 2, registerType.INPUT, registerDataType.INT32, int, "kVA sys", "kVA", 2), "scaling": 1/10000 },
            "power_reactive": { "register": (0x002C, 2, registerType.INPUT, registerDataType.INT32, int, "kVAr sys", "kVAr", 2), "scaling": 1/10000 },
            "p1_power_factor": { "register": (0x002E, 1, registerType.INPUT, registerDataType.INT16, int, "PF L1", "", 2), "scaling": 1/1000 },
            "p2_power_factor": { "register": (0x002F, 1, registerType.INPUT, registerDataType.INT16, int, "PF L2", "", 2), "scaling": 1/1000 },
            "p3_power_factor": { "register": (0x0030, 1, registerType.INPUT, registerDataType.INT16, int, "PF L3", "", 2), "scaling": 1/1000 },
            "power_factor": { "register": (0x0031, 1, registerType.INPUT, registerDataType.INT16, int, "PF sys", "", 2), "scaling": 1/1000 },
            "frequency": { "register": (0x0033, 1, registerType.INPUT, registerDataType.INT16, int, "Hz", "", 2), "scaling": 1/10 },
            "import_energy_active": { "register": (0x0034, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) TOT", "kWh", 2), "scaling": 1/10 },
            "import_energy_reactive": { "register": (0x0036, 2, registerType.INPUT, registerDataType.INT32, int, "kVArh (+) TOT", "kVArh", 2), "scaling": 1/10 },
            "demand_power_active": { "register": (0x0038, 2, registerType.INPUT, registerDataType.INT32, int, "kW dmd", "kW", 2), "scaling": 1/10000 },
            "maximum_demand_power_active": { "register": (0x003A, 2, registerType.INPUT, registerDataType.INT32, int, "kW dmd peak", "kW", 2), "scaling": 1/10000 },
            "p1_import_energy_active": { "register": (0x0040, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) L1", "kWh", 2), "scaling": 1/10 },
            "p2_import_energy_active": { "register": (0x0042, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) L2", "kWh", 2), "scaling": 1/10 },
            "p3_import_energy_active": { "register": (0x0044, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) L3", "kWh", 2), "scaling": 1/10 },
            "export_energy_active": { "register": (0x004E, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (-) TOT", "kWh", 2), "scaling": 1/10 },
            "export_energy_reactive": { "register": (0x0050, 2, registerType.INPUT, registerDataType.INT32, int, "kVArh (-) TOT", "kVArh", 2), "scaling": 1/10 }
        }

        self.registers = {k: v["register"] for k, v in self.register_description.items() }

    def _get_scaling(self, key):
        return self.register_description[key].get("scaling", 1)

    def read(self, key):
        return super().read(key) * self._get_scaling(key)

    def read_all(self, rtype=registerType.INPUT):
        val = super().read_all(rtype)
        return {k: v * self._get_scaling(k) for k, v in val.items() }

    def write(self, key, data):
        super().write(key, data / self._get_scaling(key))


def device(config):

    # Configuration parameters:
    #
    # timeout   seconds to wait for a response, default: 1
    # retries   number of retries, default: 3
    # unit      modbus address, default: 1
    #
    # For Modbus TCP:
    # host      ip or hostname
    # port      modbus tcp port
    #
    # For Modbus RTU:
    # device    serial device, e.g. /dev/ttyUSB0
    # stopbits  number of stop bits
    # parity    parity setting, N, E or O
    # baud      baud rate

    timeout = config.getint("timeout", fallback=1)
    retries = config.getint("retries", fallback=3)
    unit = config.getint("src_address", fallback=1)

    host = config.get("host", fallback=False)
    port = config.getint("port", fallback=False)
    device = config.get("device", fallback=False)

    if device:
        stopbits = config.getint("stopbits", fallback=1)
        parity = config.get("parity", fallback="N")
        baud = config.getint("baud", fallback=9600)

        if (parity
                and parity.upper() in ["N", "E", "O"]):
            parity = parity.upper()
        else:
            parity = False

        return GNM3D(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baud=baud,
            timeout=timeout,
            retries=retries,
            unit=unit
        )
    else:
        return GNM3D(
            host=host,
            port=port,
            timeout=timeout,
            retries=retries,
            unit=unit
        )

    return False


def values(device):
    if not device:
        return {}

    logger = logging.getLogger()
    logger.debug(f"device: {device}")

    values = device.read_all()

    logger.debug(f"values: {values}")

    return values
    return {
        # "energy_active"
        # "import_energy_active"
        # "power_active"
        # "p1_power_active"
        # "p2_power_active"
        # "p3_power_active"
        # "voltage_ln"
        # "p1n_voltage"
        # "p2n_voltage"
        # "p3n_voltage"
        # "voltage_ll"
        # "p12_voltage"
        # "p23_voltage"
        # "p31_voltage"
        # "frequency"
        # "p1_energy_active"
        # "p2_energy_active"
        # "p3_energy_active"
        # "p1_import_energy_active"
        # "p2_import_energy_active"
        # "p3_import_energy_active"
        # "export_energy_active"
        # "p1_export_energy_active"
        # "p2_export_energy_active"
        # "p3_export_energy_active"
        # "energy_reactive"
        # "p1_energy_reactive"
        # "p2_energy_reactive"
        # "p3_energy_reactive"
        # "energy_apparent"
        # "p1_energy_apparent"
        # "p2_energy_apparent"
        # "p3_energy_apparent"
        # "power_factor"
        # "p1_power_factor"
        # "p2_power_factor"
        # "p3_power_factor"
        # "power_reactive"
        # "p1_power_reactive"
        # "p2_power_reactive"
        # "p3_power_reactive"
        # "power_apparent"
        # "p1_power_apparent"
        # "p2_power_apparent"
        # "p3_power_apparent"
        # "p1_current"
        # "p2_current"
        # "p3_current"
        # "demand_power_active"
        # "minimum_demand_power_active"
        # "maximum_demand_power_active"
        # "demand_power_apparent"
        # "p1_demand_power_active"
        # "p2_demand_power_active"
        # "p3_demand_power_active"
    }
