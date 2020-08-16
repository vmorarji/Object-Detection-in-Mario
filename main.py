import gym
import numpy as np
import imageio
from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import RIGHT_ONLY
import cv2
from wrappers import MaxAndSkipEnv
from load_sprites import load_images
from detect import detect_cv
from metrics import metrics
import argparse


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--enemy_factor", default=0.95, type=float, help='Maximum enemy closeness before jumping')
	parser.add_argument("--gap_factor", default=0.9, type=float, help='Maximum obstacle closeness before jumping')
	parser.add_argument("--obstacle_factor", default=0.9, type=float, help='Maximum gap closeness before jumping')
	args = parser.parse_args()

	# Load the envirinment
	env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')

	env = JoypadSpace(env, RIGHT_ONLY)
	env = MaxAndSkipEnv(env, 4) # only process 1/4 frames

	observation_space = env.observation_space.shape

	# Load the sprites
	mario_list, enemy_list, obstacle_list, brick_list, rock_list = load_images()

	# Initialise the detection and the 
	detection = detect_cv(observation_space)
	analyse = metrics(observation_space)

	def action_selection(enemy_no, enemy_close, obstacle_close, obstacle_height, gap_close, gap_distance, timesteps):
		"""
		Select an action based on set parameters.
		Args:
		enemy_no: 
			The number of enemies in the frame
		enemy_close: 
			The factor for the closest enemy to mario. The larger 
			the number the closer the enemy.
		obstacle_close:
			The factor for the closest obstacle to mario. The larger 
			the number the closer the obstacle.
		obstacle_height:
			The height of the obstacle. Useful for getting over large 
			pipes.
		gap_close:
			The factor for the closest gap to mario. The larger 
			the number the closer the gap.
		gap_distance:
			The length of the gap.
		timesteps:
			The total number of frames played of the level.
		"""
		if enemy_close > args.enemy_factor:
			return 4 # jump right
		elif gap_close > args.gap_factor:
			return 4 # jump right
		elif cnt % 9 == 0:
			return 0 # noop, used to reset the jump
		elif obstacle_close > args.obstacle_factor:
			return 4 # jump right
		else:
			return 1 # walk right

	for i in range(1):
		state = env.reset()
		avg_loss = 0
		cnt = 0
		reward_total = 0
		reward_counter = 0
		while True:
			#env.render()

			# change the state colours to match openCV's imshow
			frame = cv2.cvtColor(state, cv2.COLOR_RGB2BGR)
			frame_grey = cv2.cvtColor(state, cv2.COLOR_RGB2GRAY)

			# Detect sprites in the frame
			frame, mario_loc = detection.detectmario(frame, frame_grey, mario_list)
			frame, enemy_loc = detection.detect(frame, frame_grey, enemy_list)
			frame, obstacle_loc = detection.detect(frame, frame_grey, obstacle_list)
			frame, brick_loc = detection.detect(frame, frame_grey, brick_list)
			frame, gap_x = detection.detectgap(frame, frame_grey, rock_list)

			# Calculate the metrics
			mario_location, enemy_no, closest_enemy, closest_obstacle, obstacle_height, closest_gap, gap_length = analyse.compute(mario_loc, enemy_loc, obstacle_loc, gap_x)

			# Place the metrics on the frame
			font = cv2.FONT_HERSHEY_SIMPLEX
			frame = cv2.putText(frame, 'Mario: {}'.format(mario_location), (10, 40), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Enemy no.: {}'.format(enemy_no), (10, 50), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Enemy close: {:.2f}'.format(closest_enemy), (10, 60), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Obstacle close: {:.2f}'.format(closest_obstacle), (10, 70), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Obstacle height: {:.2f}'.format(obstacle_height), (10, 80), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Gap close: {:.2f}'.format(closest_gap), (10, 90), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Gap distance: {}'.format(gap_length), (10, 100), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)

			# Display the run
			cv2.imshow("gif", frame)
			if cv2.waitKey(1)&0xFF == ord('q'):
				break

			# Select the next acttion using the metrics
			action = action_selection(enemy_no, closest_enemy, closest_obstacle, obstacle_height, closest_gap, gap_length, cnt)

			# play the next action
			next_state, reward, done, info = env.step(action)
			reward_total += reward
			state = next_state
			if done:
				print(cnt, reward_total)
				break
			cnt +=1

	env.close()
	cv2.destroyAllWindows()