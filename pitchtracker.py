#! /usr/bin/env python

import sys, librosa
from aubio import source, pitch
from collections import Counter


if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 1
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

pitch_o = pitch("yinfft", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

sound, sr = librosa.load(filename, samplerate)
onset_frames = librosa.onset.onset_detect(sound, sr, hop_length=hop_s, wait=((0.5 * sr) / hop_s))
#onsets = librosa.frames_to_samples(onset_frames, hop_length=hop_s)


pitches = []
confidences = []
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
pitchclass = {-1:'--', 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'}
notes = []
# total number of frames read
total_frames = 0
while True:
    samples, read = s()
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

    print("%f %f %s %f" % (total_frames / (float(samplerate)), pitch, note, confidence))
    #print("%f %s %f" % (total_frames / (float(samplerate)), note, confidence))
    pitches += [pitch]

    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

for i in range(len(onset_frames)):
	start = onset_frames[i]
	if i == len(onset_frames)-1:
		onset = notes[start:]
	else:
		stop = onset_frames[i+1]
		onset = notes[start:stop]
	main_pitch = Counter(onset)
	print main_pitch.most_common(1)
#print notes
print onset_frames

if 0: sys.exit(0)

#print pitches
import os.path
from numpy import array, ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from demo_waveform_plot import get_waveform_plot, set_xlabels_sample2time

skip = 1

pitches = array(pitches[skip:])
confidences = array(confidences[skip:])
times = [t * hop_s for t in range(len(pitches))]

fig = plt.figure()

ax1 = fig.add_subplot(311)
ax1 = get_waveform_plot(filename, samplerate = samplerate, block_size = hop_s, ax = ax1)
plt.setp(ax1.get_xticklabels(), visible = False)
ax1.set_xlabel('')

def array_from_text_file(filename, dtype = 'float'):
    filename = os.path.join(os.path.dirname(__file__), filename)
    return array([line.split() for line in open(filename).readlines()],
        dtype = dtype)

ax2 = fig.add_subplot(312, sharex = ax1)
ground_truth = os.path.splitext(filename)[0] + '.f0.Corrected'
if os.path.isfile(ground_truth):
    ground_truth = array_from_text_file(ground_truth)
    true_freqs = ground_truth[:,2]
    true_freqs = ma.masked_where(true_freqs < 2, true_freqs)
    true_times = float(samplerate) * ground_truth[:,0]
    ax2.plot(true_times, true_freqs, 'r')
    ax2.axis( ymin = 0.9 * true_freqs.min(), ymax = 1.1 * true_freqs.max() )
# plot raw pitches
ax2.plot(times, pitches, '.g')
# plot cleaned up pitches
cleaned_pitches = pitches
#cleaned_pitches = ma.masked_where(cleaned_pitches < 0, cleaned_pitches)
#cleaned_pitches = ma.masked_where(cleaned_pitches > 120, cleaned_pitches)
cleaned_pitches = ma.masked_where(confidences < tolerance, cleaned_pitches)
ax2.plot(times, cleaned_pitches, '.-')
#ax2.axis( ymin = 0.9 * cleaned_pitches.min(), ymax = 1.1 * cleaned_pitches.max() )
#ax2.axis( ymin = 55, ymax = 70 )
plt.setp(ax2.get_xticklabels(), visible = False)
ax2.set_ylabel('f0 (midi)')

# plot confidence
ax3 = fig.add_subplot(313, sharex = ax1)
# plot the confidence
ax3.plot(times, confidences)
# draw a line at tolerance
ax3.plot(times, [tolerance]*len(confidences))
ax3.axis( xmin = times[0], xmax = times[-1])
ax3.set_ylabel('condidence')
set_xlabels_sample2time(ax3, times[-1], samplerate)
plt.show()
plt.savefig(os.path.basename(filename) + '.svg')
