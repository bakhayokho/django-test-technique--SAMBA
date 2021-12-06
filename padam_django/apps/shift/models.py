from django.db import models
from padam_django.apps.geography.models import Place
from padam_django.apps.fleet.models import Bus, Driver


class BusStop(models.Model):
    name = models.CharField(verbose_name="Name of the bus stop", max_length=100, )
    is_transfer_stop = models.BooleanField(
        verbose_name="Transfer stop",
        default=False,
    )
    location = models.ForeignKey(
        Place,
        verbose_name="Location",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="stops",
    )

    def __str__(self):
        return f"Bus stop: {self.name}"


class BusStopTime(models.Model):
    transit_time = models.TimeField(
        verbose_name="Time of transit",
        null=False,
        blank=False,
    )
    stop = models.ForeignKey(
        BusStop,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Bus stop in {self.stop.name} at {self.transit_time}"


class BusShift(models.Model):

    departure_time = models.ForeignKey(
        BusStopTime,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_departure",
    )
    arrival_time = models.ForeignKey(
        BusStopTime,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_arrival",
    )
    driver = models.ForeignKey(
        Driver,
        verbose_name="Driver",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_driver",
    )
    bus = models.ForeignKey(
        Bus,
        verbose_name="Bus",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_bus",
    )
    bus_stops = models.ManyToManyField(
        BusStop,
        related_name="shifts_stop",
        blank=False,
        help_text="Select at least 2 bus stops",
    )

