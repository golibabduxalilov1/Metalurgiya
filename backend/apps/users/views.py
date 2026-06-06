"""
Users App Views
"""
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from utils.permissions import IsAdmin, IsAdminOrMaster
from .serializers import (
    CustomTokenObtainPairSerializer, UserListSerializer, UserDetailSerializer,
    UserCreateSerializer, UserUpdateSerializer, ChangePasswordSerializer,
    UserProfileSerializer
)

User = get_user_model()


@extend_schema(tags=['auth'])
class LoginView(TokenObtainPairView):
    """
    Вход в систему. Возвращает JWT access/refresh токены и данные пользователя.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['auth'])
class RefreshTokenView(TokenRefreshView):
    """Обновление access токена по refresh токену"""
    pass


@extend_schema(tags=['auth'])
class LogoutView(generics.GenericAPIView):
    """
    Выход из системы. Добавляет refresh токен в чёрный список.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={'application/json': {'type': 'object', 'properties': {'refresh': {'type': 'string'}}}},
        responses={200: {'type': 'object', 'properties': {'detail': {'type': 'string'}}}}
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Выход выполнен успешно'})
        except Exception:
            return Response({'detail': 'Неверный токен'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'])
class MeView(generics.RetrieveUpdateAPIView):
    """Профиль текущего пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer


@extend_schema(tags=['auth'])
class ChangePasswordView(generics.GenericAPIView):
    """Смена пароля текущего пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Пароль успешно изменён'})


@extend_schema(tags=['users'])
@extend_schema_view(
    list=extend_schema(summary='Список пользователей'),
    retrieve=extend_schema(summary='Детали пользователя'),
    create=extend_schema(summary='Создать пользователя'),
    update=extend_schema(summary='Обновить пользователя'),
    partial_update=extend_schema(summary='Частично обновить пользователя'),
    destroy=extend_schema(summary='Деактивировать пользователя'),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями системы (только для администраторов).
    """
    queryset = User.objects.all().order_by('last_name', 'first_name')
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')

        if role:
            queryset = queryset.filter(role=role)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if search:
            queryset = queryset.filter(
                last_name__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        return queryset

    def destroy(self, request, *args, **kwargs):
        """Деактивация вместо удаления"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': 'Пользователь деактивирован'}, status=status.HTTP_200_OK)

    @extend_schema(summary='Сбросить пароль пользователя')
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Сброс пароля пользователя (только admin)"""
        user = self.get_object()
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'detail': 'Новый пароль обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'detail': f'Пароль пользователя {user.username} сброшен'})

    @extend_schema(summary='Активировать пользователя')
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'detail': 'Пользователь активирован'})
