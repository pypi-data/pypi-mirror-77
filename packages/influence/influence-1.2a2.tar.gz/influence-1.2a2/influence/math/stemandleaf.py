from influence.dict.idict import InsertableDict as IDict
class StemLeaf(dict):
	def __init__(self):
		self.__dict = IDict()
	def plot(self, stem, leaf):
		if stem not in self.__dict.keys():
			index = 0
			for k in self.__dict.keys():
				if k > stem:
					break
				index += 1
			self.__dict.insert(index, stem, [leaf])
		else:
			l = self.__dict[stem]
			l.append(leaf)
			l.sort()
			self.__dict[stem] = l
	def remove(self, stem, leaf):
		if stem not in self.__dict.keys():
			raise NoStemError
		elif leaf not in self.__dict[stem]:
			raise NoLeafError
		else:
			self.__dict[stem].remove(leaf)
	def __str__(self):
		string = ''
		for key in self.__dict.keys():
			string += f'{key}: '
			for i in self.__dict[key]:
				string += f'{i} '
			string += '\n'
		return string
	def empty(self):
		return len(self.__dict) == 0

class NoStemError(Exception):
	def __str__(self):
		return 'stem could not be found in plot'

class NoLeafError(Exception):
	def __str__(self):
		return 'leaf not found in stem'