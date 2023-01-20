from django.db import models
from common.models import CommonModel

class Experience(CommonModel):
    """ Experience Model Description"""
    
    name = models.CharField(max_length=250)
    country = models.CharField(max_length=50,default="대한민국",)
    city = models.CharField(max_length=80,default="경주",)
    host = models.ForeignKey("users.User",on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    descriptions = models.TextField(max_length=500)
    perk = models.ManyToManyField("experiences.Perk",)
    
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )
    
    def __str__(self) -> str:
        return self.name
    
class Perk(CommonModel):
    """ What i included on an Experience"""
    
    name = models.CharField(max_length=100,)
    detail = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    
    
    def __str__(self) -> str:
        return self.name
    
    
    
    