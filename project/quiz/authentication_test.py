import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 设置当前工作目录为项目目录
os.chdir(os.path.join(script_dir, '..'))

# 然后再导入 Django 设置
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_wsgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_wsgi_application()
def test_authentication(username, password):
    user = authenticate(username=username, password=password)

    if user is not None:
        print(f"Authentication successful: {user}")
        # 繼續處理登入成功的邏輯
    else:
        print("Authentication failed")
        # 處理登入失敗的邏輯

# 測試用戶名和密碼
test_username = "aa"
test_password = "123"

# 執行身份驗證測試
test_authentication(test_username, test_password)
