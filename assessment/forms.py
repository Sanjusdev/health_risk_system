from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HealthAssessment, UserProfile, HealthGoal


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """User profile form"""
    class Meta:
        model = UserProfile
        fields = [
            'date_of_birth', 'gender', 'phone', 'address',
            'emergency_contact', 'emergency_phone'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact name'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact phone'}),
        }


class HealthAssessmentForm(forms.ModelForm):
    """Health assessment form"""
    class Meta:
        model = HealthAssessment
        fields = [
            # Physical measurements
            'height', 'weight', 'waist_circumference',
            # Vital signs
            'systolic_bp', 'diastolic_bp', 'heart_rate',
            # Blood work
            'blood_sugar', 'cholesterol_total', 'cholesterol_hdl', 'cholesterol_ldl',
            # Lifestyle factors
            'activity_level', 'smoking_status', 'alcohol_consumption',
            'diet_quality', 'sleep_quality', 'stress_level',
            # Medical history
            'has_diabetes', 'has_hypertension', 'has_heart_disease',
            'family_history_heart', 'family_history_diabetes', 'family_history_cancer',
        ]
        widgets = {
            # Physical measurements
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in cm (e.g., 170)',
                'min': '50',
                'max': '300',
                'step': '0.1'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg (e.g., 70)',
                'min': '20',
                'max': '500',
                'step': '0.1'
            }),
            'waist_circumference': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Waist in cm (optional)',
                'min': '30',
                'max': '200',
                'step': '0.1'
            }),
            # Vital signs
            'systolic_bp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Systolic (e.g., 120)',
                'min': '60',
                'max': '250'
            }),
            'diastolic_bp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Diastolic (e.g., 80)',
                'min': '40',
                'max': '150'
            }),
            'heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Heart rate (optional)',
                'min': '30',
                'max': '220'
            }),
            # Blood work
            'blood_sugar': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fasting blood sugar (optional)',
                'min': '30',
                'max': '600',
                'step': '0.1'
            }),
            'cholesterol_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total cholesterol (optional)',
                'min': '50',
                'max': '500'
            }),
            'cholesterol_hdl': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'HDL cholesterol (optional)',
                'min': '10',
                'max': '150'
            }),
            'cholesterol_ldl': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'LDL cholesterol (optional)',
                'min': '30',
                'max': '400'
            }),
            # Lifestyle factors
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
            'smoking_status': forms.Select(attrs={'class': 'form-control'}),
            'alcohol_consumption': forms.Select(attrs={'class': 'form-control'}),
            'diet_quality': forms.Select(attrs={'class': 'form-control'}),
            'sleep_quality': forms.Select(attrs={'class': 'form-control'}),
            'stress_level': forms.Select(attrs={'class': 'form-control'}),
            # Medical history
            'has_diabetes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_hypertension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_heart_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'family_history_heart': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'family_history_diabetes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'family_history_cancer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make optional fields not required
        optional_fields = [
            'waist_circumference', 'heart_rate', 'blood_sugar',
            'cholesterol_total', 'cholesterol_hdl', 'cholesterol_ldl'
        ]
        for field_name in optional_fields:
            self.fields[field_name].required = False


class HealthGoalForm(forms.ModelForm):
    """Health goal form"""
    class Meta:
        model = HealthGoal
        fields = [
            'goal_type', 'title', 'description', 'target_value',
            'current_value', 'start_date', 'target_date', 'status',
            'progress', 'notes'
        ]
        widgets = {
            'goal_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Goal title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your goal'}),
            'target_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Target value (e.g., 70 kg)'}),
            'current_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current value'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes'}),
        }
