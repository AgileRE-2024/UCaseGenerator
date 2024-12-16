from django.contrib.auth.models import User
from django.db import models
from jsonschema import ValidationError


class History(models.Model):
    history_id = models.CharField(max_length=6, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"History {self.history_id} untuk User {self.user.username}"

# USE CASE DIAGRAM
class UseCase(models.Model):
    use_case_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=30)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class ActorFeature(models.Model):
    actor_name = models.CharField(max_length=255)
    feature_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor_name} - {self.feature_name}"

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
    relation_type = models.CharField(max_length=100, blank=True, null=True)  # Menambahkan kolom relation_type

    def __str__(self):
        return f"{self.feature_start} -> {self.feature_end} ({self.relation_type})"  # Menambahkan relation_type dalam representasi string
    
    def to_dict(self):
        return {
            'id': self.id,
            'use_case': self.use_case.id if self.use_case else None,
            'feature_start': self.feature_start,
            'feature_end': self.feature_end,
            'relation_type': self.relation_type  # Menambahkan relation_type ke dalam dictionary
        }
# --------------------------------------------------------------------------------------------------------------------------------------------------

# SPECIFICATION
class UseCaseSpecification(models.Model):
    specification_id = models.AutoField(primary_key=True)
    use_case_name = models.CharField(max_length=200)
    actor = models.CharField(max_length=200)
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
# --------------------------------------------------------------------------------------------------------------------------------------

# SEQUENCE
class SequenceStuff(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (Actor)"
    
class Sequence(models.Model):
    sequence_stuff = models.ForeignKey(SequenceStuff, on_delete=models.CASCADE, null=True)  # Menambahkan null=True
    actor_seq = models.CharField(max_length=255)
    boundary = models.CharField(max_length=100)
    controller = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    basic_path = models.TextField(null=True, blank=True)
    alternative_path = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"Sequence for {self.sequence_stuff.name if self.sequence_stuff else 'No Stuff'} - {self.boundary}"


class Boundary(models.Model):
    name = models.CharField(max_length=100)
    sequence_stuff = models.ForeignKey(SequenceStuff, related_name="boundaries", on_delete=models.CASCADE)

    def _str_(self):
        return self.name


class Controller(models.Model):
    name = models.CharField(max_length=100)
    sequence_stuff = models.ForeignKey(SequenceStuff, related_name='controllers', on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.name} (Controller)"


class Entity(models.Model):
    name = models.CharField(max_length=100)
    sequence_stuff = models.ForeignKey(SequenceStuff, related_name='entities', on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.name} (Entity)"
    

# -----------------------------------CLASS DIAGRAM--------------------------------------------------------------
# Model untuk menyimpan kelas yang akan digunakan dalam diagram kelas
class Class(models.Model):
    name = models.CharField(max_length=255)  # Nama kelas
    description = models.TextField(blank=True)  # Deskripsi kelas

    def _str_(self):
        return self.name

class Attribute(models.Model):
    class_ref = models.ForeignKey(Class, related_name='attributes', on_delete=models.CASCADE)  # Menghubungkan dengan Class
    name = models.CharField(max_length=255)  # Nama atribut

    def _str_(self):
        return f"{self.name} (Attribute)"

class Operation(models.Model):
    class_ref = models.ForeignKey(Class, related_name='operations', on_delete=models.CASCADE)  # Menghubungkan dengan Class
    name = models.CharField(max_length=255)  # Nama operasi

    def _str_(self):
        return f"{self.name} (Operation)"


# Model untuk menyimpan hubungan antar kelas dalam diagram kelas
class Relation(models.Model):
    name = models.CharField(max_length=255)  # Nama hubungan (misal: inheritance, association, dll.)

    def _str_(self):
        return self.name


class Connection(models.Model):
    RELATION_CHOICES = [
        ('0..1', '0..1'),
        ('1..', '1..'),
        ('0..', '0..'),
        ('1', '1'),
    ]

    path_name = models.CharField(max_length=255)  # Nama jalur koneksi
    relation = models.CharField(max_length=5, choices=RELATION_CHOICES, blank=True, null=True)  # Relasi
    class_start = models.ForeignKey(
        'Class', on_delete=models.CASCADE, related_name='start_connections'
    )  # Kelas awal
    class_end = models.ForeignKey(
        'Class', on_delete=models.CASCADE, related_name='end_connections'
    )  # Kelas akhir
    relation_reverse = models.CharField(
        max_length=5, choices=RELATION_CHOICES, blank=True, null=True
    )  # Relasi terbalik

    def clean(self):
        super().clean()
        # Validasi nilai relation_reverse
        valid_choices = [choice[0] for choice in self.RELATION_CHOICES]
        if self.relation_reverse and self.relation_reverse not in valid_choices:
            raise ValidationError({'relation_reverse': "Invalid value for relation_reverse."})

    def _str_(self):
        return self.path_name