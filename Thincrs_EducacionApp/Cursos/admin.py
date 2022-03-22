from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CourseModel)
admin.site.register(CourseRetireModel)

#admin.site.register(Course2Model)
"""admin.site.register(WhatYouWillLearnModel)
admin.site.register(CourseHasWhatYouWillLearn)

admin.site.register(CaptionLanguagesModel)
admin.site.register(CourseHasCaptionLanguage)
admin.site.register(InstructorsModel)

admin.site.register(CourseHasInstructor)
admin.site.register(RequirementsModel)
admin.site.register(CourseHasRequirement)

admin.site.register(LocalesModel)
admin.site.register(CourseHasLocales)
admin.site.register(CategoriesModel)

admin.site.register(CourseHasCategories)
admin.site.register(PrimaryCategoriesModel)
admin.site.register(CourseHasPrimaryCategories)

admin.site.register(RequiredEducationModel)
admin.site.register(CourseHasRequiredEducation)"""

# Register your models here.
# Register your models here.
# Register your models here.
