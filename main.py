import warnings
warnings.filterwarnings("ignore")
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
from blob import Blob
from settings import *

style.use("ggplot")

if start_q_table is None:
	q_table = {}

	for a in range(-SIZE+1, SIZE):
		for b in range(-SIZE+1, SIZE):
			for a1 in range(-SIZE+1, SIZE):
				for b1 in range(-SIZE+1, SIZE):
					q_table[((a, b), (a1, b1))] = [np.random.uniform(-5, 0) for i in range(4)]
else:
	with open(start_q_table, "rb") as file:
		q_table = pickle.load(file)					

episode_rewards = []
for ep in range(HM_EPISODE):

	player = Blob()
	food = Blob()
	enemy = Blob()

	if ep % SHOW_EVERY == 0:

		print(f"on # {ep}, epsilon: {epsilon}")
		print(f"{SHOW_EVERY} episode mean {np.mean(episode_rewards[-SHOW_EVERY:])}")

		show = True
	else:
		show = False


	episode_reward = 0
	for i in range(200):

		obs = (player - food, player-enemy)

		if np.random.random() > epsilon:
			action = np.argmax(q_table[obs])
		else:
			action = np.random.randint(0, 4)

		player.action(action)

		## Enemy and Food movement
		# enemy.move()
		# food.enemy()


		if player.x == enemy.x and player.y == enemy.y:
			reward = -ENEMY_PENALTY	
		elif player.x == food.x and player.y == food.y:
			reward = FOOD_REWARD

		else:
			reward = -MOVE_PENALTY


		new_obs = (player - food, player-enemy)
		max_future_q = np.max(q_table[new_obs])
		current_q = q_table[obs][action]

		if reward == FOOD_REWARD:
			new_q = FOOD_REWARD
		elif reward == -ENEMY_PENALTY:
			new_q = -ENEMY_PENALTY
		else:
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)


		q_table[obs][action] = new_q

		if show:
			env = np.ones((SIZE, SIZE, 3), dtype=np.uint8) * 255
			#print(food.x, food.y, )
			env[food.y][food.x] = d[FOOD_N]
			env[player.y][player.x] = d[PLAYER_N]
			env[enemy.y][enemy.x] = d[ENEMY_N]


			img = Image.fromarray(env, "RGB")

			img = img.resize((500, 500))
			cv2.imshow("", np.array(img))

			if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
				if cv2.waitKey(500) & 0xFF == ord("q"):
					break
			else:
				if cv2.waitKey(1) & 0xFF == ord("q"):
					break


		episode_reward += reward
		if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
		 	break
	episode_rewards.append(episode_reward)
	epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY))/ SHOW_EVERY, mode="valid")

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"reward {SHOW_EVERY}")
plt.xlabel("episode #")
plt.show()


with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
	pickle.dump(q_table, f)