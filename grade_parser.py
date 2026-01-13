#!/usr/bin/env python3
import re
from .parser_utils import get_synonyms


class GradeParser:
    GRADE_PATTERN: str = r'\bA\*|D\*|A|B|C|D|E|U|M|P\b'  # Finds grades like A*, D*, B, M, P, etc

    def clean_input(self, input: str) -> str:
        """
        Cleans and standardizes the user input by converting to lowercase, removing unnecessary
        words such as 'and' or 'commas' and stripping extra whitespace.

        :param input: str
            Raw user input describing subjects, grades, and additional info.
        :return: str
            Cleaned and normalized input string.
        """

        # Replace 'and' with ',' for easier splitting, lowercase the whole string, strip extra spaces
        input: str = input.replace(" and ", ",").lower().strip()
        parts: list[str] = input.split(",")

        clean_parts: list[str] = []

        # Remove empty or whitespace-only parts
        for p in parts:
            if p.strip():
                clean_parts.append(p.strip())
            # endif
        # endfor

        # Join the cleaned parts back together, comma separated
        input: str = ", ".join(clean_parts)

        return input

    # enddef

    def find_dropped_subjects(self, input: str) -> str:
        """
        Removes all dropped/quit/failed subjects from the input string,
        based on recognized phrases like 'dropped', 'quit', 'failed', etc.
        Returns the cleaned input with dropped subjects removed.

        :param input: str
            User input describing subjects, grades, and any dropped/abandoned subjects.
        :return: str
            Cleaned input with dropped subjects removed.
        """

        dropped_phrases: list[str] = get_synonyms()["dropped"]
        sentence: str = self.clean_input(input).lower()

        # Removes 'dropped/quit/failed/...' subject phrases using regex
        for phrase in dropped_phrases:
            pattern: str = rf"(?:\bi\s+)?{phrase}\s+([a-z\s]+(?:\sand\s[a-z\s]+)*)"
            sentence: str = re.sub(pattern, "", sentence)
        # endfor

        # Tidies up leftover punctuation/whitespace
        sentence: str = re.sub(r',\s*,+', ',', sentence)  # Remove duplicate commas
        sentence: str = re.sub(r'^\s*,|,\s*$', '', sentence)  # Remove leading/trailing commas
        sentence: str = re.sub(r'\s+,', ',', sentence)  # Remove spaces before commas
        sentence: str = re.sub(r',\s+', ', ', sentence)  # Space after commas
        sentence: str = re.sub(r'\s+', ' ', sentence)  # Collapse extra spaces

        # Removes any 'and' at the start/end or floating in between commas
        sentence: str = re.sub(r'(^|\s|,)+and(\s|,|$)+', ' ', sentence)
        sentence: str = sentence.strip(', ').strip()

        # After regex, splits by commas and filter out any chunk that's just a stray subject

        keep: list[str] = []
        parts = sentence.split(",")

        # Check if input has a dropped keyword
        has_dropped_keyword: bool = False
        for phrase in dropped_phrases:
            if phrase in input.lower():
                has_dropped_keyword = True
                break
            # endif
        # endfor

        # Process each part
        for i in range(len(parts)):
            trimmed: str = parts[i].strip()

            # Only removes single words if they're at the very start AND the original
            # input had a dropped phrase. Otherwise keep them (they might be part of a list)
            is_single_word = trimmed.isalpha() and len(trimmed.split()) == 1
            at_start = i == 0

            if trimmed and not (is_single_word and at_start and has_dropped_keyword):
                keep.append(trimmed)
            # endif
        # endfor

        # Joins back together
        result: str = ", ".join(keep).strip(", ")

        return result

    # enddef

    def find_all_grades(self, input: str) -> dict[str, str]:
        """
        Unified function to extract all grade/subject pairs from input,
        handling both multi-grade patterns (AAB in ...) and single-grade patterns.

        :param input: str
            The user input containing grade/subject info.
        :return: dict
            Returns a dict of {normalized_subject: grade}.
        """

        results: dict[str, str] = {}

        # Keep track of original input for special pattern processing
        modified_input = input

        # First, handle "A in Subject1 Subject2 and Subject3" pattern on original input
        # This needs to be done before clean_input replaces "and" with ","
        # Only match when there are multiple single-word subjects (like "Math Chem and Bio")
        single_grade_multiple_subjects_pattern = r'\b(?:got\s+|have\s+|achieved\s+|received\s+)?(A\*|D\*|[A-U])\s+in\s+([A-Za-z]+\s+[A-Za-z]+\s+and\s+[A-Za-z]+)'
        matches = re.findall(single_grade_multiple_subjects_pattern, input, re.IGNORECASE)

        for match in matches:
            grade = match[0].strip().upper()
            subjects_str = match[1].strip()

            # Split by "and" to get individual subjects
            subjects = subjects_str.split(" and ")

            for subject in subjects:
                subject = subject.strip()
                # Each subject might be multiple words like "Further Maths"
                # But we also need to handle "Math Chem" as two separate subjects
                # Let's check if the whole phrase is a known subject first
                subject_norm = self.normalize_subject(subject.lower())

                if subject_norm == subject.lower():
                    # Not recognized as a whole, try splitting by spaces
                    words = subject.split()
                    for word in words:
                        word_norm = self.normalize_subject(word.lower())
                        if word_norm != word.lower():  # It got normalized
                            if word_norm not in results:
                                results[word_norm] = grade
                            # endif
                        # endif
                    # endfor
                else:
                    # Recognized as a whole subject
                    if subject_norm not in results:
                        results[subject_norm] = grade
                    # endif
                # endif
            # endfor

            # Remove the matched pattern from input to avoid double processing
            pattern_to_remove = rf'\b(?:got\s+|have\s+|achieved\s+|received\s+)?{re.escape(match[0])}\s+in\s+{re.escape(match[1])}'
            modified_input = re.sub(pattern_to_remove, '', modified_input, flags=re.IGNORECASE)
        # endfor

        # Start with clean sentence, dropped subjects removed  
        cleaned_sentence: str = self.find_dropped_subjects(modified_input)

        def process_multi_grade(match) -> str:
            """
            Helper function to process multi-grade patterns like "AAB in Maths, Physics, Chemistry".
            Takes a regex match containing grades and subjects, then assigns grades to subjects
            in sequence order (first grade to first subject, second grade to second subject, etc.).
            
            :param match: re.Match
                Regex match object containing groups for grades (group 1) and subjects (group 2).
                Example match: "AAB in Maths, Physics, Chemistry" where group(1)="AAB" and group(2)="Maths, Physics, Chemistry"
            :return: str
                Empty string (used to remove the processed pattern from the original text)
            """
            grades_str: str = match.group(1)
            subjects_str: str = match.group(2)

            # Split grades string into individual grades
            grades: list[str] = []
            i: int = 0

            while i < len(grades_str):
                # Handle A* and D* as single grades
                if grades_str[i].upper() == "A" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("A*")
                    i += 2
                elif grades_str[i].upper() == "D" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("D*")
                    i += 2
                else:
                    grades.append(grades_str[i].upper())
                    i += 1
                # endif
            # endwhile

            # Clean and split subjects
            subjects_str = subjects_str.replace(" and ", ",")
            subjects_str = subjects_str.replace("  ", " ")

            subjects_list: list[str] = []

            # check if they used commas or just spaces between subjects
            if "," in subjects_str:
                # they used commas like "Maths, Physics, Chemistry"
                for subject in subjects_str.split(","):
                    subject_clean: str = subject.lower().strip()
                    if subject_clean:
                        subjects_list.append(subject_clean)
                    # endif
                # endfor
            else:
                # they used spaces like "Maths Physics Chemistry"
                words = subjects_str.strip().split()
                for word in words:
                    subject_clean: str = word.lower().strip()
                    if subject_clean:
                        subjects_list.append(subject_clean)
                    # endif
                # endfor
            # endif

            # Pair grades with subjects
            for i in range(len(subjects_list)):
                subject_norm: str = self.normalize_subject(subjects_list[i])
                # Assign grade by position, use last grade if more subjects than grades
                grade: str = grades[i] if i < len(grades) else grades[-1]

                if subject_norm:
                    results[subject_norm] = grade
                # endif
            # endfor

            # Return empty string to remove this from sentence
            return ""

        # enddef

        # First pass: Find and process multi-grade patterns (AAB in ...)
        multi_pattern: str = r'\b((?:A\*|D\*|[A-U]){2,})\s+in\s+([a-zA-Z\s,]+?)(?:\.|,\s*[a-zA-Z]+\s+in\s|$)'
        remaining: str = re.sub(multi_pattern, process_multi_grade, cleaned_sentence, flags=re.IGNORECASE)

        # check for patterns like "I got BBB" where they don't say subjects
        # match 2-4 grades together (not single letters cos they might be words)
        standalone_grades_pattern = r'\b(?:got\s+|have\s+|achieved\s+|received\s+)?((?:A\*|D\*|[ABCDUEPM]){2,4})\b(?!\s+in\s)'
        # only look for this if we haven't already found grades with subjects
        if not results:
            standalone_matches = re.findall(standalone_grades_pattern, cleaned_sentence, re.IGNORECASE)
        else:
            standalone_matches = []
        # endif

        for grades_str in standalone_matches:
            # work out individual grades from stuff like "AAB" or "BBB"
            grades = []
            i = 0
            while i < len(grades_str):
                if grades_str[i].upper() == "A" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("A*")
                    i += 2
                elif grades_str[i].upper() == "D" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("D*")
                    i += 2
                else:
                    grades.append(grades_str[i].upper())
                    i += 1
                # endif
            # endwhile

            # store them with generic subject names cos we don't know what subjects
            for idx, grade in enumerate(grades):
                # just call them subject_1, subject_2 etc
                generic_subject = f"subject_{idx + 1}"
                results[generic_subject] = grade
            # endfor

            # take this bit out of the remaining text
            remaining = re.sub(rf'\b{re.escape(grades_str)}\b', '', remaining, flags=re.IGNORECASE)
        # endfor

        # Second pass: Find single-grade patterns in remaining text
        # First handle space-separated format like "Maths A Physics B"
        # Clean up multiple spaces first
        remaining_cleaned = re.sub(r'\s+', ' ', remaining)

        # Match subject-grade pairs with flexible spacing
        # Include A* handling - make sure to match A* first
        words_and_grades = re.findall(r'\b([a-zA-Z]+(?:\s+[a-zA-Z]+)?)\s+(A\*|D\*|[A-U]\b)', remaining_cleaned,
                                      re.IGNORECASE)
        for word, grade in words_and_grades:
            # Check if this word/phrase is a known subject
            subject_norm = self.normalize_subject(word.lower().strip())
            # Add if it's a valid subject (either normalized or already a main subject name)
            if subject_norm and subject_norm not in results:
                # Check it's actually a subject by seeing if it's in our subjects dict
                is_subject = False
                for main_subj, synonyms in get_synonyms()["subjects"].items():
                    if subject_norm == main_subj or word.lower().strip() in synonyms:
                        is_subject = True
                        break
                    # endif
                # endfor
                if is_subject:
                    results[subject_norm] = grade.upper()
                # endif
            # endif
        # endfor

        patterns: list[tuple[str, str]] = [
            (r'\b(?:got\s+)?(A\*|D\*|[A-U])\s+in\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*?)(?=\s+[A-U]\s+in\s+|[,.]|$)',
             "grade_in_subject"),
            (r"([a-zA-Z\s]+?)\s*[:\-]\s*(A\*|D\*|A|B|C|D|E|U|M|P)", "subject_colon_grade"),
            (r"(?:my grade in|in)\s+([a-zA-Z\s]+?)\s+is\s+(A\*|D\*|A|B|C|D|E|U|M|P)", "in_subject_is_grade"),
        ]

        for pattern, mode in patterns:
            matches: list[tuple[str, str]] = re.findall(pattern, remaining, re.IGNORECASE)

            for match in matches:
                if mode == "grade_in_subject":
                    grade: str = match[0]
                    subject: str = match[1]
                else:
                    subject: str = match[0]
                    grade: str = match[1]
                # endif

                # Clean and normalize
                subject_norm: str = self.normalize_subject(subject.strip().lower())
                grade_clean: str = grade.strip().upper()

                # Only add if not already found
                if subject_norm and subject_norm not in results:
                    results[subject_norm] = grade_clean
                # endif
            # endfor
        # endfor

        return results

    # enddef

    def normalize_subject(self, subject: str) -> str:
        """
        Converts a subject synonym to its main subject name.

        :param subject: str
            The subject name or synonym, e.g. "maths", "comp sci", "bio".
        :return: str
            The standardized main subject name (e.g. "mathematics", "computer science", "biology").
        """

        subject: str = subject.lower().strip()

        subject_phrases: list[str] = get_synonyms()["subjects"]

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
        Extracts all course interests mentioned by the user in their input,
        by matching against a predefined set of interest phrases and course synonyms.

        :param input: str
            Raw user input (e.g., "I'm interested in medicine and law")
        :return: list[str]
            List of main course names found in the input (duplicates/overlaps removed)
        """

        # List of phrases showing a user's interest in a subject (e.g., "interested in", "looking for")
        interest_phrases: list[str] = get_synonyms()["interest"]

        # Dictionary of all courses and their list of synonyms (e.g., {"medicine": ["med", "mbbs"]})
        courses_dict: dict[str, list[str]] = get_synonyms()["courses"]

        # Will collect the main course names found in the user input
        found_courses: list[str] = []

        # Cleans up the input: makes lowercase, removes extra words like "and"
        cleaned: str = self.clean_input(input)

        # Lowercase, stripped version for searching
        cleaned_joined: str = cleaned.lower()

        # Checks if any interest phrase is present (e.g., "interested in", "hoping to study")
        found_interest_phrase: bool = False

        for phrase in interest_phrases:
            if phrase in cleaned_joined:
                found_interest_phrase = True
                break
            # endif
        # endfor

        # If an interest phrase is found, looks for matching courses using word boundaries
        if found_interest_phrase:
            for course, synonyms in courses_dict.items():
                # Makes a list with the course name and all its synonyms
                all_names: list[str] = [course] + synonyms
                for name in all_names:
                    # Builds a regex pattern to match the name as a whole word
                    pattern: str = r'\b' + re.escape(name) + r'\b'
                    if re.search(pattern, cleaned_joined):
                        # Only adds if it hasn't already been found
                        if course not in found_courses:
                            found_courses.append(course)
                        # endif
                        break  # No need to check other synonyms for this course
                    # endif
                # endfor
            # endfor
        # endif

        # If no courses and no interest phrase matched, checks the input for any course names anyway
        if not found_courses and not found_interest_phrase:
            for course, synonyms in courses_dict.items():
                all_names: list[str] = [course] + synonyms
                for name in all_names:
                    pattern: str = r'\b' + re.escape(name) + r'\b'
                    if re.search(pattern, cleaned_joined):
                        if course not in found_courses:
                            found_courses.append(course)
                        # endif
                        break
                    # endif
                # endfor
            # endfor
        # endif

        # Removes overlapping course names (e.g., "english" inside "english literature"), keep the longest only
        clean_courses: list[str] = []

        for i in range(len(found_courses)):
            current: str = found_courses[i]
            found_overlap: bool = False
            for j in range(len(found_courses)):
                # If current course name is fully inside another, skip it (unless it's the same)
                if i != j and current in found_courses[j]:
                    found_overlap = True
                    break
                # endif
            # endfor

            if not found_overlap:
                clean_courses.append(current)
            # endif
        # endfor

        # Returns the final list of main course names the user is interested in
        return clean_courses

    # enddef

    def parse(self, input: str) -> dict:
        """
        Parses the user's raw input and returns a summary of grades and course interests.
        This function uses all helper functions to process, extract, and organize the user's input
        for further use (like searching a course/uni database).

        :param input: str
            User input containing grades, dropped subjects, and course interests
        :return: dict
            {
                "grades": {normalized_subject: grade, ...},
                "interests": [list of main course names the user is interested in]
            }
        """

        # Use the new unified function to get all grades
        all_grades: dict[str, str] = self.find_all_grades(input)

        # Gets all the course interests from the original input
        interests: list[str] = self.find_course_interest(input)

        # Need to also handle - "I like Maths" pattern
        # When found, keep mathematics as an interest even if there's a grade for it
        keep_subjects_with_grades = []
        input_lower = input.lower()

        # Check for explicit "I like X" pattern where X is a subject
        like_pattern = r'\b(?:i\s+)?(?:like|love|enjoy)\s+([a-z]+)'
        like_matches = re.findall(like_pattern, input_lower)
        for match in like_matches:
            subject_norm = self.normalize_subject(match)
            if subject_norm != match and subject_norm in interests:
                keep_subjects_with_grades.append(subject_norm)
            # endif
        # endfor

        # Detect explicit interest phrases like "want to do" so we don't drop them from interests
        explicit_interest = any(phrase in input_lower for phrase in get_synonyms()["interest"])

        # Removes any course from interests if it already appears in grades
        # UNLESS it was explicitly mentioned (interest phrases) or "I like/love/enjoy"
        clean_interests: list[str] = []
        for i in interests:
            if explicit_interest or i not in all_grades or i in keep_subjects_with_grades:
                clean_interests.append(i)
            # endif
        # endfor

        # Builds and return the final result as a dictionary
        result: dict = {
            "grades": all_grades,
            "interests": clean_interests
        }

        return result
    # enddef

# endclass
