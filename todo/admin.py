from django.contrib import admin
from .models import ToDo
from .models import ToDoPriority

class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('dt_created',)

admin.site.register(ToDo, ToDoAdmin)
admin.site.register(ToDoPriority)