import pandas as pd
import numpy as np


def decoder(text):
	return text.decode("utf-8")

'''	csvì«Ç›çûÇ›
'''
dir_data = "./data/deviation/J3/J3_2014/ã‡ëÚ_2014.csv"
data = pd.read_csv(dir_data, encoding="shift_jis")

#size_data = [len(data.index), len(data.columns)]
#for i in range(0, len(data.index))
win_img = data.iloc[0:5,4:9]
win_img = pd.concat([win_img.iloc[:,2:5], win_img.iloc[:,0:2]], axis=1)
for i in range(0, len(win_img)):
	if win_img["HorA"][i] == "H":
		win_img["HorA"][i] = 1
	else:
		win_img["HorA"][i] = 0
for i in range(0, len(win_img.columns)):
	win_img.rename(columns={win_img.columns[i]: str(i)}, inplace=True)
win_img.reset_index(drop=True, inplace=True)
win_img.to_csv("tmp.csv", index=False )