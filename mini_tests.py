import re

dropped_phrases = [
    "dropped", "quit", "failed", "retook", "gave up", "left"
]

def remove_dropped(input):
    sentence = input.lower()
    # 1. Remove dropped chunks (handles “and drama”, “music and drama”, etc.)
    for phrase in dropped_phrases:
        # Pattern: phrase [subjects list, possibly with 'and' or commas]
        # Accept 'i' before dropped phrase
        pattern = rf"(?:\bi\s+)?{phrase}\s+([a-z\s]+(?:\sand\s[a-z\s]+)*)"
        sentence = re.sub(pattern, '', sentence)
    # 2. Cleanup: remove extra commas, multiple spaces, etc.
    # Remove extra commas from where chunks were removed
    # Remove extra commas from where chunks were removed
    sentence = re.sub(r',\s*,+', ',', sentence)
    sentence = re.sub(r'^\s*,\s*', '', sentence)
    sentence = re.sub(r',\s*$', '', sentence)
    # Remove spaces before/after commas
    sentence = re.sub(r'\s+,', ',', sentence)
    sentence = re.sub(r',\s+', ', ', sentence)
    # Remove double spaces
    sentence = re.sub(r'\s+', ' ', sentence)
    # Remove trailing/leading "and"
    sentence = re.sub(r',\s*and\s*$', '', sentence)
    sentence = re.sub(r'\s*and\s*$', '', sentence)
    sentence = re.sub(r'^\s*and\s*', '', sentence)
    sentence = re.sub(r',\s*and\s*,', ',', sentence)
    sentence = re.sub(r',\s*and\s+', ', ', sentence)
    # Remove leading/trailing space
    sentence = sentence.strip()
    # If a comma was left after all other text is gone
    if sentence == ",":
        sentence = ""

    return sentence

tests = [
    ("A in maths and B in physics, and dropped chemistry", "a in maths and b in physics"),
    ("Dropped maths, quit physics and left chemistry", ""),
    ("Failed biology, retook psychology, gave up art", ""),
    ("Dropped maths, A in physics, B in chemistry", "a in physics, b in chemistry"),
    ("I dropped music and drama, but got A in English", "but got a in english"),
    ("Retook nothing, just got C in Geography", "just got c in geography"),
]

for test_input, expected in tests:
    result = remove_dropped(test_input)
    print(f"INPUT: {test_input}")
    print(f"OUTPUT: {result}")
    print(f"EXPECTED: {expected}")
    print("PASS:", result == expected)
    print("-----")