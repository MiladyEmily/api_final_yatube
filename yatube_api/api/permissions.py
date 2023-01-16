from rest_framework import permissions


class IsAuthorOrReadAndPostOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором поста или комментария,
    который хочет удалить или изменить.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        is_safe = request.method in permissions.SAFE_METHODS
        is_author = obj.author == request.user
        return is_safe or is_author
