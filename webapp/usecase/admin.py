from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(History)
admin.site.register(UseCase)
admin.site.register(UseCaseSpecification)
admin.site.register(SequenceStuff)
admin.site.register(Boundary)
admin.site.register(Controller)
admin.site.register(Entity)
admin.site.register(BasicPath)
admin.site.register(AlternativePath)



