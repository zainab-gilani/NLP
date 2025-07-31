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
        Extracts and returns a list of dropped subjects found in the input, based on recognized
        dropped/quit/failed phrases.
        Also returns a cleaned version of the input with dropped information removed.

        :param input: str. User input describing subjects, grades, and any dropped/abandoned subjects.
        :return: str. Cleaned input with dropped subjects removed.
        """

        def is_subject_word(word: str) -> bool:
            """
            :param word: Represents a potential subject name or phrase, e.g. 'further maths'
            :return: bool. True if subject has three words or less, otherwise False
            """
            words: list[str] = word.strip()
            word_count: int = len(words)
            if word_count <= 3:
                return True
            else:
                return False
            # endif

        # enddef


        cleaned: str = self.clean_input(input)
        dropped: list[str] = []

        # Split by commas for easier parsing
        cleaned: list[str] = cleaned.split(",")

        # Clean up each chunk for further processing
        parts: list[str] = []
        for x in cleaned:
            parts.append(x.strip())
        # endfor

        previous_was_dropped: bool = False
        cleaned_sentence_parts: list[str] = []

        # Loop through each part/chunk and look for dropped subjects
        for part in parts:
            found: bool = False
            for word in SYNONYMS["dropped"]:
                if part.startswith(word):
                    # Remove the dropped/quit/failed word from the chunk
                    subjects: str = part[len(word):].strip()
                    # Split subjects by 'and'
                    subjects_split: list[str] = re.split(r'and', subjects)

                    for s in subjects_split:
                        subject: str = s.strip()
                        if subject and subject not in dropped and is_subject_word(subject):
                            dropped.append(subject)
                        # endif
                    # endfor
                    found = True
                    previous_was_dropped = True
                    break
                # endif
            # endfor

            if not found:
                # Not a dropped/quit/failed phrase
                is_subject: bool = True
                for word in SYNONYMS["dropped"]:
                    if part.startswith(word):
                        is_subject: bool = False
                        break
                    # endif
                # endfor

                # If previous chunk was a dropped one, and this chunk is a subject, add to dropped
                if previous_was_dropped and is_subject and part not in dropped and is_subject_word(part):
                    dropped.append(part)
                else:
                    # Otherwise, keep this chunk in the cleaned sentence
                    cleaned_sentence_parts.append(part)
                # endif

                previous_was_dropped = False
            # endif
        # endfor

        # Join all non-dropped chunks back together
        cleaned_sentence: str = ", ".join(cleaned_sentence_parts)
        return cleaned_sentence

    # enddef

    def find_grade_subject_pairs(self, input: str) -> dict:
        """
        Extracts individual subject-grade pairs from the remaining input,
        using several patterns to catch all possible combos.
        :param input: str. The cleaned input sentence containing grade/subject info.
        :return: dict. Returns a dict of {normalized_subject: grade}.
        """

        results: dict[str, str] = {}

        # Patterns for different input formats
        patterns: list[tuple[str, str]] = [
            (r"(A\*|A|B|C|D|E|U)\s+in\s+([a-zA-Z\s]+)", "grade in subject"),  # Case 1
            (r"([a-zA-Z\s]+)[\:\-]?\s*(A\*|A|B|C|D|E|U)", "subject: grade"),  # Case 2
            (r"grade in ([a-zA-Z\s]+)(A\*|A|B|C|D|E|U)", "(...) subject is grade"),  # Case 4 pt 1
            (r"\s+([a-zA-Z\s]+)\s+(A\*|A|B|C|D|E|U)", "subject grade")  # Case 4 pt 2
        ]

        subject: str = ""
        grade: str = ""

        cleaned_sentence: str = self.find_dropped_subjects(input)

        # Try all patterns to catch different formats
        for pattern, mode in patterns:
            matches: list[tuple[str, str]] = re.findall(pattern, cleaned_sentence)

            # Debug: show matches for each pattern
            print(f"Pattern: {pattern}, Matches: {matches}")

            for match in matches:
                if mode == "grade in subject":
                    grade, subject = match[0], match[1]
                elif mode == "subject: grade":
                    subject, grade = match[0], match[1]
                elif mode == "(...) subject is grade":
                    subject, grade = match[0], match[1]
                elif mode == "subject grade":
                    subject, grade = match[0], match[1]
                # endif

                # Normalize subject to main name
                subject_norm: str = self.normalize_subject(subject.strip())

                # Only add if not already in the dict
                if subject not in cleaned_sentence and subject not in results:
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
        matches: list[tuple[str, str]] = re.findall(pattern, input)

        for match in matches:
            grades_str: str = match[0]
            subjects_str: str = match[1]

            # Splits grades_str into a list
            grades: list[str] = []
            i: int = 0

            while i < len(grades_str):
                # If current grade is "A" and next grade is "*", join together to make A*
                if grades_str[i] == "A" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("A*")
                    # Skips over the "*"
                    i += 2
                else:
                    # Else, add the single letter grade
                    grades.append(grades_str[i])
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

        return f"Results: {results}, Input: {input}"

    # enddef

    def normalize_subject(self, subject: str) -> str:
        """
        Converts a subject synonym to its main) subject name.

        :param subject: str. The subject name or synonym, e.g. "maths", "comp sci", "bio".
        :return: str. The standardized main subject name (e.g. "mathematics", "computer science", "biology").
        """
        subject: str = subject.lower().strip()

        # Loop through all main subjects and their synonyms
        for main_subject, synonyms in SYNONYMS["subjects"].items():
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

    def find_course_interest(self, input):  # Looks for course of interest
        pass

    # enddef

    def parse(self, input):
        pass
    # enddef


# endclass

parser = GradeParser()

# print(parser.find_grade_subject_pairs("I got A in maths, B in physics and dropped chemistry, and im interested in med"))
print(parser.find_multi_grades("You listen to me now, my grades are AAB in maths, CS, physics"))

