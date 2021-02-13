from django.contrib import admin
from .models import Department, Subcategory, Category, Ticket, Comment, Solution


# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name', 'department_image', 'slug']
    prepopulated_fields = {'slug': ('department_name',)}

# admin.site.register(Department)


admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Solution)
