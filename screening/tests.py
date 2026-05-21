from django.test import TestCase
from .ai import predict_category, extract_skills, is_resume

class AITests(TestCase):
    def test_predict_category_web(self):
        text = "I know html css javascript react and node"
        cat, pct, _ = predict_category(text)
        self.assertEqual(cat, "Web Development")

    def test_is_resume(self):
        text = "Education: BSc CS. Experience: 3 years. Skills: Python"
        self.assertTrue(is_resume(text))

    def test_extract_skills(self):
        text = "python machine learning pandas tensorflow"
        skills = extract_skills(text)
        self.assertIn("python", skills)
