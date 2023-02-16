from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,IsAdminUser
from .serializers import LoanSerializer
from .models import Loan, transcation
# , TransactionSerializer
# Create your views here.

class CreateLoanView(generics.CreateAPIView): 
    """
    Create a loan
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(provider=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateLoanView(generics.UpdateAPIView):
    """
    Update a loan
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer
    def get_object(self):
        loan_id = self.kwargs.get('id')
        return Loan.objects.get(id=loan_id)
    def put(self, request, *args, **kwargs):
        loan = self.get_object()
        if(loan.provider == request.user):
            serializer = self.get_serializer(loan, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"You are not authorized to update this loan"}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteLoanView(generics.DestroyAPIView):
    """
    Delete a loan
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer
    def get_object(self):
        loan_id = self.kwargs.get('id')
        return Loan.objects.get(id=loan_id)
    def delete(self, request, *args, **kwargs):
        loan = self.get_object()
        if(loan.provider == request.user or request.user.is_superuser):
            loan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"You are not authorized to delete this loan"}, status=status.HTTP_401_UNAUTHORIZED)


class LoanCreatedByUserView(generics.ListAPIView):
    """
    List all loans
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer
    def get_queryset(self):
        return Loan.objects.filter(provider=self.request.user)


class AllLoanList(generics.ListAPIView):
    permission_classes=(IsAdminUser,)
    serializer_class = LoanSerializer
    queryset=Loan.objects.all()


