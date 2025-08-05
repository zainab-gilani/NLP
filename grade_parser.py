# Goal:
# To be able to parse the following sentences and extract grade and subject pairs
# So in the end we should have SUBJECT: GRADE
#
# Make a class that will store the parsed grades and their subjects as well as perform the parsing
# Some examples that i will be able to support:
# "I got A in maths, B in physics and dropped chemistry, and im interested in med"
# "I will get A* in further maths, maybe in Physics B and C in Chemistry. I am interested in Law"
# "My grades are AAB in maths, CS, physics"
# "I have A* in biology and I would love to pursue a career in music"
# "My predicted grades are A*AA in maths physics and biology"
# "My grade in math is A, physics B, chemistry A"
# "Math: A, Physics: B, Music: A, I want to do pharmacy"
# "I achieved ABB in English, history and geography, looking to apply for law"
# "When I was little I always wanted to become a pilot. Now I got A in Math and D in Physics. What do I take"
# I got no grade at all in Math they said take it again, and I got a U in Physics. I like Art.

# "I got A in maths, B in physics and dropped chemistry, music, and english and im interested in med"
# "I got A in maths, B in physics and dropped chemistry and music and english and im interested in med"


# Case 1: I got A in maths, B in physics and dropped chemistry, and im interested in med
# Pattern in this: GRADE*SUBJECT
# NOTE: 'dropped' and its subject will be ignored as this is not a valid grade
# Course: Medicine

# Case 2: Math: A, Physics: B, Music: A, I want to do pharmacy
# Pattern in this: SUBJECT*GRADE
# Course: Pharmaceuticals

# Case 3: I achieved ABB in English, history and geography, looking to apply for law
# Pattern in this: GRADE{1...}
# SEPARATELY once we have found a multi grade, we must find EQUAL number of subjects after that
# Course: Law

# Case 4: My grade in math is A, physics B, chemistry A
# Pattern: SUBJECT*GRADE
# (no course found)

# Case 5: When I was little I always wanted to become a pilot. Now I got A in Math and D in Physics. What do I take
# Pattern: GRADE*SUBJECT
# (no course found)

# We will need to normalize subject names to their proper names that we have in our database for matching
# CS -> Computer Science
# Med -> Medicine
# Psych -> Psychology

# NEXT:
# * Type hints
# * More comments and explanation of algorithms and logic
# * Unit tests

import re
from itertools import count

from mini_tests import dropped_phrases
from synonyms import SYNONYMS

class GradeParser:
    GRADE_PATTERN: str = r'\bA\*|A|B|C|D|E|U\b'  # Finds grades like A*, B, U, etc

    def clean_input(self, input: str) -> str:
        """
        Cleans and standardizes the user input by converting to lowercase, removing unnecessary
        words such as 'and' or 'commas' and stripping extra whitespace.

        :param input: str. Raw user input describing subjects, grades, and additional info.
        :return: str. Cleaned and normalized input string.
        """
        # Replace 'and' with ',' for easier splitting, lowercase the whole string, strip extra spaces
        input = input.replace("and", ",").lower().strip()
        parts: list[str] = input.split(",")

        clean_parts: list[str] = []

        # Remove empty or whitespace-only parts
        for p in parts:
            if p.strip():
                clean_parts.append(p.strip())
            # endif
        # endfor

        # Join the cleaned parts back together, comma separated
        input = ", ".join(clean_parts)

        return input

    # enddef

    def find_dropped_subjects(self, input: str) -> str:
        """
        Removes all dropped/quit/failed subjects from the input string,
        based on recognized phrases like 'dropped', 'quit', 'failed', etc.
        Returns the cleaned input with dropped subjects removed.

        :param input: str. User input describing subjects, grades, and any dropped/abandoned subjects.
        :return: str. Cleaned input with dropped subjects removed.
        """

        dropped_phrases: list[str] = SYNONYMS["dropped"]
        sentence = self.clean_input(input).lower()

        # Removes 'dropped/quit/failed/...' subject phrases using regex
        for phrase in dropped_phrases:
            pattern = rf"(?:\bi\s+)?{phrase}\s+([a-z\s]+(?:\sand\s[a-z\s]+)*)"
            sentence = re.sub(pattern, "", sentence)
        #endfor

        # Tidies up leftover punctuation/whitespace
        sentence = re.sub(r',\s*,+', ',', sentence)  # Remove duplicate commas
        sentence = re.sub(r'^\s*,|,\s*$', '', sentence)  # Remove leading/trailing commas
        sentence = re.sub(r'\s+,', ',', sentence)  # Remove spaces before commas
        sentence = re.sub(r',\s+', ', ', sentence)  # Space after commas
        sentence = re.sub(r'\s+', ' ', sentence)  # Collapse extra spaces

        # Removes any 'and' at the start/end or floating in between commas
        sentence = re.sub(r'(^|\s|,)+and(\s|,|$)+', ' ', sentence)
        sentence = sentence.strip(', ').strip()

        # After regex, splits by commas and filter out any chunk that's just a stray subject

        keep: list[str] = []

        for part in sentence.split(","):
            trimmed = part.strip()

            # Only keeps chunk if it actually looks like a grade/real info
            # (e.g. "got a in maths", "b in chem", etc)
            # Removes single words like "music" or "drama" at start
            if trimmed and not (trimmed.isalpha() and len(trimmed.split()) == 1):
                keep.append(trimmed)
            #endif
        #endfor

        # Joins back together
        result = ", ".join(keep).strip(", ")

        return result
    # enddef

    def find_grade_subject_pairs(self, input: str) -> dict[str, str]:
        """
        Extracts individual subject-grade pairs from the remaining input,
        using several patterns to catch all possible combos.
        :param input: str. The cleaned input sentence containing grade/subject info.
        :return: dict. Returns a dict of {normalized_subject: grade}.
        """

        results: dict[str, str] = {}

        cleaned_sentence: str = self.find_dropped_subjects(input)

        # Patterns for different input formats
        patterns: list[tuple[str, str]] = [
            # 1. A* in comp sci, B in math, C in further math, etc.
            (r"(?:\b\w+\s+)?(A\*|A|B|C|D|E|U)\s+in\s+([a-zA-Z\s]+?)(?:,|$)", "grade_in_subject"),
            # 2. maths: A, english literature: B, etc.
            (r"([a-zA-Z\s]+?)\s*[:\-]\s*(A\*|A|B|C|D|E|U)", "subject_colon_grade"),
            # 3. maths B, comp sci A*, further math C, etc.
            (r"([a-zA-Z\s]+?)\s+(A\*|A|B|C|D|E|U)(?:,|$)", "subject_grade"),
            # 4. my grade in geography is D, in history is C
            (r"(?:my grade in|in)\s+([a-zA-Z\s]+?)\s+is\s+(A\*|A|B|C|D|E|U)", "in_subject_is_grade"),
        ]

        print("CLEANED SENTENCE:", cleaned_sentence)
        for pattern, _ in patterns:
            print("Pattern:", pattern, re.IGNORECASE)
            print("Matches:", re.findall(pattern, cleaned_sentence, re.IGNORECASE))
        #endfor

        # Try all patterns to catch different formats
        for pattern, mode in patterns:
            matches: list[tuple[str, str]] = re.findall(pattern, cleaned_sentence, re.IGNORECASE)

            # Debug: show matches for each pattern
            print(f"Pattern: {pattern}, Matches: {matches}")

            for match in matches:
                if mode == "grade_in_subject":
                    # Pattern matches will be either 2 or 3 groups due to (?:^|[^a-zA-Z])
                    if len(match) == 3:
                        grade = match[1]
                        subject = match[2]
                    else: # Subject first, then grade
                        grade = match[0]
                        subject = match[1]
                else:
                    subject = match[0]
                    grade = match[1]
                # endif

                # Clean subject and grade
                subject = subject.strip().lower()
                grade = grade.strip().upper()

                # Normalize subject to main name
                subject_norm: str = self.normalize_subject(subject)

                # Only add if not already in the dict
                if subject_norm and subject_norm not in results:
                    results[subject_norm] = grade
                # endif
            # endfor
        # endfor

        return results

    # enddef

    def find_multi_grades(self, input: str) -> str:
        """
        Extracts multiple grade/subject pairs from sentences with grouped grades, such as 'ABB in maths,
        physics and biology'. Pairs each grade with the corresponding subject in order and returns a dictionary
        mapping normalized subject names to grades.

        :param input: str. The cleaned input sentence containing grade/subject info.
        :return: dict. Keys are normalized subject names (str), values are grades (str).
                     Example: {'mathematics': 'A', 'physics': 'B', 'biology': 'B'}
                     Returns an empty dict if no multi-grade pattern is found.
        """
        results: dict[str, str] = {}

        # Separates the chunk of grades into singular elements in a list
        pattern: str = r'\b([A\*ABCDUE]{2,5})\b\s+in\s+([a-zA-Z\s,]+)'
        matches: list[tuple[str, str]] = re.findall(pattern, input, re.IGNORECASE)

        for match in matches:
            grades_str: str = match[0]
            subjects_str: str = match[1]

            # Splits grades_str into a list
            grades: list[str] = []
            i: int = 0

            while i < len(grades_str):
                # If current grade is "A" and next grade is "*", join together to make A*
                if grades_str[i].upper() == "A" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("A*")
                    # Skips over the "*"
                    i += 2
                else:
                    # Else, add the single letter grade
                    grades.append(grades_str[i].upper())
                    i += 1
                # endif
            # endwhile

            # Cleans up subject_str, replacing "and" with "," for splitting
            subjects_str_replaced: str = subjects_str.replace("and", ",")
            subjects_raw_list: list[str] = subjects_str_replaced.split(",")

            # Cleans each subject and adds to list
            subjects_list: list[str] = []
            for subject in subjects_raw_list:
                subject_clean: str = subject.lower().strip()
                if subject_clean:
                    subjects_list.append(subject_clean)
                # endif
            # endfor

            # Pairs each subject with grade
            for i in range(len(subjects_list)):
                # Uses normalize_subject function to clean input and remove unnecessary parts
                subject_norm: str = self.normalize_subject(subjects_list[i])
                # Assigns grade by position
                if i < len(grades):
                    # Checks to see if there is the same amount of grades and subjects, and pairs them in order
                    grade: str = grades[i]
                else:
                    # If there are more subjects than grades by mistake, the last grade is repeated
                    grade: str = grades[-1]
                # endif
                # Adds normalized subject and assigned grade to dictionary
                results[subject_norm] = grade
            # endfor

            # Removes multi-grade and subject part of the sentence
            # so other functions don't have to parse it again
            chunk: str = f"{grades_str} in {subjects_str}"
            input = input.replace(chunk, "")

        return results

    # enddef

    def normalize_subject(self, subject: str) -> str:
        """
        Converts a subject synonym to its main) subject name.

        :param subject: str. The subject name or synonym, e.g. "maths", "comp sci", "bio".
        :return: str. The standardized main subject name (e.g. "mathematics", "computer science", "biology").
        """
        subject: str = subject.lower().strip()

        subject_phrases: list[str] = SYNONYMS["subjects"]

        # Loop through all main subjects and their synonyms
        for main_subject, synonyms in subject_phrases.items():
            if subject == main_subject:
                return main_subject
            # endif
            for synonym in synonyms:
                if subject == synonym:
                    return main_subject
                # endif
            # endfor
        # endfor
        return subject

    # enddef

    def find_course_interest(self, input: str) -> list[str]:
        """
        Finds and returns all course interests mentioned in the input, using synonyms from the course list.

        :param input: str. User input, e.g. "I'm interested in medicine" or "Looking for economics"
        :return: list[str]. List of canonical course names matched in the input (could be more than one).
        """
        # Gets all possible interest phrases (like "interested in", "looking for", etc.)
        interest_phrases: list[str] = SYNONYMS["interest"]

        # Gets the dictionary of courses and their synonyms
        courses_dict: dict[str, list[str]] = SYNONYMS["courses"]

        # This will store the main course names found in the input
        found_courses: list[str] = []

        # Cleans the user input (removes "and", lowercase, strip spaces)
        cleaned: str = self.clean_input(input)

        # Lowercase version of the cleaned input for easier searching
        cleaned_joined: str = cleaned.lower()

        # Builds search list with all (main, synonym) pairs
        course_search_list: list[tuple[str, str]] = []
        for course, synonyms in courses_dict.items():
            # Adds the main course itself (e.g., "medicine")
            course_search_list.append((course, course))
            # Adds all synonyms for this course (e.g., "med", "mbbs", etc.)
            for synonym in synonyms:
                course_search_list.append((course, synonym))
            #endfor
        #endfor

        # Sorts the search list so that longer synonyms come first
        # (Prevents "english" matching before "english literature")
        for i in range(len(course_search_list)):
            for j in range(i + 1, len(course_search_list)):
                # Compares the length of the search names
                if len(course_search_list[j][1]) > len(course_search_list[i][1]):
                    # Swap if needed so longer phrases come first
                    temp = course_search_list[i]
                    course_search_list[i] = course_search_list[j]
                    course_search_list[j] = temp
                #endif
            #endfor
        #endfor

        # Checks if any interest phrase is present in the input (like "hoping to study", "interested in", etc.)
        found_interest_phrase: bool = False
        for phrase in interest_phrases:
            if phrase in cleaned_joined:
                found_interest_phrase = True
                break
            #endif
        #endfor

        # If interest phrase is found, search for course matches using our big list
        if found_interest_phrase:
            for course, search_name in course_search_list:
                # If the synonym is in the input, and the course hasn't already been added
                if search_name in cleaned_joined:
                    # add the course ONLY IF NOT ALREADY IN THE LIST
                    if course not in found_courses:
                        found_courses.append(course)
                    #endif
                #endif
            #endfor
        #endif

        # If nothing matched, just try finding courses even if there was no clear interest phrase
        # (Catches cases like "medicine" alone at the end of input)
        if not found_courses:
            for course, search_name in course_search_list:
                if search_name in cleaned_joined:
                    if course not in found_courses:
                        found_courses.append(course)
                    #endif
                #endif
            #endfor
        #endif

        # Return the list of found main course names
        return found_courses
    #enddef

    def parse(self, input):
        pass
    # enddef


# endclass

parser = GradeParser()

print(parser.find_course_interest("Interested in english literature"))
# print(parser.find_multi_grades("You listen to me now, my grades are AAB in maths, CS, physics"))

