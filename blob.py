import numpy as np
from settings import SIZE

class Blob:

	def __init__(self):

		self.x = np.random.randint(0, SIZE)
		self.y = np.random.randint(0, SIZE)

	def __str__(self):
		return f"{self.x}, {self.y}"

	def __sub__(self, other):
		return (self.x - other.x, self.y - other.y)


	def action(self, choice):
		if choice == 0:
			self.move(x=1, y=1)

		elif choice == 1:
			self.move(x=-1, y=-1)

		elif choice == 2:
			self.move(x=-1, y=1)

		elif choice == 3:
			self.move(x=1, y=-1)

	def move(self, x=False, y=False):
		
		if not x:
			self.x += np.random.ranint(-1, 2)
		else:
			self.x += x

		if not y:
			self.y += np.random.ranint(-1, 2)
		else:
			self.y += y

		if self.x < 0:
			self.x = 2
		elif self.x > SIZE-1:
			self.x = SIZE-1

		if self.y < 0:
			self.y = 2
		elif self.y > SIZE-1:
			self.y = SIZE-1














