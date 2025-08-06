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


# OBSERVATIONS
# 6 Aug 2025: Although all my tests pass and various attempts to find flaws seem to give me
# the correct output, I realize there is a big improvement I could have been earlier on and that is
# to remove all the matched strings from the original input as each function performed its own parsing.
# This way the next function call would have received a partial input but without the parts that have
# already been parsed. For instance, when parsing interests, it would have only parsed the left over
# remainder string after having removed all the parsed subjects and grades.