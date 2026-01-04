"""
Parse course interests from natural language input
"""
import re
from typing import Dict, List

try:
    from .parser_utils import get_synonyms
except ImportError:
    from synonyms import SYNONYMS


    def get_synonyms():
        return SYNONYMS
    # enddef


# endtry


def parse_interests(input_text: str) -> Dict[str, List[str]]:
    """
    Find course interests in the input text.
    
    Returns dict with:
    - interests: list of courses/subjects user is interested in
    """

    result = {
        "interests": []
    }

    if not input_text:
        return result

    text = input_text.lower()
    synonyms = get_synonyms()

    # check for interest phrases
    interest_phrases = synonyms.get("interest", [])
    courses_dict = synonyms.get("courses", {})

    # look for "interested in X", "want to study Y", etc
    for phrase in interest_phrases:
        # pattern to find course after interest phrase
        pattern = rf"{phrase}\s+([a-z\s]+)"
        matches = re.findall(pattern, text)

        for match in matches:
            course_name = match.strip()

            # check if it's a known course
            for main_course, aliases in courses_dict.items():
                if course_name in aliases or course_name == main_course:
                    if main_course not in result["interests"]:
                        result["interests"].append(main_course)
                    # endif
                    break
                # endif
                # also check partial matches
                elif any(alias in course_name for alias in aliases):
                    if main_course not in result["interests"]:
                        result["interests"].append(main_course)
                    # endif
                    break
                # endif
            # endfor
        # endfor
    # endfor

    return result
# enddef
