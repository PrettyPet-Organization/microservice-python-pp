# Everything related to the news is also here

from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.profiles import Profile


class News(models.Model):
    author = models.ForeignKey(
        to=Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="news",
        verbose_name=_("Author"),
    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.CharField(max_length=1000, verbose_name=_("Description"))
    image_url = models.ImageField(verbose_name=_("Image"))
    likes = models.PositiveIntegerField(default=0, verbose_name=_("Likes counter"))
    is_open = models.BooleanField(default=True, verbose_name=_("Is open new"))
    topics = models.ManyToManyField(to="Topic", verbose_name=_("Topics"))
    tags = models.ForeignKey(
        to="Tag", on_delete=models.SET_NULL, null=True, verbose_name=_("Tags")
    )

    # Correct display of category in an admin panel. Before displayed "newss"
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
    tags = models.ForeignKey(to="Tag", on_delete=models.SET_NULL, null=True, verbose_name=_("Tags"))