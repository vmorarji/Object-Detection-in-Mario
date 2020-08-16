import cv2
import numpy as np


class detect_cv(object):
	# Detect sprites and return thier locations.
	def __init__(self, frame_size):
		"""
		Args:
		frame_size:
			The observation space of the environment.
			If the observation space size is used to 
			scale the rectangles.
		"""
		self.frame_size = frame_size
		self.x_scale = frame_size[1] / 256
		self.y_scale = frame_size[0] / 240

	def detect(self, frame, frame_grey, sprite_list):
		"""
		Detect obstacles and enemies
		Args:
		frame:
			The frame of environment with the channels in the
			in the order BGR.
		frame_grey:
			The frame in greyscale used for detection.
		sprite_list:
			List of sprites used that will be detected
			in the frame.
		"""
		pt_list = []
		for sprite in sprite_list:
			res = cv2.matchTemplate(frame_grey, sprite[0], cv2.TM_CCOEFF_NORMED)
			loc = np.where(res >= sprite[1])
			for pt in zip(*loc[::-1]):
				cv2.rectangle(frame, pt, (pt[0] + sprite[3], pt[1] + sprite[2]), sprite[4], 2)
				if len(sprite) == 6:
					cv2.putText(frame, sprite[5], (pt[0], pt[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, sprite[4], 1, cv2.LINE_AA)
				pt_list.append(pt)
		return frame, pt_list


	def detectmario(self, frame, frame_grey, sprite_list):
		"""
		Detect Mario in the frame.
		Args:
		frame:
			The frame of environment with the channels in the
			in the order BGR.
		frame_grey:
			The frame in greyscale used for detection.
		sprite_list:
			List of sprites used that will be detected
			in the frame.
		"""
		pt_list = []
		for sprite in sprite_list:
			res = cv2.matchTemplate(frame_grey, sprite[0], cv2.TM_CCOEFF_NORMED)
			loc = np.where(res >= sprite[1])
			for pt in zip(*loc[::-1]):
				pt = (pt[0] - 4, pt[1] - 1)
				cv2.rectangle(frame, pt, (pt[0] + 14, pt[1] + 16), sprite[4], 2)
				if len(sprite) == 6:
					cv2.putText(frame, sprite[5], (pt[0], pt[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, sprite[4], 1, cv2.LINE_AA)
				pt_list.append(pt)
		return frame, pt_list

	def detectgap(self, frame, frame_grey, sprite_list):
		"""
		Detect Mario in the frame.
		Args:
		frame:
			The frame of environment with the channels in the
			in the order BGR.
		frame_grey:
			The frame in greyscale used for detection.
		sprite_list:
			Sprite of the rock used for detection.
		"""
		missing_rock = []
		rock_unique = []
		res = cv2.matchTemplate(frame_grey, sprite_list[0][0], cv2.TM_CCOEFF_NORMED)
		loc = np.where(res >= sprite_list[0][1])
		for pt in zip(*loc[::-1]):
			cv2.rectangle(frame, pt, (pt[0] + sprite_list[0][3], pt[1] + sprite_list[0][2]), sprite_list[0][4], 2)
		if len(loc[0]) > 0:
			for i in range(1, 16):
				pred_value = loc[1][0] + (i * 16)
				if pred_value not in loc[1] and pred_value < 241:
					missing_rock.append(pred_value)
			rock_unique = np.unique(loc[0])
			for i in rock_unique:
				for e in missing_rock:
					cv2.rectangle(frame, (e, i), (e + sprite_list[0][3], i + sprite_list[0][2]), (0,0,255), 2)
		return frame, missing_rock
