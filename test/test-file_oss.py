import unittest
from oss_watchdog.file_oss import OssFileManager
import yaml, time, os, random, string, shutil


class OssFileManagerTest(unittest.TestCase):
    def setUp(self):
        f = open("../config.yaml")
        config = yaml.load(f)
        self.fm = OssFileManager(config["auth_key"],
                                 config["auth_key_secret"],
                                 config["endpoint"],
                                 config["bucket_name"])

        self._timestamp = str(int(time.time()))
        self._file_content_en = ''.join(random.sample(string.ascii_letters+string.digits, 16)) * 16
        self._file_content_ch = "重要的只有一点，那就是如何将绝无仅有的今日过得无以伦比。"
        self._root = "temp/test-root/"
        self._dir_en = self._root + "test-" + self._timestamp + "-GhostInTheShell/"
        self._dir_ch = self._root + "test-" + self._timestamp + "-攻壳机动队/"
        self._file_en = "test_" + self._timestamp + "_Tachikoma.txt"
        self._file_ch = "test_" + self._timestamp + "_塔奇克玛.txt"

        shutil.rmtree(self._root, True)
        os.mkdir(self._root)
        os.mkdir(self._dir_en)
        with open(self._dir_en + self._file_en, 'w') as file_en:
            file_en.write(self._file_content_en)
        with open(self._dir_en + self._file_ch, 'w') as file_ch:
            file_ch.write(self._file_content_ch)
        os.mkdir(self._dir_ch)
        with open(self._dir_ch + self._file_en, 'w') as file_en:
            file_en.write(self._file_content_en)
        with open(self._dir_ch + self._file_ch, 'w') as file_ch:
            file_ch.write(self._file_content_ch)

    def test_upload(self):
        res = self.fm.upload(self._dir_en + self._file_en,
                             self.fm.norm_path(self._dir_en + self._file_en))
        self.assertEqual(res.status, 200, "test_upload failed")

    def tearDown(self):
        self.fm = None


if __name__ == "__main__":
    unittest.main()
