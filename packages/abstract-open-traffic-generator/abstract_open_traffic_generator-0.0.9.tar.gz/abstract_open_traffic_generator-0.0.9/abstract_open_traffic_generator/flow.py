

class Flow(object):
	"""Flow.Flow class

	A high level data plane traffic flow
	Acts as a container for endpoints, frame size, frame rate, duration and packet headers.

	Args
	----
	- name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
	- endpoint (Union[Endpoint, type(None)]): A container for different types of endpoints. The endpoint choice dictates the type of flow.
	- packet (Union[list[Union[Header, type(None)]], type(None)]): The packet is a list of traffic protocol headers. The order of traffic protocol headers assigned to the list is the order they will appear on the wire.
	- size (Union[Size, type(None)]): The frame size which overrides the total length of the packet
	- rate (Union[Rate, type(None)]): The rate of packet transmission
	"""
	def __init__(self, name=None, endpoint=None, packet=None, size=None, rate=None):
		from abstract_open_traffic_generator.flow import Endpoint
		from abstract_open_traffic_generator.flow import Size
		from abstract_open_traffic_generator.flow import Rate
		if isinstance(name, (str, type(None))) is True:
			self.name = name
		else:
			raise TypeError('name must be an instance of (str, type(None))')
		if isinstance(endpoint, (Endpoint, type(None))) is True:
			self.endpoint = endpoint
		else:
			raise TypeError('endpoint must be an instance of (Endpoint, type(None))')
		if isinstance(packet, (list, type(None))) is True:
			self.packet = packet
		else:
			raise TypeError('packet must be an instance of (list, type(None))')
		if isinstance(size, (Size, type(None))) is True:
			self.size = size
		else:
			raise TypeError('size must be an instance of (Size, type(None))')
		if isinstance(rate, (Rate, type(None))) is True:
			self.rate = rate
		else:
			raise TypeError('rate must be an instance of (Rate, type(None))')


class Endpoint(object):
	"""Flow.Endpoint class

	A container for different types of endpoints
	The endpoint choice dictates the type of flow.

	Args
	----
	- choice (Union[str, type(None)]): The type of endpoint that the flow will originate from.
	- port (Union[PortEndpoint, type(None)]): An endpoint that contains a transmit port and 0..n receive ports.
	- device (Union[DeviceEndpoint, type(None)]): An endpoint that contains 1..n emulated transmit devices and 1..n  emulated receive devices.
	"""
	_CHOICE_MAP = {
		'PortEndpoint': 'port',
		'DeviceEndpoint': 'device',
	}
	def __init__(self, choice):
		from abstract_open_traffic_generator.flow import PortEndpoint
		from abstract_open_traffic_generator.flow import DeviceEndpoint
		if isinstance(choice, (PortEndpoint, DeviceEndpoint)) is False:
			raise TypeError('choice must be of type: PortEndpoint, DeviceEndpoint')
		self.__setattr__('choice', Endpoint._CHOICE_MAP[type(choice).__name__])
		self.__setattr__(Endpoint._CHOICE_MAP[type(choice).__name__], choice)


class PortEndpoint(object):
	"""Flow.PortEndpoint class

	An endpoint that contains a transmit port and 0..n receive ports.

	Args
	----
	- tx_port (Union[str, type(None)]): The unique name of a port that is the transmit port.
	- rx_ports (Union[list[Union[str, type(None)]], type(None)]): The unique names of ports that are the intended receive ports.
	- tx_patterns (Union[list[Union[PortPattern, type(None)]], type(None)]): A list of custom patterns that will be applied to the transmit port.
	"""
	def __init__(self, tx_port=None, rx_ports=None, tx_patterns=None):
		if isinstance(tx_port, (str, type(None))) is True:
			self.tx_port = tx_port
		else:
			raise TypeError('tx_port must be an instance of (str, type(None))')
		if isinstance(rx_ports, (list, type(None))) is True:
			self.rx_ports = rx_ports
		else:
			raise TypeError('rx_ports must be an instance of (list, type(None))')
		if isinstance(tx_patterns, (list, type(None))) is True:
			self.tx_patterns = tx_patterns
		else:
			raise TypeError('tx_patterns must be an instance of (list, type(None))')


class DeviceEndpoint(object):
	"""Flow.DeviceEndpoint class

	An endpoint that contains 1..n emulated transmit devices and 1..n  emulated receive devices.

	Args
	----
	- tx_devices (Union[list[Union[str, type(None)]], type(None)]): The unique names of devices that will be transmitting.
	- rx_devices (Union[list[Union[str, type(None)]], type(None)]): The unique names of devices that will be receiving.
	- packet_encap (Union[str, type(None)]): The encapsulation determines what packet headers will be  included by default.
	- src_dst_mesh (Union[str, type(None)]): TBD
	- route_host_mesh (Union[str, type(None)]): TBD
	- bi_directional (None): TBD
	- allow_self_destined (None): TBD
	"""
	def __init__(self, tx_devices=None, rx_devices=None, packet_encap=None, src_dst_mesh=None, route_host_mesh=None, bi_directional=None, allow_self_destined=None):
		if isinstance(tx_devices, (list, type(None))) is True:
			self.tx_devices = tx_devices
		else:
			raise TypeError('tx_devices must be an instance of (list, type(None))')
		if isinstance(rx_devices, (list, type(None))) is True:
			self.rx_devices = rx_devices
		else:
			raise TypeError('rx_devices must be an instance of (list, type(None))')
		if isinstance(packet_encap, (str, type(None))) is True:
			self.packet_encap = packet_encap
		else:
			raise TypeError('packet_encap must be an instance of (str, type(None))')
		if isinstance(src_dst_mesh, (str, type(None))) is True:
			self.src_dst_mesh = src_dst_mesh
		else:
			raise TypeError('src_dst_mesh must be an instance of (str, type(None))')
		if isinstance(route_host_mesh, (str, type(None))) is True:
			self.route_host_mesh = route_host_mesh
		else:
			raise TypeError('route_host_mesh must be an instance of (str, type(None))')
		if isinstance(bi_directional, None) is True:
			self.bi_directional = bi_directional
		else:
			raise TypeError('bi_directional must be an instance of None')
		if isinstance(allow_self_destined, None) is True:
			self.allow_self_destined = allow_self_destined
		else:
			raise TypeError('allow_self_destined must be an instance of None')


class PortPattern(object):
	"""Flow.PortPattern class

	A pattern that is applied to a test port
	The name of the pattern will be reflected in the port results.

	Args
	----
	- name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
	- offset (Union[float, int, type(None)]): The offset from the beginning of the packet
	- pattern (Union[str, type(None)]): The value of the pattern
	- mask (Union[str, type(None)]): The mask value to be applied against the pattern
	"""
	def __init__(self, name=None, offset=None, pattern=None, mask=None):
		if isinstance(name, (str, type(None))) is True:
			self.name = name
		else:
			raise TypeError('name must be an instance of (str, type(None))')
		if isinstance(offset, (float, int, type(None))) is True:
			self.offset = offset
		else:
			raise TypeError('offset must be an instance of (float, int, type(None))')
		if isinstance(pattern, (str, type(None))) is True:
			self.pattern = pattern
		else:
			raise TypeError('pattern must be an instance of (str, type(None))')
		if isinstance(mask, (str, type(None))) is True:
			self.mask = mask
		else:
			raise TypeError('mask must be an instance of (str, type(None))')


class Header(object):
	"""Flow.Header class

	Container for all traffic packet headers

	Args
	----
	- choice (Union[str, type(None)]): TBD
	- custom (Union[Custom, type(None)]): Custom packet header
	- ethernet (Union[Ethernet, type(None)]): Ethernet packet header
	- vlan (Union[Vlan, type(None)]): Vlan packet header
	- ipv4 (Union[Ipv4, type(None)]): Ipv4 packet header
	- pfcpause (Union[PfcPause, type(None)]): PFC Pause packet header
	- group_by (Union[list[Union[GroupBy, type(None)]], type(None)]): TBD
	"""
	_CHOICE_MAP = {
		'Custom': 'custom',
		'Ethernet': 'ethernet',
		'Vlan': 'vlan',
		'Ipv4': 'ipv4',
		'PfcPause': 'pfcpause',
	}
	def __init__(self, choice):
		from abstract_open_traffic_generator.flow import Custom
		from abstract_open_traffic_generator.flow import Ethernet
		from abstract_open_traffic_generator.flow import Vlan
		from abstract_open_traffic_generator.flow import Ipv4
		from abstract_open_traffic_generator.flow import PfcPause
		if isinstance(choice, (Custom, Ethernet, Vlan, Ipv4, PfcPause)) is False:
			raise TypeError('choice must be of type: Custom, Ethernet, Vlan, Ipv4, PfcPause')
		self.__setattr__('choice', Header._CHOICE_MAP[type(choice).__name__])
		self.__setattr__(Header._CHOICE_MAP[type(choice).__name__], choice)


class Custom(object):
	"""Flow.Custom class

	Custom packet header

	Args
	----
	- bytes (Union[str, type(None)]): A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs  such as scapy, wireshark, pcap etc.
An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'
	- patterns (Union[list[Union[BitPattern, type(None)]], type(None)]): Modify the bytes with bit based patterns
	"""
	def __init__(self, bytes=None, patterns=None):
		if isinstance(bytes, (str, type(None))) is True:
			self.bytes = bytes
		else:
			raise TypeError('bytes must be an instance of (str, type(None))')
		if isinstance(patterns, (list, type(None))) is True:
			self.patterns = patterns
		else:
			raise TypeError('patterns must be an instance of (list, type(None))')


class BitPattern(object):
	"""Flow.BitPattern class

	Container for a bit pattern

	Args
	----
	- choice (Union[str, type(None)]): TBD
	- bitlist (Union[BitList, type(None)]): A pattern which is a list of values.
	- bitcounter (Union[BitCounter, type(None)]): An incrementing pattern
	"""
	_CHOICE_MAP = {
		'BitList': 'bitlist',
		'BitCounter': 'bitcounter',
	}
	def __init__(self, choice):
		from abstract_open_traffic_generator.flow import BitList
		from abstract_open_traffic_generator.flow import BitCounter
		if isinstance(choice, (BitList, BitCounter)) is False:
			raise TypeError('choice must be of type: BitList, BitCounter')
		self.__setattr__('choice', BitPattern._CHOICE_MAP[type(choice).__name__])
		self.__setattr__(BitPattern._CHOICE_MAP[type(choice).__name__], choice)


class BitList(object):
	"""Flow.BitList class

	A pattern which is a list of values.

	Args
	----
	- offset (Union[float, int, type(None)]): Bit offset in the packet at which the pattern will be applied
	- length (Union[float, int, type(None)]): The number of bits in the packet that the pattern will span
	- count (Union[float, int, type(None)]): The number of values to generate before repeating
	- values (Union[list[Union[str, type(None)]], type(None)]): TBD
	"""
	def __init__(self, offset=None, length=None, count=None, values=None):
		if isinstance(offset, (float, int, type(None))) is True:
			self.offset = offset
		else:
			raise TypeError('offset must be an instance of (float, int, type(None))')
		if isinstance(length, (float, int, type(None))) is True:
			self.length = length
		else:
			raise TypeError('length must be an instance of (float, int, type(None))')
		if isinstance(count, (float, int, type(None))) is True:
			self.count = count
		else:
			raise TypeError('count must be an instance of (float, int, type(None))')
		if isinstance(values, (list, type(None))) is True:
			self.values = values
		else:
			raise TypeError('values must be an instance of (list, type(None))')


class BitCounter(object):
	"""Flow.BitCounter class

	An incrementing pattern

	Args
	----
	- offset (Union[float, int, type(None)]): Bit offset in the packet at which the pattern will be applied
	- length (Union[float, int, type(None)]): The number of bits in the packet that the pattern will span
	- count (Union[float, int, type(None)]): The number of values to generate before repeating A value of 0 means the pattern will count continuously
	- start (Union[str, type(None)]): The starting value of the pattern. If the value is greater than the length it will be truncated.
	- step (Union[str, type(None)]): The amount the start value will be incremented by If the value is greater than the length it will be truncated.
	"""
	def __init__(self, offset=None, length=None, count=None, start=None, step=None):
		if isinstance(offset, (float, int, type(None))) is True:
			self.offset = offset
		else:
			raise TypeError('offset must be an instance of (float, int, type(None))')
		if isinstance(length, (float, int, type(None))) is True:
			self.length = length
		else:
			raise TypeError('length must be an instance of (float, int, type(None))')
		if isinstance(count, (float, int, type(None))) is True:
			self.count = count
		else:
			raise TypeError('count must be an instance of (float, int, type(None))')
		if isinstance(start, (str, type(None))) is True:
			self.start = start
		else:
			raise TypeError('start must be an instance of (str, type(None))')
		if isinstance(step, (str, type(None))) is True:
			self.step = step
		else:
			raise TypeError('step must be an instance of (str, type(None))')


class Ethernet(object):
	"""Flow.Ethernet class

	Ethernet packet header

	Args
	----
	- dst (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- src (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- ether_type (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	"""
	def __init__(self, dst=None, src=None, ether_type=None):
		from abstract_open_traffic_generator.flow import Pattern
		if isinstance(dst, (Pattern, type(None))) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be an instance of (Pattern, type(None))')
		if isinstance(src, (Pattern, type(None))) is True:
			self.src = src
		else:
			raise TypeError('src must be an instance of (Pattern, type(None))')
		if isinstance(ether_type, (Pattern, type(None))) is True:
			self.ether_type = ether_type
		else:
			raise TypeError('ether_type must be an instance of (Pattern, type(None))')


class Pattern(object):
	"""Flow.Pattern class

	A container for packet header field patterns
	Possible patterns are fixed, list, increment, decrement, random.

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
		from abstract_open_traffic_generator.flow import Increment
		from abstract_open_traffic_generator.flow import Decrement
		from abstract_open_traffic_generator.flow import Random
		if isinstance(choice, (str, list, Increment, Decrement, Random)) is False:
			raise TypeError('choice must be of type: str, list, Increment, Decrement, Random')
		self.__setattr__('choice', Pattern._CHOICE_MAP[type(choice).__name__])
		self.__setattr__(Pattern._CHOICE_MAP[type(choice).__name__], choice)


class Increment(object):
	"""Flow.Increment class

	An incrementing pattern.

	Args
	----
	- start (Union[str, type(None)]): TBD
	- step (Union[str, type(None)]): TBD
	- count (Union[float, int, type(None)]): TBD
	"""
	def __init__(self, start=None, step=None, count=None):
		if isinstance(start, (str, type(None))) is True:
			self.start = start
		else:
			raise TypeError('start must be an instance of (str, type(None))')
		if isinstance(step, (str, type(None))) is True:
			self.step = step
		else:
			raise TypeError('step must be an instance of (str, type(None))')
		if isinstance(count, (float, int, type(None))) is True:
			self.count = count
		else:
			raise TypeError('count must be an instance of (float, int, type(None))')


class Decrement(object):
	"""Flow.Decrement class

	A decrementing pattern.

	Args
	----
	- start (Union[str, type(None)]): TBD
	- step (Union[str, type(None)]): TBD
	- count (Union[float, int, type(None)]): TBD
	"""
	def __init__(self, start=None, step=None, count=None):
		if isinstance(start, (str, type(None))) is True:
			self.start = start
		else:
			raise TypeError('start must be an instance of (str, type(None))')
		if isinstance(step, (str, type(None))) is True:
			self.step = step
		else:
			raise TypeError('step must be an instance of (str, type(None))')
		if isinstance(count, (float, int, type(None))) is True:
			self.count = count
		else:
			raise TypeError('count must be an instance of (float, int, type(None))')


class Random(object):
	"""Flow.Random class

	A repeatable random range pattern.

	Args
	----
	- min (Union[str, type(None)]): TBD
	- max (Union[str, type(None)]): TBD
	- step (Union[float, int, type(None)]): TBD
	- seed (Union[str, type(None)]): TBD
	- count (Union[float, int, type(None)]): TBD
	"""
	def __init__(self, min=None, max=None, step=None, seed=None, count=None):
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
		if isinstance(count, (float, int, type(None))) is True:
			self.count = count
		else:
			raise TypeError('count must be an instance of (float, int, type(None))')


class Vlan(object):
	"""Flow.Vlan class

	Vlan packet header

	Args
	----
	- priority (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- cfi (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- id (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- protocol (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	"""
	def __init__(self, priority=None, cfi=None, id=None, protocol=None):
		from abstract_open_traffic_generator.flow import Pattern
		if isinstance(priority, (Pattern, type(None))) is True:
			self.priority = priority
		else:
			raise TypeError('priority must be an instance of (Pattern, type(None))')
		if isinstance(cfi, (Pattern, type(None))) is True:
			self.cfi = cfi
		else:
			raise TypeError('cfi must be an instance of (Pattern, type(None))')
		if isinstance(id, (Pattern, type(None))) is True:
			self.id = id
		else:
			raise TypeError('id must be an instance of (Pattern, type(None))')
		if isinstance(protocol, (Pattern, type(None))) is True:
			self.protocol = protocol
		else:
			raise TypeError('protocol must be an instance of (Pattern, type(None))')


class Ipv4(object):
	"""Flow.Ipv4 class

	Ipv4 packet header

	Args
	----
	- priority (Union[Priority, type(None)]): Ipv4 ip priority that can be one of RAW or DSCP.
	- src (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- dst (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	"""
	def __init__(self, priority=None, src=None, dst=None):
		from abstract_open_traffic_generator.flow_ipv4 import Priority
		from abstract_open_traffic_generator.flow import Pattern
		if isinstance(priority, (Priority, type(None))) is True:
			self.priority = priority
		else:
			raise TypeError('priority must be an instance of (Priority, type(None))')
		if isinstance(src, (Pattern, type(None))) is True:
			self.src = src
		else:
			raise TypeError('src must be an instance of (Pattern, type(None))')
		if isinstance(dst, (Pattern, type(None))) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be an instance of (Pattern, type(None))')


class PfcPause(object):
	"""Flow.PfcPause class

	PFC Pause packet header

	Args
	----
	- dst (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- src (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- ether_type (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- control_op_code (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- priority_enable_vector (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_0 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_1 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_2 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_3 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_4 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_5 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_6 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	- pfc_queue_7 (Union[Pattern, type(None)]): A container for packet header field patterns. Possible patterns are fixed, list, increment, decrement, random.
	"""
	def __init__(self, dst=None, src=None, ether_type=None, control_op_code=None, priority_enable_vector=None, pfc_queue_0=None, pfc_queue_1=None, pfc_queue_2=None, pfc_queue_3=None, pfc_queue_4=None, pfc_queue_5=None, pfc_queue_6=None, pfc_queue_7=None):
		from abstract_open_traffic_generator.flow import Pattern
		if isinstance(dst, (Pattern, type(None))) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be an instance of (Pattern, type(None))')
		if isinstance(src, (Pattern, type(None))) is True:
			self.src = src
		else:
			raise TypeError('src must be an instance of (Pattern, type(None))')
		if isinstance(ether_type, (Pattern, type(None))) is True:
			self.ether_type = ether_type
		else:
			raise TypeError('ether_type must be an instance of (Pattern, type(None))')
		if isinstance(control_op_code, (Pattern, type(None))) is True:
			self.control_op_code = control_op_code
		else:
			raise TypeError('control_op_code must be an instance of (Pattern, type(None))')
		if isinstance(priority_enable_vector, (Pattern, type(None))) is True:
			self.priority_enable_vector = priority_enable_vector
		else:
			raise TypeError('priority_enable_vector must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_0, (Pattern, type(None))) is True:
			self.pfc_queue_0 = pfc_queue_0
		else:
			raise TypeError('pfc_queue_0 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_1, (Pattern, type(None))) is True:
			self.pfc_queue_1 = pfc_queue_1
		else:
			raise TypeError('pfc_queue_1 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_2, (Pattern, type(None))) is True:
			self.pfc_queue_2 = pfc_queue_2
		else:
			raise TypeError('pfc_queue_2 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_3, (Pattern, type(None))) is True:
			self.pfc_queue_3 = pfc_queue_3
		else:
			raise TypeError('pfc_queue_3 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_4, (Pattern, type(None))) is True:
			self.pfc_queue_4 = pfc_queue_4
		else:
			raise TypeError('pfc_queue_4 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_5, (Pattern, type(None))) is True:
			self.pfc_queue_5 = pfc_queue_5
		else:
			raise TypeError('pfc_queue_5 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_6, (Pattern, type(None))) is True:
			self.pfc_queue_6 = pfc_queue_6
		else:
			raise TypeError('pfc_queue_6 must be an instance of (Pattern, type(None))')
		if isinstance(pfc_queue_7, (Pattern, type(None))) is True:
			self.pfc_queue_7 = pfc_queue_7
		else:
			raise TypeError('pfc_queue_7 must be an instance of (Pattern, type(None))')


class GroupBy(object):
	"""Flow.GroupBy class

	Group results 

	Args
	----
	- field (Union[str, type(None)]): TBD
	- label (Union[str, type(None)]): TBD
	"""
	def __init__(self, field=None, label=None):
		if isinstance(field, (str, type(None))) is True:
			self.field = field
		else:
			raise TypeError('field must be an instance of (str, type(None))')
		if isinstance(label, (str, type(None))) is True:
			self.label = label
		else:
			raise TypeError('label must be an instance of (str, type(None))')


class Size(object):
	"""Flow.Size class

	The frame size which overrides the total length of the packet

	Args
	----
	- choice (Union[str, type(None)]): TBD
	- fixed (Union[float, int, type(None)]): TBD
	- increment (Union[SizeIncrement, type(None)]): Frame size that increments from a starting size to  an ending size incrementing by a step size.
	- random (Union[SizeRandom, type(None)]): Random frame size from a min value to a max value.
	"""
	_CHOICE_MAP = {
		'float': 'fixed',
		'int': 'fixed',
		'SizeIncrement': 'increment',
		'SizeRandom': 'random',
	}
	def __init__(self, choice):
		from abstract_open_traffic_generator.flow import SizeIncrement
		from abstract_open_traffic_generator.flow import SizeRandom
		if isinstance(choice, (float, int, SizeIncrement, SizeRandom)) is False:
			raise TypeError('choice must be of type: float, int, SizeIncrement, SizeRandom')
		self.__setattr__('choice', Size._CHOICE_MAP[type(choice).__name__])
		self.__setattr__(Size._CHOICE_MAP[type(choice).__name__], choice)


class SizeIncrement(object):
	"""Flow.SizeIncrement class

	Frame size that increments from a starting size to  an ending size incrementing by a step size.

	Args
	----
	- start (Union[float, int, type(None)]): Starting frame size in bytes
	- end (Union[float, int, type(None)]): Ending frame size in bytes
	- step (Union[float, int, type(None)]): Step frame size in bytes
	"""
	def __init__(self, start=None, end=None, step=None):
		if isinstance(start, (float, int, type(None))) is True:
			self.start = start
		else:
			raise TypeError('start must be an instance of (float, int, type(None))')
		if isinstance(end, (float, int, type(None))) is True:
			self.end = end
		else:
			raise TypeError('end must be an instance of (float, int, type(None))')
		if isinstance(step, (float, int, type(None))) is True:
			self.step = step
		else:
			raise TypeError('step must be an instance of (float, int, type(None))')


class SizeRandom(object):
	"""Flow.SizeRandom class

	Random frame size from a min value to a max value.

	Args
	----
	- min (Union[float, int, type(None)]): TBD
	- max (Union[float, int, type(None)]): TBD
	"""
	def __init__(self, min=None, max=None):
		if isinstance(min, (float, int, type(None))) is True:
			self.min = min
		else:
			raise TypeError('min must be an instance of (float, int, type(None))')
		if isinstance(max, (float, int, type(None))) is True:
			self.max = max
		else:
			raise TypeError('max must be an instance of (float, int, type(None))')


class Rate(object):
	"""Flow.Rate class

	The rate of packet transmission

	Args
	----
	- unit (Union[str, type(None)]): The value is a unit of this.
	- value (Union[float, int, type(None)]): The actual rate.
	"""
	def __init__(self, unit=None, value=None):
		if isinstance(unit, (str, type(None))) is True:
			self.unit = unit
		else:
			raise TypeError('unit must be an instance of (str, type(None))')
		if isinstance(value, (float, int, type(None))) is True:
			self.value = value
		else:
			raise TypeError('value must be an instance of (float, int, type(None))')
