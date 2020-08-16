import cv2


def load_images(world=1, level=1):
	"""load the sprites based on the level and world. 
	Note: only 1-1 currently available"""
	mario = cv2.imread('./sprites/mario/mario-small-right.png', 0)
	goomba1 = cv2.imread('./sprites/enemies/goomba1.png', 0)
	goomba2 = cv2.imread('./sprites/enemies/goomba2.png', 0)
	koopa1 = cv2.imread('./sprites/enemies/koopa1.png', 0)
	koopa2 = cv2.imread('./sprites/enemies/koopa2.png', 0)
	koopa3 = cv2.imread('./sprites/enemies/koopa3.png', 0)
	koopa4 = cv2.imread('./sprites/enemies/koopa-shell.png', 0)
	pipe1 = cv2.imread('./sprites/obstacle/pipe-up.png', 0)
	rock = cv2.imread('./sprites/misc/rock.png', 0)
	block = cv2.imread('./sprites/obstacle/block-chiseled.png', 0)
	flagpole = cv2.imread('./sprites/misc/flagpole.png', 0)
	question1 = cv2.imread('./sprites/misc/question1.png', 0)
	question2 = cv2.imread('./sprites/misc/question2.png', 0)
	question3 = cv2.imread('./sprites/misc/question3.png', 0)
	brick = cv2.imread('./sprites/misc/brick.png', 0)

	# intantiate the colour for the rectangles
	red = (0,0,255)
	blue = (255,0,0)
	green = (0,255,0)
	# load the sprites for the specific level
	# sprite, threshold, height, width, colour
	if world == 1:
		if level == 1:
			mario_list = [(mario, 0.8, mario.shape[0], mario.shape[1], red, 'Mario')]

			enemy_list = [(goomba1, 0.7, goomba1.shape[0], goomba1.shape[1], green, 'Goomba'),
						(goomba2, 0.7, goomba2.shape[0], goomba2.shape[1], green, 'Goomba'),
						(koopa1, 0.7, koopa1.shape[0], koopa1.shape[1], green, 'Goomba'),
						(koopa2, 0.7, koopa2.shape[0], koopa2.shape[1], green, 'Koopa'),
						(koopa3, 0.7, koopa3.shape[0], koopa3.shape[1], green, 'Koopa'),
						(koopa4, 0.7, koopa4.shape[0], koopa4.shape[1], green, 'Koopa')]

			obstacle_list = [(pipe1, 0.8, pipe1.shape[0], pipe1.shape[1], blue),
							(block, 0.8, block.shape[0], block.shape[1], blue)]

			brick_list = [(brick, 0.9, brick.shape[0], brick.shape[1], blue),
						(question1, 0.9, question1.shape[0], question1.shape[1], blue),
						(question2, 0.9, question2.shape[0], question2.shape[1], blue),
						(question3, 0.9, question3.shape[0], question3.shape[1], blue)]

			rock_list = [(rock, 0.8, rock.shape[0], rock.shape[1], blue)]

	return mario_list, enemy_list, obstacle_list, brick_list, rock_list