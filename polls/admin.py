"""import admin choice question"""
from django.contrib import admin
from .models import Choice, Question

<<<<<<< HEAD
# class ChoiceInline(admin.TabularInline):
#     """Class that display choice in line."""
#
#     model = Choice
#     extra = 3
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     """Class that display questions."""
#
#     fieldsets = [
#         (None, {'fields': ['question_text']}),
#         ('Date information', {'fields': [
#          'pub_date', 'end_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date',
#                     'end_date', 'was_published_recently')
#     list_filter = ['pub_date']
#     search_fields = ['question_text']

# admin.site.register(Question, QuestionAdmin)
admin.site.register(Question)
admin.site.register(Choice)
=======

class ChoiceInline(admin.TabularInline):
    """Class that display choice in line."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Class that display questions."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': [
         'pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
>>>>>>> iteration2
