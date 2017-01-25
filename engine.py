from __future__ import division
import sys
import os
import wave
import importlib
import re


class Engine(object):
	"""
	Morse engine that will encode/decode a text message to morse.
	"""
	# The morse code.
	locale = str
	# The morse loaded library.
	morse_lib = None
	# The stored input as text or signal.
	input = None
	# The stored output as text or signal.
	output = None
	# Words per minute.
	# Standard is 20 words per minute. Default word is a five character word.
	wpm = 20
	# Characters per minute. The speed at which the signal is played.
	# Standard is a 100 characters per minute, without the space. (Add 20)
	real_cpm = 120
	# Speed index.
	# The speed index computed from the real_cpm.
	speed_index = 0.5
	# Signal sound frequency
	freq = 800

	def __init__(self, locale = 'ITU'):
		"""
		Constructor.
		:param locale: The morse code locale (international, us, etc...)
		"""
		self.locale = locale

	def load_morse_lib(self):
		"""
		Loads the morse code for the locale that was set.
		"""
		self.morse_lib = getattr(importlib.import_module("morse"), self.locale.upper())

	def flush_input(self):
		"""
		Flushes the stored input.
		"""
		self.input = None

	def flush_output(self):
		"""
		Flushes the output.
		"""
		self.output = None

	def store_text_input(self, text):
		"""
		Stores a text to be encoded.
		:param text: The text to be encoded.
		"""
		if type(self.input) is 'str':
			self.flush_input()
			self.input += text

	def encode(self, text, locale = None):
		"""
		Encodes a text to a morse signal.
		:param text: The text to encode.
		:param locale: The locale to encode.
		:return:
		"""
		# Buffer to store the encoded text.
		buffer = []
		for char in text:
			# If the character is alphanumeric
			if re.match('[a-zA-Z0-9]', char):
				uchar = char.upper()
				if uchar in self.morse_lib:
					buffer.append(self.morse_lib[uchar])
					buffer.append(self.morse_lib['LSPACE'])
			# If the character is a space
			elif re.match('\s', char):
				buffer.append(self.morse_lib['WSPACE'])
			# If the character is a non word character
			elif re.match('\W', char):
				if char in self.morse_lib:
					buffer.append(self.morse_lib[char])
					buffer.append(self.morse_lib['LSPACE'])
		return buffer

	def decode(self, signal, locale = None):
		"""
		Decodes a morse message to a text message.
		:param message: The message to decode, an array of.
		:param locale: The locale to use for decoding.
		:return:
		"""
		# @todo : add method to get a signal from the input.
		# Buffer to store the decoded message.
		buffer = []
		for s in signal:
			pass

	def compute_speed_index(self, wpm):
		"""
		Computes the index for a given cpm number.
		:param wpm: The words per minute.
		:return: float
		"""
		cpm = wpm * 5
		real_cpm = cpm + wpm

		return (60 / real_cpm) * 0.1

	def play(self, encoded, wpm = None, freq = None):
		"""
		Plays an encoded morse message.
		:param encoded: The encoded message.
		:param wpm: The wpm.
		:param freq: The sound signal frequency.
		"""
		if wpm is not None:
			speed_index = self.compute_speed_index(wpm)
		else:
			speed_index = self.compute_speed_index(self.wpm)
		if freq is None:
			freq = self.freq
		for signal in encoded:
			for subsignal in signal:
				if subsignal is not 0:
					dur = subsignal * speed_index
					os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (dur, freq))
				elif subsignal is 0:
					dur = 1 * speed_index
					os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (dur, 0))
