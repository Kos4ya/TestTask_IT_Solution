from django.urls import path

from .views import (RandomQuoteView, AddQuoteView,
                                       AddSourceView, LikeDislikeView,
                                       TopQuotesView, SourceListView)

urlpatterns = [
    path('', RandomQuoteView.as_view(), name='random_quote'),
    path('add/', AddQuoteView.as_view(), name='add_quote'),
    path('add-source/', AddSourceView.as_view(), name='add_source'),
    path('like-dislike/<int:quote_id>/<str:action>/',
         LikeDislikeView.as_view(), name='like_dislike'),
    path('top/', TopQuotesView.as_view(), name='top_quotes'),
    path('sources/', SourceListView.as_view(), name='source_list')
]
