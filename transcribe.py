#! /usr/bin/env python

import sys, librosa
from aubio import source
from collections import Counter

def pitchtracker(filename, source, samplerate, window_size, hop_size, tolerance, algorithm="yinfft", unit="midi"):
	from aubio import pitch
	pitch_o = pitch(algorithm, window_size, hop_size, samplerate)
	pitch_o.set_unit(unit)
	pitch_o.set_tolerance(tolerance)

	sound, sr = librosa.load(filename, samplerate)
	onset_frames = librosa.onset.onset_detect(sound, sr, hop_length=hop_size, wait=((0.5 * sr) / hop_size))
	onsets = librosa.frames_to_samples(onset_frames, hop_length=hop_size)
	times = librosa.frames_to_time(onset_frames, hop_length=hop_size)

	pitches = []
	confidences = []
	notes = []
	"""
	notes = {
		0:'--', 1:'C#0', 2:'D0', 3:'D#0', 4:'E0', 5:'F0', 6:'F#0', 7:'G0', 8:'G#0', 9:'A0', 10:'A#0', 11:'B0',
		12:'C1', 13:'C#1', 14:'D1', 15:'D#1', 16:'E1', 17:'F1', 18:'F#1', 19:'G1', 20:'G#1', 21:'A1', 22:'A#1', 23:'B1',
		24:'C2', 25:'C#2', 26:'D2', 27:'D#2', 28:'E2', 29:'F2', 30:'F#2', 31:'G2', 32:'G#2', 33:'A2', 34:'A#2', 35:'B2',
		36:'C3', 37:'C#3', 38:'D3', 39:'D#3', 40:'E3', 41:'F3', 42:'F#3', 43:'G3', 44:'G#3', 45:'A3', 46:'A#3', 47:'B3',
		48:'C4', 49:'C#4', 50:'D4', 51:'D#4', 52:'E4', 53:'F4', 54:'F#4', 55:'G4', 56:'G#4', 57:'A4', 58:'A#4', 59:'B4',
		60:'C5', 61:'C#5', 62:'D5', 63:'D#5', 64:'E5', 65:'F5', 66:'F#5', 67:'G5', 68:'G#5', 69:'A5', 70:'A#5', 71:'B5',
		72:'C6', 73:'C#6', 74:'D6', 75:'D#6', 76:'E6', 77:'F6', 78:'F#6', 79:'G6', 80:'G#6', 81:'A6', 82:'A#6', 83:'B6',
		84:'C7', 85:'C#7', 86:'D7', 87:'D#7', 88:'E7', 89:'F7', 90:'F#7', 91:'G7', 92:'G#7', 93:'A7', 94:'A#7', 95:'B7',
		96:'C8', 97:'C#8', 98:'D8', 99:'D#8', 100:'E8', 101:'F8', 102:'F#8', 103:'G8', 104:'G#8', 105:'A8', 106:'A#8', 107:'B8',
		108:'C9', 109:'C#9', 110:'D9', 111:'D#9', 112:'E9', 113:'F9', 114:'F#9', 115:'G9', 116:'G#9', 117:'A9', 118:'A#9', 119:'B9',
		120:'C10', 121:'C#10', 122:'D10', 123:'D#10', 124:'E10', 125:'F10', 126:'F#10', 127:'G10'
	}
	"""
	pitchclass = {-1:'--', 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
	
	# total number of frames read
	total_frames = 0
	while True:
		samples, read = source()
		pitch = pitch_o(samples)[0]
		pitch = int(round(pitch)) % 12
		confidence = pitch_o.get_confidence()
		#if confidence < 0.8: pitch = -1
		#if pitch in notes:
		#	note = notes[pitch]
		if pitch in pitchclass:
			note = pitchclass[pitch]
			notes.append(note)
		else:
			notes.append('0')

		# print("%f %f %s %f" % (total_frames / (float(samplerate)), pitch, note, confidence))
		# print("%f %s %f" % (total_frames / (float(samplerate)), note, confidence))
		pitches += [pitch]
		confidences += [confidence]
		total_frames += read
		if read < hop_size: break

	pitches_to_return = []

	for i in range(len(onset_frames)):
		start = onset_frames[i]
		if i == len(onset_frames)-1:
			onset = notes[start:]
		else:
			stop = onset_frames[i+1]
			onset = notes[start:stop]
		main_pitch = Counter(onset)
		pitches_to_return.append(main_pitch.most_common(1)[0][0])

	#print notes
	return pitches_to_return, onsets


# if __name__ == "__main__":
# 	if len(sys.argv) < 2:
# 		print("Usage: %s <filename> [samplerate]" % sys.argv[0])
# 		sys.exit(1)

# 	filename = sys.argv[1]

# 	downsample = 1
# 	samplerate = 44100 // downsample
# 	if len( sys.argv ) > 2: samplerate = int(sys.argv[2])



