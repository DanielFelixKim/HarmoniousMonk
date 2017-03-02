import xml.etree.ElementTree as ET
from chord import Chord

def extract_chords(input_file):
	tree = ET.parse(input_file)
	root = tree.getroot()

	#Set root to part since measure is a child in part
	for child in root:
		if child.tag == 'part':
			root = child
			break

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
			kind = chord.find('kind')
			quality = kind.get('text')
			if quality == None: 
				quality = chord.find('kind').text
				if quality == 'diminished-seventh':
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
				elif extension == '11' and extension_alt == '1':
					extension = '#11'
				elif extension == '13' and extension_alt == '0':
					extension = '13'
				elif extension == '13' and extension_alt == '-1':
					extension = 'b13'	
			else: 
				extension = None
			chord_list.append(Chord(root_step, quality, extension))
	return chord_list

