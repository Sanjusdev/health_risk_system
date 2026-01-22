from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Avg
from django.http import JsonResponse
from .models import HealthAssessment, UserProfile, HealthGoal
from .forms import (
    HealthAssessmentForm, UserProfileForm, CustomUserCreationForm,
    HealthGoalForm
)
from .utils import process_assessment, get_bmi_category, get_bp_category


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Health Risk Assessment.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard view"""
    assessments = HealthAssessment.objects.filter(user=request.user).order_by('-created_at')[:5]
    goals = HealthGoal.objects.filter(user=request.user, status='active').order_by('-created_at')[:5]
    
    # Get latest assessment for summary
    latest_assessment = assessments.first() if assessments else None
    
    # Calculate statistics
    total_assessments = HealthAssessment.objects.filter(user=request.user).count()
    
    # Get average risk score
    avg_risk = HealthAssessment.objects.filter(
        user=request.user,
        overall_risk_score__isnull=False
    ).aggregate(avg=Avg('overall_risk_score'))['avg']
    
    context = {
        'assessments': assessments,
        'goals': goals,
        'latest_assessment': latest_assessment,
        'total_assessments': total_assessments,
        'avg_risk': round(avg_risk, 1) if avg_risk else None,
    }
    
    return render(request, 'dashboard.html', context)


def new_assessment(request):
    """Create new health assessment"""
    if request.method == 'POST':
        form = HealthAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)

            # Only save to database if user is authenticated
            if request.user.is_authenticated:
                assessment.user = request.user
                assessment.save()

                # Process assessment (calculate risks and recommendations)
                assessment = process_assessment(assessment)
                assessment.save()

                messages.success(request, 'Assessment completed and saved successfully!')
                return redirect('assessment_result', pk=assessment.pk)
            else:
                # For guest users, calculate BMI and process without saving
                assessment.calculate_bmi()  # Calculate BMI manually since we don't save
                assessment = process_assessment(assessment)

                # Store assessment data in session for guest results
                # Convert Decimal objects to floats for JSON serialization
                request.session['guest_assessment'] = {
                    'height': float(assessment.height) if assessment.height else 0,
                    'weight': float(assessment.weight) if assessment.weight else 0,
                    'bmi': float(assessment.bmi) if assessment.bmi else 0,
                    'systolic_bp': assessment.systolic_bp,
                    'diastolic_bp': assessment.diastolic_bp,
                    'overall_risk_score': float(assessment.overall_risk_score) if assessment.overall_risk_score else 0,
                    'risk_level': assessment.risk_level,
                    'cardiovascular_risk': float(assessment.cardiovascular_risk) if assessment.cardiovascular_risk else 0,
                    'diabetes_risk': float(assessment.diabetes_risk) if assessment.diabetes_risk else 0,
                    'lifestyle_risk': float(assessment.lifestyle_risk) if assessment.lifestyle_risk else 0,
                    'recommendations': assessment.recommendations,
                }

                messages.info(request, 'Assessment completed! Register or login to save your results.')
                return redirect('guest_assessment_result')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HealthAssessmentForm()

    return render(request, 'assessment.html', {'form': form})


def guest_assessment_result(request):
    """View guest assessment results from session"""
    assessment_data = request.session.get('guest_assessment')

    if not assessment_data:
        messages.error(request, 'No assessment data found. Please complete an assessment first.')
        return redirect('new_assessment')

    # Create a temporary assessment object from session data
    class GuestAssessment:
        def __init__(self, data):
            self.height = data.get('height')
            self.weight = data.get('weight')
            self.bmi = data.get('bmi')
            self.systolic_bp = data.get('systolic_bp')
            self.diastolic_bp = data.get('diastolic_bp')
            self.overall_risk_score = data.get('overall_risk_score')
            self.risk_level = data.get('risk_level')
            self.cardiovascular_risk = data.get('cardiovascular_risk')
            self.diabetes_risk = data.get('diabetes_risk')
            self.lifestyle_risk = data.get('lifestyle_risk')
            self.recommendations = data.get('recommendations')

        def get_risk_level_display(self):
            return dict(HealthAssessment.RISK_LEVEL_CHOICES).get(self.risk_level, 'Unknown')

        def get_risk_level_display(self):
            return dict(HealthAssessment.RISK_LEVEL_CHOICES).get(self.risk_level, 'Unknown')

    assessment = GuestAssessment(assessment_data)

    # Get BMI and BP categories
    bmi_category = get_bmi_category(assessment.bmi)
    bp_category = get_bp_category(assessment.systolic_bp, assessment.diastolic_bp)

    # Split recommendations into a list
    recommendations_list = []
    if assessment.recommendations:
        recommendations_list = [rec.strip() for rec in assessment.recommendations.split('\n\n') if rec.strip()]

    context = {
        'assessment': assessment,
        'bmi_category': bmi_category,
        'bp_category': bp_category,
        'recommendations_list': recommendations_list,
        'is_guest': True,
    }

    return render(request, 'result.html', context)


@login_required
def assessment_result(request, pk):
    """View assessment results"""
    assessment = get_object_or_404(HealthAssessment, pk=pk, user=request.user)

    # Get BMI and BP categories
    bmi_category = get_bmi_category(assessment.bmi)
    bp_category = get_bp_category(assessment.systolic_bp, assessment.diastolic_bp)

    # Get risk level display
    risk_level_display = dict(HealthAssessment.RISK_LEVEL_CHOICES).get(
        assessment.risk_level, 'Unknown'
    )

    # Split recommendations into a list
    recommendations_list = []
    if assessment.recommendations:
        recommendations_list = [rec.strip() for rec in assessment.recommendations.split('\n\n') if rec.strip()]

    context = {
        'assessment': assessment,
        'bmi_category': bmi_category,
        'bp_category': bp_category,
        'risk_level_display': risk_level_display,
        'recommendations_list': recommendations_list,
        'is_guest': False,
    }

    return render(request, 'result.html', context)


@login_required
def assessment_detail(request, pk):
    """View detailed assessment"""
    assessment = get_object_or_404(HealthAssessment, pk=pk, user=request.user)

    bmi_category = get_bmi_category(assessment.bmi)
    bp_category = get_bp_category(assessment.systolic_bp, assessment.diastolic_bp)

    # Split recommendations into a list
    recommendations_list = []
    if assessment.recommendations:
        recommendations_list = [rec.strip() for rec in assessment.recommendations.split('\n\n') if rec.strip()]

    context = {
        'assessment': assessment,
        'bmi_category': bmi_category,
        'bp_category': bp_category,
        'recommendations_list': recommendations_list,
    }

    return render(request, 'assessment_detail.html', context)


@login_required
def assessment_history(request):
    """View all assessments history"""
    assessments = HealthAssessment.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'assessment_history.html', {'assessments': assessments})


@login_required
def profile_view(request):
    """View and edit user profile"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form, 'profile': profile})


@login_required
def goals_list(request):
    """View all health goals"""
    goals = HealthGoal.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'goals_list.html', {'goals': goals})


@login_required
def goal_create(request):
    """Create new health goal"""
    if request.method == 'POST':
        form = HealthGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('goals_list')
    else:
        form = HealthGoalForm()
    
    return render(request, 'goal_form.html', {'form': form, 'title': 'Create New Goal'})


@login_required
def goal_edit(request, pk):
    """Edit health goal"""
    goal = get_object_or_404(HealthGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = HealthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully!')
            return redirect('goals_list')
    else:
        form = HealthGoalForm(instance=goal)
    
    return render(request, 'goal_form.html', {'form': form, 'title': 'Edit Goal', 'goal': goal})


@login_required
def goal_delete(request, pk):
    """Delete health goal"""
    goal = get_object_or_404(HealthGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully!')
        return redirect('goals_list')
    
    return render(request, 'goal_confirm_delete.html', {'goal': goal})


@login_required
def api_assessment_data(request):
    """API endpoint for assessment chart data"""
    assessments = HealthAssessment.objects.filter(
        user=request.user,
        overall_risk_score__isnull=False
    ).order_by('created_at')[:10]
    
    data = {
        'labels': [a.created_at.strftime('%Y-%m-%d') for a in assessments],
        'overall': [a.overall_risk_score for a in assessments],
        'cardiovascular': [a.cardiovascular_risk for a in assessments],
        'diabetes': [a.diabetes_risk for a in assessments],
        'lifestyle': [a.lifestyle_risk for a in assessments],
    }
    
    return JsonResponse(data)
