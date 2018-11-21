# -*- coding: utf-8 -*-
# @Time     : 2018/10/08 
# @Author   : liguibin
#

###
'''
usage: xmlyMp3Dl.py [-h] [-o OUTPUT] [-v] [-n] url

download all audioes in ximalay album like
:https://www.ximalaya.com/ertong/11106118

positional arguments:
  url                   web url need to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
  -v, --verbosity       increase output verbosity
  -n, --noIndex         not add index to prefix
'''

import os
import re
import sys
import time
import pygame
import random
import argparse
import subprocess
from time import sleep

natrualPitches = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
twelvePitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

sfOgg = ['sharp.ogg', 'flat.ogg']
numOgg = ['1.ogg', '2.ogg', '3.ogg', '4.ogg', '5.ogg', '6.ogg', '7.ogg']
pitchOgg = ['C.ogg', 'D.ogg', 'E.ogg', 'F.ogg', 'G.ogg', 'A.ogg', 'B.ogg']


oggPath = './ogg/alphabet/'
numPath = './ogg/number/'
notePath = './ogg/noteSpell/'
soundPath = './ogg/pitchSound/piano/'

stringList = []
natrualList = [
[0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20], #string-1
[0, 1, 3, 5, 6, 8, 10, 12, 13, 15, 17, 18, 20], #string-2
[0, 2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19],     #string-3
[0, 2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19],     #string-4
[0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20], #string-5
[0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20]  #string-6
]
chromaticList = [
[2, 4, 6, 9, 11, 14, 16, 18],                   #string-1
[2, 4, 7, 9, 11, 14, 16, 19],                   #string-2
[1, 3, 6, 8, 11, 13, 15, 18, 20],               #string-3
[1, 4, 6, 8, 11, 13, 16, 18, 20],               #string-4
[1, 4, 6, 9, 11, 13, 16, 18],                   #string-5
[2, 4, 6, 9, 11, 14, 16, 18]                    #string-6
]


def text2voice(noteName, file):
    text = noteName.replace('#', ' sharp')
    url = 'http://tts.baidu.com/text2audio?idx=1&tex=input&cuid=baidu_speech_demo'\
            '&cod=2&lan=en&ctp=1&pdt=1&spd=1&per=2&vol=5&pit=9'.replace('input', text)
    
    print('wget "%s" -O %s.mp3'%(url, noteName), file=file)



def getNoteName(string, fret):

    if string == 1:
        noteStart = 'E'
        openScale =  4
    elif string == 2:
        noteStart = 'B'
        openScale =  3
    elif string == 3:
        noteStart = 'G'
        openScale =  3
    elif string == 4:
        noteStart = 'D'
        openScale =  3
    elif string == 5:
        noteStart = 'A'
        openScale =  2
    elif string == 6:
        noteStart = 'E'
        openScale =  2
    else:
        print('## Error ## : String-%d out of range'%(s))

    openIndex = twelvePitches.index(noteStart)
    noteName = twelvePitches[(openIndex+fret) if (openIndex+fret<12) else ((openIndex+fret)%12)]
    noteScale = openScale + int((openIndex+fret)/12)

    #print('#### Get String-%d fret-%d NoteName: %s%d #####'%(string, fret, noteName, noteScale))
    return (noteName+str(noteScale))



def fretBoardInit():
    #file = open('get_voice.sh', 'w+')

    for s in range(1, 7):
        fretList = []

        for f in range(0, 21):
            fretsDict = {}
            fretsDict['string'] = s
            fretsDict['fret'] = f
            fretsDict['noteName'] = getNoteName(s, f)
            fretsDict['soundSrc'] = str(fretsDict['noteName'])+'.ogg'

            #text2voice(fretsDict['noteName'], file)

            fretList.append(fretsDict)

        #print('\n######String-%d######'%(s))
        #print(fretList)

        stringList.append(fretList)

    #file.close()
    #print(stringList)



def pygameInit():
    pygame.mixer.init()


def main(args):
    print('\n######### Guitar String-%s, frets-%s, delay %d secs ########\n'
        %(args.strings, args.frets, args.delay))

    strStart = 1
    strEnd = 6

    if args.strings:
        rangeStr = re.findall(r"\d+\.?\d*", args.strings)
        strStart = int(rangeStr[0])
        strEnd = int(rangeStr[-1])
        print('## Info ## : String range %s'%(args.strings))

        if strStart < 1 or strStart > 6 or strEnd < 0 or strEnd > 20 or strStart > strEnd:
            print('## Error ## : strings input out of range %s'%(args.strings))
            exit()

    # pitch repeat after 12 frets, so 11 frets by default
    fretStart = 0
    fretEnd = 11

    if args.frets:
        rangeStr = re.findall(r"\d+\.?\d*",args.frets)
        fretStart = int(rangeStr[0])
        fretEnd = int(rangeStr[-1])
        print('## Info ## : frets range %s'%(args.frets))

        if fretStart < 0 or fretStart > 20 or fretEnd < 0 or fretEnd > 20 or fretStart > fretEnd:
            print('## Error ## : frets input out of range %s'%(args.frets))
            exit()

    if args.natrual:
        print('\n#### Natrual Pitches Only ####\n')
        print(natrualPitches)
    elif args.chromatic:
        print('\n#### Chromatic Pitches Only ####\n')
        print(list(set(twelvePitches)-set(natrualPitches)))
    else:
        print('\n#### All 12 Pitches ####\n')
        print(twelvePitches)

    while(True):

        s = random.randint(strStart, strEnd)

        if args.natrual or args.chromatic:
            pitchList = natrualList if args.natrual else chromaticList
            #print(pitchList)

            if fretStart in pitchList[s-1]:
                idxStart = pitchList[s-1].index(fretStart)
            elif (fretStart+1) in pitchList[s-1]:
                idxStart = pitchList[s-1].index(fretStart+1)
            else:
                idxStart = pitchList[s-1].index(fretStart+2)

            if fretEnd in pitchList[s-1]:
                idxEnd = pitchList[s-1].index(fretEnd)
            elif (fretEnd-1) in pitchList[s-1]:
                idxEnd = pitchList[s-1].index(fretEnd-1)
            else:
                idxEnd = pitchList[s-1].index(fretEnd-2)

            f = random.choice(pitchList[s-1][idxStart:(idxEnd+1)])
        else:
            f = random.randint(fretStart, fretEnd)


        if args.music == False:
            fullPath = soundPath+stringList[s-1][f]['soundSrc'] 
            p = subprocess.Popen(["mplayer", fullPath], stdout=subprocess.PIPE)
            sleep(2)

        print('\n## Info ## : ', stringList[s-1][f], '----------------------', 
            stringList[s-1][f]['noteName'], '\n')

        if args.word == False:
            noteName = stringList[s-1][f]['noteName']
            noteOgg = noteName+'.ogg'
            fullPath = notePath+noteOgg
            p = subprocess.Popen(["mplayer", fullPath], stdout=subprocess.PIPE)

        sleep(args.delay)

'''
      ## pygame play has sound transformation, so use mplayer instead

      sound = pygame.mixer.Sound(soundPath+stringList[s-1][f]['soundSrc'])
      sound.play()

      noteName = stringList[s-1][f]['noteName']
      noteOgg = noteName+'.ogg'
      noteSound = pygame.mixer.Sound(notePath+noteOgg)

      sleep(2)

      noteSound.play()
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='random generate A-G pitches and play the sound')
    parser.add_argument("-i", "--instrument", help="instrument: piano/guitar")
    parser.add_argument("-s", "--strings", help="strings number: 1-6")
    parser.add_argument("-f", "--frets", help="specify frets range like 0-12")
    parser.add_argument("-d", "--delay", default=5, type=int, nargs='?', help="delay secs after bee")
    parser.add_argument("-w", "--word", help="not play character sound A-G", action="store_true")
    parser.add_argument("-m", "--music", help="not play pitch sound", action="store_true")
    parser.add_argument("-n", "--natrual", help="natrual pitches", action="store_true")
    parser.add_argument("-c", "--chromatic", help="chromatic pitches", action="store_true")

    args = parser.parse_args()
    print(args)

    #pygameInit()
    fretBoardInit()

    main(args)

