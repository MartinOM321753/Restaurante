from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import AllowAny

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# views.py
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("La creación de usuarios está deshabilitada en este endpoint.")

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return []


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class CreateAdminUserView(APIView):
    def post(self, request):
        try:
            admin_role = Role.objects.get(name='ADMIN')
        except Role.DoesNotExist:
            return Response({'error': 'El rol ADMIN no existe'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['role'] = admin_role.id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            client_role = Role.objects.get(name='USER')
        except Role.DoesNotExist:
            return Response({'error': 'El rol USER no existe'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['role'] = client_role.id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateRestaurantOwnerUserView(APIView):
    def post(self, request):
        try:
            client_role = Role.objects.get(name='RESTAURANT_OWNER')
        except Role.DoesNotExist:
            return Response({'error': 'El rol RESTAURANT_OWNER no existe'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['role'] = client_role.id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.data.get('redirect_url')}?uid={uid}&token={token}"

            subject = 'Recuperación de contraseña'
            from_email = 'no-reply@tudominio.com'
            to_email = email

            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #333;">Hola {user.name},</h2>
                        <p style="font-size: 16px; color: #555;">
                            Has solicitado restablecer tu contraseña. Haz clic en el siguiente botón para continuar:
                        </p>
                        <p style="text-align: center; margin: 30px 0;">
                            <a href="{reset_url}" style="background-color: #f26522; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px;">
                                Restablecer contraseña
                            </a>
                        </p>
                        <p style="font-size: 14px; color: #777;">
                            Si no solicitaste este cambio, puedes ignorar este mensaje.
                        </p>
                        <p style="font-size: 14px; color: #777;">
                            Gracias,<br>El equipo de soporte
                        </p>
                    </div>
                </body>
            </html>
            """

            text_content = f"""
            Hola {user.name},

            Para restablecer tu contraseña, por favor visita el siguiente enlace:

            {reset_url}

            Si no solicitaste este cambio, puedes ignorar este mensaje.

            Gracias,
            El equipo PythonEs Food
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        # Siempre devolver el mismo mensaje por seguridad
        return Response(
            {'message': 'Si el email está registrado, recibirás un enlace para recuperar tu contraseña'},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('password')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': 'Contraseña actualizada correctamente'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Token inválido o expirado'},
            status=status.HTTP_400_BAD_REQUEST
        )

