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
natrualList = []


def text2voice(noteName, file):
    text = noteName.replace('#', ' sharp')
    url = 'http://tts.baidu.com/text2audio?idx=1&tex=input&cuid=baidu_speech_demo&cod=2&lan=en&ctp=1&pdt=1&spd=4&per=2&vol=5&pit=9'.replace('input', text)
    
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

        print('\n######String-%d######'%(s))
        print(fretList)

        stringList.append(fretList)

    #file.close()
    #print(stringList)



def pygameInit():
    pygame.mixer.init()


def main(args):
    print('\n######### Guitar String-%s, frets-%s, delay %d secs ########\n'%(args.strings, args.frets, args.delay))

    strStart = 1
    strEnd = 6

    if args.strings:
        rangeStr = re.findall(r"\d+\.?\d*", args.strings)
        strStart = int(rangeStr[0])
        strEnd = int(rangeStr[-1])
        print('## Info ## : String range %s'%(args.strings))

        if strStart < 1 or strStart > 6 or strEnd < 0 or strEnd > 20 or strStart > strEnd:
            print('## Error ## : frets input out of range %s'%(args.frets))
            exit()

    numStart = 0
    numEnd = 11

    if args.frets:
        rangeStr = re.findall(r"\d+\.?\d*",args.frets)
        numStart = int(rangeStr[0])
        numEnd = int(rangeStr[-1])
        print('## Info ## : frets range %s'%(args.frets))

        if numStart < 0 or numStart > 20 or numEnd < 0 or numEnd > 20 or numStart > numEnd:
            print('## Error ## : frets input out of range %s'%(args.frets))
            exit()


    while(True):
      #char = random.choice(pitchRange)

      s = random.randint(strStart, strEnd)
      f = random.randint(numStart, numEnd)

      sound = pygame.mixer.Sound(soundPath+stringList[s-1][f]['soundSrc'])
      sound.play()

      noteName = stringList[s-1][f]['noteName']
      noteOgg = noteName+'.ogg'
      noteSound = pygame.mixer.Sound(notePath+noteOgg)

      time.sleep(2)

      noteSound.play()

      print('## Info ## : ', stringList[s-1][f], '----------------------', 
            stringList[s-1][f]['noteName'], '\n')

      time.sleep(args.delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='random generate A-G pitches and play the sound')
    parser.add_argument("-i", "--instrument", help="instrument: piano/guitar")
    parser.add_argument("-s", "--strings", help="strings number: 1-6")
    parser.add_argument("-f", "--frets", help="specify frets range like 0-12")
    parser.add_argument("-d", "--delay", default=3, type=int, nargs='?', help="delay secs after bee")
    parser.add_argument("-w", "--word", help="character sound A-E", action="store_true")
    parser.add_argument("-m", "--music", help="play pitch sound", action="store_true")
    parser.add_argument("-n", "--natrual", help="natrual pitches", action="store_true")
    parser.add_argument("-a", "--allpitch", help="all twelve pitches", action="store_false")

    args = parser.parse_args()

    pygameInit()
    fretBoardInit()

    main(args)

