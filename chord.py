ROOTS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
QUALITIES = ['maj7', 'm7', '7', 'm7b5', 'dim7', '7alt', '7b9', '7#11', '6']

def get_all_chords():	
	CHORDS = []
	for root in ROOTS:
		for quality in QUALITIES:
			chord = root + quality
			CHORDS.append(chord)
	return CHORDS

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

	def __repr__(self):
		if self.extension == None: 
			return str(self.root) + str(self.quality)
		return str(self.root) + str(self.quality) + str(self.extension)
	# def transpose(self, root):
	# 	transposition = ROOTS.index(self.root) - ROOTS.index(root)
	# 	new_root_index = ROOTS.index(self.root) + transposition
	# 	self.root = ROOTS[new_root_index]
