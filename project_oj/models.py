from django.db import models
from .choices import DiffifultyChoice

class Problems(models.Model):
    code = models.CharField(primary_key=True, null=False, max_length=15)
    name = models.CharField(max_length=30)
    statement = models.CharField(max_length=8000)
    difficulty = models.CharField(choices=[(tag, tag.value) for tag in DiffifultyChoice], blank=True, max_length=10)

class Solutions(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=200)
    submittedAt = models.DateTimeField(auto_now_add=True)
    problem_code = models.CharField(max_length=15, null=False, default='')
    code = models.CharField(max_length=8000, null=False, default='')

class TestCases(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    input_data = models.CharField(max_length=200)
    output_data = models.CharField(max_length=200)
    problem_code = models.CharField(max_length=15, null=False, default='')
