if __name__ == "__main__":
	print("Opening File")
	with open("Percipitation.csv") as fp:
		print("Opened File")
		linesRead = 0
		for line in fp.readline():
			values = line.strip().split(',')
			linesRead += 1
		print(linesRead)
