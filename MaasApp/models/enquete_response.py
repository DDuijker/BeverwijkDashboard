from django.db import models


class EnqueteResponse(models.Model):
    respondent_id = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField()
    completion_time = models.DateTimeField()
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    last_modified_time = models.DateTimeField(blank=True, null=True)
    origin = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(max_length=20, blank=True, null=True)
    travel_frequency = models.CharField(max_length=50, blank=True, null=True)
    available_transportation = models.CharField(max_length=200, blank=True, null=True)
    most_used_transport_modes = models.CharField(max_length=200, blank=True, null=True)
    consider_shared_mobility = models.CharField(max_length=200, blank=True, null=True)
    maas_app_used = models.CharField(max_length=3, blank=True, null=True)
    maas_usage_frequency = models.CharField(max_length=50, blank=True, null=True)
    maas_app_advantages = models.TextField(blank=True, null=True)
    cost_overview_value_added = models.TextField(blank=True, null=True)
    satisfaction_transport_modes = models.CharField(max_length=50, blank=True, null=True)
    survey_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Response {self.respondent_id}"

