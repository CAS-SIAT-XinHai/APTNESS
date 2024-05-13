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


ESCONV_STRATEGIES_TO_EXPLAIN = {
    "Question": "Asking for information related to the problem to help the help-seeker articulate the issues that they face. Open-ended questions are best, and closed questions can be used to get specific information.",
    "Restatement or Paraphrasing": "A simple, more concise rephrasing of the help-seeker’s statements that could help them see their situation more clearly.",
    "Reflection of feelings": "Articulate and describe the help-seeker’s feelings.",
    "Self-disclosure": "Divulge similar experiences that you have had or emotions that you share with the help-seeker to express your empathy.",
    "Affirmation and Reassurance": "Affirm the helpseeker’s strengths, motivation, and capabilities and provide reassurance and encouragement.",
    "Providing Suggestions": "Provide suggestions about how to change, but be careful to not overstep and tell them what to do.",
    "Information": "Provide useful information to the help-seeker, for example with data, facts, opinions, resources, or by answering questions.",
    "Others": "Exchange pleasantries and use other support strategies that do not fall into the above categories.",
    }
