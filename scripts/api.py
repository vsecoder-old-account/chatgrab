import os
import random
import subprocess
import requests

def test_web(url):
	try:
		r = requests.get(url)
		result = {
			'status_code': r.status_code,
			'text': r.text,
			'headers': str(r.headers)
		}
		return result
	except Exception as e:
		result = {
			'error': e
		}
		return result
