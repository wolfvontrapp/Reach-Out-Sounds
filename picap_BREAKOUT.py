
# picap1
#
# Bits stolen from:
#					touch-mp3.py - polyphonic touch triggered MP3 playback
#					button-utility.py
#						by Stefan Dzisiewski-Smith and Szymon Kaliski
#
###############################################################################

from time import sleep, time
from subprocess import call
import signal, sys, pygame, MPR121, getopt
import RPi.GPIO as GPIO
import config
import os
import json

num_electrodes = 12

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  light_rgb([0, 0, 0])
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ----------- set up LED ---------------
                            # ORIGINALS:
red_led_pin = 18            #     6
green_led_pin = 27          #     5
blue_led_pin = 22           #    26

def light_rgb(colour):
  GPIO.output(red_led_pin, colour[0])
  GPIO.output(green_led_pin, colour[1])
  GPIO.output(blue_led_pin, colour[2])

# 7 colours:
colours = [[1, 1, 1], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 0, 0]]
red = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(blue_led_pin, GPIO.OUT)
# ----------------------------------------

# ------------- setup BUTTON ------------------------
power_pin = 16                  # J8.36 = GPIO16
cycle_button_pin = 23           # J8.16 = GPIO23
reset_button_pin = 24           # J8.18 = GPIO24
button_pause = 0.25		# seconds

GPIO.setup(power_pin, GPIO.OUT)
GPIO.setup(cycle_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(reset_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.output(power_pin, True)
# -------------------------------------------------------------------

# --------------------- Setup MP3s ----------------------------------
# initialize mixer and pygame
pygame.mixer.pre_init(frequency = 44100, channels = 1, buffer = 1024)
pygame.init()
pygame.mixer.set_num_channels(12)
num_sample_sets = 0
# get number of folders in 'samples'
#num_sample_sets = len(os.walk('samples').next()[1])
isdir = True
while (isdir):
  num_sample_sets += 1
  isdir = os.path.isdir("/home/pi/PiCap/samples/tracks{0:02d}".format(num_sample_sets+1))

print "{} sets of samples".format(num_sample_sets)
light_rgb(colours[1])

# TODO
# convert mp3s to wavs with picap-samples-to-wav
##for ii in range(num_sample_sets):
  #call("picap-samples-to-wav /home/pi/PiCap/samples/tracks{0:02d}".format(ii+1), shell = True)

# load paths
sets = []
for jj in range(num_sample_sets):
  paths = []
  for i in range(num_electrodes):
    path = "/home/pi/PiCap/samples/tracks{0:02d}/.wavs/TRACK{1:03d}.wav".format(jj+1,i)
    print "loading file: " + path

    paths.append(path)
  sets.append(paths)

# Readout: list of track files
for ii in range(num_sample_sets):
  for jj in range(num_electrodes):
    print sets[ii][jj]
# ----------------------------------------------------------------------------

# Set Change function:
def changeset():
  global current_set, current_colour
  current_set += 1
  current_colour += 1
  if current_set >= num_sample_sets:
    current_set = 0
    current_colour = 0
  if current_colour >= len(colours):
    current_colour = 0
  print "Set: {}".format(current_set)
  return current_set

# --------------------- Initial values -----------------------
current_colour = 0
current_set = 0
cycle_is_pressed = False
cycle_last_released = time()
reset_is_pressed = False
reset_last_released = time()

# --------------------------- LOAD THE CONFIG JSON ---------------------
config = {}
with open('config.json', 'r') as f:
    config = json.load(f)

base_dir = "/home/pi/PiCap/samples/"
paths = [os.path.join(base_dir, f) for f in config['config1']['samples1']]

pad0 = Pad(config, 0, 0, 0)
print(pad0)

# --------------------------- MAIN CODE LOOP ---------------------------

while True:
  light_rgb([0,0,0])
  try:
    sensor = MPR121.begin()
  except Exception as e:
    print e
    sys.exit(1)
  last_pressed    = None
  last_released   = None
  is_pressed      = False
  running = True
  sleep(0.5)
  print "start picap"
  light_rgb(colours[current_colour])
  while running:
  # Sensors:
    if sensor.touch_status_changed():
      sensor.update_touch_data()
      is_any_touch_registered = False
      for i in range(num_electrodes):
        if sensor.get_touch_data(i):
        # check if touch is registred to set the led status
          is_any_touch_registered = True
        if sensor.is_new_touch(i):
        # play sound associated with that touch
          print "playing: set:" + str(current_set+1)+ ", sound: " + str(i)
          path = sets[current_set][i]
          print path
          sound = pygame.mixer.Sound(path)
          pygame.mixer.Channel(i).play(sound)

    # ------ Buttons: ------
    now = time()
    # Cycle Button:
    if GPIO.input(cycle_button_pin):
      if not cycle_is_pressed:
        if ((now - cycle_last_released) > button_pause):
          # NEW CYCLE BUTTON PRESS, DO SOMETHING:
          changeset()
          light_rgb(colours[current_colour])
          cycle_is_pressed = True
        else:
          print "TOO SOON {}".format(now - cycle_last_released)
          cycle_is_pressed = True

    elif not GPIO.input(cycle_button_pin) and cycle_is_pressed:
      print "cycle button released"
      cycle_is_pressed = False
      cycle_last_released = now
    # Reset Button:
    if GPIO.input(reset_button_pin):
      if not reset_is_pressed:
        if ((now - reset_last_released) > button_pause):
          # NEW RESET BUTTON PRESS, DO SOMETHING:
          running = False
          reset_is_pressed = True
        else:
          print "TOO SOON {}".format(now - reset_last_released)
          reset_is_pressed = True

    elif not GPIO.input(reset_button_pin) and reset_is_pressed:
      print "reset button released"
      reset_is_pressed = False
      reset_last_released = now

    sleep(0.01)
