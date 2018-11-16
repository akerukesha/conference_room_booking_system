from __future__ import unicode_literals

from django.db import models


class Room(models.Model):
    """
    """
    name = models.CharField(max_length=1000, null=False, blank=False,
                                            verbose_name=u"Room name")
    description = models.CharField(max_length=1000, null=False, blank=False,
                                            verbose_name=u"Room description")
    image_url = models.URLField(max_length=1000, null=False, blank=False,
                                            verbose_name=u"Room imageURL")


    def to_json(self):
    	return {
    		"id": self.id,
    		"name": self.name,
    		"description": self.description,
    		"image_url": self.image_url,
    	}


    def __unicode__(self):
        return self.name

        
    class Meta:
        verbose_name = u"Room"
        verbose_name_plural = u"Rooms"


class Booking(models.Model):
    """
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                                                        related_name="rooms")
    start_timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                            verbose_name=u"Start timestamp")
    end_timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                            verbose_name=u"End timestamp")
    is_activated = models.BooleanField(default=False, verbose_name=u"Activated room")

    def __unicode__(self):
        return "{0} {1} {2}".format(self.room.name, self.start_timestamp, self.end_timestamp)

    class Meta:
        verbose_name = u"Booking"
        verbose_name_plural = u"Bookings"