from xml_parser import extract_chords, extract_key
import chord
import numpy as np

TUNES = ['there_will_never_be_another_you.xml', 'four.xml',
 'on_green_dolphin_street.xml', 'it_could_happen_to_you.xml']

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

def find_starting_probability(tunes=TUNES):
	first_chords = []
	for tune in tunes:
		key, key_quality = extract_key(tune)
		tune_chords = extract_chords(tune, key)
		first_chords.append(tune_chords[0])
	return first_chords

def chord_prob(chord_1, chord_2, probability_matrix):
	y_index = ALL_CHORDS.index(chord_1)
	x_index = ALL_CHORDS.index(chord_2)
	return probability_matrix[y_index,x_index]

"""Test"""
chord_1 = 'Cmaj7'
chord_2 = 'Ebm7'
chord_probs=tunes_chord_probs()
chord_prob=chord_prob(chord_1,chord_2,chord_probs)
first_chords = find_starting_probability()
print first_chords
print 'The probability of ', chord_1, ' going to ', chord_2, ' is ', chord_prob

key,key_quality = extract_key('there_will_never_be_another_you.xml')
print key, key_quality