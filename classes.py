from models import Device as DeviceModel
from models import Thermostat as ThermostatModel
from models import DoorLock as DoorLockModel
from models import Window as WindowModel
from models import TemperatureSensor as TemperatureSensorModel
from models import MultiSensorDevice as MultiSensorDeviceModel
from models import CoSmokeDetector as CoSmokeDetectorModel

import time
import threading


class Household:
    def __init__(self, devices=[]):
        self.devices = devices

    def add_device(self, device):
        self.devices.append(device)

    def is_secure(self):
        # Secure is being defined as the windows are closed and the door is locked, since I don't see anything
        # more specific in any of the devices
        secure = True
        for device in self.devices:
            if device.type == 'Window':
                if not device.is_closed():
                    secure = False
            if device.type == 'Door Lock':
                if not device.is_locked():
                    secure = False
        return secure

    def get_temperature(self):
        temp = None
        for device in self.devices:
            try:
                temp = device.get_current_temp()
            except AttributeError:
                # This will try to call get_temperature on all devices. If it doesn't have the method
                # it should end up in here.
                pass
        return temp

    def get_humidity(self):
        humid = None
        for device in self.devices:
            try:
                humid = device.get_current_humidity()
            except AttributeError:
                # Same as above. Ask everything for humidity, catch it if it doesn't exist
                pass
        return humid

    def silence_alarms(self):
        for device in self.devices:
            try:
                device.silence_alarm(0)
            except AttributeError:
                # Tell everything to shut off alarms, if they can. Pass if they don't have the method
                pass

    def num_pins_left(self):
        max_pins = 0
        for device in self.devices:
            try:
                max_pins = device.door_lock.pin_limit
                currnet_pins = device.door_lock.num_pins()
                return max_pins - currnet_pins
            except AttributeError:
                # Grab the pin_limit from any device that has it.
        # Return zero if no devices have a pin limit option
        return max_pins

class Device:
    def __init__(self, id):
        self.device = DeviceModel.objects.get(id=id)

    def toggle_on_off(self):
        raise NotImplementedError


class Thermostat(Device):
    def __init__(self, id):
        self.thermostat = ThermostatModel.objects.get(id=id)
        super.__init__(id=id)

    def toggle_fan(self):
        raise NotImplementedError

    def disable_fan(self):
        raise NotImplementedError

    def turn_on_fan_temp(self):
        raise NotImplementedError

    def get_current_temp(self):
        raise NotImplementedError


class ThermostatTypeOne(Thermostat):
    def toggle_fan(self):
        self.thermostat.fan_on = not self.thermostat.fan_on
        # We'd need to send a command to the device. Ideally it already has a toggle fan, and we can just call that.
        # If not, we can use the fan_on to tell it to turn it on or off specifically

    def disable_fan(self):
        time.sleep(300)
        self.thermostat.fan_on = False
        # Send the command to the device here to disable the fan

    def turn_on_fan_temp(self):
        #using a thread here so that we don't sit here for the 5 minutes.
        t = threading.Thread(target=self.thermostat.disable_fan)
        t.start()

    def get_current_temp(self):
        temp = None
        # call the device and ask for the current temperature. Pass in if you want celsius or not
        return temp

    def toggle_celsius(self):
        self.thermostat.toggle_celsius()

    def toggle_on_off(self):
        #this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()


class ThermostatTypeTwo(Thermostat):
    def get_current_humidity(self):
        humid = None
        # call the device and ask for the current humidity
        return humid

    def toggle_fan(self):
        self.thermostat.fan_on = not self.thermostat.fan_on
        # We'd need to send a command to the device. Ideally it already has a toggle fan, and we can just call that.
        # If not, we can use the fan_on to tell it to turn it on or off specifically

    def disable_fan(self):
        time.sleep(300)
        self.thermostat.fan_on = False
        # Send the command to the device here to disable the fan

    def turn_on_fan_temp(self):
        # using a thread here so that we don't sit here for the 5 minutes.
        t = threading.Thread(target=self.thermostat.disable_fan)
        t.start()

    def get_current_temp(self):
        temp = None
        # call the device and ask for the current temperature. Set the value to temp
        return temp

    def toggle_on_off(self):
        # this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()


class DoorLock(Device):
    def __init__(self, id, pin_limit):
        self.door_lock = DoorLockModel.objects.get(id)
        self.door_lock.pin_limit = pin_limit
        super.__init__(id=id)

    def unlock_door(self):
        # Send a command to the DoorLock to unlock
        pass

    def add_pin(self, pin):
        if self.door_lock.num_pins < self.door_lock.pin_limit:
            self.door_lock.add_pin(pin)
            #Send the new pin to the actual device and update its pin list

    def remove_pin(self, pin):
        self.door_lock.remove_pin(pin)
        #Send the command to remove the pin to the device

    def factory_reset(self):
        # Send a factory reset command to the device. This is going to be different per device.
        # I am going to assume the device has a master pin that it provides after a reset, set to master_pin
        master_pin = None
        self.door_lock.set_master_pin(master_pin)

    def toggle_on_off(self):
        # this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()


class Window(Device):
    def __init__(self, id):
        self.window = WindowModel.objects.get(id)
        super.__init__(id=id)

    def get_status(self):
        #call the device to look for open or closed, save the status as a bool is_open
        is_open = False
        if is_open != self.window.is_open:
            self.window.toggle_open()

    def toggle_on_off(self):
        # this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()


class TemperatureSensor(Device):
    def __init__(self, id):
        self.temperature_sensor = TemperatureSensorModel.objects.get(id)
        super.__init__(id=id)

    def get_current_temp(self):
        # call the device to ask for the temp. Pass in if you want it in celsius or not
        temp = None
        return temp

    def toggle_on_off(self):
        # this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()


class MultiSensorDevice(Device):
    def __init(self, id):
        self.multi_sensor = MultiSensorDeviceModel.objects.get(id)
        super.__init__(id=id)

    def get_current_temp(self):
        # call the device to ask for the temp. Pass in if you want it in celsius or not (self.multi_sensor.celsius)
        temp = None
        return temp

    def get_current_humidity(self):
        humid = None
        # call the device and ask for the current humidity
        return humid

    def get_flood_status(self):
        status = None
        # call the device and ask for the current flood status
        return status

    def silence_alarm(self, length):
        time.sleep(length)
        self.multi_sensor.toggle_alarm()
        #call the device to turn the alarm back on

    def silence_alarm_temp(self, length=300):
        # call the device and tell it to silence the alarm
        if self.multi_sensor.alarm: #toggle it off, if it's on
            self.multi_sensor.toggle_alarm()
            t = threading.Thread(target=self.silence_alarm)
            t.start()

    def toggle_on_off(self):
        # this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()


class CoSmokeDetector(Device):

    def __init__(self, id):
        self.co_smoke_detector = CoSmokeDetectorModel.objects.get(id)
        super.__init__(id=id)

    def silence_alarm(self, length):
        time.sleep(length)
        self.co_smoke_detector.toggle_alarm()
        #call the device to turn the alarm back on

    def silence_alarm_temp(self, length=300):
        # call the device and tell it to silence the alarm
        if self.co_smoke_detector.alarm: #toggle it off, if it's on
            self.co_smoke_detector.toggle_alarm()
            t = threading.Thread(target=self.silence_alarm)
            t.start()

    def get_smoke_level(self):
        # call the device and request the smoke level
        smoke_level = None
        return smoke_level

    def get_co_level(self):
        # call the device and request the co level
        co_level = None
        return co_level

    def toggle_on_off(self):
        # this is going to call the device's specific methods for toggling on and off
        self.device.toggle_on_off()
