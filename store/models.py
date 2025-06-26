from django.db import models
from datetime import timedelta

class TableCategory(models.Model):
    CATEGORY_CHOICES = [
        (4, '4-Seater'),
        (6, '6-Seater'),
        (8, '8-Seater'),
    ]

    category = models.IntegerField(choices=CATEGORY_CHOICES, unique=True)
    available_tables = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.category}-Seater: {self.available_tables} Available"

class Booking(models.Model):
    name = models.CharField(max_length=100)
    table_type = models.ForeignKey(TableCategory, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10, null=True,blank=True)
    booking_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    actual_end_time = models.DateTimeField(null=True, blank=True)

    @property
    def release_time(self):
        return self.booking_time + self.duration
    def time_used(self):
        if self.actual_end_time:
            return self.actual_end_time - self.booking_time
        return None
    
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner','Dinner'),
    ]
    name = models.CharField( max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category  = models.CharField(max_length = 20 ,choices=CATEGORY_CHOICES,default='starter')
    def __str__(self):
        return F"{self.name}  -  RS {self.price}({self.category})"
class Order(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    @property
    def total_price(self):
        return self.quantity *self.item.price

