import xml.etree.ElementTree

class configReader:
	def __init__(self, path):
		self._cfg_path = path
		self._raw_data_path = None
		self._max_phrase_length = 0
		self._proxys = list()

	def load_config(self):
		cfg_tree = xml.etree.ElementTree.parse(self._cfg_path)
		cfg_root = cfg_tree.getroot()
		tmp_node = cfg_root.find('phrase')
		if (tmp_node is None) or (tmp_node.get('max_length') is None): return -1
		self._max_phrase_length = int(tmp_node.get('max_length'))
		tmp_node = cfg_root.find('raw_data')
		if (tmp_node is None) or (tmp_node.get('path') is None): return -1
		self._raw_data_path = tmp_node.get('path')
		proxys = cfg_root.findall('./proxy_list/proxy')
		if proxys is None or len(proxys) == 0: return -1
		for proxy in proxys:
			self._proxys.append([proxy.get('ip'), int(proxy.get('port'))])

		return 0

	def max_phrase_length(self):
		return self._max_phrase_length

	def raw_data_path(self):
		return self._raw_data_path

	def get_proxy(self, idx):
		return self._proxys[idx]

	def get_proxys(self):
		return self._proxys

	def get_proxy_num(self):
		return len(self._proxys)
