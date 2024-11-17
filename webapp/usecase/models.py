from django.contrib.auth.models import User
from django.db import models


class History(models.Model):
    history_id = models.CharField(max_length=6, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"History {self.history_id} untuk User {self.user.username}"

class UseCase(models.Model):
    use_case_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=30)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    # Menyediakan hubungan Many-to-Many untuk Aktor dan Fitur jika diperlukan
    # Jika Anda ingin menambahkan banyak aktor dan fitur pada Use Case, aktifkan baris berikut:
    # aktor = models.ManyToManyField('Aktor', related_name='usecases')
    # fitur = models.ManyToManyField('Fitur', related_name='usecases')

    def __str__(self):
        return self.nama

class UseCaseSpecification(models.Model):
    specification_id = models.CharField(max_length=10, primary_key=True)
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE)
    specification_name = models.CharField(max_length=30)
    exceptions_path = models.TextField()
    preconditions = models.TextField()
    postconditions = models.TextField()
    basic_path = models.TextField()
    alternative_path = models.TextField()
    specification_desc = models.TextField()

    def __str__(self):
        return self.specification_name

# Model hubungan Aktor dan Fitur
class ActorFeature(models.Model):
    actor_name = models.CharField(max_length=255)
    feature_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor_name} - {self.feature_name}"

# Model hubungan antar fitur dalam UseCase
class FeatureConnection(models.Model):
    use_case = models.ForeignKey(
        UseCase, 
        on_delete=models.CASCADE, 
        related_name='feature_connections',
        null=True,  # Membuat field opsional
        blank=True  # Membuat field opsional di form
    )
    feature_start = models.CharField(max_length=255)
    feature_end = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.feature_start} -> {self.feature_end}"
    def to_dict(self):
        return {
            'id': self.id,
            'use_case': self.use_case.id if self.use_case else None,
            'feature_start': self.feature_start,
            'feature_end': self.feature_end,
        }


