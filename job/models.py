from django.db import models

from core.models import TimeStampedModel
from company.models import Company
from users.models   import User

class Recruitment(TimeStampedModel):
    content      = models.TextField()
    compensation = models.IntegerField()
    position     = models.CharField(max_length=100)
    skill        = models.CharField(max_length=100)
    company      = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "recruitments"

class UserRecruitment(TimeStampedModel):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    recruitment = models.ForeignKey(Recruitment, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_recruitment"
