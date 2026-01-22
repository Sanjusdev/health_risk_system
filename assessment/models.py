from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """Extended user profile for additional health information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class HealthAssessment(models.Model):
    """Main health risk assessment model"""
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Light (exercise 1-3 days/week)'),
        ('moderate', 'Moderate (exercise 3-5 days/week)'),
        ('active', 'Active (exercise 6-7 days/week)'),
        ('very_active', 'Very Active (hard exercise daily)'),
    ]
    
    SMOKING_CHOICES = [
        ('never', 'Never smoked'),
        ('former', 'Former smoker'),
        ('occasional', 'Occasional smoker'),
        ('regular', 'Regular smoker'),
        ('heavy', 'Heavy smoker'),
    ]
    
    ALCOHOL_CHOICES = [
        ('none', 'None'),
        ('occasional', 'Occasional (1-2 drinks/week)'),
        ('moderate', 'Moderate (3-7 drinks/week)'),
        ('heavy', 'Heavy (8+ drinks/week)'),
    ]
    
    DIET_CHOICES = [
        ('poor', 'Poor (mostly processed foods)'),
        ('fair', 'Fair (some healthy choices)'),
        ('good', 'Good (balanced diet)'),
        ('excellent', 'Excellent (very healthy diet)'),
    ]
    
    SLEEP_CHOICES = [
        ('poor', 'Poor (less than 5 hours)'),
        ('fair', 'Fair (5-6 hours)'),
        ('good', 'Good (7-8 hours)'),
        ('excellent', 'Excellent (8+ hours)'),
    ]
    
    STRESS_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    
    # Physical measurements
    height = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        help_text="Height in centimeters"
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(20), MaxValueValidator(500)],
        help_text="Weight in kilograms"
    )
    waist_circumference = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text="Waist circumference in centimeters"
    )
    
    # Vital signs
    systolic_bp = models.IntegerField(
        validators=[MinValueValidator(60), MaxValueValidator(250)],
        help_text="Systolic blood pressure (mmHg)",
        verbose_name="Systolic Blood Pressure"
    )
    diastolic_bp = models.IntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(150)],
        help_text="Diastolic blood pressure (mmHg)",
        verbose_name="Diastolic Blood Pressure"
    )
    heart_rate = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(220)],
        help_text="Resting heart rate (bpm)"
    )
    
    # Blood work (optional)
    blood_sugar = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(600)],
        help_text="Fasting blood sugar (mg/dL)"
    )
    cholesterol_total = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(500)],
        help_text="Total cholesterol (mg/dL)"
    )
    cholesterol_hdl = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(150)],
        help_text="HDL cholesterol (mg/dL)"
    )
    cholesterol_ldl = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(400)],
        help_text="LDL cholesterol (mg/dL)"
    )
    
    # Lifestyle factors
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    smoking_status = models.CharField(max_length=20, choices=SMOKING_CHOICES)
    alcohol_consumption = models.CharField(max_length=20, choices=ALCOHOL_CHOICES)
    diet_quality = models.CharField(max_length=20, choices=DIET_CHOICES)
    sleep_quality = models.CharField(max_length=20, choices=SLEEP_CHOICES)
    stress_level = models.CharField(max_length=20, choices=STRESS_CHOICES)
    
    # Medical history
    has_diabetes = models.BooleanField(default=False, verbose_name="Has Diabetes")
    has_hypertension = models.BooleanField(default=False, verbose_name="Has Hypertension")
    has_heart_disease = models.BooleanField(default=False, verbose_name="Has Heart Disease")
    family_history_heart = models.BooleanField(default=False, verbose_name="Family History of Heart Disease")
    family_history_diabetes = models.BooleanField(default=False, verbose_name="Family History of Diabetes")
    family_history_cancer = models.BooleanField(default=False, verbose_name="Family History of Cancer")
    
    # Calculated fields
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overall_risk_score = models.IntegerField(null=True, blank=True)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, blank=True)
    
    # Risk breakdown
    cardiovascular_risk = models.IntegerField(null=True, blank=True)
    diabetes_risk = models.IntegerField(null=True, blank=True)
    lifestyle_risk = models.IntegerField(null=True, blank=True)
    
    # Recommendations
    recommendations = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_bmi(self):
        """Calculate BMI from height and weight"""
        if self.height and self.weight:
            height_m = float(self.height) / 100
            self.bmi = round(float(self.weight) / (height_m ** 2), 2)
        return self.bmi
    
    def save(self, *args, **kwargs):
        self.calculate_bmi()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Assessment for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = 'Health Assessment'
        verbose_name_plural = 'Health Assessments'
        ordering = ['-created_at']


class HealthGoal(models.Model):
    """User health goals tracking"""
    GOAL_TYPE_CHOICES = [
        ('weight', 'Weight Management'),
        ('exercise', 'Exercise/Fitness'),
        ('diet', 'Diet Improvement'),
        ('smoking', 'Quit Smoking'),
        ('alcohol', 'Reduce Alcohol'),
        ('sleep', 'Improve Sleep'),
        ('stress', 'Stress Management'),
        ('bp', 'Blood Pressure Control'),
        ('sugar', 'Blood Sugar Control'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_value = models.CharField(max_length=100, blank=True)
    current_value = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s goal: {self.title}"
    
    class Meta:
        verbose_name = 'Health Goal'
        verbose_name_plural = 'Health Goals'
        ordering = ['-created_at']
