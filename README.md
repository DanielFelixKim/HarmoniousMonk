# Harmonious Monk
A python program that allows you to jazzify your voice.
http://harmoniousmonk.info/

A Northwestern University EECS 352 Final Project

## Team Members:
+ Daniel Felix-Kim, danielfelixkim2016@u.northwestern.edu
+ Kevin Li, kevinli2017@u.northwestern.edu
+ Michelle Carbo, michellecarbo2016@u.northwestern.edu

Instructor: Prof. Bryan Pardo

## Requirements:
Harmonious Monk (HM) currently assumes that you are comfortable with using the command line. HM runs on any OS as long as your OS can install and run the following:
+ Python (>= 2.7)
+ Numpy (>= 1.12.0)
+ Librosa (>= 0.5.0)
+ Aubio (0.4.4) and it's Python Module
+ SciPy (>= 0.9)

An easy way to check if these are installed correctly is to import them. If no errors come up, you should be good to go. 

## Installation:
Open your favorite command line interface (CLI) and navigate to a convenient folder on your computer. Run the following command:
```
$ git clone https://github.com/DanielFelixKim/HarmoniousMonk.git
```
And you're done!

**If you don't have git**, you can download the ZIP to a convenient location and unzip there.

## Usage: 
Use your favorite audio manipulation program to record a clip of your speech. Save it as a .wav file. Once that's done, save it in the folder where Harmonious Monk is.

If you don't have a favorite audio manipulation program, we recommend [Audacity](http://www.audacityteam.org/). It's free and easy!

Next open your CLI and navigate to the folder where Harmonious Monk has been installed on your computer. Run the following command: 
```
$ python hm.py your_sound_file.wav {volume} {threshold}
```
where volume is a postive float greater than 0 and threshold is a float between 0 and 1.

Congrats! Open up the folder where Harmonious Monk is to find the harmonized sound file, listen, and enjoy!



