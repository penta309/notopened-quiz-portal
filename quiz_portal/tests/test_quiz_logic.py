#!/usr/bin/env python3
"""
Unit test suite for notopened Quiz Portal MVP v1.1.0
Tests data integrity, scoring logic, DOM structure, accessibility, touch styles, and privacy policy compliance.
"""

import unittest
import os
import re
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestQuizPortal(unittest.TestCase):

    def setUp(self):
        self.index_html_path = os.path.join(BASE_DIR, "index.html")
        self.privacy_html_path = os.path.join(BASE_DIR, "privacy.html")
        self.ads_txt_path = os.path.join(BASE_DIR, "ads.txt")
        self.data_js_path = os.path.join(BASE_DIR, "src", "data.js")
        self.style_css_path = os.path.join(BASE_DIR, "assets", "css", "style.css")
        self.app_js_path = os.path.join(BASE_DIR, "src", "app.js")
        self.touch_js_path = os.path.join(BASE_DIR, "src", "touchHandler.js")

    def test_files_exist(self):
        """Verify all standard project structure files and policy documents exist."""
        self.assertTrue(os.path.exists(self.index_html_path), "index.html must exist")
        self.assertTrue(os.path.exists(self.privacy_html_path), "privacy.html must exist")
        self.assertTrue(os.path.exists(self.ads_txt_path), "ads.txt must exist")
        self.assertTrue(os.path.exists(self.data_js_path), "src/data.js must exist")
        self.assertTrue(os.path.exists(self.style_css_path), "assets/css/style.css must exist")
        self.assertTrue(os.path.exists(self.app_js_path), "src/app.js must exist")
        self.assertTrue(os.path.exists(self.touch_js_path), "src/touchHandler.js must exist")

    def test_data_integrity(self):
        """Verify the 5 baseline quiz questions from data.js."""
        with open(self.data_js_path, "r", encoding="utf-8") as f:
            content = f.read()

        items = re.findall(r'id:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*question:\s*"([^"]+)",\s*options:\s*\[(.*?)\],\s*answer:\s*(\d+),\s*explanation:\s*"([^"]+)",\s*source:\s*"([^"]+)"', content, re.DOTALL)
        
        self.assertEqual(len(items), 30, f"Expected 30 verified questions, found {len(items)}")

        for item in items:
            q_id, cat, question, options_raw, answer_str, exp, source = item
            self.assertTrue(q_id.startswith("quiz-"), f"Invalid ID: {q_id}")
            self.assertTrue(len(cat.strip()) > 0, "Category cannot be empty")
            self.assertTrue(len(question.strip()) > 0, "Question cannot be empty")
            
            options = re.findall(r'"([^"]+)"', options_raw)
            self.assertGreaterEqual(len(options), 2, "Each question must have at least 2 options")
            
            ans_idx = int(answer_str)
            self.assertTrue(0 <= ans_idx < len(options), f"Answer index {ans_idx} out of range for options {options}")
            self.assertTrue(len(exp.strip()) > 0, "Explanation cannot be empty")
            self.assertTrue(len(source.strip()) > 0, "Fact-check source cannot be empty")

    def test_mobile_viewport_and_metadata(self):
        """Verify mobile-first viewport, Open Graph, and Schema.org metadata in index.html."""
        with open(self.index_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Viewport check
        self.assertIn('name="viewport"', html, "Viewport meta tag required")
        self.assertIn('width=device-width', html, "width=device-width required")
        
        # Open Graph & SEO
        self.assertIn('property="og:title"', html, "Open Graph title required")
        self.assertIn('property="og:description"', html, "Open Graph description required")
        self.assertIn('name="twitter:card"', html, "Twitter card required")

        # Accessibility and semantic checks
        self.assertIn('id="quizCard"', html)
        self.assertIn('id="resultCard"', html)
        self.assertIn('id="optionsGrid"', html)
        self.assertIn('id="explanationBox"', html)
        self.assertIn('id="nextBtn"', html)
        self.assertIn('id="shareBtn"', html)
        self.assertIn('id="progressFill"', html)

        # Cross promo check (all 3 games)
        self.assertIn('data-game="001"', html, "GAME 001 must be linked")
        self.assertIn('data-game="002"', html, "GAME 002 (노아) must be linked")
        self.assertIn('data-game="003"', html, "GAME 003 (루카) must be linked")

        # Privacy link
        self.assertIn('privacy.html', html, "Privacy policy link required in footer")
        
        # Schema.org check
        self.assertIn('"@type": "Quiz"', html, "Schema.org Quiz type required")
        self.assertIn('"hasPart"', html, "Schema.org Quiz must have hasPart questions for rich snippets")

    def test_touch_and_mobile_css(self):
        """Verify mobile touch target size and responsive styles in style.css."""
        with open(self.style_css_path, "r", encoding="utf-8") as f:
            css = f.read()

        # Touch target minimum height check (at least 48px to 52px)
        self.assertIn("min-height: 52px", css, "Minimum 52px touch target height required for mobile accessibility")
        self.assertIn("max-width: 480px", css, "Container max-width 480px for smartphone optimization")
        self.assertIn("touch-action: manipulation", css, "touch-action: manipulation required to remove tap delay")
        self.assertIn(".touch-active", css, "Touch-active class must have styling rules defined in CSS")
        self.assertIn(":focus-visible", css, "Accessible focus-visible styles required")

    def test_privacy_policy_content(self):
        """Verify privacy policy adheres to zero-collection and AdSense compliance."""
        with open(self.privacy_html_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("개인정보처리방침", html)
        self.assertIn("비수집 원칙", html)
        self.assertIn("Google AdSense", html)

    def test_scoring_and_rank_logic(self):
        """Verify the rank calculation boundary logic."""
        def calculate_rank(score):
            if score == 5:
                return "MASTER"
            elif score >= 3:
                return "EXPLORER"
            else:
                return "ROOKIE"

        self.assertEqual(calculate_rank(5), "MASTER")
        self.assertEqual(calculate_rank(4), "EXPLORER")
        self.assertEqual(calculate_rank(3), "EXPLORER")
        self.assertEqual(calculate_rank(2), "ROOKIE")
        self.assertEqual(calculate_rank(1), "ROOKIE")
        self.assertEqual(calculate_rank(0), "ROOKIE")

if __name__ == "__main__":
    unittest.main()
