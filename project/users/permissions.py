from rest_framework import permissions

class Is_Client(permissions.BasePermission):
  def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_client)


class Is_Avocat(permissions.BasePermission):
  def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_Avocat)


class Is_Admin(permissions.BasePermission):
  def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)
