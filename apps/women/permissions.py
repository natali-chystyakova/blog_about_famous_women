from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def hes_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только его владельцу.
    Предполагается, что у объекта есть атрибут `owner`.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешены любые безопасные методы (GET, HEAD или OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение на запись предоставляется только владельцу объекта
        return obj.user == request.user
