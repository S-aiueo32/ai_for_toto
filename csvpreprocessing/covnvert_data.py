import pandas as pd
import numpy as np
import os
import csv

# チームのリストを取得
def makeTeamList(data):
	teams = []
	teams_columns = data[decoder("アウェイ")]
	for team in teams_columns:
		if (team not in teams):
			teams.append(team)
	return teams

# スコアの分割
def splitScore(score):
	splitted = score.split("-")
	for i in range(0,2):
		splitted[i] = int(splitted[i])
	return splitted

def splitScores(scores):
	score_col = []
	for ele in  scores:
		score_col.append(splitScore(ele))
	return score_col
	
# 列の削除
def dropColumn(data, mode):
	if mode == 1:
		drop_col = ["K/O時刻","スタジアム","入場者数","TV放送"]
	if mode == 2:
		drop_col = ["スコア"]
	for col in drop_col:
		data = data.drop(decoder(col), axis=1)
	return data
 
 #チームの抽出
def extractTeam(data, team):
	home = data[data[decoder("ホーム")] == team]
	away = data[data[decoder("アウェイ")] == team]
	assemble = pd.concat([home, away]).sort_index(ascending=True)
	return assemble.reset_index(drop=True)

# 相手を抽出
def extractOpponent():
	pass

# UTF-8にデコード
def decoder(text):
	return text.decode("utf-8")
	
def convert_data():
	years = range(1992,2017)
	ids = range(1,4)
	for id in ids:
		for year in years:
			try:
				data = pd.read_csv("../data/raw/J" + str(id) + "/J" + str(id) + "_" + str(year) + ".csv", encoding="shift_jis")
				data = dropColumn(data,1)
				
				# ディレクトリ作成
				try:
					os.mkdir("../data/convert")
				except WindowsError:
					pass
				try:
					os.mkdir("../data/convert/J" + str(id))
				except WindowsError:
					pass
				try:
					os.mkdir("../data/convert/J" + str(id) + "/J" + str(id) + "_" + str(year))
				except WindowsError:
					pass
				
				teams = makeTeamList(data)	# チームリスト
				for team in teams:
					# チームの抽出
					teamData = extractTeam(data,team)
					
					# スコアの分割
					for i in range(0,len(teamData)):
						teamData[decoder("スコア")][i] = teamData[decoder("スコア")][i][0:3]
					scores = pd.DataFrame(splitScores(teamData[decoder("スコア")]), columns=list([decoder("得点"),decoder("失点")]))
					teamData = pd.concat([teamData,scores],axis=1)
					teamData = dropColumn(teamData,2)
					
					h_and_a = []	# HorA格納用
					points = []		# 勝ち点格納用
					
					# 行を舐める
					for i in range(0,len(teamData)):
						# 曜日をカット
						teamData[decoder("試合日")][i] = teamData[decoder("試合日")][i][0:5]
						# HorAで入れ換え
						if teamData[decoder("ホーム")][i] != team:
							teamData[decoder("ホーム")][i], teamData[decoder("アウェイ")][i]\
								= teamData[decoder("アウェイ")][i], teamData[decoder("ホーム")][i]
							teamData[decoder("得点")][i], teamData[decoder("失点")][i]\
								= teamData[decoder("失点")][i], teamData[decoder("得点")][i]
							h_and_a.append("A")
						else:
							h_and_a.append("H")
						# 勝ち点を計算
						if i == 0:
							if teamData[decoder("得点")][i] > teamData[decoder("失点")][i]:
								points.append(3)
							elif teamData[decoder("得点")][i] == teamData[decoder("失点")][i]:
								points.append(1)
							else:
								points.append(0)
						else:
							if teamData[decoder("得点")][i] > teamData[decoder("失点")][i]:
								points.append(3+points[i-1])
							elif teamData[decoder("得点")][i] == teamData[decoder("失点")][i]:
								points.append(1+points[i-1])
							else:
								points.append(0+points[i-1])
					
					teamData[decoder("HorA")] = h_and_a
					teamData[decoder("勝ち点")] = points
					teamData.rename(columns={decoder("ホーム"):decoder("チーム"),decoder("アウェイ"):decoder("対戦相手")}, inplace=True)
					#teamData.rename(columns={decoder("ホーム"):decoder("チーム")}, inplace=True)
					teamData.to_csv("../data/convert/J" + str(id) + "/J" + str(id) + "_" + str(year) + "/" + team + "_" + str(year) + ".csv", index=False )
			except IOError:
				pass
				
def team2deviation():
	years = range(1992,2017)
	ids = range(1,4)
	for id in ids:
		for year in years:
			try:
				data = pd.read_csv("../data/raw/J" + str(id) + "/J" + str(id) + "_"+str(year)+".csv", encoding="shift_jis")
				data = dropColumn(data,1)
				teams = makeTeamList(data)	# チームリスト
				#print teams
				for team in teams:
					#勝ち点テーブルの作成
					points = pd.DataFrame()
					for team_ in teams:
						teamData = pd.read_csv("../data/convert/J" + str(id) + "/J" + str(id) + "_" + str(year) + "/" + team_ + "_" + str(year) + ".csv", encoding="shift_jis")
						points[team_] = teamData[decoder("勝ち点")]
						#print points
					#偏差値テーブルの作成
					deviation = pd.DataFrame()
					for i in range(0,len(points)):
						x = points[i:i+1].values
						#print x
						ans = np.round_(50+10*(x-np.average(x))/np.std(x)) #この時点で駄目
						#print pd.DataFrame(ans)
						deviation = pd.concat([deviation,pd.DataFrame(ans)]).reset_index(drop=True)
					deviation.columns = teams
					teamData = pd.read_csv("../data/convert/J" + str(id) + "/J" + str(id) + "_" + str(year) + "/" + team + "_" + str(year) + ".csv", encoding="shift_jis")
					teamData[decoder("チーム")] = deviation[team]
					for i in range(0,len(teamData)):
						teamData[decoder("対戦相手")][i] = deviation[teamData[decoder("対戦相手")][i]][i]
					# ディレクトリ作成
					try:
						os.mkdir("../data/deviation")
					except WindowsError:
						pass
					try:
						os.mkdir("../data/deviation/J" + str(id))
					except WindowsError:
						pass
					try:
						os.mkdir("../data/deviation/J" + str(id) + "/J" + str(id) + "_" + str(year))
					except WindowsError:
						pass
					teamData.to_csv("../data/deviation/J" + str(id) + "/J" + str(id) + "_" + str(year) + "/" + team + "_" + str(year) + ".csv", index=False)
			except IOError:
				pass
				
if __name__ == '__main__':
	team2deviation()