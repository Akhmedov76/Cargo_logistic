from django.db import models

from django.conf import settings

from api.base import TimeModelMixin


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/profile_images/', default='default.jpg')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.user.username


class Contact(TimeModelMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts', on_delete=models.CASCADE)
    contact = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='related_contacts', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'contact')

    def __str__(self):
        return f"{self.user.username} ↔ {self.contact.username}"


class Chat(TimeModelMixin, models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"Chat between {', '.join([user.username for user in self.participants.all()])}"


class Message(TimeModelMixin, models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
