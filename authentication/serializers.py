import phonenumbers
from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField
class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False,allow_blank=False)
    password = serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model = User
        fields = ['username','email','phone_number','password']
    def validate(self,attrs):
        username_exist = User.objects.filter(username=attrs['username']).exists()
        if username_exist:
            raise serializers.ValidationError(detail="User with username already exist")
        email_exist = User.objects.filter(email = attrs.get('email')).exists()
        if email_exist:
            raise serializers.ValidationError(detail="User with email already exist")
        phonenumber_exist = User.objects.filter(email = attrs['phone_number']).exists()
        if phonenumber_exist:
            raise serializers.ValidationError(detail="User with email already exist")
        return super().validate(attrs)
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user