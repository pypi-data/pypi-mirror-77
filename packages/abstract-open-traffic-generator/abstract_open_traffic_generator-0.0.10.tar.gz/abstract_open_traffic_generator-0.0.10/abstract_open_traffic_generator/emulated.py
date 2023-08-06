

class DeviceGroup(object):
    """Emulated.DeviceGroup class

    An abstract container for emulated device containers.

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - ports (Union[list[Union[str, type(None)]], type(None)]): One or more port names that the emulated device containers will share.
    - devices (Union[list[Union[Device, type(None)]], type(None)]): One or more emulated device containers.
    """
    def __init__(self, name=None, ports=None, devices=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(ports, (list, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (list, type(None))')
        if isinstance(devices, (list, type(None))) is True:
            self.devices = devices
        else:
            raise TypeError('devices must be an instance of (list, type(None))')


class Device(object):
    """Emulated.Device class

    An abstract container for emulated devices.

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - devices_per_port (Union[float, int, type(None)]): The number of emulated devices that will be created on each port.
    - parent (Union[str, type(None)]): The name of a device container or network container that is  the parent of this container.  Use this property to establish a hierarchical relationship between  device containers. A non-existent value indicates the device container is the  root of the hierarchy.  
    - protocols (Union[list[Union[Protocol, type(None)]], type(None)]): The emulated protocols in this device container.
    """
    def __init__(self, name=None, devices_per_port=None, parent=None, protocols=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(devices_per_port, (float, int, type(None))) is True:
            self.devices_per_port = devices_per_port
        else:
            raise TypeError('devices_per_port must be an instance of (float, int, type(None))')
        if isinstance(parent, (str, type(None))) is True:
            self.parent = parent
        else:
            raise TypeError('parent must be an instance of (str, type(None))')
        if isinstance(protocols, (list, type(None))) is True:
            self.protocols = protocols
        else:
            raise TypeError('protocols must be an instance of (list, type(None))')


class Protocol(object):
    """Emulated.Protocol class

    An abstract container for emulated protocols.

    Args
    ----
    - choice (Union[str, type(None)]): TBD
    - ethernet (Union[Ethernet, type(None)]): Emulated ethernet protocol
    - vlan (Union[Vlan, type(None)]): Emulated vlan protocol
    - ipv4 (Union[Ipv4, type(None)]): Emulated ipv4 protocol
    - bgpv4 (Union[Bgpv4, type(None)]): Emulated bgpv4 protocol
    """
    _CHOICE_MAP = {
        'Ethernet': 'ethernet',
        'Vlan': 'vlan',
        'Ipv4': 'ipv4',
        'Bgpv4': 'bgpv4',
    }
    def __init__(self, choice):
        from abstract_open_traffic_generator.emulated import Ethernet
        from abstract_open_traffic_generator.emulated import Vlan
        from abstract_open_traffic_generator.emulated import Ipv4
        from abstract_open_traffic_generator.emulated import Bgpv4
        if isinstance(choice, (Ethernet, Vlan, Ipv4, Bgpv4)) is False:
            raise TypeError('choice must be of type: Ethernet, Vlan, Ipv4, Bgpv4')
        self.__setattr__('choice', Protocol._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Protocol._CHOICE_MAP[type(choice).__name__], choice)


class Ethernet(object):
    """Emulated.Ethernet class

    Emulated ethernet protocol

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - parent (Union[str, type(None)]): The name of a device container or network container that is  the parent of this container.  Use this property to establish a hierarchical relationship between  device containers. A non-existent value indicates the device container is the  root of the hierarchy.  
    - mac (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - mtu (Union[Pattern, type(None)]): A container for emulated device property patterns.
    """
    def __init__(self, name=None, parent=None, mac=None, mtu=None):
        from abstract_open_traffic_generator.emulated import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(parent, (str, type(None))) is True:
            self.parent = parent
        else:
            raise TypeError('parent must be an instance of (str, type(None))')
        if isinstance(mac, (Pattern, type(None))) is True:
            self.mac = mac
        else:
            raise TypeError('mac must be an instance of (Pattern, type(None))')
        if isinstance(mtu, (Pattern, type(None))) is True:
            self.mtu = mtu
        else:
            raise TypeError('mtu must be an instance of (Pattern, type(None))')


class Pattern(object):
    """Emulated.Pattern class

    A container for emulated device property patterns.

    Args
    ----
    - choice (Union[str, type(None)]): TBD
    - fixed (Union[str, type(None)]): TBD
    - list (Union[list[Union[str, type(None)]], type(None)]): TBD
    - increment (Union[Increment, type(None)]): An incrementing pattern.
    - decrement (Union[Decrement, type(None)]): A decrementing pattern.
    - random (Union[Random, type(None)]): A repeatable random range pattern.
    """
    _CHOICE_MAP = {
        'str': 'fixed',
        'list': 'list',
        'Increment': 'increment',
        'Decrement': 'decrement',
        'Random': 'random',
    }
    def __init__(self, choice):
        from abstract_open_traffic_generator.emulated import Increment
        from abstract_open_traffic_generator.emulated import Decrement
        from abstract_open_traffic_generator.emulated import Random
        if isinstance(choice, (str, list, Increment, Decrement, Random)) is False:
            raise TypeError('choice must be of type: str, list, Increment, Decrement, Random')
        self.__setattr__('choice', Pattern._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Pattern._CHOICE_MAP[type(choice).__name__], choice)


class Increment(object):
    """Emulated.Increment class

    An incrementing pattern.

    Args
    ----
    - start (Union[str, type(None)]): TBD
    - step (Union[str, type(None)]): TBD
    """
    def __init__(self, start=None, step=None):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')


class Decrement(object):
    """Emulated.Decrement class

    A decrementing pattern.

    Args
    ----
    - start (Union[str, type(None)]): TBD
    - step (Union[str, type(None)]): TBD
    """
    def __init__(self, start=None, step=None):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')


class Random(object):
    """Emulated.Random class

    A repeatable random range pattern.

    Args
    ----
    - min (Union[str, type(None)]): TBD
    - max (Union[str, type(None)]): TBD
    - step (Union[float, int, type(None)]): TBD
    - seed (Union[str, type(None)]): TBD
    """
    def __init__(self, min=None, max=None, step=None, seed=None):
        if isinstance(min, (str, type(None))) is True:
            self.min = min
        else:
            raise TypeError('min must be an instance of (str, type(None))')
        if isinstance(max, (str, type(None))) is True:
            self.max = max
        else:
            raise TypeError('max must be an instance of (str, type(None))')
        if isinstance(step, (float, int, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (float, int, type(None))')
        if isinstance(seed, (str, type(None))) is True:
            self.seed = seed
        else:
            raise TypeError('seed must be an instance of (str, type(None))')


class Vlan(object):
    """Emulated.Vlan class

    Emulated vlan protocol

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - parent (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - tpid (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - priority (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - id (Union[Pattern, type(None)]): A container for emulated device property patterns.
    """
    def __init__(self, name=None, parent=None, tpid=None, priority=None, id=None):
        from abstract_open_traffic_generator.emulated import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(parent, (str, type(None))) is True:
            self.parent = parent
        else:
            raise TypeError('parent must be an instance of (str, type(None))')
        if isinstance(tpid, (Pattern, type(None))) is True:
            self.tpid = tpid
        else:
            raise TypeError('tpid must be an instance of (Pattern, type(None))')
        if isinstance(priority, (Pattern, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (Pattern, type(None))')
        if isinstance(id, (Pattern, type(None))) is True:
            self.id = id
        else:
            raise TypeError('id must be an instance of (Pattern, type(None))')


class Ipv4(object):
    """Emulated.Ipv4 class

    Emulated ipv4 protocol

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - address (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - gateway (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - prefix (Union[Pattern, type(None)]): A container for emulated device property patterns.
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None):
        from abstract_open_traffic_generator.emulated import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')


class Bgpv4(object):
    """Emulated.Bgpv4 class

    Emulated bgpv4 protocol

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - as_number_2_byte (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - dut_as_number_2_byte (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - as_number_4_byte (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - as_number_set_mode (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - type (Union[str, type(None)]): The type of BGP topology.  External BGP (EBGP) is used for BGP links between two or more  Autonomous Systems. Internal BGP (IBGP) is used within a single Autonomous System.
    - hold_time_interval (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - keep_alive_interval (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - graceful_restart (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - authentication (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - ttl (Union[Pattern, type(None)]): A container for emulated device property patterns.
    - dut_ipv4_address (Union[Pattern, type(None)]): A container for emulated device property patterns.
    """
    def __init__(self, name=None, as_number_2_byte=None, dut_as_number_2_byte=None, as_number_4_byte=None, as_number_set_mode=None, type=None, hold_time_interval=None, keep_alive_interval=None, graceful_restart=None, authentication=None, ttl=None, dut_ipv4_address=None):
        from abstract_open_traffic_generator.emulated import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(as_number_2_byte, (Pattern, type(None))) is True:
            self.as_number_2_byte = as_number_2_byte
        else:
            raise TypeError('as_number_2_byte must be an instance of (Pattern, type(None))')
        if isinstance(dut_as_number_2_byte, (Pattern, type(None))) is True:
            self.dut_as_number_2_byte = dut_as_number_2_byte
        else:
            raise TypeError('dut_as_number_2_byte must be an instance of (Pattern, type(None))')
        if isinstance(as_number_4_byte, (Pattern, type(None))) is True:
            self.as_number_4_byte = as_number_4_byte
        else:
            raise TypeError('as_number_4_byte must be an instance of (Pattern, type(None))')
        if isinstance(as_number_set_mode, (Pattern, type(None))) is True:
            self.as_number_set_mode = as_number_set_mode
        else:
            raise TypeError('as_number_set_mode must be an instance of (Pattern, type(None))')
        if isinstance(type, (str, type(None))) is True:
            self.type = type
        else:
            raise TypeError('type must be an instance of (str, type(None))')
        if isinstance(hold_time_interval, (Pattern, type(None))) is True:
            self.hold_time_interval = hold_time_interval
        else:
            raise TypeError('hold_time_interval must be an instance of (Pattern, type(None))')
        if isinstance(keep_alive_interval, (Pattern, type(None))) is True:
            self.keep_alive_interval = keep_alive_interval
        else:
            raise TypeError('keep_alive_interval must be an instance of (Pattern, type(None))')
        if isinstance(graceful_restart, (Pattern, type(None))) is True:
            self.graceful_restart = graceful_restart
        else:
            raise TypeError('graceful_restart must be an instance of (Pattern, type(None))')
        if isinstance(authentication, (Pattern, type(None))) is True:
            self.authentication = authentication
        else:
            raise TypeError('authentication must be an instance of (Pattern, type(None))')
        if isinstance(ttl, (Pattern, type(None))) is True:
            self.ttl = ttl
        else:
            raise TypeError('ttl must be an instance of (Pattern, type(None))')
        if isinstance(dut_ipv4_address, (Pattern, type(None))) is True:
            self.dut_ipv4_address = dut_ipv4_address
        else:
            raise TypeError('dut_ipv4_address must be an instance of (Pattern, type(None))')
