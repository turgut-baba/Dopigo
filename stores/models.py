from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from enum import Enum, unique, auto


# This is where we declare added stores.
@unique
class StoreID(Enum):
    Trendyol = 1
    Hepsiburada = 2
    GittiGidiyor = 3
    END = auto()
    # Don't forget to migrate after adding a new store.


class Store(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=50, default="")
    store_id = models.SmallIntegerField(default=0,
                                        validators=[MinValueValidator(0), MaxValueValidator(StoreID.END.value)]
                                        )
    seller_id = models.CharField(max_length=15, default="1234")

    def __str__(self) -> models.CharField:
        return self.name
