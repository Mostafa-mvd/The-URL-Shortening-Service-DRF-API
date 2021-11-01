from rest_framework import status, views
from rest_framework.response import Response

from django.contrib.auth import authenticate

from users import (utils as users_utils, 
                   serializers as users_serializers,
                   models as users_models)
    
import pyotp


class GenerateOTPCode(views.APIView):
    serializer_class = users_serializers.UserOTPCodeSerializer
    model = users_models.UserOTPCode
    user_obj = None

    def user_exists(self, username, password):
        user = authenticate(username=username, password=password)

        if user:
            self.user_obj = user
            return True

        return False
    
    def get_user_obj(self):
        return self.user_obj
    
    def get_otp_model(self):
        return self.model
    
    def generate_random_totp_code_and_secret_key(self):
        secret_key = pyotp.random_base32()
        totp = pyotp.TOTP(s=secret_key, interval=users_utils.get_otp_code_ttl())
        otp_code = totp.now()

        return secret_key, otp_code

    def perform_create_totp_code(self):
        """this function generates and returns otp_obj,
            if otp_obj existed, this would have update otp_obj"""

        user_obj = self.get_user_obj()
        otp_qs = self.get_otp_model().objects.filter(user=user_obj)
        secret_key_str, otp_code_str_digit = self.generate_random_totp_code_and_secret_key()

        if otp_qs.exists():
            otp_obj = otp_qs.first()
            otp_obj = otp_obj.update_then_return_obj(
                secret_key_str, otp_code_str_digit)
        else:
            otp_obj = users_models.UserOTPCode(
                user=user_obj,
                secret_key=secret_key_str,
                otp_code=int(otp_code_str_digit))
            otp_obj.save()

        return otp_obj

    def create_otp_obj(self):
        
        totp_code_obj = self.perform_create_totp_code()

        return Response(
            data={
                "totp_code": str(totp_code_obj.otp_code),
                "ttl in minutes": users_utils.get_otp_code_ttl() / 60
            }, status=status.HTTP_201_CREATED
        )
    
    def get_serializer(self):
        return self.serializer_class

    def post(self, request):
        serializer = self.get_serializer()
        serialized_data = serializer(data=request.data)

        if serialized_data.is_valid():
            username = serialized_data.validated_data['username']
            password = serialized_data.validated_data['password']

            if self.user_exists(username=username, password=password):
                json_response = self.create_otp_obj()
                return json_response

            return Response(
                data={
                    "ERROR": "username and password didn't match"
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            data={
                "ERROR": "Your data is not valid."
            }, status=status.HTTP_400_BAD_REQUEST)

