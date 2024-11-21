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


    def __str__(self):
        return self.nama


# Model hubungan Aktor dan Fitur
class ActorFeature(models.Model):
    actor_name = models.CharField(max_length=255)
    feature_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor_name} - {self.feature_name}"


class UseCaseSpecification(models.Model):
    specification_id = models.AutoField(primary_key=True)
    use_case_name = models.CharField(max_length=200)
    actor = models.ForeignKey(ActorFeature, on_delete=models.CASCADE)
    summary_description = models.TextField()
    pre_conditions = models.TextField()
    post_conditions = models.TextField()

    def __str__(self):
        return self.use_case_name


class BasicPath(models.Model):
    use_case_specification = models.ForeignKey(
        UseCaseSpecification,
        on_delete=models.CASCADE,
        related_name="basic_paths"
    )
    basic_actor_step = models.TextField(null=True, blank=True)
    basic_system_step = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Basic Path - Actor: {self.basic_actor_step}, System: {self.basic_system_step}"


class AlternativePath(models.Model):
    use_case_specification = models.ForeignKey(
        UseCaseSpecification,
        on_delete=models.CASCADE,
        related_name="alternative_paths"
    )
    alternative_actor_step = models.TextField(null=True, blank=True)
    alternative_system_step = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Alternative Path - Actor: {self.alternative_actor_step}, System: {self.alternative_system_step}"


class ExceptionPath(models.Model):
    use_case_specification = models.ForeignKey(
        UseCaseSpecification,
        on_delete=models.CASCADE,
        related_name="exception_paths"
    )
    exception_actor_step = models.TextField(null=True, blank=True)
    exception_system_step = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Exception Path - Actor: {self.exception_actor_step}, System: {self.exception_system_step}"


# Uncomment these classes if you want to define Aktor and Fitur models
# class Aktor(models.Model):
#     nama = models.CharField(max_length=100)


class FeatureConnection(models.Model):
    RELATION_TYPE_CHOICES = [
        ('include', 'Include'),
        ('extend', 'Extend'),
        ('none', 'None'),
    ]

    use_case = models.ForeignKey(
        UseCase, 
        on_delete=models.CASCADE, 
        related_name='feature_connections',
        null=True,  
        blank=True  
    )
    feature_start = models.CharField(max_length=255)
    feature_end = models.CharField(max_length=255)
    relation_type = models.CharField(
        max_length=20,
        choices=RELATION_TYPE_CHOICES,
        default='none'
    )

    def __str__(self):
        return f"{self.feature_start} -> {self.feature_end} ({self.relation_type})"

    def to_dict(self):
        return {
            'id': self.id,
            'use_case': self.use_case.id if self.use_case else None,
            'feature_start': self.feature_start,
            'feature_end': self.feature_end,
            'relation_type': self.relation_type,
        }


#     def __str__(self):
#         return self.nama

class SequenceStuff(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (Actor)"


class Sequence(models.Model):
    sequence_stuff = models.ForeignKey(
        SequenceStuff, on_delete=models.CASCADE, null=True)  # Menambahkan null=True
    boundary = models.CharField(max_length=100)
    controller = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    basic_path = models.TextField(null=True, blank=True)
    alternative_path = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Sequence for {self.sequence_stuff.name if self.sequence_stuff else 'No Stuff'} - {self.boundary}"


class Boundary(models.Model):
    name = models.CharField(max_length=100)
    sequence_stuff = models.ForeignKey(
        SequenceStuff, related_name="boundaries", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Controller(models.Model):
    name = models.CharField(max_length=100)
    sequence_stuff = models.ForeignKey(
        SequenceStuff, related_name='controllers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Controller)"


class Entity(models.Model):
    name = models.CharField(max_length=100)
    sequence_stuff = models.ForeignKey(
        SequenceStuff, related_name='entities', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Entity)"


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
