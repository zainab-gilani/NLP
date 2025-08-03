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
        cleaned = self.clean_input(input)
        parts = [x.strip() for x in cleaned.split(",") if x.strip()]

        print("DEBUG: parts after clean/split =", parts)

        dropped = []
        skip_indices = set()

        for idx, part in enumerate(parts):
            found = False
            for word in SYNONYMS["dropped"]:
                pos = part.find(word)
                if pos != -1:
                    found = True
                    possible = part[pos + len(word):].strip()
                    if possible:
                        # Split by 'and' and ','
                        for subj in re.split(r'and|,', possible):
                            if subj.strip():
                                dropped.append(subj.strip())
                                skip_indices.add(idx)
                    # Look ahead for the orphan subject chunk
                    if idx + 1 < len(parts):
                        nxt = parts[idx + 1]
                        # If it's just a subject word (all alpha, no keywords), drop it too
                        if re.match(r'^[a-z\s]+$', nxt) and not any(x in nxt for x in ['but', 'got', 'in']):
                            dropped.append(nxt.strip())
                            skip_indices.add(idx + 1)
                    break
            if found:
                continue

        print("DEBUG: dropped =", dropped)
        print("DEBUG: skip_indices =", skip_indices)

        kept = []
        for idx, part in enumerate(parts):
            if idx in skip_indices:
                continue
            if part in dropped:
                continue
            kept.append(part)

        print("DEBUG: kept =", kept)
        return ", ".join(kept)


#endclass

parser = GradeParser()
cleaned = parser.find_dropped_subjects("I dropped music and drama, but got A in English")