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
    # Dictionary of synonyms for all subjects
    SYNONYMS = {
        # All the ways to say someone dropped/abandoned a subject
        "dropped": [
            "dropped", "quit", "left", "failed", "gave up", "gave in", "gave away", "stopped",
            "didn't take", "did not take", "didn't do", "did not do", "retook", "retake",
            "withdrawn", "withdrew", "withdrew from", "was withdrawn", "discontinued", "discontinued with",
            "stopped taking", "never took", "didn't finish", "did not finish", "wasn't entered for",
            "not entered for", "didn't sit", "did not sit", "removed", "removed from timetable",
            "excluded", "scrapped", "scrapped off", "resigned from", "didn't pass", "did not pass",
            "didn't complete", "did not complete", "unregistered", "opted out", "eliminated", "switched out",
            "was switched out", "cancelled", "dropped out", "let go", "lost", "missed", "abandoned",
            "didn't carry forward", "did not carry forward"
        ],

        # Canonical subjects and all the common ways they're written
        "subjects": {
            "mathematics": [
                "math", "maths", "mathematics", "further maths", "further mathematics", "core maths", "pure maths",
                "stats", "statistics", "mechanics", "applied maths", "decision maths"
            ],
            "computer science": [
                "cs", "comp sci", "computing", "computer science", "information technology", "it", "ict", "informatics",
                "information systems", "ict", "information tech"
            ],
            "biology": [
                "biology", "bio", "biological sciences"
            ],
            "physics": [
                "physics", "phys", "applied physics", "astro physics", "astrophysics"
            ],
            "chemistry": [
                "chemistry", "chem", "applied chemistry", "organic chemistry", "inorganic chemistry"
            ],
            "psychology": [
                "psychology", "psych", "applied psychology"
            ],
            "english literature": [
                "english literature", "lit", "english lit", "literature", "literary studies"
            ],
            "english language": [
                "english language", "english lang", "eng lang", "lang", "language", "english studies"
            ],
            "history": [
                "history", "hist", "world history", "ancient history", "modern history"
            ],
            "geography": [
                "geography", "geo", "physical geography", "human geography"
            ],
            "business": [
                "business", "business studies", "biz", "bs", "business admin", "business administration", "commerce"
            ],
            "economics": [
                "economics", "econ", "microeconomics", "macroeconomics"
            ],
            "music": [
                "music", "mus", "music technology", "music theory"
            ],
            "philosophy": [
                "philosophy", "phil", "philosophy and ethics", "religious studies", "rs", "ethics"
            ],
            "law": [
                "law", "legal studies", "criminal law", "public law", "constitutional law"
            ],
            "sociology": [
                "sociology", "socio", "social studies"
            ],
            "french": [
                "french", "francais", "fr"
            ],
            "spanish": [
                "spanish", "español", "espanol", "sp"
            ],
            "german": [
                "german", "deutsch", "de"
            ],
            "arabic": [
                "arabic", "ar"
            ],
            "urdu": [
                "urdu"
            ],
            "chinese": [
                "chinese", "mandarin", "zh"
            ],
            "italian": [
                "italian", "it"
            ],
            "latin": [
                "latin"
            ],
            "greek": [
                "greek"
            ],
            "russian": [
                "russian", "ru"
            ],
            "japanese": [
                "japanese", "jp"
            ],
            "portuguese": [
                "portuguese", "pt"
            ],
            "hindi": [
                "hindi"
            ],
            "persian": [
                "persian"
            ],
            "art": [
                "art", "fine art", "visual art", "graphics", "graphic design", "photography", "art & design",
                "sculpture"
            ],
            "media studies": [
                "media studies", "media", "media science", "film studies", "film", "media production"
            ],
            "design and technology": [
                "design and technology", "d&t", "dt", "design tech", "product design", "food tech", "textiles",
                "fashion", "resistant materials"
            ],
            "politics": [
                "politics", "government and politics", "govt and politics", "pol", "government",
                "international relations"
            ],
            "pharmacy": [
                "pharmacy", "pharmacology"
            ],
            "accounting": [
                "accounting", "accountancy", "finance", "financial studies"
            ],
            "drama": [
                "drama", "theatre studies", "performing arts"
            ],
            "pe": [
                "pe", "physical education", "sports science"
            ],
            "travel and tourism": [
                "travel and tourism"
            ],
            "health and social care": [
                "health and social care"
            ],
            "child development": [
                "child development"
            ],
            "classical civilisation": [
                "classical civilisation"
            ],
        },

        # Courses for degree-level interests, not A-levels
        "courses": {
            "medicine": [
                "medicine", "med", "med school", "medical degree", "doctor", "mbbs", "md", "medical studies",
                "clinical medicine", "medicine programme", "medic"
            ],

            "computer science": [
                "computer science", "cs", "comp sci", "software engineering", "computing", "informatics",
                "information systems", "ict", "information tech",
                "data science", "artificial intelligence", "ai", "cybersecurity", "computer engineering",
                "digital technology", "machine learning"
            ],

            "law": [
                "law", "llb", "legal studies", "criminal law", "public law", "constitutional law", "barrister",
                "solicitor", "law school", "jurisprudence",
                "law degree", "legal practice", "commercial law", "international law", "family law"
            ],

            "pharmacy": [
                "pharmacy", "pharmacology", "pharma", "pharmaceutical sciences", "pharmaceutical studies",
                "pharmacy school", "pharmacist"
            ],

            "engineering": [
                "engineering", "eng", "engineering degree", "mechanical engineering", "electrical engineering",
                "civil engineering",
                "chemical engineering", "biomedical engineering", "mechatronics", "aerospace engineering",
                "structural engineering",
                "electronic engineering", "software engineering", "engineering science"
            ],

            "business": [
                "business", "business management", "bba", "business admin", "accounting", "accountancy",
                "business administration", "commerce",
                "business studies", "finance", "economics and finance", "mba", "management studies", "entrepreneurship",
                "marketing", "human resource management", "supply chain management"
            ],

            "psychology": [
                "psychology", "psych", "psyche", "clinical psychology", "forensic psychology", "applied psychology",
                "psychological sciences", "counselling psychology", "industrial psychology", "educational psychology",
                "psychology degree"
            ],

            "music": [
                "music", "music studies", "musician", "music performance", "music composition", "music production",
                "music technology", "conservatoire", "bmus", "musicology", "music degree"
            ],

            "history": [
                "history", "historian", "historical studies", "history degree", "ancient history", "modern history",
                "history and politics", "history and economics"
            ],

            "english": [
                "english", "english literature", "english language", "english studies", "english degree", "literature",
                "creative writing", "english lit", "english lang", "literary studies", "linguistics",
                "comparative literature"
            ],

            "architecture": [
                "architecture", "architect", "barch", "architectural studies", "architectural design",
                "architectural engineering", "architecture degree", "urban design", "landscape architecture",
                "architectural technology"
            ],

            "biology": [
                "biology", "bio", "biological sciences", "life sciences", "biomedical sciences", "molecular biology",
                "cell biology", "biological science degree", "marine biology", "ecology", "biotechnology",
                "plant biology", "zoology"
            ],

            "sociology": [
                "sociology", "socio", "social sciences", "social studies", "social research", "sociological studies",
                "sociology degree", "anthropology"
            ],

            "art": [
                "art", "fine art", "visual art", "artist", "studio art", "art and design", "design", "applied arts",
                "sculpture", "painting", "graphic design", "illustration", "photography", "art history", "art degree"
            ],

            "dentistry": [
                "dentistry", "dentist", "bds", "dental surgery", "dental studies", "dental school", "dental science",
                "dental degree"
            ],

            "veterinary": [
                "veterinary", "veterinary medicine", "vet science", "vet", "vet school", "veterinary surgeon",
                "veterinary studies", "bvetmed", "vet degree"
            ],

            "nursing": [
                "nursing", "nurse", "bsc nursing", "nursing degree", "nursing science", "nursing studies",
                "registered nurse", "adult nursing", "paediatric nursing", "mental health nursing", "midwifery"
            ],

            "education": [
                "education", "teaching", "teacher training", "pgce", "b.ed", "educational studies", "education studies",
                "education degree", "school direct", "initial teacher training", "childhood studies",
                "educational psychology"
            ],

            "criminology": [
                "criminology", "crime science", "criminal justice", "criminal studies", "criminology degree"
            ],

            "journalism": [
                "journalism", "media journalism", "news reporting", "broadcast journalism", "sports journalism",
                "journalist", "news media", "magazine journalism"
            ],

            "public relations": [
                "public relations", "pr", "corporate communications", "strategic communications",
                "communications management", "public affairs"
            ],

            "international relations": [
                "international relations", "global studies", "international studies", "international affairs",
                "diplomacy", "international politics", "international development"
            ],

            "politics": [
                "politics", "political science", "government and politics", "government studies", "public policy",
                "politics degree", "international politics"
            ],

            "economics": [
                "economics", "econ", "microeconomics", "macroeconomics", "economic studies", "economics degree",
                "finance and economics"
            ],

            "philosophy": [
                "philosophy", "philosophy and ethics", "philosophy degree", "philosophical studies", "ethics",
                "theology", "philosophy and religion", "metaphysics"
            ],

            "environmental science": [
                "environmental science", "enviro science", "environmental studies", "environmental management",
                "environmental policy", "environmental engineering", "sustainability", "conservation science",
                "ecology", "environmental science degree"
            ],

            "media": [
                "media", "media studies", "communications", "communication studies", "digital media",
                "media production", "film studies", "film and media", "broadcast media", "mass communication",
                "media degree"
            ],
        }
    }
    GRADE_PATTERN = r'\bA\*|A|B|C|D|E|U\b'  # Finds grades like A*, B, U, etc

    def clean_input(self, input):
        """
        Cleans and standardizes the user input by converting to lowercase, removing unnecessary symbols,
        and stripping extra whitespace.

        :param input: str. Raw user input describing subjects, grades, and additional info.
        :return: str. Cleaned and normalized input string.
        """
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

    def find_dropped_subjects(self, input):
        """
        Extracts and returns a list of dropped subjects found in the input, based on recognized
        dropped/quit/failed phrases.
        Also returns a cleaned version of the input with dropped information removed.

        :param input: str. User input describing subjects, grades, and any dropped/abandoned subjects.
        :return: str. Cleaned input with dropped subjects removed.
        """

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
        cleaned_sentence_parts = []

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
                else:
                    cleaned_sentence_parts.append(part)
                # endif
                previous_was_dropped = False
            # endif
        # endfor
        cleaned_sentence = ", ".join(cleaned_sentence_parts)
        return cleaned_sentence

    # enddef

    def find_grade_subject_pairs(self, input):  # Returns dictionary: {subject:grade}
        pass
        # Case 1: \b(A\*|A|B|C|D|E|U)\b\s+in\s+([a-zA-Z\s]+)
        # # Case 2: Math: A, Physics: B, Music: A, I want to do pharmacy
        # # Pattern in this: SUBJECT*GRADE
        # # Course: Pharmaceuticals
        #
        # # Case 3: I achieved ABB in English, history and geography, looking to apply for law
        # # Pattern in this: GRADE{1...}
        # # SEPARATELY once we have found a multi grade, we must find EQUAL number of subjects after that
        # # Course: Law
        #
        # # Case 4: My grade in math is A, physics B, chemistry A
        # # Pattern: SUBJECT*GRADE
        # # (no course found)
        #
        # # Case 5: When I was little I always wanted to become a pilot. Now I got A in Math and D in Physics. What do I take
        # # Pattern: GRADE*SUBJECT
        # # (no course found)

    # enddef

    def find_multi_grades(self, input):
        """
        Extracts multiple grade/subject pairs from sentences with grouped grades, such as 'ABB in maths,
        physics and biology'. Pairs each grade with the corresponding subject in order and returns a dictionary
        mapping normalized subject names to grades.

        :param input: str. The cleaned input sentence containing grade/subject info.
        :return: dict. Keys are normalized subject names (str), values are grades (str).
                     Example: {'mathematics': 'A', 'physics': 'B', 'biology': 'B'}
                     Returns an empty dict if no multi-grade pattern is found.
        """
        results = {}

        # Separates the chunk of grades into singular elements in a list
        pattern = r'\b([A\*ABCDUE]{2,5})\b\s+in\s+([a-zA-Z\s,]+)'
        matches = re.findall(pattern, input)

        for match in matches:
            grades_str = match[0]
            subjects_str = match[1]

            # Splits grades_str into a list
            grades = []
            for char in grades_str:
                grades.append(char)
            # endfor

            # Cleans up subject_str, replacing "and" with "," for splitting
            subjects_str_replaced = subjects_str.replace("and", ",")
            subjects_raw_list = subjects_str_replaced.split(",")

            # Cleans each subject and adds to list
            subjects_list = []
            for subject in subjects_raw_list:
                subject_clean = subject.lower().strip()
                if subject_clean:
                    subjects_list.append(subject_clean)
                # endif
                # endfor

            # Pairs each subject with grade
            for i in range(len(subjects_list)):
                # Uses normalize_subject function to clean input and remove unnecessary parts
                subject_norm = self.normalize_subject(subjects_list[i])
                # Assigns grade by position
                if i < len(grades):
                    # Checks to see if there is the same amount of grades and subjects, and pairs them in order
                    grade = grades[i]
                else:
                    # If there are more subjects than grades by mistake, the last grade is repeated
                    grade = grades[-1]
                # endif
                # Adds normalized subject and assigned grade to dictionary
                results[subject_norm] = grade
            # endfor

            # Removes multi-grade and subject part of the sentence
            # so other functions don't have to parse it again
            chunk = f"{grades_str} in {subjects_str}"
            input = input.replace(chunk, "")

        return f"Results: {results}, Input: {input}"

    # enddef

    def normalize_subject(self, subject):
        """
        Converts a subject synonym to its canonical (main) subject name.

        :param subject: str. The subject name or synonym, e.g. "maths", "comp sci", "bio".
        :return: str. The standardized main subject name (e.g. "mathematics", "computer science", "biology").
        """
        subject = subject.lower().strip()

        for canon_subject, synonyms in self.SYNONYMS["subjects"].items():
            if subject == canon_subject:
                return canon_subject
            #endif
            for synonym in synonyms:
                if subject == synonym:
                    return canon_subject
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
print(parser.find_multi_grades("AAB in Physics and math and chem"))