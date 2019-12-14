import unittest
import pprint
import kifuDownloader
import os
import os.path


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


	# まだダウンロードしていない棋譜を抽出（初めての場合）
	def test_filter_newkifu1(self):
		# arrange
		urls = [{"kifu": "new1"}, {"kifu": "new2"}]
		filename = "test_filter_newkifu.txt"
		if os.path.exists(filename):
			os.remove(filename)
		# act
		result = kifuDownloader.filter_newkifu(urls, filename)
		# assert
		pprint.pprint(result)
		#self.assertEqual(result[0]["kifu"], expected_value)
		self.assertEqual(len(urls), len(result))


	# まだダウンロードしていない棋譜を抽出（2回め以降）
	def test_filter_newkifu2(self):
		# arrange
		urls = [{"kifu": "https://kif-pona.heroz.jp/games/safeoff-maiden77777-20191214_061829"}, {"kifu": "old"}]
		filename = "test_filter_newkifu.txt"
		with open(filename, "w") as f:
			f.write("old\n")
		expected_value = "https://kif-pona.heroz.jp/games/safeoff-maiden77777-20191214_061829"
		# act
		result = kifuDownloader.filter_newkifu(urls, filename)
		# assert
		pprint.pprint(result)
		self.assertEqual(result[0]["kifu"], expected_value)