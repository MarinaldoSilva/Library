# borrowing/urls.py (Mapeamento das Views)

from django.urls import path
from .views import (
    BorrowingListAPIView, 
    BorrowingCreateAPIView, 
    BorrowingDetailAPIView, 
    BorrowingUpdateAPIView, 
    BorrowingDeleteAPIView,
    BorrowingRenewalAPIView
)

urlpatterns = [

    path('', BorrowingListAPIView.as_view(), name='borrowing-list'),
    path('create/', BorrowingCreateAPIView.as_view(), name='borrowing-create'), 
    path('<uuid:pk>/', BorrowingDetailAPIView.as_view(), name='borrowing-detail'), 
    path('<uuid:pk>/update/', BorrowingUpdateAPIView.as_view(), name='borrowing-update'),
    path('<uuid:pk>/delete/', BorrowingDeleteAPIView.as_view(), name='borrowing-delete'),
    path('<uuid:pk>/renew/', BorrowingRenewalAPIView.as_view(), name='borrowing-renew')
]