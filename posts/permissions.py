from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        print(f"Method: {request.method}")  
        print(f"User: {request.user}, Post owner: {obj.owner}") 
        
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the post
        return obj.owner == request.user

