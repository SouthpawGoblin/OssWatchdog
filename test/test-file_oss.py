import unittest
from oss_watchdog.file_oss import OssFileManager
import yaml, time, os, random, string, shutil


class OssFileManagerTest(unittest.TestCase):
    def setUp(self):
        f = open("../config.yaml")
        config = yaml.load(f)
        self.t_class = OssFileManager(config["auth_key"],
                                      config["auth_key_secret"],
                                      config["endpoint"],
                                      config["bucket_name"])

        self._timestamp = str(int(time.time()))
        self._file_content_en = ''.join(random.sample(string.ascii_letters+string.digits, 16)) * 16
        self._file_content_ch = "重要的只有一点，那就是如何将绝无仅有的今日过得无以伦比。"
        self._test_dir_root = "temp/test-root/"
        self._test_dir_en = self._test_dir_root + "test-" + self._timestamp + "-GhostInTheShell/"
        self._test_dir_ch = self._test_dir_root + "test-" + self._timestamp + "-攻壳机动队/"

        shutil.rmtree(self._test_dir_root, True)
        os.mkdir(self._test_dir_root)
        os.mkdir(self._test_dir_en)
        with open(self._test_dir_en + "test_" + self._timestamp + "_Tachikoma.txt", 'w') as file_en:
            file_en.write(self._file_content_en)
        with open(self._test_dir_en + "test_" + self._timestamp + "_塔奇克玛.txt", 'w') as file_ch:
            file_ch.write(self._file_content_ch)
        os.mkdir(self._test_dir_ch)
        with open(self._test_dir_ch + "test_" + self._timestamp + "_Tachikoma.txt", 'w') as file_en:
            file_en.write(self._file_content_en)
        with open(self._test_dir_ch + "test_" + self._timestamp + "_塔奇克玛.txt", 'w') as file_ch:
            file_ch.write(self._file_content_ch)

    def test_test(self):
        self.assertEqual(1, 2, "fail test")

    def tearDown(self):
        self.t_class = None


if __name__ == "__main__":
    unittest.main()
