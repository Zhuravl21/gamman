from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField("Сообщение")
    created = models.DateTimeField("Создано", auto_now_add=True)
    read = models.BooleanField("Прочитано", default=False)

    def __str__(self):
        return f'Notification for {self.user.username}'
