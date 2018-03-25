import pyaudio
import wave
import sys

from time import sleep
from threading import Thread, Lock
from pytox import Tox, ToxAV
from MenuUI import MenuUi
from MenuPage import MenuPageIncomingCall, MenuPageCall

SERVER = ["217.182.143.254", 2306, "7AED21F94D82B05774F697B209628CD5A9AD17E0C073D9329076A4C28ED28147"]
FORMAT = pyaudio.paInt16
RATE = 8000
CHANNELS = 1
SAMPLE = int(RATE * 60 / 1000)

DATA = 'echo.data'

audio = pyaudio.PyAudio()

class ToxOptions():
	''' Tox options class.
	
	Define some default options
	'''
	def __init__(self):
		self.ipv6_enabled = True
		self.udp_enabled = True
		self.proxy_type = 0  # 1=http, 2=socks
		self.proxy_host = ''
		self.proxy_port = 0
		self.start_port = 0
		self.end_port = 0
		self.tcp_port = 0
		self.savedata_type = 0  # 1=toxsave, 2=secretkey
		self.savedata_data = b''
		self.savedata_length = 0
		self.savedata_path = ''
		
		
		
class ToxPhoneAV(ToxAV):
	''' AV class.
	
	Used to declare the callbacks
	
	:param core: a tox session
	:type core: Tox object
	'''
	def __init__(self, core):
		super().__init__(core)
		self.core = self.get_tox()
		
	def on_call(self, friend_number, audio_enabled, video_enabled):
		""" On call callback from tox object. Default implementation does nothing.
		
		:param friend_number: the number of the friend calling
		:type friend_number: int
		:param audio_enabled: True if audio is enabled
		:type audio_enabled: bool
		:param video_enabled: True if video is enabled
		:type video_enabled: bool
		"""
		pass
				                
	def on_call_state(self, friend_number, state):
		""" Called when there is a change in the call's state. Default implementation does nothing.
		
		:param friend_number: friend number
		:type friend_number: int
		:param state: call's state
		:type state: int
		"""
		pass

	def on_bit_rate_status(self, friend_number, audio_bit_rate, video_bit_rate):
		""" Called when there is a change in the bit rate status (WHAT ?). Default implementation does nothing.
		
		:param friend_number: friend number
		:type friend_number: int
		:param audio_bit_rate: audio bit rate
		:type audio_bit_rate: int16
		:param video_bit_rate: video bit rate
		:type video_bit_rate: int16
		"""
		pass

	def on_audio_receive_frame(self, friend_number, pcm, sample_count, channels, sampling_rate):
		""" Called when an audio frame is received. Default implementation does nothing.
		
		:param friend_number: friend number
		:type friend_number: int
		:param pcm: pcm data
		:type pcm: bytes
		:param sample_count: sample count
		:type sample_count: int
		:param channels: number of channels
		:type channels: int
		:param sampling_rate: sampling rate
		:type sampling_rate: int16
		"""
		pass
		
		
		
class ToxPhone(MenuUi, Tox):
	"""
	Act as a controller for the whole UI and the tox session
	Manage the breadcrumb (tracking of the navigation), the current page and the tox session
	
	:param surface: a pygame.Surface object where we will be drawing the UI
	:type surface: pygame.Surface object
	:param start_page: a MenuPage object representing the tree of the UI
	:type start_page: MenuPage object
	:param tox: a tox session
	:type tox: Tox object
	"""
	
	def __init__(self, surface, start_page, tox_opts):
		MenuUi.__init__(self, surface, start_page)
		if tox_opts is not None:
			Tox.__init__(self, tox_opts)
		
		self.self_set_name("Toxphone")
		print('ID: %s' % self.self_get_address())
        
		self.av = ToxPhoneAV(self)
		
		self.ring_enabled = False
		self.ringtone = wave.open('res/audio/ringtone.wav', 'rb')
		self.ring_stream = None
		self.ring_thread = None
		
		self.aostream = None
		self.aistream = None
		
		self.av.on_call = self.on_call
		self.av.on_call_state = self.on_call_state
		self.av.on_bit_rate_status = self.on_bit_rate_status
		self.av.on_audio_receive_frame = self.on_audio_receive_frame
		
		self.iterate_lock = Lock()

		'''
		self.core_iterate_thread_stop = False
		self.core_iterate_thread = Thread(target=self.core_iterate)
		self.core_iterate_thread.daemon = True
		self.core_iterate_thread.start()
		
		self.av_iterate_thread_stop = False
		self.av_iterate_thread = Thread(target=self.av_iterate)
		self.av_iterate_thread.daemon = True
		self.av_iterate_thread.start()
		'''
		
		self.call_status = {'status': False, 'friend_number': None}
		self.device_index = 0
		self.audio_buffer = b''
		
		print('========== AUDIO DEVICES ==========')
		for i in range(audio.get_device_count()):
			if audio.get_device_info_by_index(i)['name'] == 'pulse':
				self.device_index = i
				print(audio.is_format_supported(RATE, input_device=self.device_index, input_channels=CHANNELS, input_format=pyaudio.paInt16))
			print(audio.get_device_info_by_index(i))
			
		self.connect()
	
	
	def connect(self):
		""" Connect to the DHT
		"""
		print('connecting...')
		self.bootstrap(SERVER[0], SERVER[1], SERVER[2])
		
	def core_iterate(self):
		print("Launching core iterate thread...")
		while not self.core_iterate_thread_stop:
			if self.iterate_lock.acquire(True):
				self.iterate()
				self.iterate_lock.release()
				sleep((self.iteration_interval() * 1.0) / 1000.0)
		
	def av_iterate(self):
		print("Launching av iterate thread...")
		while not self.av_iterate_thread_stop:
			if self.iterate_lock.acquire(True):
				self.av.iterate()
				self.iterate_lock.release()
				sleep((self.av.iteration_interval() * 1.0) / 1000.0)
	
	
	def prepare_call(self, friend_number):
		""" Prepare transmission
		
		:param friend_number: friend number
		:type friend_number: int
		"""
		print("Preparing call for number %d" % friend_number)
		
		self.call_status['status'] = True
		self.call_status['friend_number'] = friend_number
		
		self.aistream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, output_device_index=self.device_index, input_device_index=self.device_index, frames_per_buffer=SAMPLE, stream_callback=self.audio_send)
		self.aistream.start_stream()
        
	def kill_call(self):
		""" Kill the call
		"""
		if self.aostream:
			self.aostream.close()
			self.aostream = None
			
		if self.aistream:
			self.aistream.stop_stream()
			self.aistream.close()
			self.aistream = None
			
		self.call_status['friend_number'] = None
		self.call_status['status'] = False
        
	def on_friend_request(self, pk, message):
		""" Called when receiving a friend request
		
		:param pk: public key
		:type pk: str
		:param message: request message
		:type message: str
		"""
		print('Friend request from %s: %s' % (pk, message))
		self.friend_add_norequest(pk)
		print('Accepted.')
		self.save_tox_conf()
		
	def on_friend_message(self, friend_number, type, message):
		""" Called when receiving a message from a friend
		
		:param friend_number: friend number
		:type friend_number: int
		:param message: sent message
		:type message: str
		"""	
		self.friend_send_message(friend_number, self.MESSAGE_TYPE_NORMAL, "I can't receive messages yet...")
        
	def list_friends(self):
		""" List friends in a more complete way.
		
		:returns: a more complete list of friends
		:rtype: list
		"""
		friend_list = []
		for friend_number in self.self_get_friend_list():
			friend = [friend_number, self.friend_get_name(friend_number), self.friend_get_connection_status(friend_number), self.friend_get_status(friend_number)]
			friend_list.append(friend)
		return friend_list
	
	def call(self, friend_number):
		""" Call a friend
		
		:param friend_number: friend number
		:type friend_number: int
		"""
		self.av.call(friend_number, int(RATE/1000), 0)
		self.go_to_page(MenuPageCall(self, friend_number))
		
	def hangup(self, friend_number):
		""" Hangup a call
		
		:param friend_number: friend number
		:type friend_number: int
		"""
		self.kill_call()
		self.av.call_control(friend_number, self.av.CALL_CONTROL_CANCEL)
		self.return_page()
		
	def answer(self, friend_number):
		""" Answer a call
		
		:param friend_number: number of the friend calling
		:type friend_number: int
		"""
		self.stop_ring()
		print("Answering incoming call")
		if self.av.answer(friend_number, int(RATE/1000), 0):
			self.prepare_call(friend_number)
			print("Call established!")
		self.set_current_page(MenuPageCall(self, friend_number))
			
	def ring(self):
		""" Ring the phone
		"""
		self.ring_stream = audio.open(
			format=audio.get_format_from_width(self.ringtone.getsampwidth()),
			channels=self.ringtone.getnchannels(),
			rate=self.ringtone.getframerate(),
			output_device_index=1,
			output=True)
		self.ring_enabled = True
		self.ring_thread = Thread(target=self.audio_ring)
		self.ring_thread.daemon = True
		self.ring_thread.start()
		
	def audio_ring(self):
		""" Thread for the ring's audio playback
		"""
		while self.ring_enabled:
			data = self.ringtone.readframes(1024)
			if self.ringtone.tell() < self.ringtone.getnframes():
				self.ring_stream.write(data)
			else:
				self.ringtone.rewind()
	
	def stop_ring(self):
		""" Stop the ring
		"""
		self.ring_enabled = False
		if self.ring_thread:
			self.ring_thread.join()
		self.ringtone.rewind()
		self.ring_stream.stop_stream()
		self.ring_stream.close()
		
	def on_call(self, friend_number, audio_enabled, video_enabled):
		""" On call callback from tox object
		
		:param friend_number: the number of the friend calling
		:type friend_number: int
		:param audio_enabled: True if audio is enabled
		:type audio_enabled: bool
		:param video_enabled: True if video is enabled
		:type video_enabled: bool
		"""
		print("Incoming call: %d, %d, %d" % (friend_number, audio_enabled, video_enabled))
		
		if video_enabled:
			self.av.call_control(friend_number, self.av.CALL_CONTROL_CANCEL)
			print("Cancelled video call")
			self.friend_send_message(friend_number, self.MESSAGE_TYPE_NORMAL, "I'm a phone, I can't accept video calls.\nPlease retry with an audio call.")
		else:
			self.go_to_page(MenuPageIncomingCall(self, friend_number))
			self.ring()
			
	def on_call_state(self, friend_number, state):
		""" Called when there is a change in the call's state
		
		:param friend_number: friend number
		:type friend_number: int
		:param state: call's state
		:type state: int
		"""
		if state is self.av.FRIEND_CALL_STATE_FINISHED:
			print('Call %d finished' % (friend_number))
			self.kill_call()
			self.return_page()
		elif state is self.av.FRIEND_CALL_STATE_ERROR:
			print('Error on call %d' % (friend_number))
			self.kill_call()
		elif state is 60:
			print('Number %d picking up' % (friend_number))
			self.prepare_call(friend_number)
		else:
			print('Call %d sent status number %d' % (friend_number, state))

	def on_bit_rate_status(self, friend_number, audio_bit_rate, video_bit_rate):
		""" Called when there is a change in the bit rate status (WHAT ?)
		
		:param friend_number: friend number
		:type friend_number: int
		:param audio_bit_rate: audio bit rate
		:type audio_bit_rate: int16
		:param video_bit_rate: video bit rate
		:type video_bit_rate: int16
		"""
		print('bit rate status: fn=%d, abr=%d, vbr=%d' %
				(friend_number, audio_bit_rate, video_bit_rate))

	def on_audio_receive_frame(self, friend_number, pcm, sample_count, channels, sampling_rate):
		""" Called when an audio frame is received
		
		:param friend_number: friend number
		:type friend_number: int
		:param pcm: pcm data
		:type pcm: bytes
		:param sample_count: sample count
		:type sample_count: int
		:param channels: number of channels
		:type channels: int
		:param sampling_rate: sampling rate
		:type sampling_rate: int16
		"""
		'''
		if not self.aostream:
			self.aostream = audio.open(format=FORMAT, channels=channels, rate=sampling_rate, output_device_index=0, output=True)
			self.aostream_set = True
		'''
		#print('audio frame: %d, %d, %d, %d' % (friend_number, sample_count, channels, sampling_rate))
		#print('pcm len:%d, %s' % (len(pcm), str(type(pcm))))
		#if len(pcm) is not 5760:
		#	self.audio_buffer += pcm
			#print('audio_buffer len: %d, %s' % (len(self.audio_buffer), str(type(self.audio_buffer))))
		pass
		'''
		try:
			self.aostream.write(pcm, sample_count)
		except IOError as e:
			print(e)
		'''
		
			
	def audio_send(self, in_data, frame_count, time_info, status_flags):
		if len(self.audio_buffer) > 0:
			data = self.audio_buffer[0:frame_count]
			self.audio_buffer = self.audio_buffer[frame_count:-1]
		else:
			data = None
			
		try:
			self.av.audio_send_frame(self.call_status['friend_number'], in_data, SAMPLE, CHANNELS, RATE)
		except Exception as e:
			print(e)
		
		#print("Ready to return shit")
		return (data, pyaudio.paContinue)
		
	
	def tox_kill(self):
		Tox.kill(self)
		
	def save_tox_conf(self):
		data = self.get_savedata()
		with open(DATA, 'wb') as f:
			f.write(data)

	def load_tox_conf(self):
		return open(DATA, 'rb').read()
	
	def on_self_connection_status(self, status):
		print("status : %d" % (status))
		self.topbar.on_self_connection_status(status)
		
		
		
