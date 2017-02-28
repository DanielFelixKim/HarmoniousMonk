ROOTS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


class Chord(object):
	"""A Chord has the following properties:
	Attributes:
		root: A string identifying the root of the chord including the accidental
			e.g. "Eb", "A", "F#".
		quality: A string identifying the quality of the chord, including seventh chords
			e.g. "maj", "maj7".
		extension: An optional string identifying the extensions of a chord
			e.g. "13", "b9#9#11", "6/9".
	"""
	def __init__(self, root, quality, extension=None):
		self.root = root
		self.quality = quality
		self.extension = extension

	# def transpose(self, root):
	# 	transposition = ROOTS.index(self.root) - ROOTS.index(root)
	# 	new_root_index = ROOTS.index(self.root) + transposition
	# 	self.root = ROOTS[new_root_index]
