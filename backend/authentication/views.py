from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import login

from drf_spectacular.utils import extend_schema

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from dj_rest_auth.registration.views import VerifyEmailView
from allauth.account.models import EmailAddress

from knox.views import LoginView as KnoxLoginView, LogoutAllView as KnoxLogoutAllView, LogoutView as KnoxLogoutView

from .serializer import LogoutAllSerializer, LogoutSerializer

class UserConfirmEmailView(VerifyEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        # Substitua pelo URL do seu front-end
        redirect_url = f"{settings.FRONTEND_URL}{settings.FRONTEND_EMAIL_CONFIRMATION_ENDPOINT}"
        return HttpResponseRedirect(redirect_url)

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        login(request, user)
        
        response = super(LoginView, self).post(request, format=None)
        
        if response.status_code == 200:
            user = request.user
            
            if not user.emailaddress_set.filter(verified=True).exists():
                email = user.email
                if not email:
                    return Response({"error": "No email address associated with the user."}, status=400)
                
                try:
                    email_address = EmailAddress.objects.get(user=user, email=email, verified=False)
                except EmailAddress.DoesNotExist:
                    email_address = EmailAddress.objects.create(
                        user=user,
                        email=email,
                        verified=False,
                        primary=True
                    )
                
                email_address.send_confirmation(request, signup=False)
                
                return Response({"error": f"Email not verified yet. Resending confirmation email to {user.email}."}, status=400)
        
        return response

class LogoutView(KnoxLogoutView):
    serializer_class = LogoutSerializer
    
    @extend_schema(request=LogoutSerializer, responses={204: LogoutSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LogoutAllView(KnoxLogoutAllView): 
    serializer_class = LogoutAllSerializer
    
    @extend_schema(request=LogoutAllSerializer, responses={204: LogoutAllSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)