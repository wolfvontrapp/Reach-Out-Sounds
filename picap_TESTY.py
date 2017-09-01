# TESTING TESTING TESTING TESTING TESTING TESTING
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
import os

try:
  sensor = MPR121.begin()
except Exception as e:
  print e
  sys.exit(1)

num_electrodes = 12

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  light_rgb([0, 0, 0])
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ----------- set up LED ---------------
red_led_pin = 6
green_led_pin = 5
blue_led_pin = 26

def light_rgb(colour):
  # we are inverting the values, because the LED is active LOW
  # LOW - on
  # HIGH - off
  GPIO.output(red_led_pin, not colour[0])
  GPIO.output(green_led_pin, not colour[1])
  GPIO.output(blue_led_pin, not colour[2])

# 7 colours:
current_colour = 0
colours = [[1, 1, 1], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 0, 0]]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(blue_led_pin, GPIO.OUT)
# ----------------------------------------

# ------------- setup BUTTON ------------------------
button_pin = 4		# assuming GPIO.BOARD pin 7 is same as GPIO.BCM pin 4
doublepress_timeout = 0.30
longpress_timeout   = 0.75

# button state
last_pressed    = None
last_released   = None
is_pressed      = False

# button action callback
def button_callback(button_pin):
  # we need to tell python that those variables are global
  # we don't want to create new local copies, but change global state
  global is_pressed, last_pressed, last_released

  # state 0 is pressed, 1 is released
  is_pressed = not GPIO.input(button_pin)

  if is_pressed:
    last_pressed = time()
  else:
    last_released = time()

# parse arguments on start
#parse_args(sys.argv[1:])

# setup button, and add the callback
# we could do everything in while True looop, but here we get nice handling of button debouncing
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(button_pin, GPIO.BOTH, callback = button_callback, bouncetime = 10)

# -------------------------------------------------------------------
# --------------------- Sensors -------------------------------------

SENSOR_TIMEOUT = 5
touch_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for ii in range(num_electrodes):
  thresh = get_touch_threshold(ii)
  release = get_release_threshold(ii)
  print "Sensor: " + str(ii) + ", Touch: " + str(thresh) + "Release: " + str(release)

# -------------------------------------------------------------------

# --------------------- Setup MP3s ----------------------------------
# initialize mixer and pygame
pygame.mixer.pre_init(frequency = 44100, channels = 64, buffer = 1024)
pygame.init()
num_sample_sets = 0
# get number of folders in 'samples'
#num_sample_sets = len(os.walk('samples').next()[1])
isdir = True
while (isdir):
  num_sample_sets += 1
  isdir = os.path.isdir("/home/pi/PiCap/samples/tracks{0:02d}".format(num_sample_sets+1))

print "{} sets of samples".format(num_sample_sets)

# convert mp3s to wavs with picap-samples-to-wav
for ii in range(num_sample_sets):
  light_rgb(colours[1])
  call("picap-samples-to-wav /home/pi/PiCap/samples/tracks{0:02d}".format(ii+1), shell = True)
  light_rgb(colours[0])

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

filtered = 1
baseline = 2
# ----------------------------------------------------------------------------

current_set = 0

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
# --------------------------- MAIN CODE LOOP ---------------------------
while True:
  now = time()
  sensor.update_all()
  # ---- Sensors:
  for i in range(num_electrodes):
    if touch_time[i] and ((now - touch_time[i]) > SENSOR_TIMEOUT):
      print "RECALIBRATE RECALIBRATE RECALIBRATE ... SENSOR" + str(i)
      touch_time[i] = 0

  if sensor.touch_status_changed():
    sensor.update_all()
    is_any_touch_registered = False

    for i in range(num_electrodes):
      if sensor.get_touch_data(i):
        # check if touch is registred to set the led status
        is_any_touch_registered = True
      if sensor.is_new_touch(i):
        # play sound associated with that touch
        print "playing: set: " + str(current_set+1)+ ", sound: " + str(i)
        filtered = sensor.get_filtered_data(i)
        baseline = sensor.get_baseline_data(i)
        print filtered
        print baseline
        path = sets[current_set][i]
        touch_time[i] = now
        print path
        sound = pygame.mixer.Sound(path)
        sound.play()
      elif sensor.is_new_release(i):
        touch_time[i] = 0

  # ---- Button:

  if is_pressed:
  	# DOUBLE PRESS:
    # (if we get another press before doublepress_timeout of last_released)
    if last_pressed is not None and last_released is not None and last_pressed < (last_released + doublepress_timeout):
      # does something:
      print "double press"
      
      last_pressed = None
      last_released = None
    
    # LONG PRESS:
    # (if last_pressed happened before longpress_timeout from now)
    elif last_pressed is not None and last_pressed < (now - longpress_timeout):
      print "long press"
      os.system("shutdown -t9 -r now")  # RESET PI IF LONG BUTTON PRESS
      last_pressed = None
      last_released = None

  else:
    # SINGLE PRESS:
      # (if button got released, and nothing happens in doublepress_timeout time, then we had single press)
      # (we could remove the timeout, but then each double press would also register single press)
    if last_released is not None and last_pressed is not None and last_released < (now - doublepress_timeout):
      print "single press"
      changeset()
      light_rgb(colours[current_colour])
      last_pressed = None

    # light up red led if we have any touch registered currently
#    if is_any_touch_registered:
#      light_rgb(1, 0, 0)#
#    else:
#     light_rgb(0, 0, 0)

  # sleep a bit
  sleep(0.01)
