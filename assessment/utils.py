"""
Utility functions for health risk assessment calculations
"""
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


def calculate_age(birth_date):
    """Calculate age from birth date"""
    if not birth_date:
        return None
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def get_bmi_category(bmi):
    """Get BMI category based on BMI value"""
    if bmi is None:
        return "Unknown"
    bmi = float(bmi)
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    elif bmi < 35:
        return "Obese Class I"
    elif bmi < 40:
        return "Obese Class II"
    else:
        return "Obese Class III"


def get_bp_category(systolic, diastolic):
    """Get blood pressure category"""
    if systolic is None or diastolic is None:
        return "Unknown"
    
    if systolic < 120 and diastolic < 80:
        return "Normal"
    elif systolic < 130 and diastolic < 80:
        return "Elevated"
    elif systolic < 140 or diastolic < 90:
        return "High Blood Pressure Stage 1"
    elif systolic < 180 or diastolic < 120:
        return "High Blood Pressure Stage 2"
    else:
        return "Hypertensive Crisis"


def calculate_cardiovascular_risk(assessment):
    """
    Calculate cardiovascular risk score (0-100)
    Based on multiple factors including BP, cholesterol, smoking, etc.
    """
    risk_score = 0
    
    # BMI contribution (0-15 points)
    if assessment.bmi:
        bmi = float(assessment.bmi)
        if bmi < 18.5:
            risk_score += 5
        elif bmi < 25:
            risk_score += 0
        elif bmi < 30:
            risk_score += 8
        elif bmi < 35:
            risk_score += 12
        else:
            risk_score += 15
    
    # Blood pressure contribution (0-20 points)
    if assessment.systolic_bp >= 180 or assessment.diastolic_bp >= 120:
        risk_score += 20
    elif assessment.systolic_bp >= 140 or assessment.diastolic_bp >= 90:
        risk_score += 15
    elif assessment.systolic_bp >= 130:
        risk_score += 10
    elif assessment.systolic_bp >= 120:
        risk_score += 5
    
    # Cholesterol contribution (0-15 points)
    if assessment.cholesterol_total:
        if assessment.cholesterol_total >= 240:
            risk_score += 15
        elif assessment.cholesterol_total >= 200:
            risk_score += 10
        elif assessment.cholesterol_total >= 170:
            risk_score += 5
    
    # HDL contribution (0-10 points) - lower is worse
    if assessment.cholesterol_hdl:
        if assessment.cholesterol_hdl < 40:
            risk_score += 10
        elif assessment.cholesterol_hdl < 50:
            risk_score += 5
    
    # Smoking contribution (0-20 points)
    smoking_scores = {
        'never': 0,
        'former': 5,
        'occasional': 10,
        'regular': 15,
        'heavy': 20,
    }
    risk_score += smoking_scores.get(assessment.smoking_status, 0)
    
    # Activity level contribution (0-10 points) - less active is worse
    activity_scores = {
        'very_active': 0,
        'active': 2,
        'moderate': 4,
        'light': 7,
        'sedentary': 10,
    }
    risk_score += activity_scores.get(assessment.activity_level, 5)
    
    # Medical history contribution (0-10 points)
    if assessment.has_heart_disease:
        risk_score += 5
    if assessment.has_hypertension:
        risk_score += 3
    if assessment.family_history_heart:
        risk_score += 2
    
    return min(risk_score, 100)


def calculate_diabetes_risk(assessment):
    """
    Calculate diabetes risk score (0-100)
    Based on BMI, blood sugar, family history, etc.
    """
    risk_score = 0
    
    # BMI contribution (0-25 points)
    if assessment.bmi:
        bmi = float(assessment.bmi)
        if bmi < 25:
            risk_score += 0
        elif bmi < 30:
            risk_score += 10
        elif bmi < 35:
            risk_score += 18
        else:
            risk_score += 25
    
    # Blood sugar contribution (0-30 points)
    if assessment.blood_sugar:
        sugar = float(assessment.blood_sugar)
        if sugar >= 126:
            risk_score += 30  # Diabetic range
        elif sugar >= 100:
            risk_score += 20  # Pre-diabetic
        elif sugar >= 90:
            risk_score += 10
    
    # Waist circumference contribution (0-15 points)
    if assessment.waist_circumference:
        waist = float(assessment.waist_circumference)
        # Using general guidelines (may vary by gender)
        if waist > 102:  # High risk for men
            risk_score += 15
        elif waist > 88:  # High risk for women
            risk_score += 10
        elif waist > 80:
            risk_score += 5
    
    # Activity level contribution (0-10 points)
    activity_scores = {
        'very_active': 0,
        'active': 2,
        'moderate': 4,
        'light': 7,
        'sedentary': 10,
    }
    risk_score += activity_scores.get(assessment.activity_level, 5)
    
    # Diet contribution (0-10 points)
    diet_scores = {
        'excellent': 0,
        'good': 3,
        'fair': 6,
        'poor': 10,
    }
    risk_score += diet_scores.get(assessment.diet_quality, 5)
    
    # Medical history contribution (0-10 points)
    if assessment.has_diabetes:
        risk_score += 5
    if assessment.family_history_diabetes:
        risk_score += 5
    
    return min(risk_score, 100)




def calculate_lifestyle_risk(assessment):
    """
    Calculate lifestyle risk score (0-100)
    Based on blood pressure readings, BMI, age, smoking, family history, and other lifestyle risk factors
    """
    risk_score = 0

    # Blood pressure contribution (0-40 points) - Most important factor
    systolic = assessment.systolic_bp
    diastolic = assessment.diastolic_bp

    if systolic >= 180 or diastolic >= 120:
        risk_score += 40  # Hypertensive crisis
    elif systolic >= 140 or diastolic >= 90:
        risk_score += 30  # Stage 2 hypertension
    elif systolic >= 130 or diastolic >= 80:
        risk_score += 20  # Stage 1 hypertension
    elif systolic >= 120:
        risk_score += 10  # Elevated

    # BMI contribution (0-15 points)
    if assessment.bmi:
        bmi = float(assessment.bmi)
        if bmi >= 30:
            risk_score += 15  # Obese
        elif bmi >= 25:
            risk_score += 10  # Overweight
        elif bmi < 18.5:
            risk_score += 5   # Underweight (also a risk factor)

    # Age contribution (0-10 points) - Hypertension risk increases with age
    try:
        age = calculate_age(assessment.user.profile.date_of_birth) if hasattr(assessment.user, 'profile') and assessment.user.profile.date_of_birth else None
    except (ObjectDoesNotExist, AttributeError):
        age = None
    if age:
        if age >= 65:
            risk_score += 10
        elif age >= 45:
            risk_score += 7
        elif age >= 35:
            risk_score += 4

    # Smoking contribution (0-15 points)
    smoking_scores = {
        'never': 0,
        'former': 5,
        'occasional': 8,
        'regular': 12,
        'heavy': 15,
    }
    risk_score += smoking_scores.get(assessment.smoking_status, 0)

    # Family history contribution (0-10 points)
    if assessment.family_history_heart:
        risk_score += 7
    if assessment.family_history_diabetes:
        risk_score += 3  # Diabetes is also a risk factor for hypertension

    # Alcohol contribution (0-10 points)
    alcohol_scores = {
        'none': 0,
        'occasional': 2,
        'moderate': 6,
        'heavy': 10,
    }
    risk_score += alcohol_scores.get(assessment.alcohol_consumption, 0)

    return min(risk_score, 100)


def calculate_overall_risk(assessment):
    """
    Calculate overall health risk score and level
    Returns tuple of (score, level, cardiovascular, diabetes, lifestyle)
    """
    cardiovascular = calculate_cardiovascular_risk(assessment)
    diabetes = calculate_diabetes_risk(assessment)
    lifestyle = calculate_lifestyle_risk(assessment)
    
    # Weighted average (cardiovascular is weighted more heavily)
    overall = int(cardiovascular * 0.4 + diabetes * 0.3 + lifestyle * 0.3)
    
    # Determine risk level
    if overall < 25:
        level = 'low'
    elif overall < 50:
        level = 'moderate'
    elif overall < 75:
        level = 'high'
    else:
        level = 'very_high'
    
    return overall, level, cardiovascular, diabetes, lifestyle


def generate_recommendations(assessment):
    """
    Generate personalized health recommendations based on assessment
    """
    recommendations = []
    
    # BMI recommendations
    if assessment.bmi:
        bmi = float(assessment.bmi)
        if bmi < 18.5:
            recommendations.append(
                "Your BMI indicates you are underweight. Consider consulting a nutritionist "
                "to develop a healthy weight gain plan with balanced nutrition."
            )
        elif bmi >= 25 and bmi < 30:
            recommendations.append(
                "Your BMI indicates you are overweight. Aim to lose 5-10% of your body weight "
                "through a combination of healthy eating and regular exercise."
            )
        elif bmi >= 30:
            recommendations.append(
                "Your BMI indicates obesity. We strongly recommend consulting with a healthcare "
                "provider to develop a comprehensive weight management plan."
            )
    
    # Blood pressure recommendations
    if assessment.systolic_bp >= 140 or assessment.diastolic_bp >= 90:
        recommendations.append(
            "Your blood pressure is elevated. Reduce sodium intake, exercise regularly, "
            "manage stress, and consult your doctor about medication if needed."
        )
    elif assessment.systolic_bp >= 130:
        recommendations.append(
            "Your blood pressure is slightly elevated. Monitor it regularly and consider "
            "lifestyle modifications like reducing salt and increasing physical activity."
        )
    
    # Blood sugar recommendations
    if assessment.blood_sugar:
        sugar = float(assessment.blood_sugar)
        if sugar >= 126:
            recommendations.append(
                "Your fasting blood sugar is in the diabetic range. Please consult a healthcare "
                "provider immediately for proper diagnosis and treatment."
            )
        elif sugar >= 100:
            recommendations.append(
                "Your fasting blood sugar indicates pre-diabetes. Focus on weight management, "
                "reduce sugar intake, and increase physical activity to prevent progression."
            )
    
    # Cholesterol recommendations
    if assessment.cholesterol_total and assessment.cholesterol_total >= 200:
        recommendations.append(
            "Your total cholesterol is elevated. Reduce saturated fats, increase fiber intake, "
            "exercise regularly, and consider consulting your doctor about treatment options."
        )
    
    # Smoking recommendations
    if assessment.smoking_status in ['regular', 'heavy']:
        recommendations.append(
            "Quitting smoking is one of the best things you can do for your health. "
            "Consider nicotine replacement therapy, counseling, or medication to help quit."
        )
    elif assessment.smoking_status == 'occasional':
        recommendations.append(
            "Even occasional smoking increases health risks. Consider quitting completely "
            "to significantly reduce your risk of heart disease and cancer."
        )
    
    # Alcohol recommendations
    if assessment.alcohol_consumption == 'heavy':
        recommendations.append(
            "Heavy alcohol consumption increases health risks. Consider reducing intake "
            "to moderate levels (1 drink/day for women, 2 for men) or abstaining."
        )
    
    # Activity recommendations
    if assessment.activity_level in ['sedentary', 'light']:
        recommendations.append(
            "Increase your physical activity. Aim for at least 150 minutes of moderate "
            "aerobic activity or 75 minutes of vigorous activity per week."
        )
    
    # Diet recommendations
    if assessment.diet_quality in ['poor', 'fair']:
        recommendations.append(
            "Improve your diet by eating more fruits, vegetables, whole grains, and lean proteins. "
            "Reduce processed foods, sugary drinks, and excessive salt."
        )
    
    # Sleep recommendations
    if assessment.sleep_quality in ['poor', 'fair']:
        recommendations.append(
            "Improve your sleep habits. Aim for 7-9 hours of quality sleep per night. "
            "Maintain a consistent sleep schedule and create a relaxing bedtime routine."
        )
    
    # Stress recommendations
    if assessment.stress_level in ['high', 'very_high']:
        recommendations.append(
            "High stress levels can impact your health. Consider stress management techniques "
            "like meditation, deep breathing, yoga, or speaking with a mental health professional."
        )
    
    # General recommendation if no specific issues
    if not recommendations:
        recommendations.append(
            "Great job! Your health indicators look good. Continue maintaining your healthy "
            "lifestyle with regular exercise, balanced nutrition, and routine health check-ups."
        )
    
    return "\n\n".join(recommendations)


def process_assessment(assessment):
    """
    Process a health assessment: calculate risks and generate recommendations
    """
    # Calculate all risk scores
    overall, level, cardiovascular, diabetes, lifestyle = calculate_overall_risk(assessment)

    # Update assessment with calculated values
    assessment.overall_risk_score = overall
    assessment.risk_level = level
    assessment.cardiovascular_risk = cardiovascular
    assessment.diabetes_risk = diabetes
    assessment.lifestyle_risk = lifestyle
    
    # Generate recommendations
    assessment.recommendations = generate_recommendations(assessment)
    
    return assessment
