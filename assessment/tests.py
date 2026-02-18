from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from assessment.models import HealthGoal


class HealthGoalProgressCalculationTests(TestCase):
    """Test cases for automatic progress calculation in HealthGoal model"""
    
    def setUp(self):
        """Create a test user for goal creation"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.start_date = date.today()
        self.target_date = date.today() + timedelta(days=30)
    
    def test_progress_calculation_basic(self):
        """Test basic progress calculation: 50/100 = 50%"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='weight',
            title='Lose Weight',
            target_value='100',
            current_value='50',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        self.assertEqual(goal.progress, 50)
    
    def test_progress_calculation_decimal(self):
        """Test progress calculation with decimal values: 75.5/100 = 76%"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='weight',
            title='Lose Weight',
            target_value='100',
            current_value='75.5',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        self.assertEqual(goal.progress, 76)  # Rounded from 75.5
    
    def test_progress_calculation_over_100(self):
        """Test progress clamping: 150/100 = 100% (clamped)"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='exercise',
            title='Exercise Goal',
            target_value='100',
            current_value='150',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        self.assertEqual(goal.progress, 100)
    
    def test_progress_calculation_zero_target(self):
        """Test division by zero handling: 50/0 = 0%"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='weight',
            title='Test Goal',
            target_value='0',
            current_value='50',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        self.assertEqual(goal.progress, 0)
    
    def test_progress_calculation_non_numeric(self):
        """Test non-numeric value handling: '70 kg'/'100 kg' = unchanged"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='weight',
            title='Weight Goal',
            target_value='100 kg',
            current_value='70 kg',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active',
            progress=25  # Manually set progress
        )
        # Progress should remain at manually set value since values are non-numeric
        self.assertEqual(goal.progress, 25)
    
    def test_progress_calculation_empty_values(self):
        """Test empty value handling: empty values should keep current progress"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='other',
            title='General Goal',
            target_value='',
            current_value='',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active',
            progress=30  # Manually set progress
        )
        self.assertEqual(goal.progress, 30)
    
    def test_progress_update_on_current_value_change(self):
        """Test that progress updates when current_value is changed"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='weight',
            title='Weight Loss',
            target_value='100',
            current_value='25',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        self.assertEqual(goal.progress, 25)
        
        # Update current_value
        goal.current_value = '75'
        goal.save()
        
        # Progress should be recalculated
        self.assertEqual(goal.progress, 75)
    
    def test_progress_calculation_negative_values(self):
        """Test negative value handling: -50/100 = 0% (clamped)"""
        goal = HealthGoal.objects.create(
            user=self.user,
            goal_type='other',
            title='Test Goal',
            target_value='100',
            current_value='-50',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        self.assertEqual(goal.progress, 0)  # Clamped to 0
    
    def test_calculate_progress_method_directly(self):
        """Test the calculate_progress method directly"""
        goal = HealthGoal(
            user=self.user,
            goal_type='weight',
            title='Test',
            target_value='200',
            current_value='100',
            start_date=self.start_date,
            target_date=self.target_date,
            status='active'
        )
        calculated = goal.calculate_progress()
        self.assertEqual(calculated, 50)

