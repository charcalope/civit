from django.db import models
from accounts.models import User

# Create your models here.
class Initiative(models.Model):
    primary_organizer = models.ForeignKey(User, related_name='primary_organizer', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    type = models.CharField(max_length=25)

    supporters = models.ManyToManyField(User, related_name='supporters')
    donors = models.ManyToManyField(User, related_name='donors')
    sponsors = models.ManyToManyField(User, related_name='sponsors')
    organizers = models.ManyToManyField(User, related_name='organizers')

class StatusUpdate(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)

    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    text_content = models.TextField()

class Donation(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)

    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    amount = models.IntegerField()

class Event(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    dt = models.DateTimeField()
    title = models.CharField(max_length=150)
    description = models.TextField()

    attendees = models.ManyToManyField(User, related_name='attendees')

class Expense(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20)
