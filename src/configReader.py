import xml.etree.ElementTree

class configReader:
	def __init__(self, path):
		self._cfg_path = path
		self._raw_data_path = None
		self._max_phrase_length = 0

	def loadConfig(self):
		cfg_tree = xml.etree.ElementTree.parse(self._cfg_path)
		cfg_root = cfg_tree.getroot()
		tmp_node = cfg_root.find('phrase')

		if (tmp_node is None) or (tmp_node.get('max_length') is None):
			return -1

		self._max_phrase_length = int(tmp_node.get('max_length'))
		tmp_node = cfg_root.find('raw_data')

		if (tmp_node is None) or (tmp_node.get('path') is None):
			return -1

		self._raw_data_path = tmp_node.get('path')
		return 0

	def maxPhraseLength(self):
		return self._max_phtrase_length

	def rawDataPath(self):
		return self._raw_data_path
