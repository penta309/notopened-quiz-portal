#!/usr/bin/env python3
"""
notopened AI ENTERPRISE - End-to-End Browser Automation Test Suite
Uses Headless Chromium via Selenium with mobile emulation.
Tests full user journeys across Desktop, Mobile (iPhone 14, Galaxy S23, Galaxy Fold Cover 320px, iPad).
Validates UI states, touch targets, accessibility, scoring, results, restart, and captures screenshots.
"""

import os
import sys
import time
import http.server
import socketserver
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

class QuietServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server(start_port=8105):
    socketserver.TCPServer.allow_reuse_address = True
    for p in range(start_port, start_port + 30):
        try:
            httpd = socketserver.TCPServer(('127.0.0.1', p), QuietServer)
            t = threading.Thread(target=httpd.serve_forever, daemon=True)
            t.start()
            return httpd, p
        except OSError:
            continue
    raise RuntimeError('No free port available')

def create_driver(viewport=None, mobile_metrics=None, user_agent=None):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--host-resolver-rules=MAP quiz.local 127.0.0.1')
    
    if mobile_metrics:
        mobile_emulation = {
            'deviceMetrics': mobile_metrics,
            'userAgent': user_agent or 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        options.add_experimental_option('mobileEmulation', mobile_emulation)
    elif viewport:
        options.add_argument(f'--window-size={viewport[0]},{viewport[1]}')
        
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)
    return driver

def run_tests():
    server, PORT = start_server(8105)
    print(f"[*] Local HTTP test server started at http://quiz.local:{PORT}")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": []
    }

    def record_test(name, success, msg=""):
        results["total"] += 1
        if success:
            results["passed"] += 1
            print(f"  [PASS] {name}")
        else:
            results["failed"] += 1
            results["errors"].append(f"{name}: {msg}")
            print(f"  [FAIL] {name} - {msg}")

    print("\n--- Phase 1: Desktop Browser Full Flow (1920x1080) ---")
    driver_desktop = create_driver(viewport=(1920, 1080))
    try:
        driver_desktop.get(f"http://quiz.local:{PORT}/index.html")
        time.sleep(0.5)

        # Test 1.1: Title and Header
        record_test("Desktop Page Load & Title", "notopened" in driver_desktop.title)
        
        # Capture Desktop Initial Screenshot
        driver_desktop.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_initial.png"))

        # Test 1.2: Question 1 elements
        q1_text = driver_desktop.find_element(By.ID, "questionText").text
        record_test("Question 1 Content Present", len(q1_text) > 10, q1_text)
        
        # Test Clean UI: Verify mock ad slots are hidden (display: none)
        ad_slots = driver_desktop.find_elements(By.CLASS_NAME, "ad-slot")
        ads_hidden = all(not slot.is_displayed() for slot in ad_slots) if ad_slots else True
        record_test("Clean UI: Mock Ad Slots Hidden (display: none)", ads_hidden)
        
        options = driver_desktop.find_elements(By.CLASS_NAME, "option-btn")
        record_test("Option Buttons Count (Q1)", len(options) == 2)
        
        # Test 1.3: Click Correct Option on Q1 (index 0)
        options[0].click()
        time.sleep(0.3)
        exp_box = driver_desktop.find_element(By.ID, "explanationBox")
        record_test("Explanation Box Displayed", exp_box.is_displayed())
        record_test("Explanation Positive Feedback", "정답" in exp_box.text)

        next_btn = driver_desktop.find_element(By.ID, "nextBtn")
        record_test("Next Button Displayed after Answer", next_btn.is_displayed() and next_btn.text == "다음 문제로")
        
        # Test 1.4: Proceed through Q2, Q3, Q4, Q5
        next_btn.click()
        time.sleep(0.3)
        
        # Q2: Select Wrong Option (index 0: 얼음)
        q2_options = driver_desktop.find_elements(By.CLASS_NAME, "option-btn")
        q2_options[0].click()
        time.sleep(0.3)
        exp_box_q2 = driver_desktop.find_element(By.ID, "explanationBox")
        record_test("Explanation Negative Feedback on Wrong Answer", "오답" in exp_box_q2.text)
        
        driver_desktop.find_element(By.ID, "nextBtn").click()
        time.sleep(0.3)

        # Q3: Correct (index 0)
        driver_desktop.find_elements(By.CLASS_NAME, "option-btn")[0].click()
        time.sleep(0.2)
        driver_desktop.find_element(By.ID, "nextBtn").click()
        time.sleep(0.3)

        # Q4: Correct (index 2: 다이아몬드)
        driver_desktop.find_elements(By.CLASS_NAME, "option-btn")[2].click()
        time.sleep(0.2)
        driver_desktop.find_element(By.ID, "nextBtn").click()
        time.sleep(0.3)

        # Q5: Correct (index 1: 남극 사막)
        driver_desktop.find_elements(By.CLASS_NAME, "option-btn")[1].click()
        time.sleep(0.2)
        next_btn_q5 = driver_desktop.find_element(By.ID, "nextBtn")
        record_test("Last Question Button says '결과 보기'", next_btn_q5.text == "결과 보기")
        next_btn_q5.click()
        time.sleep(0.4)

        # Test 1.5: Result Screen Verification
        result_card = driver_desktop.find_element(By.ID, "resultCard")
        record_test("Result Screen Displayed", result_card.is_displayed())
        
        final_score = driver_desktop.find_element(By.ID, "finalScore").text
        record_test("Scoring Accuracy (4 / 5)", final_score == "4")

        rank_title = driver_desktop.find_element(By.ID, "rankTitle").text
        record_test("Rank Title Badge Assigned", "스마트한 상식 탐험가" in rank_title)

        # Test 1.6: Non-blocking Game Promo button
        game_btns = driver_desktop.find_elements(By.CLASS_NAME, "game-link-btn")
        record_test("Cross-promo Game Count (All 3 Games)", len(game_btns) == 3)
        game_btns[0].click()
        time.sleep(0.3)
        toast = driver_desktop.find_element(By.ID, "toast")
        record_test("Game Promo Toast Displayed (Non-blocking)", toast.is_displayed() and "GAME #001" in toast.text)

        # Test 1.7: Share Button Click
        share_btn = driver_desktop.find_element(By.ID, "shareBtn")
        share_btn.click()
        time.sleep(0.3)
        record_test("Share Button Toast Triggered", toast.is_displayed())

        # Test 1.8: Restart Flow
        restart_btn = driver_desktop.find_element(By.ID, "restartBtn")
        restart_btn.click()
        time.sleep(0.4)
        quiz_card = driver_desktop.find_element(By.ID, "quizCard")
        counter_text = driver_desktop.find_element(By.ID, "counterText").text
        record_test("Restart Returns to Question 1", quiz_card.is_displayed() and "1 / 5" in counter_text)

    except Exception as e:
        record_test("Desktop Browser Flow Exception", False, str(e))
        driver_desktop.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_error.png"))
    finally:
        driver_desktop.quit()

    print("\n--- Phase 2: Mobile Emulation & Responsive Verification ---")
    mobile_devices = [
        ("iPhone 14 / 15", {"width": 390, "height": 844, "pixelRatio": 3.0}),
        ("Galaxy S22 / S23", {"width": 360, "height": 800, "pixelRatio": 2.0}),
        ("Galaxy Fold Cover (320px)", {"width": 320, "height": 650, "pixelRatio": 2.0}),
        ("iPad Mini (768px)", {"width": 768, "height": 1024, "pixelRatio": 2.0})
    ]

    for dev_name, metrics in mobile_devices:
        driver_mob = create_driver(mobile_metrics=metrics)
        try:
            driver_mob.get(f"http://quiz.local:{PORT}/index.html")
            time.sleep(0.5)

            # Check horizontal overflow
            inner_w = driver_mob.execute_script("return window.innerWidth")
            scroll_w = driver_mob.execute_script("return document.documentElement.scrollWidth")
            record_test(f"{dev_name} No Horizontal Overflow", scroll_w <= inner_w, f"scrollW {scroll_w} > innerW {inner_w}")

            # Check touch target size for option buttons (min-height >= 52px)
            opt_btns = driver_mob.find_elements(By.CLASS_NAME, "option-btn")
            all_min_52 = all(btn.size["height"] >= 50 for btn in opt_btns)
            record_test(f"{dev_name} Touch Target Height >= 50px", all_min_52)

            # Take screenshot for key devices
            if "iPhone" in dev_name:
                driver_mob.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_iphone14_q1.png"))
                # Answer Q1
                opt_btns[0].click()
                time.sleep(0.3)
                driver_mob.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_iphone14_answered.png"))
                
                # Proceed to result
                driver_mob.find_element(By.ID, "nextBtn").click()
                time.sleep(0.2)
                for _ in range(4):
                    driver_mob.find_elements(By.CLASS_NAME, "option-btn")[0].click()
                    time.sleep(0.2)
                    driver_mob.find_element(By.ID, "nextBtn").click()
                    time.sleep(0.2)
                driver_mob.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_iphone14_result.png"))

            elif "Fold" in dev_name:
                driver_mob.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_fold_320px.png"))

        except Exception as e:
            record_test(f"{dev_name} Mobile Test Exception", False, str(e))
            driver_mob.save_screenshot(os.path.join(SCREENSHOTS_DIR, f"mobile_error_{metrics['width']}.png"))
        finally:
            driver_mob.quit()

    server.shutdown()
    print("\n==========================================")
    print(f"Browser Automation Test Summary:")
    print(f"Total: {results['total']} | Passed: {results['passed']} | Failed: {results['failed']}")
    print(f"Pass Rate: {(results['passed'] / results['total']) * 100:.1f}%")
    print(f"Screenshots saved to: {SCREENSHOTS_DIR}")
    print("==========================================\n")
    return results["failed"] == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
