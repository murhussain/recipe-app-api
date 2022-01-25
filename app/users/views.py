from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """CREATE NEW USER IN THE SYSTEM"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """CREATE A NEW AUTH TOKEN FOR USER"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class ManageUserView(generics.RetrieveUpdateAPIView):
#     """MANAGE THE AUTHENTICATED USERS"""
#     authentication_classes = (authentication.TokenAuthentication,)
#     permissions_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer
#
#     def get_object(self):
#         """RETRIEVE AND RETURN AUTHENTICATION USER"""
#         return self.request.user
