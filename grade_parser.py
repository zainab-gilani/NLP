import re
from synonyms import SYNONYMS


class GradeParser:
    GRADE_PATTERN: str = r'\bA\*|A|B|C|D|E|U\b'  # Finds grades like A*, B, U, etc

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
            #endif
        #endfor

        # Join the cleaned parts back together, comma separated
        input: str = ", ".join(clean_parts)

        return input

    #enddef

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

        dropped_phrases: list[str] = SYNONYMS["dropped"]
        sentence: str = self.clean_input(input).lower()

        # Removes 'dropped/quit/failed/...' subject phrases using regex
        for phrase in dropped_phrases:
            pattern: str = rf"(?:\bi\s+)?{phrase}\s+([a-z\s]+(?:\sand\s[a-z\s]+)*)"
            sentence: str = re.sub(pattern, "", sentence)
        #endfor

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
            #endif
        #endfor

        # Process each part
        for i in range(len(parts)):
            trimmed: str = parts[i].strip()

            # Only removes single words if they're at the very start AND the original
            # input had a dropped phrase. Otherwise keep them (they might be part of a list)
            is_single_word = trimmed.isalpha() and len(trimmed.split()) == 1
            at_start = i == 0

            if trimmed and not (is_single_word and at_start and has_dropped_keyword):
                keep.append(trimmed)
            #endif
        #endfor

        # Joins back together
        result: str = ", ".join(keep).strip(", ")

        return result

    #enddef

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

        # Start with clean sentence, dropped subjects removed
        cleaned_sentence: str = self.find_dropped_subjects(input)

        # Helper function to process multi-grade matches
        def process_multi_grade(match) -> str:
            grades_str: str = match.group(1)
            subjects_str: str = match.group(2)

            # Split grades string into individual grades
            grades: list[str] = []
            i: int = 0

            while i < len(grades_str):
                # Handle A* as single grade
                if grades_str[i].upper() == "A" and (i + 1) < len(grades_str) and grades_str[i + 1] == "*":
                    grades.append("A*")
                    i += 2
                else:
                    grades.append(grades_str[i].upper())
                    i += 1
                #endif
            #endwhile

            # Clean and split subjects
            subjects_str = subjects_str.replace(" and ", ",")
            subjects_str = subjects_str.replace("  ", " ")

            subjects_list: list[str] = []
            for subject in subjects_str.split(","):
                subject_clean: str = subject.lower().strip()
                if subject_clean:
                    subjects_list.append(subject_clean)
                #endif
            #endfor

            # Pair grades with subjects
            for i in range(len(subjects_list)):
                subject_norm: str = self.normalize_subject(subjects_list[i])
                # Assign grade by position, use last grade if more subjects than grades
                grade: str = grades[i] if i < len(grades) else grades[-1]

                if subject_norm:
                    results[subject_norm] = grade
                #endif
            #endfor

            # Return empty string to remove this from sentence
            return ""

        #enddef

        # First pass: Find and process multi-grade patterns (AAB in ...)
        multi_pattern: str = r'\b((?:[ABCDUE]|A\*){2,})\s+in\s+([a-zA-Z\s,]+?)(?:\.|,\s*[a-zA-Z]+\s+in\s|$)'
        remaining: str = re.sub(multi_pattern, process_multi_grade, cleaned_sentence, flags=re.IGNORECASE)

        # Second pass: Find single-grade patterns in remaining text
        patterns: list[tuple[str, str]] = [
            (r'\b(?:got\s+)?(A\*|[A-U])\s+in\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*?)(?=\s+[A-U]\s+in\s+|[,.]|$)',
             "grade_in_subject"),
            (r"([a-zA-Z\s]+?)\s*[:\-]\s*(A\*|A|B|C|D|E|U)", "subject_colon_grade"),
            (r"([a-zA-Z\s]+?)\s+(A\*|A|B|C|D|E|U)(?:,|$)", "subject_grade"),
            (r"(?:my grade in|in)\s+([a-zA-Z\s]+?)\s+is\s+(A\*|A|B|C|D|E|U)", "in_subject_is_grade"),
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
                #endif

                # Clean and normalize
                subject_norm: str = self.normalize_subject(subject.strip().lower())
                grade_clean: str = grade.strip().upper()

                # Only add if not already found
                if subject_norm and subject_norm not in results:
                    results[subject_norm] = grade_clean
                #endif
            #endfor
        #endfor

        return results

    #enddef

    def normalize_subject(self, subject: str) -> str:
        """
        Converts a subject synonym to its main) subject name.

        :param subject: str
            The subject name or synonym, e.g. "maths", "comp sci", "bio".
        :return: str
            The standardized main subject name (e.g. "mathematics", "computer science", "biology").
        """

        subject: str = subject.lower().strip()

        subject_phrases: list[str] = SYNONYMS["subjects"]

        # Loop through all main subjects and their synonyms
        for main_subject, synonyms in subject_phrases.items():
            if subject == main_subject:
                return main_subject
            #endif

            for synonym in synonyms:
                if subject == synonym:
                    return main_subject
                #endif
            #endfor
        #endfor

        return subject

    #enddef

    def find_course_interest(self, input: str) -> list[str]:
        """
        Finds and returns all course interests mentioned in the input, using synonyms from the course list.

        :param input: str
            User input, e.g. "I'm interested in medicine" or "Looking for economics"
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
                    temp: tuple[str, str] = course_search_list[i]
                    course_search_list[i]: list[tuple[str, str]] = course_search_list[j]
                    course_search_list[j]: list[tuple[str, str]] = temp
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
            for course, synonyms in courses_dict.items():
                # Always include the main course name as its own synonym
                all_names: list[str] = [course] + synonyms
                for name in all_names:
                    pattern: str = r'\b' + re.escape(name) + r'\b'
                    if re.search(pattern, cleaned_joined):
                        if course not in found_courses:
                            found_courses.append(course)
                        #endif
                        break
                    #endif
                #endfor
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

        clean_courses: list[str] = []

        for i in range(len(found_courses)):
            current: str = found_courses[i]
            found_overlap: bool = False
            for j in range(len(found_courses)):
                if i != j and current in found_courses[j]:
                    found_overlap = True
                    break
                #endif
            #endfor
            if not found_overlap:
                clean_courses.append(current)
            #endif
        #endfor

        # Return the list of found main course names
        return clean_courses

    #enddef

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
        interest_phrases: list[str] = SYNONYMS["interest"]

        # Dictionary of all courses and their list of synonyms (e.g., {"medicine": ["med", "mbbs"]})
        courses_dict: dict[str, list[str]] = SYNONYMS["courses"]

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
            #endif
        #endfor

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
                        #endif
                        break  # No need to check other synonyms for this course
                    #endif
                #endfor
            #endfor
        #endif

        # If no courses and no interest phrase matched, checks the input for any course names anyway
        if not found_courses and not found_interest_phrase:
            for course, synonyms in courses_dict.items():
                all_names: list[str] = [course] + synonyms
                for name in all_names:
                    pattern: str = r'\b' + re.escape(name) + r'\b'
                    if re.search(pattern, cleaned_joined):
                        if course not in found_courses:
                            found_courses.append(course)
                        #endif
                        break
                    #endif
                #endfor
            #endfor
        #endif

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
                #endif
            #endfor

            if not found_overlap:
                clean_courses.append(current)
            #endif
        #endfor

        # Returns the final list of main course names the user is interested in
        return clean_courses

    #enddef

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

        # Removes any course from interests if it already appears in grades (e.g., "A in medicine")
        clean_interests: list[str] = []
        for i in interests:
            if i not in all_grades:
                clean_interests.append(i)
            #endif
        #endfor

        # Builds and return the final result as a dictionary
        result: dict = {
            "grades": all_grades,
            "interests": clean_interests
        }

        return result
    #enddef


#endclass

parser = GradeParser()

# print(parser.parse(
#     "I got A in maths, B in physics and dropped chemistry, and I'm interested in medicine and english literature."))

# print(parser.parse("Please help me decide as I like Maths and want to do Engineering. I got A in Math Chem and Bio."))

# print(parser.parse("I expect to get A* in Further Maths, B in Chemistry and C in Bio. I want to pursue Drama in my uni."))
# print(
#     parser.parse("I expect to get A* in Further Maths, B in Chemistry and C in Bio. I want to pursue Drama in my uni."))

# print(
#      parser.parse("I got A in arts b in maths and A in chemistry. Which course and uni do you recommend."))

print(
     parser.parse("I am hoping to get A in Math B in chem and B in Physics. I want to study medicine. Which uni do I go to?"))
