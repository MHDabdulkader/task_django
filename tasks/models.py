from django.db import models
from typing import cast
# Create your models here.
class Task(models.Model):
  STATUS_CHOICES = [
    ('todo', 'Todo'),
    ('in_progress', 'In Progress'),
    ('done', 'Done')
  ]
  PRIORITY_CHOICES = [
    ('low', "Low"),
    ("medium", "Medium"),
    ('high', "High")
  ]
  
  # id = models.BigAutoField()
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
  priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low") # 0 = low, medium = 1, high = 2 
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  due_date = models.DateTimeField(null=True, blank=True)
  
  class Meta: 
    ordering = ['-created_at']
    
  def __str__(self) -> str:
    return cast(str, self.title)