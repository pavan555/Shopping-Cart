from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class CustomerHistoryDjangoPermission(BasePermission):
    def has_permission(self, request, view):
        # print("Checking customer history permission", request.user.has_perm('store.view_history_info'))
        return request.user.has_perm('store.view_history_info')