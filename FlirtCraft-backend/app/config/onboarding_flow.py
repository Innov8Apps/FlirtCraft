"""
Onboarding flow configuration for the 5-Screen Streamlined Flow.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class OnboardingStepConfig:
    """Configuration for a single onboarding step."""
    step_id: str
    step_name: str
    step_index: int
    estimated_duration_seconds: int
    can_skip: bool
    required_fields: List[str]
    description: str


# 5-Screen Streamlined Flow Configuration
ONBOARDING_STEPS: List[OnboardingStepConfig] = [
    OnboardingStepConfig(
        step_id="welcome",
        step_name="Welcome & Value Proposition",
        step_index=0,
        estimated_duration_seconds=30,
        can_skip=False,
        required_fields=[],
        description="Introduce FlirtCraft and its value proposition to build trust and excitement"
    ),
    OnboardingStepConfig(
        step_id="age_verification",
        step_name="Age Verification",
        step_index=1,
        estimated_duration_seconds=15,
        can_skip=False,
        required_fields=["birth_date", "age_verified"],
        description="Legal compliance with friendly age verification design"
    ),
    OnboardingStepConfig(
        step_id="registration",
        step_name="Registration/Sign In",
        step_index=2,
        estimated_duration_seconds=45,
        can_skip=False,
        required_fields=["email", "password", "agreed_to_terms", "agreed_to_privacy"],
        description="Secure account creation with Supabase Auth"
    ),
    OnboardingStepConfig(
        step_id="preferences",
        step_name="Preference Setup",
        step_index=3,
        estimated_duration_seconds=60,
        can_skip=False,
        required_fields=["target_gender", "target_age_min", "target_age_max", "relationship_goal"],
        description="Personalize experience without overwhelming the user"
    ),
    OnboardingStepConfig(
        step_id="skill_goals",
        step_name="Skill Goal Selection",
        step_index=4,
        estimated_duration_seconds=45,
        can_skip=False,
        required_fields=["primary_skill_goals", "experience_level", "practice_frequency"],
        description="Align app to user's specific needs and goals"
    )
]

# Total onboarding flow configuration
ONBOARDING_FLOW_CONFIG = {
    "flow_name": "5-Screen Streamlined Flow",
    "version": "2.0.0",
    "total_steps": 5,
    "total_estimated_duration_seconds": 195,  # 3 minutes 15 seconds
    "steps": ONBOARDING_STEPS,
    "completion_requirements": {
        "min_steps_completed": 5,  # All steps required
        "required_steps": ["age_verification", "registration", "preferences", "skill_goals"],
        "allow_skip_welcome": False
    },
    "analytics_tracking": {
        "track_step_timing": True,
        "track_interaction_events": True,
        "track_validation_errors": True,
        "track_abandonment": True
    }
}

# Step validation rules
STEP_VALIDATION_RULES: Dict[str, Dict[str, Any]] = {
    "age_verification": {
        "min_age": 18,
        "max_age": 100,
        "error_messages": {
            "underage": "FlirtCraft is designed for adults 18 and older",
            "invalid_date": "Please enter a valid birth date",
            "future_date": "Birth date cannot be in the future"
        }
    },
    "registration": {
        "email_regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "password_min_length": 8,
        "password_requires_uppercase": True,
        "password_requires_lowercase": True,
        "password_requires_number": True,
        "password_requires_special": True,
        "error_messages": {
            "invalid_email": "Please enter a valid email address",
            "weak_password": "Password must be at least 8 characters with uppercase, lowercase, number, and special character",
            "password_mismatch": "Passwords do not match",
            "terms_required": "You must agree to the Terms of Service",
            "privacy_required": "You must agree to the Privacy Policy"
        }
    },
    "preferences": {
        "min_age_range": 3,  # Minimum age range span
        "max_age_range": 20,  # Maximum age range span
        "valid_genders": ["male", "female", "everyone"],
        "valid_goals": ["dating", "relationships", "practice", "confidence"],
        "error_messages": {
            "invalid_age_range": "Age range must be at least 3 years",
            "invalid_gender": "Please select a valid gender preference",
            "invalid_goal": "Please select a valid relationship goal"
        }
    },
    "skill_goals": {
        "min_skills": 1,
        "max_skills": 4,
        "valid_skills": [
            "conversation_starters",
            "keeping_flow",
            "storytelling",
            "building_confidence",
            "flirting_appropriately",
            "reading_cues",
            "handling_rejection"
        ],
        "valid_experience_levels": ["beginner", "some_experience", "returning", "experienced"],
        "valid_frequencies": ["daily", "weekly", "occasional"],
        "error_messages": {
            "no_skills": "Please select at least one skill goal",
            "too_many_skills": "Please select no more than 4 skill goals to focus on",
            "invalid_experience": "Please select your experience level",
            "invalid_frequency": "Please select how often you'd like to practice"
        }
    }
}

# A/B testing variants for onboarding experiments
AB_TEST_VARIANTS = {
    "welcome_message": {
        "control": "standard",
        "variant_a": "benefit_focused",
        "variant_b": "social_proof"
    },
    "skill_selection": {
        "control": "checkbox_list",
        "variant_a": "card_selection"
    },
    "progress_indicator": {
        "control": "step_numbers",
        "variant_a": "progress_bar",
        "variant_b": "dots"
    }
}

def get_step_config(step_id: str) -> OnboardingStepConfig:
    """Get configuration for a specific step."""
    for step in ONBOARDING_STEPS:
        if step.step_id == step_id:
            return step
    raise ValueError(f"Unknown step_id: {step_id}")

def get_step_validation_rules(step_id: str) -> Dict[str, Any]:
    """Get validation rules for a specific step."""
    return STEP_VALIDATION_RULES.get(step_id, {})

def get_total_estimated_duration() -> int:
    """Get total estimated duration for the onboarding flow in seconds."""
    return sum(step.estimated_duration_seconds for step in ONBOARDING_STEPS)

def get_step_sequence() -> List[str]:
    """Get the ordered sequence of step IDs."""
    return [step.step_id for step in sorted(ONBOARDING_STEPS, key=lambda x: x.step_index)]