from django.urls   import path
from creator.views import FirstTemporaryView, SecondTemporaryView, ThirdTemporaryView, FourthTemporaryView, CreateTemporaryView

urlpatterns = [
    path('/<int:temporary_id>/first', FirstTemporaryView.as_view(), name='first_temporary'),
    path('/<int:temporary_id>/second', SecondTemporaryView.as_view(), name='second_temporary'),
    path('/<int:temporary_id>/third', ThirdTemporaryView.as_view(), name='third_temporary'),
    path('/<int:temporary_id>/fourth', FourthTemporaryView.as_view(), name='fourth_temporary'),
    path('/<int:temporary_id>/create', CreateTemporaryView.as_view(), name='create_temporary'),
]
