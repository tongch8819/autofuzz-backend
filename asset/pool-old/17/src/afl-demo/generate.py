import random


def main():
	length = random.randint(1, 100)
	rst = ""
	for _ in range(length):
		rst += chr(random.randint(0, 255))
	print("Length: " + str(len(rst)))
	print(rst)

	


if __name__ == "__main__":
	main()
