# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

import requests

class API:
	"""Class to interact with the API of ProgettiHWSW boards."""

	def __init__(self, ip: str):
		"""Initialize the API."""
		self.ip = ip

	def request(self, method: str, path: str, **kwargs):
		"""Make raw requests to exposed API."""
		headers = {}
		headers["requestedby"] = "homeassistant"

		return requests.request(
			method, f"{self.ip}/{path}", **kwargs, headers=headers,	
		)

	def execute(self, code: int, **kwargs):
		"""Make requests with API codes for boards."""
		headers = {}
		headers["requestedby"] = "homeassistant"

		return requests.request(
			"get", f"{self.ip}/index.htm?execute={code}", **kwargs, headers=headers,
		)