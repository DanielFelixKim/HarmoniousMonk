from xml_parser import extract_chords, extract_key
import chord
import numpy as np

TUNES = ['there_will_never_be_another_you.xml', 'four.xml',
 'on_green_dolphin_street.xml', 'it_could_happen_to_you.xml', 'i_love_you.xml']

ALL_CHORDS = chord.get_all_chords()

"""transition_matrix is a function that takes in a list of chords from a tune and 
returns a matrix with the number of transitions from one chord to another. 
The X and Y axes are from ALL_CHORDS"""

def transition_matrix(tune_chords):
	n = len(ALL_CHORDS)
	trans_matrix = np.zeros((n, n))
	for i, chord in enumerate(tune_chords[:-1]):
		next_chord = tune_chords[i+1]
		y_index = ALL_CHORDS.index(str(chord))
		x_index = ALL_CHORDS.index(str(next_chord))
		trans_matrix[y_index, x_index] += 1
	return trans_matrix 

def probability_matrix(trans_matrices):
	prob_matrix = trans_matrices[0]
	for trans_matrix in trans_matrices[1:]:
		prob_matrix = np.add(prob_matrix, trans_matrix)
	sum_rows = np.apply_along_axis(sum, 1, prob_matrix)
	np.putmask(sum_rows, sum_rows==0, 1)
	prob_matrix = prob_matrix/sum_rows[:,None]
	return prob_matrix

def probability_dictionary(prob_matrix):
	prob_dict = {}		
	for i, chord in enumerate(ALL_CHORDS):
		dict_key = chord
		sub_chord_dict = {}
		row = prob_matrix[i,:]
		sub_chord_dict = {ALL_CHORDS[x]: prob for (x, prob) in enumerate(row)}
		dict_val = sub_chord_dict
		prob_dict[dict_key] = dict_val
	return prob_dict


def tunes_chord_probs(tunes=TUNES):
	trans_matrices = []
	for tune in tunes:
		key, key_quality = extract_key(tune)
		tune_chords = extract_chords(tune, key)
		print tune_chords
		trans_matrix = transition_matrix(tune_chords)
		trans_matrices.append(trans_matrix)
	tunes_prob_matrix = probability_matrix(trans_matrices)
	return tunes_prob_matrix

def starting_probability_array(tunes=TUNES):
	first_chords = []
	n = len(ALL_CHORDS)
	start_array = np.zeros(n)
	for tune in tunes:
		key, key_quality = extract_key(tune)
		tune_chords = extract_chords(tune, key)
		first_chords.append(tune_chords[0])
	for i, chord in enumerate(first_chords):
		chord_index = ALL_CHORDS.index(str(chord))
		start_array[chord_index] += 1
	sum_chords = np.sum(start_array)
	start_prob = [float(chord / sum_chords) for chord in start_array]
	return start_prob

def starting_probability_dict(start_prob_array):
	start_prob_dict = {ALL_CHORDS[x]: prob for (x, prob) in enumerate(start_prob_array)}
	return start_prob_dict

def find_start_prob(chord, starting_probability):
	chord_index = ALL_CHORDS.index(chord)
	return starting_probability[chord_index]

def chord_prob(chord_1, chord_2, probability_matrix):
	y_index = ALL_CHORDS.index(chord_1)
	x_index = ALL_CHORDS.index(chord_2)
	return probability_matrix[y_index,x_index]


"""Test"""
chord_1 = 'Cmaj7'
chord_2 = 'Dm7b5'
chord_probs=tunes_chord_probs()
chord_prob=chord_prob(chord_1,chord_2,chord_probs)
start_prob = starting_probability_array()
print start_prob
start_prob_dict = starting_probability_dict(start_prob)
print start_prob_dict
chord_start = 'Dm7b5'
starting_chord_prob = find_start_prob(chord_start, start_prob)
print 'The probability of a tune starting on ', chord_start, ' is ', starting_chord_prob
print 'The probability of ', chord_1, ' going to ', chord_2, ' is ', chord_prob

key,key_quality = extract_key('there_will_never_be_another_you.xml')
print key, key_quality

prob_dict = probability_dictionary(chord_probs)
#print ALL_CHORDS

print 'The probability of ', chord_1, ' going to ', chord_2, ' is ', prob_dict[chord_1][chord_2]