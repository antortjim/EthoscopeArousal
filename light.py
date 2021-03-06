import datetime 
import time 
import logging
import typing

import RPi.GPIO as GPIO 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

duration_1 = 1 
intensity_1 = 0.01 
stimulus_1 = "2021:02:12-02:01:00" 
#stimulus_1 = "2019:12:13-15:45:00"
#ZT16 == 02:00, lights on at 10:00 am

duration_2 = 1 
intensity_2 = 0.1 
stimulus_2 = "2021:02:12-02:06:00" 
#stimulus_2 = "2019:06:07-13:41:02" 

duration_3 = 1 
intensity_3 = 1 
stimulus_3 = "2021:02:12-02:11:00" 
#stimulus_3 = "2019:06:07-13:41:04" 

duration_4 = 10 
intensity_4 = 100 
stimulus_4 = "2021:02:12-02:16:00" 
#stimulus_4 = "2019:07:17-15:36:06"

pins = [17, 27, 4]

# Write here your own schedule
# You can use the code before class LightInteractor
# to provide the data
schedule = {
	stimulus_1: (duration_1, intensity_1, 1),
	stimulus_2: (duration_2, intensity_2, 2),
	stimulus_3: (duration_3, intensity_3, 3),
	stimulus_4: (duration_4, intensity_4, 4),

}

class LightInteractor:

	# check what the time is every
	# `_waiting_time_seconds` seconds
	_waiting_time_seconds = 0.200



	def __init__(self, schedule, log="/home/pi/data_log.csv", pins: typing.List = None, testing: bool = False):
		self._log = log
		self._pin_ids = pins
		self._schedule = schedule
		self._testing = testing

		if pins is not None:
			self._pin_ids = pins

		self._pins = [None for p in self._pin_ids]
		GPIO.setmode(GPIO.BCM) 

		for i, p in enumerate(self._pin_ids):
			GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)
			GPIO.output(p, GPIO.LOW)
			# Create a PWM object
			self._pins[i] = GPIO.PWM(p, 100)


	def interact(self, stimulus: str):
		"""
		For every pin in self._pins
		* Turn it off
		* Turn it on with an intensity and for a duration
		as given by the schedule
		* Turn them off

		This is done simultaneously (+- ms) for all pins
		"""

		pins = self._pins
		
		if not testing:
			duration, intensity, index = self._schedule[stimulus]
		else:
			duration, intensity, index = 5, 1, 0

		for pin in pins:
			pin.start(0)
		
		print("stimulus")
		for pin in pins:
			pin.ChangeDutyCycle(intensity)

		time.sleep(duration)

		for pin in pins:
			pin.stop()

		return 0
			
	def save(self, stimulus: str):
		"""
		Log the interaction saved in the self._schedule dictionary
		with key given by stimulus 
		"""

		if stimulus not in self._schedule:
			logger.warning("%s is not an interaction in the schedule", stimulus)
			return 1


		duration, intensity, index = self._schedule[stimulus]
		file = open(self._log, "a")
		file.write(f"\n\nstimulus_{index}:\n")
		file.write(now+"\n")
		file.write("duration:"+str(duration)+"_intensity:"+str(intensity)+"\n")
		
		return 0

	def run(self):
		while True:
			print("Iteration")
			try:
				now = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
                # if now in self._schedule: 
				if True:
					logger.info("Interacting")
					self.interact(now)
					self.save(now)
					time.sleep(self._waiting_time_seconds) 
							
			# trap a CTRL+C keyboard interrupt
			except KeyboardInterrupt:
					logger.info("Exiting...")
					# resets all GPIO ports used by this program
					GPIO.cleanup()
					return 0

			except Exception as error:
					GPIO.cleanup()
					logger.error(error)
					return 1

		return 0
    
    
    

if __name__ == "__main__":
        interactor = LightInteractor(schedule, pins=[27], testing=True)
        interactor.run()
