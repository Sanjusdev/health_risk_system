from django.contrib import admin
from .models import UserProfile, HealthAssessment, HealthGoal


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'phone', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'date_of_birth', 'gender', 'phone', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HealthAssessment)
class HealthAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'created_at', 'bmi', 'risk_level',
        'overall_risk_score', 'systolic_bp', 'diastolic_bp'
    )
    list_filter = ('risk_level', 'activity_level', 'smoking_status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = (
        'bmi', 'overall_risk_score', 'risk_level',
        'cardiovascular_risk', 'diabetes_risk', 'lifestyle_risk',
        'recommendations', 'created_at', 'updated_at'
    )
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Physical Measurements', {
            'fields': ('height', 'weight', 'waist_circumference', 'bmi')
        }),
        ('Vital Signs', {
            'fields': ('systolic_bp', 'diastolic_bp', 'heart_rate')
        }),
        ('Blood Work', {
            'fields': ('blood_sugar', 'cholesterol_total', 'cholesterol_hdl', 'cholesterol_ldl'),
            'classes': ('collapse',)
        }),
        ('Lifestyle Factors', {
            'fields': (
                'activity_level', 'smoking_status', 'alcohol_consumption',
                'diet_quality', 'sleep_quality', 'stress_level'
            )
        }),
        ('Medical History', {
            'fields': (
                'has_diabetes', 'has_hypertension', 'has_heart_disease',
                'family_history_heart', 'family_history_diabetes', 'family_history_cancer'
            )
        }),
        ('Risk Assessment Results', {
            'fields': (
                'overall_risk_score', 'risk_level',
                'cardiovascular_risk', 'diabetes_risk', 'lifestyle_risk'
            )
        }),
        ('Recommendations', {
            'fields': ('recommendations',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HealthGoal)
class HealthGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'goal_type', 'status', 'progress', 'target_date')
    list_filter = ('goal_type', 'status', 'created_at')
    search_fields = ('user__username', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Goal Details', {
            'fields': ('goal_type', 'title', 'description')
        }),
        ('Progress', {
            'fields': ('target_value', 'current_value', 'progress', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'target_date')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
