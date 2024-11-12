from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    history_id = models.CharField(max_length=6, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"History {self.history_id} for User {self.user.username}"

class UseCase(models.Model):
    use_case_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=30)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    # Uncomment and modify if you have Aktor and Fitur models defined
    # aktor = models.ManyToManyField('Aktor', related_name='usecases')
    # fitur = models.ManyToManyField('Fitur', related_name='usecases')

    def __str__(self):
        return self.nama


class ActorFeature(models.Model):
    actor_name = models.CharField(max_length=255)
    feature_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor_name} - {self.feature_name}"
    

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


# Uncomment these classes if you want to define Aktor and Fitur models
# class Aktor(models.Model):
#     nama = models.CharField(max_length=100)

#     def __str__(self):
#         return self.nama

# class Fitur(models.Model):
#     nama = models.CharField(max_length=100)

#     def __str__(self):
#         return self.nama
