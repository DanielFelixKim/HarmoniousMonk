import xml.etree.ElementTree as ET
from chord import Chord
tree = ET.parse('it_could_happen_to_you.xml')
root = tree.getroot()

#Set root to part since measure is a child in part
root = root.find ("part")

chord_list = []

for measure in root:
	chords = measure.findall('harmony')
	for chord in chords:
		chord_root = chord.find('root')
		root_step = chord_root.find('root-step').text
		root_alter = chord_root.find('root-alter').text
		if root_alter == '1':
			root_step += '#'
		elif root_alter == '-1':
			root_step += 'b'
		#Find chord qualities and convert to shorthand
		quality = chord.find('kind').text
		if quality == 'major-seventh':
			quality = 'maj7'
		elif quality == 'minor-seventh':
			quality = 'm7'
		elif quality == 'dominant':
			quality = '7'
		elif quality == 'diminished-seventh':
			quality = 'dim7'
		degree = chord.find('degree')
		if degree is not None:
			extension = degree.find('degree-value').text
			extension_alt = degree.find('degree-alter').text
			if extension == '5' and extension_alt == '-1':
				extension = 'b5'
			elif extension == '5' and extension_alt == '1':
				extension = '#5'
			elif extension == '9' and extension_alt == '-1':
				extension = 'b9'
			elif extension == '9' and extension_alt == '1':
				extension = '#9'
			elif extension == '9' and extension_alt == '0':
				extension = '9'
			print extension
		else: 
			extension = None
		chord_list.append(Chord(root_step, quality, extension))

