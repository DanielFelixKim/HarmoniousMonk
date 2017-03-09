ROOTS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

QUALITIES = ['maj7', '6', 'm6', 'm7', 'mmaj7','7', 'm7b5', 'dim7', '7alt', '7b9', '7#11']

STARTING_CHORD_PROBABILITY = {'maj7', '6', 'm6', 'm7', 'mmaj7','7', 'm7b5', 'dim7', '7alt', '7b9', '7#11'}

KEY_ROOTS = {'C_0':'Gb','C_1':'Db','C_2':'Ab','C_3':'Eb','C_4':'Bb','C_5':'F',
			 'C_6': 'C', 'C_7': 'G', 'C_8': 'D', 'C_9': 'A', 'C_10': 'E', 'C_11': 'B'}

ROOT_NUM = {'Gb':'0', 'Db':'1', 'Ab':'2', 'Eb':'3', 'Bb':'4', 'F':'5', 
			'C':'6', 'G':'7', 'D':'8', 'A':'9', 'E':'10', 'B':'11'}

CHORD_TONE_PROB = {
	'Cmaj7' : {'C': 0.5, 'E': 0.2, 'G': 0.2, 'B': 0.1},
	'Dm7' : {'D': 0.1, 'F': 0.2, 'A': 0.1, 'C': 0.6},
	'G7' : {'G': 0.7, 'B': 0.1, 'D': 0.15, 'F': 0.05}
}




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
