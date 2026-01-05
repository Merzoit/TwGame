@api_view(['POST'])
def create_admin(request):
    """Создание суперпользователя (только для инициализации)"""
    try:
        from django.contrib.auth.models import User

        username = 'admin'
        password = 'admin123'
        email = 'admin@twgame.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            return Response({'message': f'Admin user "{username}" created'})
        else:
            # Обновляем пароль
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return Response({'message': f'Admin user "{username}" password updated'})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
