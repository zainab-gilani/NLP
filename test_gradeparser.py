import unittest
from grade_parser import GradeParser

class TestGradeParser(unittest.TestCase):
    def setUp(self):
        self.parser = GradeParser()

    # enddef

    def test_clean_input(self):
        result = self.parser.clean_input("A in maths and B in physics,  and  dropped chemistry")
        self.assertEqual(result, "a in maths, b in physics, dropped chemistry")

    # enddef

    def test_find_dropped_subjects(self):
        cleaned = self.parser.find_dropped_subjects("A in maths and B in physics, and dropped chemistry")
        self.assertNotIn("chemistry", cleaned)
        self.assertNotIn("dropped chemistry", cleaned)

    # enddef

    def test_find_multi_grades(self):
        output = self.parser.find_multi_grades("My grades are AAB in maths, CS, physics")
        # The output is a string: "Results: {...}, Input: ..."
        self.assertIn("'mathematics': 'A'", output)
        self.assertIn("'computer science': 'A'", output)
        self.assertIn("'physics': 'B'", output)

    # enddef

    def test_normalize_subject(self):
        self.assertEqual(self.parser.normalize_subject("maths"), "mathematics")
        self.assertEqual(self.parser.normalize_subject("comp sci"), "computer science")
        self.assertEqual(self.parser.normalize_subject("bio"), "biology")
        self.assertEqual(self.parser.normalize_subject("chemistry"), "chemistry")  # No synonym, returns as is

    # enddef

    def test_find_grade_subject_pairs(self):
        # will fail because function isnt FUNCTIONing properly right now 😆 but it will.
        pairs = self.parser.find_grade_subject_pairs(
            "I got A in maths, B in physics and dropped chemistry, and im interested in med")
        # Should map normalized subject to grade
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("physics"), "B")
        self.assertIsNone(pairs.get("chemistry"))  # dropped, shouldn't show up
    # enddef


if __name__ == "__main__":
    unittest.main()
# endif