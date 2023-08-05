

class Priority(object):
	"""Flow.Ipv4.Priority class

	Ipv4 ip priority that can be one of RAW or DSCP.

	Args
	----
	- choice (Union[str, type(None)]): TBD
	- dscp (Union[Dscp, type(None)]): TBD
	- raw (Union[NumberPattern, type(None)]): TBD
	"""
	_CHOICE_MAP = {
		'Dscp': 'dscp',
		'NumberPattern': 'raw',
	}
	def __init__(self, choice):
		from abstract_open_traffic_generator.flow_ipv4 import Dscp
		from abstract_open_traffic_generator.flow import NumberPattern
		if isinstance(choice, (Dscp, NumberPattern)) is False:
			raise TypeError('choice must be of type: Dscp, NumberPattern')
		self.__setattr__('choice', Priority._CHOICE_MAP[type(choice).__name__])
		self.__setattr__(Priority._CHOICE_MAP[type(choice).__name__], choice)


class Dscp(object):
	"""Flow.Ipv4.Dscp class

	Differentiated services code point (DSCP) packet field.
	PHB (per-hop-behavior) value is 6 bits: >=0 PHB <=63
	ECN (explicit-congestion-notification) value is 2 bits: >=0 ECN <=3

	Args
	----
	- phb (Union[NumberPattern, type(None)]): TBD
	- ecn (Union[NumberPattern, type(None)]): TBD
	"""
	
	PHB_DEFAULT = 0
	PHB_CS1 = 8
	PHB_CS2 = 16
	PHB_CS3 = 24
	PHB_CS4 = 32
	PHB_CS5 = 40
	PHB_CS6 = 48
	PHB_CS7 = 56
	PHB_EF46 = 46
	PHB_AF11 = 10
	PHB_AF12 = 12
	PHB_AF13 = 14
	PHB_AF21 = 18
	PHB_AF22 = 20
	PHB_AF23 = 22
	PHB_AF31 = 26
	PHB_AF32 = 28
	PHB_AF33 = 30
	PHB_AF41 = 24
	PHB_AF42 = 36
	PHB_AF43 = 38
	ECN_NON_CAPABLE = 0
	ECN_CAPABLE_TRANSPORT_0 = 1
	ECN_CAPABLE_TRANSPORT_1 = 2
	ECN_CONGESTION_ENCOUNTERED = 3
	
	def __init__(self, phb=None, ecn=None):
		from abstract_open_traffic_generator.flow import NumberPattern
		if isinstance(phb, (NumberPattern, type(None))) is True:
			self.phb = phb
		else:
			raise TypeError('phb must be an instance of (NumberPattern, type(None))')
		if isinstance(ecn, (NumberPattern, type(None))) is True:
			self.ecn = ecn
		else:
			raise TypeError('ecn must be an instance of (NumberPattern, type(None))')
