import urllib
import urllib.request
import re
import os.path


# HTMLの行から将棋ウォーズのURLを抽出
def strip_warsurl(line):
	match = re.search(r"href=\"(.+)\">", line)
	return match.group(1)


# HTMLの行から将棋ウォーズの戦法を抽出
# 戦法なしなら戦法なしを返す
def strip_warsbattletype(line):
	match = re.search(r"<small>(.+)</small>", line)
	#if match:
	#	return match.group(1)
	return match.group(1) if match else "#戦法なし"


# 将棋ウォーズの棋譜URLにアクセスして、棋譜の行を抽出する
def get_kifuline(url):
	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as res:
		body = res.readlines()
	# 棋譜を抽出
	l = [s for s in body if 'gameHash' in str(s)]

	return l[0].decode("utf-8")


# まだダウンロードしていない棋譜を抽出
def filter_newkifu(kifus, filename):
	if not os.path.exists(filename):
		return kifus

	with open(filename, 'r') as f:
		kifuurls = f.readlines()
		newkifus = []
		for kifu in kifus:
			if kifu["kifuurl"] + "\n" not in kifuurls:
				newkifus.append(kifu)

	return newkifus


# 将棋ウォーズの棋譜をダウンロードする
# idは名前 gtは10分"", 3分"sb", 10秒"s1"
def download_warskifu(id, gt, limit_num):

	# 将棋ウォーズ 棋譜検索くんにアクセス
	url = "https://shogi.pvs.jp/shogiwars/?ui=" + id + "&gt=" + gt + "&sb=off"
	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as res:
		body = res.read().decode("utf-8")

	# 将棋ウォーズの棋譜URLと戦法の組み合わせを抽出
	kifus = []
	lines = body.split("\n")
	for i, line in enumerate(lines):
		if "kif-pona.heroz.jp/games" in line:
			kifuurl = strip_warsurl(line)
			battle_type = strip_warsbattletype(lines[i-3])
			kifus.append({"kifuurl": kifuurl, "battle_type": battle_type})

	# まだダウンロードしていない棋譜を抽出
	filename = "kifuurl.txt"
	newkifus = filter_newkifu(kifus, filename)

	# ダウンロード数を制限
	if limit_num is not None:
		newkifus = newkifus[:limit_num]

	# 将棋ウォーズの棋譜URLにアクセス
	for i, _ in enumerate(newkifus):
		# 棋譜を抽出
		kifu = get_kifuline(newkifus[i]["kifuurl"])
		newkifus[i]["kifu"] = kifu

	# ダウンロードした棋譜URLを登録
	with open(filename, "a") as f:
		for newkifu in newkifus:
			f.write(newkifu["kifuurl"] + "\n")

	return newkifus