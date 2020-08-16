# Using Object Detection to Play Mario

A simple OpenCV object detection of sprites within an emulated game of Super Mario Bros. Using the relative locations of Mario against enemies and obstacles, an agent can be used to play the level 1-1 to completion.

![alt text](https://github.com/vmorarji/Object-Detection-in-Mario/blob/master/assets/Mario.gif "Level 1-1")


### Requirements


gym: `pip install gym`

nes-py:	`pip install nes-py`

Super Mario: `pip install gym-super-mario-bros`

numpy: `pip install numpy`

OpenCV:  `pip install opencv-python`



### Running the Agent

The Agent will play based on the how close Mario is to enemies, gaps and obstacles. For example, as Mario approaches an enemy “Enemy close” will increase, `--enemy_factor` is the maximum value that “Enemy close” can take before Mario will jump right.

|Arg|Default|Description
|------------------|-------------------------------|-----------------------------|
|`--enemy_factor`| 0.95| The maximum value “Enemy close” can have before Mario jumps|
|`--gap_factor`|0.9| The maximum value “Gap close” can have before Mario jumps |
|`--obstacle_factor`|0.9| The maximum value “Obstacle close” can have before Mario jumps |
