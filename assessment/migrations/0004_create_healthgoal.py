# Generated manually for HealthGoal model

from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0003_alter_healthassessment_height'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_type', models.CharField(choices=[('weight', 'Weight Management'), ('exercise', 'Exercise/Fitness'), ('diet', 'Diet Improvement'), ('smoking', 'Quit Smoking'), ('alcohol', 'Reduce Alcohol'), ('sleep', 'Improve Sleep'), ('stress', 'Stress Management'), ('bp', 'Blood Pressure Control'), ('sugar', 'Blood Sugar Control'), ('other', 'Other')], max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('target_value', models.CharField(blank=True, max_length=100)),
                ('current_value', models.CharField(blank=True, max_length=100)),
                ('start_date', models.DateField()),
                ('target_date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('paused', 'Paused'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('progress', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_goals', to='auth.user')),
            ],
            options={
                'verbose_name': 'Health Goal',
                'verbose_name_plural': 'Health Goals',
            },
        ),
    ]