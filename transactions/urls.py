from django.urls import path, include
from .views import CreateLoanView,UpdateLoanView
#  CreateTransactionView, LoanListView, TransactionListView
urlpatterns = [
    path('create-loan/',CreateLoanView.as_view(),name='create-loan'),
    path('update-loan/<int:id>',UpdateLoanView.as_view(),name='update-loan'),
]