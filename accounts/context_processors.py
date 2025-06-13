from .models import Avatar


def avatar_context(request):
    avatar_url = None
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(user=request.user).first()
        if avatar and avatar.imagen:
            avatar_url = avatar.imagen.url
    return {'avatar_url': avatar_url}
