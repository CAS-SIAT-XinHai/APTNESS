from enum import Enum


class ESConvStrategies(str, Enum):
    QUESTION = 'Question'
    GREETINGS = 'Greetings'
    INFORMATION = "Information"
    RESTATEMENT_OR_PARAPHRASING = 'Restatement or Paraphrasing'
    PROVIDING_SUGGESTIONS = 'Providing Suggestions'
    AFFIRMATION_AND_REASSURANCE = 'Affirmation and Reassurance'
    SELF_DISCLOSURE = 'Self-disclosure'
    REFLECTION_OF_FEELINGS = 'Reflection of feelings'
