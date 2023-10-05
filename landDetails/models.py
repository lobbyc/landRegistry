from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def upload_location(instance, filename):
    file_path = "images/{landmark}-{filename}".format(
        landmark=str(instance.landmark.id), filename=filename
    )
    return file_path

def document_upload_location(instance, filename):
    file_path = "images/{county}-{filename}".format(
        county=str(instance.landmark.id), filename=filename
    )
    return file_path


class OwnerDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    id_number = models.BigIntegerField()

    def __str__(self):
        return self.first_name+" "+self.last_name
    
class Location(models.Model):
    county = models.CharField(max_length=200)
    sub_county = models.CharField(max_length=200)
    home_location = models.CharField(max_length=200)
    sub_location = models.CharField(max_length=200)
    address_no = models.IntegerField()

    def __str__(self):
        return self.county+ " "+self.sub_county

class Landmark(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location,max_length=200, on_delete=models.CASCADE)
    owner = models.ForeignKey(OwnerDetail, on_delete=models.CASCADE)
    deed_no = models.IntegerField(unique=True)
    sheet_no = models.BigIntegerField(unique=True)
    sheet_image =models.ImageField(upload_to=upload_location)

    def __str__(self):
        return self.name


class GreenCard(models.Model):
    land = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    owner = models.ForeignKey(OwnerDetail, on_delete=models.CASCADE)
    card_number = models.BigIntegerField(unique=True, blank=True)
    expiration_date = models.DateField()

    def __str__(self):
        return str(self.card_number)

    def save(self, *args, **kwargs):
        # Set the card_number to the deed_no of the associated Landmark
        self.card_number = self.land.deed_no
        super(GreenCard, self).save(*args, **kwargs)

class Documents(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    lease = models.ImageField(null=True, upload_to=document_upload_location)
    rent = models.ImageField(null=True,upload_to= document_upload_location)
