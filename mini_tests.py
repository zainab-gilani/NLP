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

    def find_course_interest(self, input: str) -> list[str]:
        interest_phrases: list[str] = SYNONYMS["interest"]
        courses_dict: dict[str, list[str]] = SYNONYMS["courses"]
        found_courses: list[str] = []

        cleaned: str = self.clean_input(input)
        cleaned_joined: str = cleaned.lower()

        # Build search list with all (main, synonym) pairs
        course_search_list: list[tuple[str, str]] = []

        for course, synonym in course_search_list:
            if "lit" in synonym:
                print(course, ":", synonym)



        for course, synonyms in courses_dict.items():
            course_search_list.append((course, course))
            for synonym in synonyms:
                course_search_list.append((course, synonym))

        # NOW check for lit:
        for course, synonym in course_search_list:
            if "lit" in synonym:
                print(course, ":", synonym)

        # sort by length of search_name, so longer names get checked first
        for i in range(len(course_search_list)):
            for j in range(i + 1, len(course_search_list)):
                if len(course_search_list[j][1]) > len(course_search_list[i][1]):
                    temp = course_search_list[i]
                    course_search_list[i] = course_search_list[j]
                    course_search_list[j] = temp

        # find if any interest phrase is in the string
        found_interest_phrase: bool = False
        for phrase in interest_phrases:
            if phrase in cleaned_joined:
                found_interest_phrase = True
                break

        # always try to add all matches if interest phrase is present
        if found_interest_phrase:
            for course, search_name in course_search_list:
                if search_name in cleaned_joined:
                    # add the course ONLY IF NOT ALREADY IN THE LIST
                    if course not in found_courses:
                        found_courses.append(course)
        # fallback if nothing matched
        if not found_courses:
            for course, search_name in course_search_list:
                if search_name in cleaned_joined:
                    if course not in found_courses:
                        found_courses.append(course)

        for course, synonyms in SYNONYMS["courses"].items():
            if "english literature" in synonyms:
                print("FOUND in:", course)

        print("Cleaned joined input:", cleaned_joined)
        print("Course search list:", course_search_list)
        print("Final found_courses:", found_courses)

        return found_courses


#endclass

parser = GradeParser()
cleaned = parser.find_course_interest("Hoping to study English literature")