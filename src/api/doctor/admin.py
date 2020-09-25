from django.contrib import admin


class AssessmentAbstractModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'initial_score', 'score']
    search_fields = ['user__name', 'user__email']


class DailyAssessmentAbstractModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'day', 'status', 'assessment_date']
    search_fields = ['user__name', 'user__email']
    list_filter = ['status']


class DaysRangeAbstractModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'start_range',
        'end_range',
        'required_completions',
        'challenge'
    ]
    search_fields = ['assessments__user__name',
                     'assessments__user__email']
