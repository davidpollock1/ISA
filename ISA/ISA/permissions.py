from rest_framework import permissions

class IsCustomerData(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        
        if request.user.userprofile.customer:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.author == request.user:
            return True
        
        if obj.customer_id  == request.user.customer:
            return True

        return False
