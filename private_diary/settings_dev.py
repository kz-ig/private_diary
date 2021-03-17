# 本番運用環境と開発環境、共通の設定ファイルを読み込み
from .settings_common import *

# DEBUG = Trueにすることでエラー発生時にデバック情報を画面に出力。
# 開発環境ではTrue。本番運用環境ではセキュリティの観点からFalseにする
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ロギング設定
LOGGING = {
    'version': 1, # 1固定
    'disable_existing_loggers': False, # 既存のロガーを無効化する設定

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'diary': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler', # StreamHandlerはコンソールへ出力するハンドラ
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定。ログをタブ区切り出力するように設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

# メール処理で使うバックエンドを定義
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# メディアファイルの配置場所を指定
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

