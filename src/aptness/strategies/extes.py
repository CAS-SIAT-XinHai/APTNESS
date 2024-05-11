import dataclasses
from enum import Enum

extes_strategy = ['Reflective Statements', 'Clarification', 'Emotional Validation', 'Empathetic Statements',
                  'Affirmation', 'Offer Hope', 'Avoid judgment and criticism', 'Suggest Options',
                  'Collaborative Planning', 'Provide Different Perspectives', 'Reframe Negative Thoughts',
                  'Share Information', 'Normalize Experiences', 'Promote Self-Care Practices', 'Stress Management',
                  'Others', 'None']


def strategy_name(strategy):
    if strategy == '':
        strategy = 'None'
    if 'Validation' in strategy or 'Validate' in strategy:
        strategy = 'Emotional Validation'
    if 'Information' in strategy:
        strategy = 'Share Information'
    if 'Reflection' in strategy or 'Reflective' in strategy or 'Reflected' in strategy:
        strategy = 'Reflective Statements'
    if 'Options' in strategy or 'Suggestions' in strategy:
        strategy = 'Suggest Options'
    if 'Encouragement' in strategy:
        strategy = 'Affirmation'
    return strategy


class EXTESStrategies(str, Enum):
    REFLECTIVE_STATEMENTS = "Reflective Statements"
    CLARIFICATION = "Clarification"
    EMOTIONAL_VALIDATION = "Emotional Validation"
    EMPATHETIC_STATEMENTS = "Empathetic Statements"
    AFFIRMATION = "Affirmation"
    OFFER_HOPE = "Offer Hope"
    AVOID_JUDGMENT_AND_CRITICISM = "Avoid Judgment and Criticism"
    SUGGEST_OPTIONS = "Suggest Options"
    COLLABORATIVE_PLANNING = "Collaborative Planning"
    PROVIDE_DIFFERENT_PERSPECTIVES = "Provide Different Perspectives"
    REFRAME_NEGATIVE_THOUGHTS = "Reframe Negative Thoughts"
    SHARE_INFORMATION = "Share Information"
    NORMALIZE_EXPERIENCES = "Normalize Experiences"
    PROMOTE_SELF_CARE_PRACTICES = "Promote Self-Care Practices"
    STRESS_MANAGEMENT = "Stress Management"
    Others = "Others"
    Greetings = "Greetings"


EXTES_STRATEGIES_TO_EXPLAIN = {
    "Reflective Statements": "Repeat or rephrase what the person has expressed to show that you're actively listening.",
    "Clarification": "Seek clarification to ensure a clear understanding of the person's emotions and experiences.",
    "Emotional Validation": "Acknowledge and validate the person's emotions without judgment.",
    "Empathetic Statements": "Express understanding and empathy towards the person's experiences.",
    "Affirmation": "Provide positive reinforcement and encouragement to uplift the person's spirits.",
    "Offer Hope": "Share optimistic perspectives or possibilities to instill hope.",
    "Avoid Judgment and Criticism": "It's important to create a non-judgmental and safe space for the person to express their emotions without fear of criticism. Refrain from passing judgment or being overly critical of their experiences or choices.",
    "Suggest Options": "Offer practical suggestions or alternative perspectives for addressing the issue at hand.",
    "Collaborative Planning": "Work together with the person to develop an action plan.",
    "Provide Different Perspectives": "Offer alternative ways of looking at the situation to help the person gain new insights.",
    "Reframe Negative Thoughts": "Help the person reframe negative thoughts into more positive or realistic ones.",
    "Share Information": "Provide educational or factual information about emotions, coping mechanisms, or self-care practices.",
    "Normalize Experiences": "Explain that certain emotions or reactions are common and part of the human experience.",
    "Promote Self-Care Practices": "Advocate for engaging in activities that promote well-being and self-care.",
    "Stress Management": "Provide suggestions for stress management techniques like exercise, meditation, or spending time in nature.",
    "Others": "Other strategies.",
    "Greetings": "The greeting or closing part of a conversation."}
