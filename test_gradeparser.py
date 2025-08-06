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

    # Tests for find_all_grades function (handles multi-grades)
    def test_find_multi_grades(self):
        results = self.parser.find_all_grades("My grades are AAB in maths, CS, physics")
        self.assertEqual(results.get("mathematics"), "A")
        self.assertEqual(results.get("computer science"), "A")
        self.assertEqual(results.get("physics"), "B")

    #enddef

    def test_find_multi_grades_2(self):
        results = self.parser.find_all_grades("Predicted grades are ABB in maths, chemistry, biology")
        self.assertEqual(results.get("mathematics"), "A")
        self.assertEqual(results.get("chemistry"), "B")
        self.assertEqual(results.get("biology"), "B")

    #enddef

    def test_find_multi_grades_3(self):
        results = self.parser.find_all_grades("I got AAA in physics, maths and CS")
        self.assertEqual(results.get("physics"), "A")
        self.assertEqual(results.get("mathematics"), "A")
        self.assertEqual(results.get("computer science"), "A")

    #enddef

    def test_find_multi_grades_4(self):
        results = self.parser.find_all_grades("My grades are BCD in art, music, drama")
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

    # Tests for find_all_grades function (handles single grade pairs)
    def test_find_grade_subject_pairs(self):
        # will fail because function isnt FUNCTIONing properly right now 😆 but it will.
        pairs = self.parser.find_all_grades(
            "I got A in maths, B in physics and dropped chemistry, and im interested in med")
        # Should map normalized subject to grade
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("physics"), "B")
        self.assertIsNone(pairs.get("chemistry"))  # dropped, shouldn't show up

    #enddef

    def test_find_grade_subject_pairs_2(self):
        pairs = self.parser.find_all_grades("A in maths, B in chemistry, dropped physics")
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("chemistry"), "B")
        self.assertIsNone(pairs.get("physics"))

    #enddef

    def test_find_grade_subject_pairs_3(self):
        pairs = self.parser.find_all_grades("Maths: A, Physics: B, English: C")
        self.assertEqual(pairs.get("mathematics"), "A")
        self.assertEqual(pairs.get("physics"), "B")
        self.assertEqual(pairs.get("english"), "C")

    #enddef

    def test_find_grade_subject_pairs_4(self):
        pairs = self.parser.find_all_grades("biology B, chemistry A*, maths C")
        self.assertEqual(pairs.get("biology"), "B")
        self.assertEqual(pairs.get("chemistry"), "A*")
        self.assertEqual(pairs.get("mathematics"), "C")

    #enddef

    def test_find_grade_subject_pairs_5(self):
        pairs = self.parser.find_all_grades("My grade in geography is D, and in history is C")
        self.assertEqual(pairs.get("geography"), "D")
        self.assertEqual(pairs.get("history"), "C")

    #enddef

    def test_find_grade_subject_pairs_6(self):
        pairs = self.parser.find_all_grades("I have A* in comp sci, B in math, C in further math, failed art")
        self.assertEqual(pairs.get("computer science"), "A*")
        self.assertEqual(pairs.get("mathematics"), "B")
        self.assertEqual(pairs.get("further mathematics"), "C")
        self.assertIsNone(pairs.get("art"))

    #enddef

    def test_find_grade_subject_pairs_7(self):
        pairs = self.parser.find_all_grades(
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

    # Tests for natural student input variations
    def test_parse_have_grades(self):
        result = self.parser.parse("I have A* in Maths, B in Physics and C in Chem")
        self.assertEqual(result['grades'], {'mathematics': 'A*', 'physics': 'B', 'chemistry': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_scored_with_interests(self):
        result = self.parser.parse("scored A in Bio, B in English Lit and hoping to do medicine")
        self.assertEqual(result['grades'], {'biology': 'A', 'english literature': 'B'})
        self.assertEqual(result['interests'], ['medicine'])

    #enddef

    def test_parse_expecting_grades(self):
        result = self.parser.parse("expecting AAB in Maths, Physics and Chemistry")
        self.assertEqual(result['grades'], {'mathematics': 'A', 'physics': 'A', 'chemistry': 'B'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_multiple_uni_interests(self):
        result = self.parser.parse("Got A in Bio and B in Chem, interested in medicine and pharmacy")
        self.assertEqual(result['grades'], {'biology': 'A', 'chemistry': 'B'})
        self.assertEqual(result['interests'], ['medicine', 'pharmacy'])

    #enddef

    def test_parse_colon_and_dash_format(self):
        result = self.parser.parse("Maths: A*, Physics - B, Chem C")
        self.assertEqual(result['grades'], {'mathematics': 'A*', 'physics': 'B', 'chemistry': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_further_maths_full(self):
        result = self.parser.parse("I got A* in Further Maths, B in Chemistry and C in Bio")
        self.assertEqual(result['grades'], {'further mathematics': 'A*', 'chemistry': 'B', 'biology': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_looking_to_study(self):
        result = self.parser.parse("A in CS, B in Maths. Looking to study engineering")
        self.assertEqual(result['grades'], {'computer science': 'A', 'mathematics': 'B'})
        self.assertEqual(result['interests'], ['engineering'])

    #enddef

    def test_parse_triple_a_medicine(self):
        result = self.parser.parse("Got AAA in Bio, Chem, Physics. I want to do medicine")
        self.assertEqual(result['grades'], {'biology': 'A', 'chemistry': 'A', 'physics': 'A'})
        self.assertEqual(result['interests'], ['medicine'])

    #enddef

    def test_parse_lowercase_input(self):
        result = self.parser.parse("got a in maths, b in physics, C IN CHEMISTRY")
        self.assertEqual(result['grades'], {'mathematics': 'A', 'physics': 'B', 'chemistry': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_predicted_with_abbreviations(self):
        # Note: CS won't appear in interests since they already have it as a grade
        result = self.parser.parse(
            "My predicted grades are A* in FM, A in Maths, B in CS. Applying for computer science")
        self.assertEqual(result['grades'], {'further mathematics': 'A*', 'mathematics': 'A', 'computer science': 'B'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_only_uni_interests(self):
        result = self.parser.parse("I'm really interested in law and hoping to study it at uni")
        self.assertEqual(result['grades'], {})
        self.assertEqual(result['interests'], ['law'])

    #enddef

    def test_parse_grades_then_interests(self):
        result = self.parser.parse("A* in Maths, A in Physics, B in Chemistry, interested in engineering")
        self.assertEqual(result['grades'], {'mathematics': 'A*', 'physics': 'A', 'chemistry': 'B'})
        self.assertEqual(result['interests'], ['engineering'])

    #enddef

    def test_parse_consecutive_grades_no_comma(self):
        # Test case where grades are written consecutively without commas
        result = self.parser.parse(
            "I got A in Arts B in maths and A in chemistry. Which course and uni is best for me?")
        self.assertEqual(result['grades'], {'arts': 'A', 'mathematics': 'B', 'chemistry': 'A'})
        # No specific interests mentioned (just asking for advice)
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_multiple_grades_no_commas(self):
        result = self.parser.parse("I got A in Arts B in Maths C in Physics")
        self.assertEqual(result['grades'], {'arts': 'A', 'mathematics': 'B', 'physics': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_mix_comma_no_comma(self):
        result = self.parser.parse("Got A in Bio, B in Chem C in Physics")
        self.assertEqual(result['grades'], {'biology': 'A', 'chemistry': 'B', 'physics': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_lower_grades(self):
        result = self.parser.parse("I got D in Art, E in Music and U in Drama")
        self.assertEqual(result['grades'], {'art': 'D', 'music': 'E', 'drama': 'U'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_achieved_received(self):
        result = self.parser.parse("Achieved A* in FM, received B in CS")
        self.assertEqual(result['grades'], {'further mathematics': 'A*', 'computer science': 'B'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_with_newlines(self):
        result = self.parser.parse("A in Maths\nB in Physics\nC in Chemistry")
        self.assertEqual(result['grades'], {'mathematics': 'A', 'physics': 'B', 'chemistry': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_with_typos(self):
        result = self.parser.parse("i hav a in bio b in chem and c in phys")
        self.assertEqual(result['grades'], {'biology': 'A', 'chemistry': 'B', 'physics': 'C'})
        self.assertEqual(result['interests'], [])

    #enddef

    def test_parse_mixed_formats(self):
        result = self.parser.parse("Maths: A*, B in Physics, Chemistry - C")
        self.assertEqual(result['grades'], {'mathematics': 'A*', 'physics': 'B', 'chemistry': 'C'})
        self.assertEqual(result['interests'], [])
    #enddef


#endclass


if __name__ == "__main__":
    unittest.main()
#endif