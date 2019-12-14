import unittest
import pprint
import kifuDownloader


class TestkifuDownloader(unittest.TestCase):

	# ウォーズの棋譜を取得する（10分切れ）
	def test_download_warskifu1(self):
		# arrange
		id = "safeoff"
		gt = ""
		# act
		result = kifuDownloader.download_warskifu(id, gt)

		pprint.pprint(result)


	# ウォーズの棋譜を取得する（3分切れ）
	def test_download_warskifu2(self):
		# arrange
		id = "safeoff"
		gt = "sb"
		# act
		result = kifuDownloader.download_warskifu(id, gt)

		pprint.pprint(result)


	# ウォーズの棋譜を取得する（10秒指し）
	def test_download_warskifu3(self):
		# arrange
		id = "safeoff"
		gt = "s1"
		# act
		result = kifuDownloader.download_warskifu(id, gt)

		pprint.pprint(result)


# ウォーズの棋譜URLにアクセスして棋譜部分を抽出する
	def test_get_kifuline(self):
		# arrange
		url = "https://kif-pona.heroz.jp/games/safeoff-maiden77777-20191214_061829"
		# act
		result = kifuDownloader.get_kifuline(url)

		pprint.pprint(result)