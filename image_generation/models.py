from django.db import models
from django.utils import timezone

class Image(models.Model):
    prompt = models.CharField(max_length=200, blank=False, null=False, db_index=True, default='generic prompt')
    file_name = models.CharField(max_length=200, blank=False, null=False, db_index=True)
    image = models.ImageField(upload_to='images', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.file_name
