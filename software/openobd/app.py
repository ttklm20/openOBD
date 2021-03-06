"""Main app for openOBD"""

import sys
sys.path.append('../')

from config.iconfiguration import IConfiguration
from config.configuration import Configuration

from obd.iobddevice import IOBDDevice
from obd.obddevice import OBDDevice
from obd.mockobddevice import MockOBDDevice

from gps.igpsdevice import IGPSDevice
from gps.mockfixedgpsdevice import MockFixedGPSDevice
from gps.gps3device import GPS3Device

from accelerometer.iacceldevice import IAccelDevice
from accelerometer.mockfixedacceldevice import MockFixedAccelDevice
from accelerometer.mpuacceldevice import MPUAccelDevice

from thermo.ithermodevice import IThermoDevice
from thermo.mockfixedthermodevice import MockFixedThermoDevice
from thermo.mockrisingthermodevice import MockRisingThermoDevice
from thermo.mputhermodevice import MPUThermoDevice

from volt.ivoltdevice import IVoltDevice
from volt.mockvoltdevice import MockVoltDevice

from baro.ibarodevice import IBaroDevice
from baro.mockbarodevice import MockBaroDevice

from manager.manager import Manager
from devicecollection.devicecollection import DeviceCollection


class App():
	def __init__(self):
		self.CONFIG_FILENAME = 'config/config.ini'
		self._config = None
		self._api = None
		self._gpsDevice = None
		self._accelDevice = None
		self._thermoDevice = None
		self._voltDevice = None
		self._baroDevice = None
		self._obdDevice = None
		self.read_configuration_file()
		self.configure_obd()
		self.configure_gps()
		self.configure_thermo()
		self.configure_acceleromenter()
		self.configure_volt()
		self.configure_baro()

		self._deviceList = DeviceCollection(thermoDevice = self._thermoDevice,
			gpsDevice = self._gpsDevice, accelDevice = self._accelDevice,
			voltDevice = self._voltDevice, baroDevice = self._baroDevice,
			obdDevice = self._obdDevice)
		self._manager = Manager(self._config, self._deviceList)

	def read_configuration_file(self):
		self._config = Configuration()
		self._config.read(self.CONFIG_FILENAME)

	def configure_obd(self):
		if self._config.obd_device == "obd":
			self._obdDevice = OBDDevice()
		elif self._config.obd_device == "mock":
			self._obdDevice = MockOBDDevice()
		else:
			print("incorrect obd config")

	def configure_gps(self):
		if self._config.gps_device == "fixed_mock":
			self._gpsDevice = MockFixedGPSDevice()
		elif self._config.gps_device == "gps3":
			self._gpsDevice = GPS3Device()
		else:
			print("incorrect gps config")

	def configure_thermo(self):
		if self._config.thermo_device == 'fixed_mock':
			self._thermoDevice = MockFixedThermoDevice()
		elif self._config.thermo_device == 'rising_mock':
			self._thermoDevice = MockRisingThermoDevice()
		elif self._config.thermo_device == "mpu":
			self._thermoDevice = MPUThermoDevice()
		else:
			print("incorrect thermo config")

	def configure_acceleromenter(self):
		if self._config.accel_device == "fixed_mock":
			self._accelDevice = MockFixedAccelDevice()
		elif self._config.accel_device == "mpu":
			self._accelDevice = MPUAccelDevice()
		else:
			print("incorrect accel config")

	def configure_volt(self):
		if self._config.volt_device == 'mock':
			self._voltDevice = MockVoltDevice()
		else:
			print("incorrect volt config")

	def configure_baro(self):
		if self._config.baro_device == 'mock':
			self._baroDevice = MockBaroDevice()
		else:
			print("incorrect baro config")

	def run(self):
		self._manager.print_all_accumulator_means()

if __name__ == '__main__':
	app = App()
	app.run()
