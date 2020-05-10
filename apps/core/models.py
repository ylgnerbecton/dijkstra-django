from django.db import models


class Route(models.Model):
    departure = models.CharField(verbose_name='departure', max_length=3)
    arrival = models.CharField(verbose_name='arrival', max_length=3)
    price = models.DecimalField(verbose_name='price', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'

    def __init__(self, departure, arrival, price):
        if not (price > 0):
            raise Exception('Valor da rota deve ser maior que zero')

        self.departure = departure
        self.arrival = arrival
        self.price = price

    def __str__(self):
        return '%s %s %s' % (self.departure, self.arrival, self.price)
    
    def get_departure(self):
        return self.departure
    
    def get_arrival(self):
        return self.arrival

    def get_price(self):
        return self.price
