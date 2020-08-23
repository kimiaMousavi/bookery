from django.db import models
from django.contrib.auth.models import User


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.TextField(max_length=30)
    date_added = models.DateField()
    # 1) status == 0 >> want to read 2) status == 1 >> read
    status = models.IntegerField(default=0)
    review = models.TextField(default='', max_length=500)

    def read(self):
        self.status = 1
        self.save()
