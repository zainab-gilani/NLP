import re

input_str = "i got a in maths, b in physics, im interested in med"

pattern = r"\b(A\*|A|B|C|D|E|U)\b\s+in\s+([a-zA-Z\s]+?)(?:,|$)"

matches = re.findall(pattern, input_str, re.IGNORECASE)

print("Matches:", matches)
