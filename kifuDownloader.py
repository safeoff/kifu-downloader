import urllib
import urllib.request
import re


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
	return match.group(1) if match else "戦法なし"


# 将棋ウォーズの棋譜URLにアクセスして、棋譜の行を抽出する
def get_kifuline(url):
	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as res:
		body = res.readlines()
	# 棋譜を抽出
	l = [s for s in body if 'receiveMove' in str(s)]

	return l[0].decode("utf-8")


# 将棋ウォーズの棋譜をダウンロードする
# idは名前 gtは10分"", 3分"sb", 10秒"s1"
def download_warskifu(id, gt):

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
			kifu = strip_warsurl(line)
			battle_type = strip_warsbattletype(lines[i-3])
			kifus.append({"kifu": kifu, "battle_type": battle_type})

	# 将棋ウォーズの棋譜URLにアクセス
	for i, _ in enumerate(kifus):
		# 棋譜を抽出
		kifu = get_kifuline(kifus[i]["kifu"])
		kifus[i]["kifu"] = kifu

	return kifus