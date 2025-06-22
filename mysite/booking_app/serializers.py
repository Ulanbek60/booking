from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken 


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_role', 'age', 'phone_number']

    extra_kwargs = {'passwords': {'write only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user':{
                'username':instance.username,
                'email':instance.email,
            },
            'access':str(refresh.access_token),
            'refresh':str(refresh),
        }



class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'

class RoomListSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['id', 'owner', 'room_number', 'room_type', 'room_status', 'room_price', 'room_images']


class RoomDetailSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'room_status', 'room_price', 'all_inclusive',
                  'room_description', 'room_images']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['user_name', 'text', 'parent', 'stars']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class HotelListSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_image', 'address', 'stars', 'get_avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    owner = UserProfileSimpleSerializer()
    created_date = serializers.DateField(format('%d-%m-%Y'))
    rooms = RoomListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['hotel_name','description','country', 'city', 'address', 'stars',
                  'hotel_video', 'hotel_image', 'created_date', 'owner', 'rooms', 'reviews']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','country_name']

class CountryDetailSerializer(serializers.ModelSerializer):
    country_hotel = HotelListSerializer(many=True, read_only=True)
    class Meta:
        model = Country
        fields = ['country_hotel']

