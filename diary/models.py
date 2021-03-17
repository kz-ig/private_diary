from django.db import models
from accounts.models import CustomUser

class Diary(models.Model):
    """ 日記モデル """
    # ForeignKeyでCustomUserモデルとDiaryテーブルを1対多で結び付ける。on_deleteは親データ(CustomUser)削除時の挙動を設定。
    # フィールド内のverbose_nemeは画面表示される項目名。デフォルトだとモデル名を解体した名前が表示される。
    user = models.ForeignKey(CustomUser,verbose_name='ユーザー',on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル',max_length=40)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now_add=True)

    class Meta:
        """
        付帯情報(管理画面でのモデル名、モデルインスタンスの整列順など「フィールドに関係ない情報」を設定
        """
        # Metaクラス内のverbose_name_pluralは管理画面に表示されるモデル名。
        # verbose_nameだと語尾に複数形の"s"が自動でつく。verbose_name_pluralだと語尾に"s"がつかない
        verbose_name_plural = 'Diary'

    def __str__(self):
        return self.title




