# Manual Test Script for HealthGoal Progress Calculation
# Run this with: python manage.py shell < test_progress.py

from django.contrib.auth.models import User
from assessment.models import HealthGoal
from datetime import date, timedelta

# Get or create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print("✓ Created test user")
else:
    print("✓ Using existing test user")

# Test 1: Basic calculation (50/100 = 50%)
print("\n--- Test 1: Basic Calculation ---")
goal1 = HealthGoal.objects.create(
    user=user,
    goal_type='weight',
    title='Test Goal 1: Basic Calculation',
    target_value='100',
    current_value='50',
    start_date=date.today(),
    target_date=date.today() + timedelta(days=30),
    status='active'
)
print(f"Target: {goal1.target_value}, Current: {goal1.current_value}")
print(f"Expected Progress: 50%, Actual Progress: {goal1.progress}%")
print(f"✓ PASS" if goal1.progress == 50 else f"✗ FAIL")

# Test 2: Over 100% (150/100 = 100% clamped)
print("\n--- Test 2: Over 100% Clamping ---")
goal2 = HealthGoal.objects.create(
    user=user,
    goal_type='exercise',
    title='Test Goal 2: Over 100%',
    target_value='100',
    current_value='150',
    start_date=date.today(),
    target_date=date.today() + timedelta(days=30),
    status='active'
)
print(f"Target: {goal2.target_value}, Current: {goal2.current_value}")
print(f"Expected Progress: 100%, Actual Progress: {goal2.progress}%")
print(f"✓ PASS" if goal2.progress == 100 else f"✗ FAIL")

# Test 3: Division by zero (50/0 = 0%)
print("\n--- Test 3: Division by Zero ---")
goal3 = HealthGoal.objects.create(
    user=user,
    goal_type='other',
    title='Test Goal 3: Division by Zero',
    target_value='0',
    current_value='50',
    start_date=date.today(),
    target_date=date.today() + timedelta(days=30),
    status='active'
)
print(f"Target: {goal3.target_value}, Current: {goal3.current_value}")
print(f"Expected Progress: 0%, Actual Progress: {goal3.progress}%")
print(f"✓ PASS" if goal3.progress == 0 else f"✗ FAIL")

# Test 4: Update current_value (25 -> 75)
print("\n--- Test 4: Update Current Value ---")
goal4 = HealthGoal.objects.create(
    user=user,
    goal_type='weight',
    title='Test Goal 4: Update Test',
    target_value='100',
    current_value='25',
    start_date=date.today(),
    target_date=date.today() + timedelta(days=30),
    status='active'
)
print(f"Initial - Target: {goal4.target_value}, Current: {goal4.current_value}, Progress: {goal4.progress}%")
goal4.current_value = '75'
goal4.save()
print(f"Updated - Target: {goal4.target_value}, Current: {goal4.current_value}, Progress: {goal4.progress}%")
print(f"✓ PASS" if goal4.progress == 75 else f"✗ FAIL")

# Test 5: Non-numeric values
print("\n--- Test 5: Non-Numeric Values ---")
goal5 = HealthGoal.objects.create(
    user=user,
    goal_type='weight',
    title='Test Goal 5: Non-Numeric',
    target_value='100 kg',
    current_value='70 kg',
    start_date=date.today(),
    target_date=date.today() + timedelta(days=30),
    status='active',
    progress=35  # Manually set
)
print(f"Target: {goal5.target_value}, Current: {goal5.current_value}")
print(f"Expected Progress: 35% (unchanged), Actual Progress: {goal5.progress}%")
print(f"✓ PASS" if goal5.progress == 35 else f"✗ FAIL")

print("\n" + "="*50)
print("All manual tests completed!")
print("="*50)

# Clean up
print("\nCleaning up test goals...")
HealthGoal.objects.filter(title__startswith='Test Goal').delete()
print("✓ Cleanup complete")
