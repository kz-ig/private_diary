# from django.shortcuts import render
import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm, DiaryCreateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Diary

# ロガーを取得
logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

class InquiryView(generic.FormView):
    template_name = 'inquiry.html'
    # form_classにInquiryFormをオーバーライド
    form_class = InquiryForm
    # 処理に問題なかった時のリダイレクト先URLを指定。reverse_lazy('<url.pyのapp_name>:<ルーティングにつけた名前>の書式でURLを逆引きできる
    success_url = reverse_lazy('diary:inquiry')

    #親クラスのform_validメソッドをオーバーライド。フォームのバリデーションに問題がなかった時に実行される
    def form_valid(self, form):
        # forms.pyのメール送信メソッドを呼び出し
        form.send_email()
        # 送信処理後のメッセージ
        messages.success(self.request,'メッセージを送信しました。')
        #ビューからログを出力。logger.<ログレベル>(<出力内容>)の書式
        # form.cleaned_data['<フィールド名'>]の書式でユーザーの入力値を取り出す
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class DiaryListView(LoginRequiredMixin, generic.ListView):
    """
    日記一覧表示
    一覧表示のためListViewを継承。またLoginRequiredMixinを継承しログイン状態でないと
    DiaryListViewにアクセスできないようにする
    """
    model = Diary
    template_name = 'diary_list.html'
    # ページネーション設定。1ページに表示するデータ数を指定
    paginate_by = 2

    def get_queryset(self):
        """
        ログインデータに紐づいたデータを表示するためget_querysetメソッドをオーバーライド
        self.request.userでログインしているユーザーインスタンスを取得してorder_by('-created_at')と"-"をつけて作成日時で降順に並び替え
        """
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(LoginRequiredMixin,generic.DeleteView):
    """
    日記詳細
    """
    model = Diary
    template_name = 'diary_detail.html'

class DiaryCreateView(LoginRequiredMixin,generic.CreateView):
    """
    日記作成
    """
    model = Diary
    template_name = 'diary_create.html'
    # form_classをオーバーライドしてDiaryCreateFormを利用
    form_class = DiaryCreateForm
    # 正常に処理が完了したときの遷移先
    success_url = reverse_lazy('diary:diary_list')

    # フォームのバリデーションに問題がなかった時に実行されるメソッド
    def form_valid(self, form):
        # form.saveでフォームの入力値をデータベースに保存できるが、フォームからはログインユーザー値が足りないので
        # 一旦cmmit=Falseとすることでデータベースにフォーム内容を保存しないで、オブジェクトを取得
        diary = form.save(commit=False)
        # ログインユーザーを取得
        diary.user = self.request.user
        # フォーム入力値とログインユーザーを含んだオブジェクトデータをデータベースに保存
        diary.save()
        # 成功メッセージ
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    # フォームのバリデーションが失敗したときに実行されるメソッド
    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    日記更新
    """
    model = Diary
    template_name = 'diary_update.html'
    # フィールド項目が同じなので日記作成フォーム(DiaryCreateForm)を使い回す
    form_class = DiaryCreateForm

    # 正常に処理が完了したときの遷移先(遷移先が動的なurlとなるのでget_success_urlメソッドをオーバーライド)
    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={ 'pk': self.kwargs['pk'] })

    # フォームのバリデーションに問題がなかった時に実行されるメソッド
    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    # フォームのバリデーションが失敗したときに実行されるメソッド
    def form_invalid(self, form):
        messages.error(self.request, '日記のを更新に失敗しました。')
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin,generic.DeleteView):
    """
    日記削除
    """
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    # 削除成功時にメッセージが出力されるようdeleteメソッドをオーバーライド
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request, *args, **kwargs)


