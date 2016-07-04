#!/usr/bin/python3

# learning2flute.py - learn to play the flute
# Copyright (C) 2016 Benjamin Abendroth
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
from os import system
from time import sleep
from random import choice
from textwrap import indent
from subprocess import Popen, PIPE

argp = argparse.ArgumentParser(description='Learn to play the flute')
argp.add_argument('--countdown', metavar='SECONDS', type=int, help='Set the start count down', default=3)
argp.add_argument('--rounds', metavar='ROUNDS',  type=int, help='Set the number of rounds per interval', default=5)
argp.add_argument('--start', metavar='SECONDS', type=float, help='Set the start interval', default=2)
argp.add_argument('--step',  metavar='SECONDS', type=float, help='Set the step', default=0.1)
argp.add_argument('--stop',  metavar='SECONDS', type=float, help='Set the stop interval', default=0.7)

full_char  = '●'
empty_char = '○'
half_char  = '◐'

ascii_flute = """\
  _
 / \\
/   \\
││_││
)───(
) {0} (
│   │
│ {1} │
│ {2} │
│ {3} │
│ {4} │
│ {5} │
│ {6} │
│ {7} │
)   (
^^^^^\
"""

def getFlute(pattern):
   chars = []
   for hole in pattern:
      if hole == 0:      chars.append(empty_char)
      elif hole == 0.5:  chars.append(half_char)
      elif hole == 1:    chars.append(full_char)

   return ascii_flute.format(*chars)

def emptyFlute(back=1, one=0, two=0, three=0, four=0, five=0, six=0, seven=0):
   return (back, one, two, three, four, five, six, seven)

def fullFlute(back=1, one=1, two=1, three=1, four=1, five=1, six=1, seven=1):
   return (back, one, two, three, four, five, six, seven)

notes = {
   '1.C':  fullFlute(),
   '1.D':  fullFlute(seven=0),
   '1.E':  fullFlute(seven=0, six=0),
   '1.F':  fullFlute(seven=0, six=0, five=0),
   '1.F#': fullFlute(four=0),
   '1.G':  fullFlute(seven=0, six=0, five=0, four=0),
   '1.A':  emptyFlute(one=1, two=1),
   '1.B':  emptyFlute(one=1, three=1, four=1),
   '1.H':  emptyFlute(one=1),
   '2.C':  emptyFlute(two=1),
   '2.D':  emptyFlute(back=0, two=1),
   '2.E':  fullFlute(back=0.5, six=0, seven=0),
}

available_notes = list(notes.keys())

def figlet(string, font='big'):
   out = Popen(['figlet', '-f', font, string], stdout=PIPE).communicate()[0]
   return out.decode('utf-8')

def choice_unduplicated(items, not_item):
   item = choice(items)
   while item == not_item:
      item = choice(items)

   return item


class Rounds:
   def __init__(self, start, step, stop=0, rounds=0):
      if (step <= 0):    raise Exception("Step may not be <= 0")
      if (start < stop): raise Exception("Start may not be less than stop")

      self.start, self.step, self.stop, self.rounds = start, step, stop, rounds

   def play(self):
      selection = None
      current_sleep = self.start
      current_round = 0

      while True:
         selection = choice_unduplicated(available_notes, selection)
         octave, note = selection.split('.')

         flute = getFlute(notes[selection])
         figlet_note = figlet('{}  {}'.format(octave, note))

         header = ' Interval: {:.2f} | Sleep: {:.2f} | Round {:d}/{:d}'.format(
            self.step, current_sleep, current_round, self.rounds)

         flute_padded = indent(flute, ' ' * 14)
         figlet_width = len(max(figlet_note.splitlines(), key=len))
         note_padded = indent(figlet_note, ' ' * (17 - int(figlet_width/2)))

         system('clear')
         print(header, "\n\n", note_padded, flute_padded, sep='')

         sleep(current_sleep)

         current_round += 1

         if (current_round >= self.rounds):
            current_round = 0
            current_sleep -= self.step

         if (current_sleep <= self.stop):
            break


def print_countdown(countdown):
   for i in range(countdown, 0, -1):
      print("{} ...".format(i))
      sleep(1)

try:
   args = argp.parse_args()
   print_countdown(args.countdown)
   Rounds(args.start, args.step, args.stop, args.rounds).play()

except KeyboardInterrupt:
   pass
