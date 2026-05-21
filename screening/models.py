from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    portal = models.CharField(max_length=10, default='user')  # 'user' or 'hr'

    def __str__(self):
        return self.file.name

class Prediction(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    score = models.FloatField()
    skills_found = models.TextField(blank=True)
    skills_missing = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category} ({self.score})"

class HRSession(models.Model):
    keywords = models.TextField(blank=True)
    category_filter = models.CharField(max_length=100, blank=True)
    min_score = models.IntegerField(default=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HR Session {self.id} — {self.created_at.strftime('%Y-%m-%d %H:%M')}"
