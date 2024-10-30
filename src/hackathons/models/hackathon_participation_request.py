from django.db import models
from django.utils.translation import gettext_lazy as _

from hackathons.models.hackathons import Hackathon
from profiles.models.profiles import Profile


class HackathonParticipationRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = "Pending", _("Waiting for confirmation")
        ACCEPTED = "Accepted", _("Active")
        DECLINED = "Declined", _("Blocked")

    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name=_("profile"))
    hackathon = models.ForeignKey(to=Hackathon, null=True, on_delete=models.SET_NULL, verbose_name=_("hackathon"))
    cover_letter = models.TextField(max_length=400, blank=True, null=True, verbose_name=_("cover letter"))
    resume_url = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("resume url"))
    status = models.CharField(
        max_length=25,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING,
        blank=True,
        null=True,
        verbose_name=_("status"),
    )

    def __str__(self):
        return f"{self.profile} | {self.hackathon}"
