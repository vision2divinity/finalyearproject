from django.db import models
from django.contrib.auth.models import User
from random import randint


badge = (
    ('voted', 'voted'),
    ('not voted', 'not voted'),
)

class Voter(models.Model):
    email = models.EmailField()
    code = models.CharField(blank=True, null=True, max_length=6, default=randint(100000, 999999))
    sent_code = models.BooleanField(default=False)

    def __str__(self):
        return self.email



class Candidate(models.Model):
    """[summary]
        For creating list of candidates in the database table with related fields
    """
    name = models.CharField(max_length=200)
    course = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ManyToManyField(User)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.candidate.name
