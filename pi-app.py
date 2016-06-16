
# Speaker Selector Flask/Python script

from flask import Flask, request, render_template
import time
import RPi.GPIO
import os

RPi.GPIO.setmode(RPi.GPIO.BCM)

RPi.GPIO.setup(17, RPi.GPIO.OUT) # LED 01 - Speakers 1
RPi.GPIO.setup(18, RPi.GPIO.OUT) # LED 02 - Speakers 2
RPi.GPIO.setup(19, RPi.GPIO.OUT) # LED 03 - Speakers 3
#RPi.GPIO.setup(20, RPi.GPIO.OUT) # LED 04 - Not used / connected currently
RPi.GPIO.setup(21, RPi.GPIO.OUT) # LED 05 - Protection

RPi.GPIO.setup(22, RPi.GPIO.OUT, initial=0) # Relays (1 & 2) - Speakers 1 (L/R)
RPi.GPIO.setup(23, RPi.GPIO.OUT, initial=1) # Relays (3 & 4) - Speakers 2 (L/R)
RPi.GPIO.setup(24, RPi.GPIO.OUT, initial=1) # Relays (5 & 6) - Speakers 3 (L/R)
RPi.GPIO.setup(25, RPi.GPIO.OUT, initial=1) # Relays (7 & 8) - Protection (L/R)

app = Flask(__name__)

# Init Global Variable for Speaker Switch States
spkr_state = ['on', 'off', 'off', 'off', 'off']

LED01 = RPi.GPIO.PWM(17, 100)
LED02 = RPi.GPIO.PWM(18, 100)
LED03 = RPi.GPIO.PWM(19, 100)
#LED04 = RPi.GPIO.PWM(20, 100)
LED05 = RPi.GPIO.PWM(21, 100)

LED01.start(25)  # Turn on LED
LED02.start(0)  # Turn off LED
LED03.start(0)  # Turn off LED
#LED04.start(0)  # Turn off LED
LED05.start(0)  # Turn off LED

@app.route('/', methods=['POST','GET'])
def index():

	global spkr_state
	spkr_count = 0
	error = False
# If posting, process input from POST
	if request.method == 'POST':
		spkr_state[0] = request.form['spkrs_01']
		spkr_state[1] = request.form['spkrs_02']
		spkr_state[2] = request.form['spkrs_03']
		spkr_state[3] = request.form['spkrs_04']

# Count number of speakers selected, turn on protection if > 1
	for x in range(4):
		if spkr_state[x] == 'on':
			spkr_count = spkr_count + 1
	if (spkr_count > 1):
		spkr_state[4] = 'on'
	else:
		spkr_state[4] = 'off'

	SetRelays(spkr_state)

	return render_template('index.html', spkr_state=spkr_state, error=error)


@app.route('/admin/<action>')
@app.route('/admin')
def admin(action=None):
	if action == 'reboot':
		os.system("sudo shutdown -r now")
		return 'Rebooting...'
	if action == 'shutdown':
		os.system("sudo shutdown -h now")
		return 'Shutting Down...'

	temp = checkcputemp()

	return render_template('admin.html', temp=temp, action=action)

def checkcputemp():
	temp = os.popen('vcgencmd measure_temp').readline()
	return temp.replace("temp=","")

def SetRelays(spkr_state):
	# *****************************************
	# Function to set relays (and set LEDs if applicable)
	# *****************************************

	if spkr_state[0] == 'on':
		RPi.GPIO.output(22, 1) 	#Turn on Relay (0 = On) - Channel 1 Reverse Logic
		LED01.start(5) 	#Turn on LED (1 = On)
	else:
		RPi.GPIO.output(22, 0) 	#Turn off Relay (1 = Off) - Channel 1 Reverse Logic
		LED01.stop()  #Turn off LED (0 = Off)

	if spkr_state[1] == 'on':
		RPi.GPIO.output(23, 0) 	#Turn on Relay (0 = On)
		LED02.start(5) 	#Turn on LED (1 = On)
	else:
		RPi.GPIO.output(23, 1) 	#Turn off Relay (1 = Off)
		LED02.stop()  #Turn off LED (0 = Off)

	if spkr_state[2] == 'on':
		RPi.GPIO.output(24, 0) 	#Turn on Relay (0 = On)
		LED03.start(5) 	#Turn on LED (1 = On)
	else:
		RPi.GPIO.output(24, 1) 	#Turn off Relay (1 = Off)
		LED03.stop()  #Turn off LED (0 = Off)

	# spkr_state[3] unconnected and disabled
	#if spkr_state[3] == 'on':
		#RPi.GPIO.output(25, 0) 	#Turn on Relay (0 = On)
		#LED04.start(5) 	#Turn on LED (1 = On)
	#else:
		#RPi.GPIO.output(25, 1) 	#Turn off Relay (1 = On)
		#LED04.stop()  #Turn off LED (0 = Off)

	if spkr_state[4] == 'on':
		RPi.GPIO.output(25, 0) 	#Turn on Relay, turn on protection - Reverse logic for Protection Relay
		LED05.start(5) 	#Turn on LED (1 = On)
	else:
		RPi.GPIO.output(25, 1) 	#Turn on Relay, turn off protection - Reverse logic for Protection Relay
		LED05.stop()  #Turn off LED (0 = Off)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False)
