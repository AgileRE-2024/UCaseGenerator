from django.contrib import admin
from .models import (
    History, UseCase, ActorFeature, FeatureConnection,
    UseCaseSpecification, BasicPath, AlternativePath, ExceptionPath,
    SequenceStuff, Sequence, Boundary, Controller, Entity,
    Class, Attribute, Operation, Relation, Connection
)

# Register models
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'user')
    search_fields = ('history_id', 'user__username')

@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('use_case_id', 'nama', 'user', 'created_date')
    search_fields = ('use_case_id', 'nama', 'user__username')
    list_filter = ('created_date',)

@admin.register(ActorFeature)
class ActorFeatureAdmin(admin.ModelAdmin):
    list_display = ('actor_name', 'feature_name')
    search_fields = ('actor_name', 'feature_name')

@admin.register(FeatureConnection)
class FeatureConnectionAdmin(admin.ModelAdmin):
    list_display = ('use_case', 'feature_start', 'feature_end', 'relation_type')
    search_fields = ('feature_start', 'feature_end', 'relation_type')
    list_filter = ('relation_type',)

@admin.register(UseCaseSpecification)
class UseCaseSpecificationAdmin(admin.ModelAdmin):
    list_display = ('specification_id', 'use_case_name', 'actor')
    search_fields = ('use_case_name', 'actor')

@admin.register(BasicPath)
class BasicPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'use_case_specification', 'basic_actor_step', 'basic_system_step')
    search_fields = ('basic_actor_step', 'basic_system_step')

@admin.register(AlternativePath)
class AlternativePathAdmin(admin.ModelAdmin):
    list_display = ('id', 'use_case_specification', 'alternative_actor_step', 'alternative_system_step')
    search_fields = ('alternative_actor_step', 'alternative_system_step')

@admin.register(ExceptionPath)
class ExceptionPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'use_case_specification', 'exception_actor_step', 'exception_system_step')
    search_fields = ('exception_actor_step', 'exception_system_step')

@admin.register(SequenceStuff)
class SequenceStuffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'sequence_stuff', 'actor_seq', 'boundary', 'controller', 'entity')
    search_fields = ('actor_seq', 'boundary', 'controller', 'entity')

@admin.register(Boundary)
class BoundaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sequence_stuff')
    search_fields = ('name',)

@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sequence_stuff')
    search_fields = ('name',)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sequence_stuff')
    search_fields = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_ref')
    search_fields = ('name', 'class_ref__name')

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_ref')
    search_fields = ('name', 'class_ref__name')

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'path_name', 'relation', 'class_start', 'class_end', 'relation_reverse')
    search_fields = ('path_name', 'relation', 'relation_reverse')
    list_filter = ('relation', 'relation_reverse')
