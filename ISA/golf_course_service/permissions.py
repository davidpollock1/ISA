from rest_framework import permissions

class CustomerAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.author == request.user:
            return True
        
        if obj.customer_id  == request.user.customer_id:
            return True

        return False
    
class GolfCourseAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.author == request.user:
            return True
        
        if obj.customer_id  == request.user.customer_id:
            return True

        return False
