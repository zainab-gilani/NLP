import unittest
from grade_parser import GradeParser

class TestGradeParser(unittest.TestCase):
    def setUp(self):
        self.parser = GradeParser()

    #enddef

    # Tests for clean_input function
    def test_clean_input(self):
        result = self.parser.clean_input("A in maths and B in physics,  and  dropped chemistry")
        self.assertEqual(result, "a in maths, b in physics, dropped chemistry")
    #enddef

    def test_clean_input_2(self):
        result = self.parser.clean_input("A in math and B in physics and dropped chemistry")
        self.assertEqual(result, "a in math, b in physics, dropped chemistry")
    #enddef

    def test_clean_input_3(self):
        result = self.parser.clean_input("A* in Biology, C in English and dropped Geography")
        self.assertEqual(result, "a* in biology, c in english, dropped geography")
    #enddef

    def test_clean_input_4(self):
        result = self.parser.clean_input("A in maths, , dropped music, and dropped art")
        self.assertEqual(result, "a in maths, dropped music, dropped art")
    #enddef



    # Tests for find_dropped_subjects function
    def test_find_dropped_subjects(self):
        cleaned = self.parser.find_dropped_subjects("A in maths and B in physics, and dropped chemistry")
        self.assertNotIn("chemistry", cleaned)
        self.assertNotIn("dropped chemistry", cleaned)
    #enddef

    def test_find_dropped_subjects_2(self):
        cleaned = self.parser.find_dropped_subjects("Dropped maths, quit physics and left chemistry")
        self.assertNotIn("maths", cleaned)
        self.assertNotIn("physics", cleaned)
        self.assertNotIn("chemistry", cleaned)
    #enddef

    def test_find_dropped_subjects_3(self):
        cleaned = self.parser.find_dropped_subjects("Failed biology, retook psychology, gave up art")
        self.assertNotIn("biology", cleaned)
        self.assertNotIn("psychology", cleaned)
        self.assertNotIn("art", cleaned)
    #enddef

    def test_find_dropped_subjects_4(self):
        cleaned = self.parser.find_dropped_subjects("Dropped maths, A in physics, B in chemistry")
        self.assertNotIn("maths", cleaned)
        self.assertIn("physics", cleaned)
        self.assertIn("chemistry", cleaned)
    #enddef

    def test_find_dropped_subjects_5(self):
        cleaned = self.parser.find_dropped_subjects("I dropped music and drama, but got A in English")
        self.assertNotIn("music", cleaned)
        self.assertNotIn("drama", cleaned)
        self.assertIn("english", cleaned)
    #enddef

    def test_find_dropped_subjects_6(self):
        # Will fail cuz i havent handled the retook nothing
        cleaned = self.parser.find_dropped_subjects("Retook nothing, just got C in Geography")
        self.assertIn("geography", cleaned)
        self.assertNotIn("nothing", cleaned)
    #enddef



    # Tests for find_multi_grades function
    def test_find_multi_grades(self):
        results = self.parser.find_multi_grades("My grades are AAB in maths, CS, physics")
        self.assertEqual(results.get("mathematics"), "A")
        self.assertEqual(results.get("computer science"), "A")
        self.assertEqual(results.get("physics"), "B")
    #enddef

    def test_find_multi_grades_2(self):
        results = self.parser.find_multi_grades("Predicted grades are ABB in maths, chemistry, biology")
        self.assertEqual(results.get("mathematics"), "A")
        self.assertEqual(results.get("chemistry"), "B")
        self.assertEqual(results.get("biology"), "B")
    #enddef

    def test_find_multi_grades_3(self):
        results = self.parser.find_multi_grades("I got AAA in physics, maths and CS")
        self.assertEqual(results.get("physics"), "A")
        self.assertEqual(results.get("mathematics"), "A")
        self.assertEqual(results.get("computer science"), "A")
    #enddef

    def test_find_multi_grades_4(self):
        results = self.parser.find_multi_grades("My grades are BCD in art, music, drama")
        self.assertEqual(results.get("art"), "B")
        self.assertEqual(results.get("music"), "C")
        self.assertEqual(results.get("drama"), "D")
    #enddef



    # Tests for normalise_subject function
    def test_normalize_subject(self):
        self.assertEqual(self.parser.normalize_subject("maths"), "mathematics")
        self.assertEqual(self.parser.normalize_subject("comp sci"), "computer science")
        self.assertEqual(self.parser.normalize_subject("bio"), "biology")
        self.assertEqual(self.parser.normalize_subject("chemistry"), "chemistry")
        self.assertEqual(self.parser.normalize_subject("Eng lit"), "english literature")
        self.assertEqual(self.parser.normalize_subject("psych"), "psychology")
        self.assertEqual(self.parser.normalize_subject("ECON"), "economics")
        self.assertEqual(self.parser.normalize_subject("geog"), "geography")
        self.assertEqual(self.parser.normalize_subject("History"), "history")
        self.assertEqual(self.parser.normalize_subject("Law"), "law")
    #enddef



    # Tests for find_grade_subject_pairs function
    def test_find_grade_subject_pairs(self):
        # will fail because function isnt FUNCTIONing properly right now 😆 but it will.
        pairs = self.parser.find_grade_subject_pairs(
            "I got A in maths, B in physics and dropped chemistry, and im interested in med")
        # Should map normalized subject to grade
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("physics"), "B")
        self.assertIsNone(pairs.get("chemistry"))  # dropped, shouldn't show up
    #enddef

    def test_find_grade_subject_pairs_2(self):
        pairs = self.parser.find_grade_subject_pairs("A in maths, B in chemistry, dropped physics")
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("chemistry"), "B")
        self.assertIsNone(pairs.get("physics"))
    #enddef

    def test_find_grade_subject_pairs_3(self):
        pairs = self.parser.find_grade_subject_pairs("Maths: A, Physics: B, English: C")
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("physics"), "B")
        self.assertEqual(pairs.get("english"), "C")
    #enddef

    def test_find_grade_subject_pairs_4(self):
        pairs = self.parser.find_grade_subject_pairs("biology B, chemistry A*, maths C")
        self.assertEqual(pairs.get("biology"), "B")
        self.assertEqual(pairs.get("chemistry"), "A*")
        self.assertEqual(pairs.get("mathematics"), "C")
    #enddef

    def test_find_grade_subject_pairs_5(self):
        pairs = self.parser.find_grade_subject_pairs("My grade in geography is D, and in history is C")
        self.assertEqual(pairs.get("geography"), "D")
        self.assertEqual(pairs.get("history"), "C")
    #enddef

    def test_find_grade_subject_pairs_6(self):
        pairs = self.parser.find_grade_subject_pairs("I have A* in comp sci, B in math, C in further math, failed art")
        self.assertEqual(pairs.get("computer science"), "A*")
        self.assertEqual(pairs.get("mathematics"), "B")
        self.assertEqual(pairs.get("further mathematics"), "C")
        self.assertIsNone(pairs.get("art"))
    #enddef

    def test_find_grade_subject_pairs_7(self):
        pairs = self.parser.find_grade_subject_pairs(
            "Retook psychology, got A in english literature, B in media studies")
        self.assertEqual(pairs.get("english literature"), "A")
        self.assertEqual(pairs.get("media studies"), "B")
        self.assertIsNone(pairs.get("psychology"))
    #enddef



    # Tests for find_course_interest function
    def test_find_course_interest_medicine(self):
        result = self.parser.find_course_interest("I'm interested in medicine")
        self.assertIn("medicine", result)
    #enddef

    def test_find_course_interest_law(self):
        result = self.parser.find_course_interest("I want to apply for law")
        self.assertIn("law", result)
    #enddef

    def test_find_course_interest_economics(self):
        result = self.parser.find_course_interest("Looking for economics")
        self.assertIn("economics", result)
    #enddef

    def test_find_course_interest_psychology(self):
        result = self.parser.find_course_interest("Curious about psychology")
        self.assertIn("psychology", result)
    #enddef

    def test_find_course_interest_english_lit(self):
        result = self.parser.find_course_interest("Hoping to study English literature")
        self.assertIn("english literature", result)
    #enddef
#endclass


if __name__ == "__main__":
    unittest.main()
#endif