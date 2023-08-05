# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from ProgettiHWSW.api import API
from ProgettiHWSW.const import (TURN_ON_BASE, TURN_OFF_BASE, TEMP_MONOSTABLE_BASE, TOGGLE_BASE, STATUS_XML_PATH)
import xml.etree.ElementTree as et

class Relay:
	"""Clas that represents a relay object."""

	def __init__(self, api: API, relay_number: int, relay_mode: str):
		"""Initialize Relay class."""
		self.relay_number = relay_number
		self.relay_mode = relay_mode
		self.api = api
		self.state = None

	@property
	def id(self) -> int:
		"""Return the relay number."""
		return self.relay_number

	@property
	def is_on(self) -> bool:
		"""Return if the relay is on."""
		return self.state

	def toggle(self):
		"""Toggle the relay."""
		command = TOGGLE_BASE + self.relay_number 
		self.api.execute(command)

	def control(self, state: bool):
		"""Control the relay state."""
		command = ((TURN_ON_BASE if self.relay_mode == "bistable" else TEMP_MONOSTABLE_BASE) if state == True else TURN_OFF_BASE) + self.relay_number
		self.api.execute(command)

	def update(self):
		"""Update the relay status."""
		request = self.api.request("get", STATUS_XML_PATH)
		resp = request.text
		root = et.fromstring(resp)
		self.state = True if root.find(f"led{self.relay_number}").text == "1" else False