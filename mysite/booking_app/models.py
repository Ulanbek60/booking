from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('simpleUser', 'simpleUser'),
        ('ownerUser', 'ownerUser')
    )
    user_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='simpleUser')
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(70)],
                                           null=True, blank=True)
    phone_number= PhoneNumberField(null=True, blank=True, region='KG')


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class Hotel(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=64)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_hotel')
    city = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    created_date = models.DateField(auto_now_add=True)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    hotel_video = models.FileField(upload_to='hotel_video/', null=True, blank=True)

    def __str__(self):
        return f'{self.hotel_name}, - {self.country} - {self.city} '

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum([i.stars for i in ratings]) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_image')
    hotel_image = models.ImageField(upload_to='hotel_image/')


class Room(models.Model):
    room_number = models.PositiveSmallIntegerField()
    hotel_room = models.ForeignKey(Hotel,on_delete=models.CASCADE, related_name='rooms')
    TYPE_CHOICES = (
        ('люкс', 'люкс'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный')
    )
    room_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    room_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='свободен')
    room_price = models.PositiveIntegerField()
    all_inclusive = models.BooleanField(default=False)
    room_description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hotel_room}, - {self.room_number} - {self.room_type}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    hotel_image = models.ImageField(upload_to='room_image/')


class Review(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='рейтинг', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user_name}, - {self.hotel} - {self.stars}'


class Booking(models.Model):
    hotel_book = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_book = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_book = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.PositiveIntegerField(default=0)
    STATUS_BOOK_CHOICES = (
        ('отменено', 'отменено'),
        ('подтверждено', 'подтверждено'),
    )
    status_book = models.CharField(max_length=16, choices=STATUS_BOOK_CHOICES)

    def __str__(self):
        return f'{self.user_book}, - {self.hotel_book} - {self.room_book}, {self.status_book}'










