with open("Percipitation.csv") as fp:
		print("Opened Percipitation")
		linesRead = 0
		for line in fp.readline():
			values = line.strip().split(',')
			linesRead += 1
		print(linesRead)