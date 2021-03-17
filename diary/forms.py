from django import forms
from django.core.mail import EmailMessage
from .models import Diary

class InquiryForm(forms.Form):
    name = forms.CharField(label="お名前",max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル',max_length=30)
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # self.fields['<フィールド名>'].widget.attrs['<属性名>']を編集することでcss属性を操作
        # Bootstrapのフォーム用クラス「form-control」と「placeholder」を追加している
        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        #各フォームフィールドのデータを取得。書式: self.cleaned_data['<フィールド名>']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ: \n{2}'.format(name,email,message)
        from_email = 'admin@exsample.com'
        to_list = [
                     'test@exsample.com'
        ]
        cc_list = [
                     email
        ]

        # EmailMessageインスタンス作成
        message = EmailMessage(subject=subject,body=message,from_email=from_email,to=to_list,cc=cc_list)
        # メール送信
        message.send()

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        # Diaryモデルと定義情報の大部分が重複しているしているのでDiaryモデルの情報を取得
        model = Diary
        # 対象フィールドを指定。userは一意に決まるため項目不要。created_atとupdate_atもモデルで自動セットされるため不要
        fields = ('title','content','photo1','photo2','photo3',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 全フォームフィールドに一括でBootstrapのform-controlクラスを追加
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
