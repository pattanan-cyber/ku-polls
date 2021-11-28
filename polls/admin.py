"""import admin, Question, and Choice."""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """Choice for admin."""

    model = Choice
    extra = 3


class QueestionAdmin(admin.ModelAdmin):
    """Question for admin."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {
            'fields': ['pub_date', 'end_date'],
            'classes': ['collapse']
            }),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text',
                    'pub_date',
                    'was_published_recently',
                    'can_vote',
                    'end_date')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QueestionAdmin)
admin.site.register(Choice)
