from django.urls import path
from . import views

app_name = 'diary' # diaryアプリケーションのルーティングの名前
urlpatterns = [
    path('',views.IndexView.as_view(),name="index"), #TOPページ
    path('inquiry/',views.InquiryView.as_view(),name="inquiry"), #問い合わせページ
    path('diary-list/',views.DiaryListView.as_view(),name="diary_list"), #日記一覧ページ
    path('diary-detail/<int:pk>',views.DiaryDetailView.as_view(),name="diary_detail"), #日記詳細ページ
    path('diary-create/',views.DiaryCreateView.as_view(),name="diary_create"), #日記作成ページ
    path('diary-update/<int:pk>',views.DiaryUpdateView.as_view(),name="diary_update"), #日記編集ページ
    path('diary-delete/<int:pk>',views.DiaryDeleteView.as_view(),name="diary_delete"), #日記削除ページ
]