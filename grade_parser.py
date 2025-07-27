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
        # All the ways to say someone dropped/abandoned a subject
        "dropped": [
            "dropped", "quit", "left", "failed", "gave up", "gave in", "gave away", "stopped",
            "didn't take", "did not take", "didn't do", "did not do", "retook", "retake",
            "withdrawn", "withdrew", "didn't pass", "did not pass", "scrapped", "removed", "excluded"
        ],

        # Canonical subjects and all the common ways they're written
        "subjects": {
            "mathematics": [
                "math", "maths", "mathematics", "further maths", "further mathematics", "core maths", "pure maths"
            ],
            "computer science": [
                "cs", "comp sci", "computing", "computer science", "information technology", "it", "ict", "informatics"
            ],
            "biology": [
                "biology", "bio", "biological sciences"
            ],
            "physics": [
                "physics", "phys"
            ],
            "chemistry": [
                "chemistry", "chem"
            ],
            "psychology": [
                "psychology", "psych"
            ],
            "english literature": [
                "english literature", "lit", "english lit"
            ],
            "english language": [
                "english language", "english lang", "eng lang"
            ],
            "history": [
                "history", "hist"
            ],
            "geography": [
                "geography", "geo"
            ],
            "business": [
                "business", "business studies", "biz", "bs"
            ],
            "economics": [
                "economics", "econ"
            ],
            "music": [
                "music", "mus"
            ],
            "philosophy": [
                "philosophy", "phil"
            ],
            "law": [
                "law", "legal studies"
            ],
            "sociology": [
                "sociology", "socio"
            ],
            "french": [
                "french", "fr"
            ],
            "spanish": [
                "spanish", "sp"
            ],
            "art": [
                "art", "fine art", "visual art"
            ],
            "media studies": [
                "media studies", "media", "media science"
            ],
            "design and technology": [
                "design and technology", "d&t", "dt", "design tech", "product design"
            ],
            "politics": [
                "politics", "government and politics", "govt and politics", "pol"
            ],
            "pharmacy": [
                "pharmacy", "pharmacology"
            ],
            "accounting": [
                "accounting", "accountancy"
            ],
        },

        # Courses for degree-level interests, not A-levels
        "courses": {
            "medicine": [
                "medicine", "med", "doctor", "mbbs", "medical", "medic", "med school"
            ],
            "computer science": [
                "computer science", "cs", "comp sci", "software engineering", "computing", "informatics"
            ],
            "law": [
                "law", "llb", "legal studies"
            ],
            "pharmacy": [
                "pharmacy", "pharmacology", "pharma"
            ],
            "engineering": [
                "engineering", "eng", "mechanical engineering", "electrical engineering", "civil engineering"
            ],
            "business": [
                "business", "business management", "bba", "business admin", "accounting", "accountancy"
            ],
            "psychology": [
                "psychology", "psych", "psyche"
            ],
            "music": [
                "music", "music studies", "musician"
            ],
            "history": [
                "history", "historian"
            ],
            "english": [
                "english", "english literature", "english language", "english studies"
            ],
            "architecture": [
                "architecture", "architect"
            ],
            "biology": [
                "biology", "bio", "biological sciences"
            ],
            "sociology": [
                "sociology", "socio"
            ],
            "art": [
                "art", "fine art", "visual art", "artist"
            ],
        }
    }
    GRADE_PATTERN = r'\bA\*|A|B|C|D|E|U\b'  # Finds grades like A*, B, U, etc

    def clean_input(self, input):  # Turns input to lowercase, replaces symbols, etc
        input = input.replace("and", ",").lower().strip()
        parts = input.split(",")

        clean_parts = []

        for p in parts:
            if p.strip():
                clean_parts.append(p.strip())
            # endif
        # endfor

        input = ", ".join(clean_parts)

        return input

    # enddef

    def find_dropped_subjects(self, input):  # Returns list of dropped subjects to not include in search process
        def is_subject_word(word):
            """
            :param word: Represents a potential subject name or phrase, e.g. 'further maths'
            :return: bool. True if subject has three words or less, otherwise False
            """
            words = word.split()
            word_count = len(words)
            if word_count <= 3:
                return True
            else:
                return False
            # endif

        # enddef

        cleaned = self.clean_input(input)
        dropped = []

        cleaned = cleaned.split(",")

        parts = []
        for x in cleaned:
            parts.append(x.strip())
        # endfor

        previous_was_dropped = False

        for part in parts:
            found = False
            for word in self.SYNONYMS["dropped"]:
                if part.startswith(word):
                    subjects = part[len(word):].strip()
                    subjects_split = re.split(r'and', subjects)
                    for s in subjects_split:
                        subject = s.strip()
                        if subject and subject not in dropped and is_subject_word(subject):
                            dropped.append(subject)
                        # endif
                    # endfor
                    found = True
                    previous_was_dropped = True
                    break
                # endif
            # endfor
            # endfor
            if not found:
                is_subject = True
                for word in self.SYNONYMS["dropped"]:
                    if part.startswith(word):
                        is_subject = False
                        break
                    # endif
                # endfor
                if previous_was_dropped and is_subject and part not in dropped and is_subject_word(part):
                    dropped.append(part)
                # endif
                previous_was_dropped = False
            # endif
        # endfor
        return dropped

    # enddef

    def find_grade_subject_pairs(self, input):  # Returns dictionary: {subject:grade}
        pass

    # enddef

    def find_multi_grades(self, input):  # Looks for AAA/AAB and assigns to subjects listed after
        pass

    # enddef

    def normalize_subject(self, subject):  # Turns synonyms into the main subject name
        pass

    # enddef

    def find_course_interest(self, input):  # Looks for course of interest
        pass

    # enddef

    def parse(self, input):
        pass
    # enddef


# endclass

parser = GradeParser()
print(parser.find_dropped_subjects(
    "I got A in maths and dropped chemistry and music and quit biology and failed english and i am interested in medicine"))
