from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ExerciseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=50)
    input_data = models.TextField()
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} - {self.created_at}"
