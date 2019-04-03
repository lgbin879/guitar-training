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
pianoBlackKeys = [
 'Db2', 'Eb2', 'Gb2', 'Ab2', 'Bb2', 
 'Db3', 'Eb3', 'Gb3', 'Ab3', 'Bb3', 
 'Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4', 
 'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5', 
 'Db6', 'Eb6', 'Gb6', 'Ab6', 'Bb6'  
 ]
pianoAllKeys = [
 'C2', 'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2', 'A2', 'Bb2', 'B2', 
 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 
 'C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4', 
 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5', 
 'C6', 'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6', 'A6', 'Bb6', 'B6', 
 'C7']
'''
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
'''

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

#"3/6/46/sus2/sus4/7/56/34/2/9/11/13/15"
chordNoteDict = {
    '3' : [0,2,4],          #C4,E4,G4
    '6' : [2,4,7],          #E4,G4,C5
    '46': [4,7,9],          #G4,C5,E5
    'sus2' : [0,1,4],       #C4,E4,G4
    'sus4' : [0,3,4],       #C4,E4,G4
    '7' : [0,2,4,6],        #C4,E4,G4,B4
    '56': [2,4,6,7],        #E4,G4,B4,C5
    '34': [4,6,7,9],        #G4,B4,C5,E5
    '2' : [6,7,9,11],       #B4,C5,E5,G5
    '9' : [0,2,4,6,8],      #C4,E4,G4,B4,D5
    '11': [0,2,4,6,8,10],   #C4,E4,G4,B4,D5,F5
    '13': [0,2,4,6,8,10,12],#C4,E4,G4,B4,D5,F5,A5
}


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

majorScaleDict = {
    'C' : ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'G' : ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'D' : ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'A' : ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'E' : ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'B' : ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
    'F#' : ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
    'Gb' : ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'],
    'Db' : ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
    'Ab' : ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
    'Eb' : ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
    'Bb' : ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    'F' : ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
}

# half tone number of each scale
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

notePath = './mp3/spell/note/'
soundPath = './mp3/pitchSound/piano/'

guitarChordPath = 'mp3/chords/guitar/'
pianoChordPath = 'mp3/chords/piano/'
chordNamePath = 'mp3/spell/chords/'
scaleNamePath = 'mp3/spell/scale/'
intervalNamePath = 'mp3/spell/interval/'


def playKeys(noteChoice):
    for noteName in noteChoice:
        musicPath = soundPath+noteName+'.mp3'
        namePath = notePath+noteName+'.mp3'

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

    index = 0
    while(True):
        if args.random == 'on':
            noteName = random.choice(noteChoice)
        else:
            noteName = noteChoice[index%len(noteChoice)]
            index = index + 1

        musicPath = soundPath+noteName+'.mp3'
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

    first_index = second_index = 0
    while(True):
        if args.random == 'on':
            firstNote = random.choice(firstChoice)
        else:
            firstNote = firstChoice[int(first_index%len(firstChoice))]

        if args.updown == 'up':
            secondChoice = noteChoice[noteChoice.index(firstNote)+1:]
        else:
            secondChoice = noteChoice[0:noteChoice.index(firstNote)]

        print(firstNote, secondChoice)
        if args.random == 'on':
            secondNote = random.choice(secondChoice)
        else:
            secondNote = secondChoice[int(second_index%len(secondChoice))]
            second_index = second_index + 1
            if second_index%len(secondChoice) == 0:
                first_index = first_index + 1
                second_index = 0
            print(first_index, second_index)

        firstMusicPath = soundPath+firstNote+'.mp3'
        secondMusicPath = soundPath+secondNote+'.mp3'

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
        print('\n## Info ## : ', '---------------------- Semitone(%d)'%halfNum, 
            intervalNames[halfNum], ':', firstNote, secondNote, '\n')
        sleep(args.delay)


def playChords(tonic, chordName, scaleList, delay):
    pitchNum = re.findall('\d+', tonic)[0]
    chordStepList = chordNoteDict[chordName]

    scalePlayList1 = [x+pitchNum for x in scaleList]
    scalePlayList2 = [x+str(int(pitchNum)+1) for x in scaleList]
    scalePlayList3 = [x+str(int(pitchNum)+2) for x in scaleList]

    scalePlayList = scalePlayList1+scalePlayList2+scalePlayList3
    print(scalePlayList1, scalePlayList2, scalePlayList3, scalePlayList)

    chordBuff = []

    for step in chordStepList:
        noteName = scalePlayList[scalePlayList.index(tonic)+step]
        musicPath = soundPath+noteName+'.mp3'
        chordBuff.append(noteName)
        print(noteName)

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(delay)

    print('\n## Info ## : ', '----------------------', tonic, chordName, ':', chordBuff, '\n')
        


def chordTraining(args):
    print('\n##### Chord Ear Training Mode, Range %s #####\n'%(args.range))

    noteRange = args.range.split('-')
    noteStart = noteRange[0]
    noteEnd = noteRange[-1]

    scaleList = majorScaleDict[args.scale]
    #print(scaleList)

    chordName = args.chord

    index = 0
    while(True):
        if args.random == 'on':
            tonic = random.choice(scaleList)
        else:
            tonic = scaleList[int(index%len(scaleList))]
            index = index + 1

        tonic = tonic + re.findall('\d+', noteStart)[0]
        playChords(tonic, chordName, scaleList, 1)
        playChords(tonic, chordName, scaleList, 0)
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
    print(noteChoice, '\n', scaleChoice)

    scale_index = 0
    while(True):
        if args.random == 'on':
            scaleName = random.choice(scaleChoice)
        else:
            scaleName = scaleChoice[scale_index%len(scaleChoice)]
            scale_index = scale_index + 1

        firstNote = random.choice(noteChoice)
        scaleSpell = scaleNamePath+scaleName.replace(' ','')+'.mp3'

        scaleStep = scaleDict[scaleName]
        scaleBuff = []
        noteName = firstNote

        for step in scaleStep:
            noteName = noteList[noteList.index(noteName)+step]
            scaleBuff.append(noteName)

            musicPath = soundPath+noteName+'.mp3'
            namePath = notePath+noteName+'.mp3'

            p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
            sleep(1)

        print('\n## Info ## : ', '----------------------', scaleName, ':', scaleBuff, '\n')
        p = subprocess.Popen(["mplayer", scaleSpell], stdout=subprocess.PIPE)
        sleep(args.delay)    



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ear training, similar as www.musictheory.net/exercises')
    parser.add_argument("-i", "--instrument", default='piano', type=str, help="piano/guitar")
    parser.add_argument("-m", "--mode", default='note', type=str, help="note/interval/chord/scale")
    parser.add_argument("-a", "--range", default='C4-C5', type=str, help="Note range like C4-C5")
    parser.add_argument("-k", "--key", default='white', type=str, help="white/black/full")
    parser.add_argument("-d", "--delay", default=5, type=int, nargs='?', help="delay secs after bee")
    parser.add_argument("-s", "--scale", default='C', type=str, help="C/G/D/A/E/B/F#/Gb/Db/Ab/Eb/Bb/F")
    parser.add_argument("-u", "--updown", default='up', type=str, help="up/down")
    parser.add_argument("-r", "--random", default='on', type=str, help="on/off")
    parser.add_argument("-c", "--chord", default='3', type=str, help="3/6/46/sus2/sus4/7/56/34/2/9/11/13")

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

