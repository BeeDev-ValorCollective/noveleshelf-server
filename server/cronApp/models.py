from django.db import models


class CronLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('warning', 'Warning'),
    ]

    job_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    message = models.TextField(null=True, blank=True)
    records_affected = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job_name} - {self.status} - {self.created_at}'

    class Meta:
        ordering = ['-created_at']