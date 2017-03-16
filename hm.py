import sys, librosa, transcribe, IPython
import transition_probability as tp
import viterbi as vt
import numpy as np
from aubio import source
from IPython.display import Audio
import scipy.io.wavfile

from collections import Counter


def setup():
	states = tp.ALL_CHORDS
	start_p = tp.start_prob_dict
	trans_p = tp.prob_dict
	emit_p = tp.emmit
	return states, start_p, trans_p, emit_p

def wavwrite(filepath, data, sr, norm=True, dtype='int16',):
    if norm:
        data /= np.max(np.abs(data))
    data = data * np.iinfo(dtype).max
    data = data.astype(dtype)
    scipy.io.wavfile.write(filepath, sr, data)

def harmonious(melody, source, samplerate, window_size, hop_size, tolerance):
	notes, times = transcribe.pitchtracker(melody, source, samplerate, window_size, hop_size, tolerance)
	chords = vt.viterbi(notes, states, start_p, trans_p, emit_p)
	melody, samplerate = librosa.load(melody, sr=samplerate, duration=15)
	time_start = times[0]
	time_end = times[1]
	chord_length = time_end - time_start
	chord_add = 'chords/' + chords[0] + '.wav'
	for index, chord in enumerate(chords):
		if '7#5'in chord:
			chord = chord.replace('7#5', '7alt')
		elif '7b9'in chord:
			chord = chord.replace('7b9', '7alt')
		chord_add = 'chords/' + chord + '.wav'
		harmonization, samplerate = librosa.load(chord_add, sr=samplerate, duration=4)
		time_start = times[index]
		if (index+1 < len(times)):
			time_end = times[index+1]
		else: 
			time_end = len(melody)
		chord_length = time_end - time_start
		melody[time_start:time_end] += harmonization[:chord_length]
	wavwrite('harmonized.wav', melody, samplerate)
	return chords, notes, times, melody




filename = 'CBDC.wav'
win_s = 4096 
hop_s = 512 
samplerate = 44100
tol = .8
s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
states, start_p, trans_p, emit_p = setup()
chords, notes, times, harmonized = harmonious('Speech.wav', s, samplerate, win_s, hop_s, tol)
print "These are the notes", notes
print "These are the chords", chords