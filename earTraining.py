# -*- coding: utf-8 -*-
# @Time     : 2019/01/08 
# @Author   : liguibin
#

###
'''
usage: earTraining.py [-h] [-i INSTRUMENT] [-m MODE] [-r RANGE] [-k KEY]
                      [-d [DELAY]] [-s SCALE]

random generate A-G pitches and play the sound

optional arguments:
  -h, --help            show this help message and exit
  -i INSTRUMENT, --instrument INSTRUMENT
                        piano/guitar
  -m MODE, --mode MODE  note/interval/chord/scale
  -r RANGE, --range RANGE
                        Note range like C4-C5
  -k KEY, --key KEY     white/black/full
  -d [DELAY], --delay [DELAY]
                        delay secs after bee
  -s SCALE, --scale SCALE
                        C/D/E/F/G/A/B


'''

import os
import re
import sys
import time
import random
import argparse
import subprocess
from time import sleep

natrualPitches = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
twelvePitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chromaticPitches = ['C#', 'D#', 'F#', 'G#', 'A#']

pianoWhiteKeys = ['C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2', 
 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 
 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 
 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 
 'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
 'C7']
pianoBlackKeys = ['C#2', 'D#2', 'F#2', 'G#2', 'A#2', 
 'C#3', 'D#3', 'F#3', 'G#3', 'A#3', 
 'C#4', 'D#4', 'F#4', 'G#4', 'A#4', 
 'C#5', 'D#5', 'F#5', 'G#5', 'A#5', 
 'C#6', 'D#6', 'F#6', 'G#6', 'A#6']
pianoAllKeys = ['C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 
 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 
 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 
 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 
 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6',
 'C7']

natrual3Chords = [  
'C', 'Cm',   
'D', 'Dm',   
'E', 'Em',   
'F', 'Fm',   
'G', 'Gm', 
'A', 'Am',   
'B', 'Bm' ]

chromatic3Chords = [
'Ab', 'Abm', 
'Bb', 'Bbm', 
'Eb', 'Ebm', 
'F#', 'F#m' ]


intervalNames = [
'Unison',                           #0
'Minor 2nd', 'Major 2nd',           #1,2
'Minor 3rd', 'Major 3rd',           #3,4
'Perfect 4th',                      #5
'Tritone',                          #6
'Perfect 5th',                      #7
'Minor 6th', 'Major 6th',           #8,9
'Minor 7th', 'Major 7th',           #10,11
'Octave',                           #12

'Minor 9th', 'Major 9th',           #13,14
'Minor 10th', 'Major 10th',         #15,16
'Perfect 11th',                     #17
'Diminished 12th','Perfect 12th',   #18,19
'Minor 13th', 'Major 13th',         #20,21
'Minor 14th', 'Major 14th',         #22,23
'Double Octave',                    #24

]

# half pitch number of each scale
scaleDict = {
    'Natural Major' : [0,2,2,1,2,2,2,1],          #: C,D,E,F,G,A,B,C
    'Natural Minor' : [0,2,1,2,2,1,2,2],          #: C,D,Eb,F,G,Ab,Bb,C
    'Harmonic Minor' : [0,2,1,2,2,1,3,1],         #: C,D,Eb,F,G,Ab,B,C
    'Melodic Minor' : [0,2,1,2,2,2,2,1],          #: C,D,Eb,F,G,A,B,C

    'Ionian' : [0,2,2,1,2,2,2,1],                 #: C,D,E,F,G,A,B,C
    'Dorian' : [0,2,1,2,2,2,1,2],                 #: C,D,Eb,F,G,A,Bb,C
    'Phrygian' : [0,1,2,2,2,1,2,2],               #: C,Db,Eb,F,G,Ab,Bb,C
    'Lydian' : [0,2,2,2,1,2,2,1],                 #: C,D,E,F#,G,A,B,C
    'Mixolydian' : [0,2,2,1,2,2,1,2],             #: C,D,E,F,G,A,Bb,C
    'Aeolian' : [0,2,1,2,2,1,2,2],                #: C,D,Eb,F,G,Ab,Bb,C
    'Locrian' : [0,1,2,2,1,2,2,2],                #: C,Db,Eb,F,Gb,Ab,Bb,C
}

cChords = ['C', 'Dm', 'Em', 'F', 'G', 'Am']

notePath = './ogg/spell/note/'
soundPath = './ogg/pitchSound/piano/'

guitarChordPath = 'ogg/chords/guitar/'
pianoChordPath = 'ogg/chords/piano/'
chordNamePath = 'ogg/spell/chords/'
scaleNamePath = 'ogg/spell/scale/'
intervalNamePath = 'ogg/spell/interval/'


def playKeys(noteChoice):
    for noteName in noteChoice:
        musicPath = soundPath+noteName+'.ogg'
        namePath = notePath+noteName+'.ogg'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(2)

        #print('\n## Info ## : ', '----------------------', noteName, '\n')
        #p = subprocess.Popen(["mplayer", namePath], stdout=subprocess.PIPE)
        #sleep(2)

def noteTraining(args):
    print('\n##### Note Ear Training Mode, Range %s #####\n'%(args.range))

    noteRange = args.range.split('-')
    noteStart = noteRange[0]
    noteEnd = noteRange[-1]

    if args.key == 'white':
        noteList = pianoWhiteKeys
    elif args.key == 'black':
        noteList = pianoBlackKeys
    else:
        noteList = pianoAllKeys

    if noteStart not in noteList or noteEnd not in noteList:
        print('## Error :', noteStart, noteEnd, 'not in', noteList)
        sys.exit()


    noteChoice = noteList[noteList.index(noteStart):noteList.index(noteEnd)+1]
    print(noteChoice)

    playKeys(noteChoice)

    while(True):
        noteName = random.choice(noteChoice)

        musicPath = soundPath+noteName+'.ogg'
        namePath = notePath+noteName+'.ogg'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(2)

        print('\n## Info ## : ', '----------------------', noteName, '\n')
        p = subprocess.Popen(["mplayer", namePath], stdout=subprocess.PIPE)
        sleep(args.delay)



def intervalTraining(args):
    print('\n##### Interval Ear Training Mode, Range %s #####\n'%(args.range))

    noteRange = args.range.split('-')
    noteStart = noteRange[0]
    noteEnd = noteRange[-1]

    if args.key == 'white':
        noteList = pianoWhiteKeys
    elif args.key == 'black':
        noteList = pianoBlackKeys
    else:
        noteList = pianoAllKeys

    if noteStart not in noteList or noteEnd not in noteList:
        print('## Error :', noteStart, noteEnd, 'not in', noteList)
        sys.exit()

    noteChoice = noteList[noteList.index(noteStart):noteList.index(noteEnd)+1]
    print(noteChoice)

    if args.updown == 'up':
        firstChoice = noteList[noteList.index(noteStart):noteList.index(noteEnd)]
    else:
        firstChoice = noteList[noteList.index(noteStart)+1:noteList.index(noteEnd)+1]


    while(True):
        firstNote = random.choice(firstChoice)

        if args.updown == 'up':
            secondChoice = noteChoice[noteChoice.index(firstNote)+1:]
        else:
            secondChoice = noteChoice[0:noteChoice.index(firstNote)]

        #print(firstNote, secondChoice)
        secondNote = random.choice(secondChoice)

        firstMusicPath = soundPath+firstNote+'.ogg'
        secondMusicPath = soundPath+secondNote+'.ogg'

        # serial play first
        p = subprocess.Popen(["mplayer", firstMusicPath], stdout=subprocess.PIPE)
        sleep(1)
        p = subprocess.Popen(["mplayer", secondMusicPath], stdout=subprocess.PIPE)

        # parallel play
        sleep(1)
        p = subprocess.Popen(["mplayer", firstMusicPath], stdout=subprocess.PIPE)
        p = subprocess.Popen(["mplayer", secondMusicPath], stdout=subprocess.PIPE)

        halfNum = abs(pianoAllKeys.index(firstNote) - pianoAllKeys.index(secondNote))
        sleep(2)

        intervalMusicPath = intervalNamePath + intervalNames[halfNum].replace(' ','') + '.mp3'
        p = subprocess.Popen(["mplayer", intervalMusicPath], stdout=subprocess.PIPE)
        print('\n## Info ## : ', '----------------------', 
            halfNum, intervalNames[halfNum], ':', firstNote, secondNote, '\n')
        sleep(args.delay)


def playChords(chordChoice, args):
    if args.instrument == 'guitar':
        chordPath = guitarChordPath
    else:
        chordPath = pianoChordPath

    for chordName in chordChoice:
        musicPath = chordPath+chordName+'.mp3'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(5)


def chordTraining(args):
    print('\n##### Chord Ear Training Mode, Range %s #####\n'%(args.range))

    if args.instrument == 'guitar':
        chordPath = guitarChordPath
    else:
        chordPath = pianoChordPath

    if args.key == 'white':
        chordList = natrual3Chords
    elif args.key == 'black':
        chordList = chromatic3Chords
    else:
        chordList = natrual3Chords+chromatic3Chords

    if args.scale == 'C':
        chordList = cChords

    chordChoice = chordList

    print(chordChoice)

    playChords(chordChoice, args)

    while(True):
        chordName = random.choice(chordChoice)

        musicPath = chordPath+chordName+'.mp3'
        namePath = chordNamePath+chordName+'.mp3'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(5)

        print('\n## Info ## : ', '----------------------', chordName, '\n')
        p = subprocess.Popen(["mplayer", namePath], stdout=subprocess.PIPE)
        sleep(args.delay)


def scaleTraining(args):
    print('\n##### Scale Ear Training Mode, Range %s #####\n'%(args.range))

    noteRange = args.range.split('-')
    noteStart = noteRange[0]
    noteEnd = noteRange[-1]

    noteList = pianoAllKeys

    if noteStart not in noteList or noteEnd not in noteList:
        print('## Error :', noteStart, noteEnd, 'not in', noteList)
        sys.exit()


    noteChoice = noteList[noteList.index(noteStart):noteList.index(noteEnd)+1]
    scaleChoice = list(scaleDict.keys())
    print(noteChoice)

    while(True):
        firstNote = random.choice(noteChoice)
        scaleName = random.choice(scaleChoice)
        scaleSpell = scaleNamePath+scaleName.replace(' ','')+'.mp3'

        scaleStep = scaleDict[scaleName]
        scaleBuff = []
        noteName = firstNote

        for step in scaleStep:
            noteName = noteList[noteList.index(noteName)+step]
            scaleBuff.append(noteName)

            musicPath = soundPath+noteName+'.ogg'
            namePath = notePath+noteName+'.ogg'

            p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
            sleep(1)

        print('\n## Info ## : ', '----------------------', scaleName, ':', scaleBuff, '\n')
        p = subprocess.Popen(["mplayer", scaleSpell], stdout=subprocess.PIPE)
        sleep(args.delay)    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='random generate A-G pitches and play the sound')
    parser.add_argument("-i", "--instrument", default='piano', type=str, help="piano/guitar")
    parser.add_argument("-m", "--mode", default='note', type=str, help="note/interval/chord/scale")
    parser.add_argument("-r", "--range", default='C4-C5', type=str, help="Note range like C4-C5")
    parser.add_argument("-k", "--key", default='white', type=str, help="white/black/full")
    parser.add_argument("-d", "--delay", default=5, type=int, nargs='?', help="delay secs after bee")
    parser.add_argument("-s", "--scale", default='C', type=str, help="C/D/E/F/G/A/B")
    parser.add_argument("-u", "--updown", default='up', type=str, help="up/down")

    args = parser.parse_args()
    print(args)

    if args.mode == 'note':
        noteTraining(args)
    elif args.mode == 'interval':
        intervalTraining(args)
    elif args.mode == 'chord':
        chordTraining(args)
    elif args.mode == 'scale':
        scaleTraining(args)
    else:
        pass

