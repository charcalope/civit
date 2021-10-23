from django.db import models
from accounts.models import User
from tagging.registry import register

# Create your models here.
class Initiative(models.Model):
    primary_organizer = models.ForeignKey(User, related_name='primary_organizer', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    problem_statement = models.TextField()
    people_impact = models.TextField()
    legislative_scope = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    # city or state
    type = models.CharField(max_length=25)

    supporters = models.ManyToManyField(User, related_name='supporters')
    donors = models.ManyToManyField(User, related_name='donors')
    sponsors = models.ManyToManyField(User, related_name='sponsors')
    organizers = models.ManyToManyField(User, related_name='organizers')

    def totalDonations(self):
        donations = Donation.objects.filter(initiative=self.pk)
        sum = 0
        for donation in donations:
            sum += donation.amount
        return sum

    def getStatusUpdates(self):
        statusUpdates = StatusUpdate.objects.filter(initiative=self.pk)
        return statusUpdates

    def getExpenses(self):
        expenses = Expense.objects.filter(initiative=self.pk)
        return expenses

# hello world
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

    title = models.CharField(max_length=200, default='No Expense Title Set')
    description = models.TextField()
    amount = models.IntegerField(default=0)

    approved = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

class Legislator(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

class LegislatorGroup(models.Model):
    group_title = models.CharField(max_length=150)
    legislators = models.ManyToManyField(Legislator)

class MeetingRequest(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, null=True)

    requesting_organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True, editable=False)

    legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)

register(Initiative)
