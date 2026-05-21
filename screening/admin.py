from django.contrib import admin
from .models import Resume, Prediction, HRSession

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('file', 'portal', 'uploaded_at')
    list_filter = ('portal', 'uploaded_at')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('resume', 'category', 'score')

@admin.register(HRSession)
class HRSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_filter', 'min_score', 'created_at')
