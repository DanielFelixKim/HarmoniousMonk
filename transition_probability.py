from xml_parser import extract_chords, extract_key
from chord import Chord, KEY_ROOTS, ROOT_NUM, get_all_chords, ROOTS
import numpy as np
import collections 
import os 
# TUNES = ['stablemates.xml', 'along_came_betty.xml', 'it_could_happen_to_you.xml', 'alone_together.xml', 
# 'there_will_never_be_another_you.xml' , 'on_green_dolphin_street.xml', 'four.xml', 'i_love_you.xml']

TUNES = []
path = 'C:/Users/danie/Documents/GitHub/JazzHarm/src/jazz_standards'
for tune in os.listdir(path):
    if not tune.endswith('.xml'): continue
    tune = os.path.join(path, tune)
    TUNES.append(tune)

ALL_CHORDS = get_all_chords()

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
		print tune, tune_chords
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

def chord_tone_prob(chord):
	chord_tone = collections.namedtuple('chord_tone', 'root index third_off third_prob fifth_off fifth_prob seventh_off seventh_prob ninth_off ninth_prob')
	if 'maj7' in chord and 'mmaj7' not in chord:
		return chord_tone(.3, -4, 4, .2, 1, .3, 5, .1 , 2, .1)

	elif '6' in chord and 'm6' not in chord:
		return chord_tone(.3, -1, 4, .2, 1, .3, 3, .1 , 2, .1)

	elif 'm6' in chord:
		return chord_tone(.3, -2, 9, .2, 1, .3, 8, .1 , 2, .1)

	elif 'm7' in chord and 'm7b5' not in chord and 'dim7' not in chord:
		return chord_tone(.3, -2, 9, .2, 1, .3, 10, .1 , 2, .1)

	elif 'mmaj7' in chord:
		return chord_tone(.3, -5, 9, .2, 1, .3, 5, .1 , 2, .1)

	elif '7' in chord and len(chord) <= 3 and 'm7' not in chord:
		return chord_tone(.3, -1, 4, .2, 6, .3, 10, .1 , 7, .1)

	elif '7#5' in chord:
		return chord_tone(.3, -3, 4, .2, 8, .3, 10, .1 , 7, .1)

	elif '7#11' in chord:
		return chord_tone(.3, -4, 4, .2, 6, .3, 10, .1 , 7, .1)

	elif '7b13' in chord:
		return chord_tone(.3, -4, 4, .2, 8, .3, 10, .1 , 7, .1)

	elif '7alt' in chord:
		return chord_tone(.3, -4, 4, .2, 6, .3, 10, .1 , 7, .1)

	elif '7b9' in chord:
		return chord_tone(.3, -3, 4, .2, 6, .3, 10, .1 , 7, .1)

	elif '7#9' in chord:
		return chord_tone(.3, -3, 4, .2, 6, .3, 10, .1 , 9, .1)

	elif 'dim7' in chord:
		return chord_tone(.3, -4, 9, .3, 6, .3, 3, .1 , 7, 0)

	elif 'm7b5' in chord:
		return chord_tone(.3, -4, 9, .3, 6, .3, 10, .1 , 2, .1)



def emit_prob():
	chord_tone_prob_dict = {}
	for chord in ALL_CHORDS:
		if 'F#' in chord:
			chord = chord.replace('F#', 'Gb')
		chord_tone_info = chord_tone_prob(chord)
		sub_chord_tone_dict = {}
		root = chord[:chord_tone_info.index]
		sub_chord_tone_dict[root] = chord_tone_info.root
		root_num = ROOT_NUM[root]
		third = (root_num + chord_tone_info.third_off) %12
		third = KEY_ROOTS['C_' + str(third)]
		sub_chord_tone_dict[third] = chord_tone_info.third_prob
		fifth = (root_num + chord_tone_info.fifth_off) % 12
		fifth = KEY_ROOTS['C_' + str(fifth)]
		sub_chord_tone_dict[fifth] = chord_tone_info.fifth_prob
		seventh =(root_num + chord_tone_info.seventh_off) % 12
		seventh = KEY_ROOTS['C_' + str(seventh)]
		sub_chord_tone_dict[seventh] = chord_tone_info.seventh_prob
		ninth = (root_num + chord_tone_info.ninth_off) % 12
		ninth = KEY_ROOTS['C_' + str(ninth)]
		sub_chord_tone_dict[ninth] = chord_tone_info.ninth_prob
		for root in ROOTS:
			if root not in sub_chord_tone_dict:
				sub_chord_tone_dict[root] = 0
		chord_tone_prob_dict[chord] = sub_chord_tone_dict		
	return chord_tone_prob_dict

"""Test"""
chord_1 = 'Cmaj7'
chord_2 = 'Dm7b5'
chord_probs=tunes_chord_probs()
chord_prob=chord_prob(chord_1,chord_2,chord_probs)
start_prob = starting_probability_array()
start_prob_dict = starting_probability_dict(start_prob)
chord_start = 'Dm7b5'
starting_chord_prob = find_start_prob(chord_start, start_prob)
print 'The probability of a tune starting on ', chord_start, ' is ', starting_chord_prob
print 'The probability of ', chord_1, ' going to ', chord_2, ' is ', chord_prob


prob_dict = probability_dictionary(chord_probs)
#print ALL_CHORDS

print 'The probability of ', chord_1, ' going to ', chord_2, ' is ', prob_dict[chord_1][chord_2]

emmit = emit_prob()

#print emmit