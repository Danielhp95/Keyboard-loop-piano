#!/usr/bin/env python

from scipy.io import wavfile
import argparse
import numpy as np
import pygame, pygame.mixer
import os
import sys
import warnings
import time
import threading

keys = None
key_sound = None

def parse_arguments():
    description = ('Use your computer keyboard as a "piano"')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='typewriter.kb',
        help='keyboard file (default: typewriter.kb)')
    return (parser.parse_args(), parser)


def playLoop(key_sound, loop_notes, end_time):
    if len(loop_notes) == 0:
        print('Empty loop, won\'t play')
        return
    print("Loop is being played")
    previous_wait = 0
    i = 0
    while True:
       print_loops(loop_notes, i)
       (note, waiting_time) = loop_notes[i]
       time.sleep(waiting_time - previous_wait)
       previous_wait = waiting_time
       key_sound[note].play(fade_ms=50)
       i = (i + 1) % len(loop_notes)
       if i == 0:
           time.sleep(end_time - previous_wait)
           previous_wait = 0

def print_loops(notes, i):
    os.system('clear')
    allNotes = '\t'.join([n[0] for n in notes])
    print(allNotes)
    numOfSpaces = '\t' * i
    print(numOfSpaces + '^')
 

def play():
    os.system('clear')
    # Parse command line arguments
    (args, parser) = parse_arguments()

    fps, sound = wavfile.read('bowl.wav')

    # So flexibl)
    pygame.mixer.init(fps, -16, 1, 2048)
    # For the focus
    screen = pygame.display.set_mode((150, 150))

    keys = args.keyboard.read().split('\n')
    key_sound = load_sounds()
    is_playing = {k: 0 for k in keys}

    recording_loop = 0
    loop_notes     = []
    threads        = []

    while True:
          
          event = pygame.event.wait()

          if event.type in (pygame.KEYDOWN, pygame.KEYUP):
              key = pygame.key.name(event.key)

          if event.type == pygame.KEYDOWN:
              if key == '#':
                  return
              elif key == 'space':
                  if recording_loop:
                      end_time =  (time.time() - recording_loop)
                      recording_loop = 0
                      # signals the end of the loop
                      threads.append(
                              threading.Thread(target=playLoop,
                                                      args=(key_sound,
                                                            loop_notes,
                                                            end_time,)))
                      threads[-1].start()
                      loop_notes     = []
                  else:
                      print("Loop is being recorded")
                      recording_loop = time.time()
                      loop_notes     = []

              if (key in key_sound.keys()) and (is_playing[key] == 0):
                  key_sound[key].play(fade_ms=50)
                  is_playing[key] = time.time()
                  if recording_loop > 0:
                    loop_notes.append((key, (time.time() - recording_loop)))

              elif event.key == pygame.K_ESCAPE:
                  pygame.quit()
                  raise KeyboardInterrupt

          elif event.type == pygame.KEYUP and key in key_sound.keys():
              # Stops with 50ms fadeout
              key_sound[key].fadeout(50)
              is_playing[key] = 0


def load_sounds():
    # Upper piano
    key_sounds = {}
    key_sounds[']'] = pygame.mixer.Sound('notes/063.wav')
    key_sounds['=']    = pygame.mixer.Sound('notes/062.wav')
    key_sounds['[']  =pygame.mixer.Sound('notes/061.wav')
    key_sounds['-']     =pygame.mixer.Sound('notes/060.wav')
    key_sounds['p'] =pygame.mixer.Sound('notes/059.wav')
    key_sounds['0'] =pygame.mixer.Sound('notes/058.wav')
    key_sounds['o'] =pygame.mixer.Sound('notes/057.wav')
    key_sounds['i'] =pygame.mixer.Sound('notes/056.wav')
    key_sounds['8'] =pygame.mixer.Sound('notes/055.wav')
    key_sounds['u'] =pygame.mixer.Sound('notes/054.wav')
    key_sounds['7'] =pygame.mixer.Sound('notes/053.wav')
    key_sounds['y'] =pygame.mixer.Sound('notes/052.wav')
    key_sounds['t'] =pygame.mixer.Sound('notes/051.wav')
    key_sounds['5'] =pygame.mixer.Sound('notes/050.wav')
    key_sounds['r'] =pygame.mixer.Sound('notes/049.wav')
    key_sounds['4'] =pygame.mixer.Sound('notes/048.wav')
    key_sounds['e'] =pygame.mixer.Sound('notes/047.wav')
    key_sounds['3'] =pygame.mixer.Sound('notes/046.wav')
    key_sounds['w'] =pygame.mixer.Sound('notes/045.wav')
    key_sounds['q'] =pygame.mixer.Sound('notes/044.wav')

    # Lower piano
    key_sounds['/'] =pygame.mixer.Sound('notes/039.wav')
    key_sounds[';'] =pygame.mixer.Sound('notes/038.wav')
    key_sounds['.'] =pygame.mixer.Sound('notes/037.wav')
    key_sounds['l'] =pygame.mixer.Sound('notes/036.wav')
    key_sounds[','] =pygame.mixer.Sound('notes/035.wav')
    key_sounds['k'] =pygame.mixer.Sound('notes/034.wav')
    key_sounds['m'] =pygame.mixer.Sound('notes/033.wav')
    key_sounds['n'] =pygame.mixer.Sound('notes/032.wav')
    key_sounds['h'] =pygame.mixer.Sound('notes/031.wav')
    key_sounds['b'] =pygame.mixer.Sound('notes/030.wav')
    key_sounds['g'] =pygame.mixer.Sound('notes/029.wav')
    key_sounds['v'] =pygame.mixer.Sound('notes/028.wav')
    #key_sounds['f'] =pygame.mixer.Sound('notes/044.wav')
    key_sounds['c'] =pygame.mixer.Sound('notes/027.wav')
    key_sounds['d'] =pygame.mixer.Sound('notes/026.wav')
    key_sounds['x'] =pygame.mixer.Sound('notes/025.wav')
    key_sounds['s'] =pygame.mixer.Sound('notes/024.wav')
    key_sounds['z'] =pygame.mixer.Sound('notes/023.wav')
    key_sounds['a'] =pygame.mixer.Sound('notes/022.wav')

    return key_sounds



if __name__ == '__main__':
    try:
        play()
    except KeyboardInterrupt:
        print('Goodbye')
