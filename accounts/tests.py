from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver

class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        # 親クラスのメソッド呼び出し
        super().setUpClass()
        # ChromeDriver配置場所
        cls.selenium = WebDriver(executable_path='C:/Django/venv_private_diary/private_diary/static/webdriver/chromedriver.exe')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        # 親クラスのメソッド呼び出し
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('account_login')))

        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        # 登録済みユーザーのメールアドレス
        username_input.send_keys('k-iguchi@aisys-p.work')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('asdf7890')
        self.selenium.find_element_by_class_name('btn').click()

        # ページタイトルの検証
        self.assertEquals('日記一覧 | Private Diary',self.selenium.title)
