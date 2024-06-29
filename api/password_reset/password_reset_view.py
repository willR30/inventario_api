from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import PasswordResetToken
from api.serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.core.mail import send_mail

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)
            token, created = PasswordResetToken.objects.get_or_create(user=user)
            reset_url = f"http://your-frontend-url/reset-password/{token.token}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                'polaris@willtech.site',  # Asegúrate de que esto coincida con tu configuración
                [email]
            )
            return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):

    def post(self, request, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            token = get_object_or_404(PasswordResetToken, token=token)
            if token.is_valid():
                user = token.user
                user.set_password(password)
                user.save()
                token.delete()
                return Response({"message": "Password has been reset"}, status=status.HTTP_200_OK)
            return Response({"error": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
