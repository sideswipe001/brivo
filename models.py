from django.db import models



class Device(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    on = models.BooleanField(default=True)

    class Meta:
        device_type="UNKNOWN"

    @classmethod
    def toggle_on_off(cls):
        cls.on = not cls.on
        # Here we'd need to send the command to actual device, updating the state to on or off


class Thermostat(Device):
    upper_limit = models.IntegerField()
    lower_limit = models.IntegerField()
    ac_heater_enabled = models.BooleanField()
    celsius = models.BooleanField(default=False)
    fan_on = models.BooleanField(default=False)
    humidity = models.IntegerField(default=None)

    class Meta:
        device_type = "Thermostat"

    @classmethod
    def toggle_celsius(cls):
        cls.celsius = not cls.celsius


class DoorLock(Device):
    auto_lock_timeout = models.IntegerField()
    pin_limit = models.IntegerField()

    class Meta:
        device_type = "Door Lock"

    @classmethod
    def set_master_pin(cls, pin):
        master_pin = PIN(pin=pin)
        cls.pin_set.add(master_pin)

    @classmethod
    def add_pin(cls, pin):
        new_pin = PIN(pin=pin)
        cls.pin_set.add(new_pin)

    @classmethod
    def remove_pin(cls, pin):
        cls.pin_set.objects.filter(pin=pin).delete()

    @property
    def num_pins(self):
        return len(self.pin_set())


class PIN(models.Model):
    pin = models.CharField()
    door_lock = models.ForeignKey(DoorLock, on_delete=CASCADE)

    @classmethod
    def set_pin(cls, pin):
        if len(pin) in [4, 6, 8]:
            cls.pin = pin


class Window(Device):
    is_open = models.BooleanField(default=False)

    class Meta:
        device_type = "Window"

    @classmethod
    def toggle_open(cls):
        cls.is_open = not cls.is_open


class TemperatureSensor(Device):
    celsius = models.BooleanField(default=False)

    class Meta:
        device_type = "Temperature Sensor"

    @classmethod
    def toggle_celsius(cls):
        cls.celsius = not cls.celsius


class MultiSensorDevice(Device):
    volume_level = models.IntegerField(default=5)
    celsius = models.BooleanField(default=False)
    alarm = models.BooleanField(default=True)

    class Meta:
        device_type = "MultiSensorDevice"

    @classmethod
    def toggle_celsius(cls):
        cls.celsius = not cls.celsius

    @classmethod
    def toggle_alarm(cls):
        cls.alarm = not cls.alarm

    @classmethod
    def set_volume(cls, new_volume):
        if new_volume >= 1 and new_volume <= 10:
            cls.volume_level = new_volume


class CoSmokeDetector(Device):
    alarm_noise = models.IntegerField(default=1)
    volume_level = models.IntegerField(default=5)
    alarm = models.BooleanField(default=True)

    class Meta:
        device_type = "CoSmokeDetector"

    @classmethod
    def set_volume(cls, new_volume):
        if new_volume >= 1 and new_volume <= 10:
            cls.volume_level = new_volume

    @classmethod
    def set_alarm(cls, new_alarm):
        if new_alarm >= 1 and new_alarm <= 4:
            cls.alarm_noise = new_alarm

    @classmethod
    def toggle_alarm(cls):
        cls.alarm = not cls.alarm