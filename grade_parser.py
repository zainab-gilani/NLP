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

import re

class GradeParser:
    SYNONYMS = {
        "dropped": ['dropped', 'quit', 'left', 'failed', "didn't take", "didn't do", 'retook', 'gave up'],
    } # Dictionary of synonyms for all subjects
    GRADE_PATTERN = r'\bA\*|A|B|C|D|E|U\b' # Finds grades like A*, B, U, etc

    def clean_input(self, input): # Turns input to lowercase, replaces symbols, etc
        input = input.replace("and", ",").lower().strip()
        parts = input.split(",")

        clean_parts = []

        for p in parts:
            if p.strip():
                clean_parts.append(p.strip())
            #endif
        #endfor

        input = ", ".join(clean_parts)

        return input
    #enddef

    def find_dropped_subjects(self, input): # Returns list of dropped subjects to not include in search process
        cleaned = self.clean_input(input)
        dropped = []
        # dropped_keywords = "|".join(map(re.escape, self.SYNONYMS["dropped"]))

        for word in self.SYNONYMS["dropped"]:
            pattern = rf"{word}\s+([a-zA-Z\s]+?)(?=,|$)"
            matches = re.findall(pattern, cleaned)
            for match in matches:
                for subject in re.split(r'and', match):
                    subject = subject.strip()
                    if subject:
                        dropped.append(subject)
                    #endif
                #endfor
            #endfor
        #endfor
        dropped_clean = []
        for subject in dropped:
            for word in self.SYNONYMS["dropped"]:
                subject = re.sub(rf"\b{word}\b", "", subject)
            #endfor
            subject = subject.strip()
            if subject and subject not in dropped_clean:
                dropped_clean.append(subject)
            #endif
        #endfor
        return dropped_clean
    #enddef

    def find_grade_subject_pairs(self, input): # Returns dictionary: {subject:grade}
        pass
    #enddef

    def find_multi_grades(self, input): # Looks for AAA/AAB and assigns to subjects listed after
        pass
    #enddef

    def normalize_subject(self, subject): # Turns synonyms into the main subject name
        pass
    #enddef

    def find_course_interest(self, input): # Looks for course of interest
        pass
    #enddef

    def parse(self, input):
        pass
    #enddef
#endclass

parser = GradeParser()
print(parser.find_dropped_subjects("I got A in maths and dropped chemistry, music, quit biology, failed english"))