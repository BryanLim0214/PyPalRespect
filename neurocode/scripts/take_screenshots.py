"""
Capture PyPal screenshots for the README.

Starts both the backend and the Vite dev server before running this script.
Writes PNGs to docs/screenshots/.
"""
import os
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)

FRONTEND = "http://localhost:5173"
BACKEND = "http://127.0.0.1:8000"


def ensure_test_accounts():
    """Make sure a demo teacher and student exist so screens have data."""
    # Teacher
    try:
        urllib.request.urlopen(
            urllib.request.Request(
                f"{BACKEND}/api/auth/register",
                data=json.dumps({
                    "username": "demo_teacher",
                    "password": "demo12345",
                    "birth_year": 1988,
                    "grade_level": 0,
                    "role": "teacher",
                    "display_name": "Ms. Kim",
                    "school": "Lincoln Middle",
                }).encode(),
                headers={"Content-Type": "application/json"},
            ),
            timeout=5,
        )
    except Exception:
        pass
    # Student
    try:
        urllib.request.urlopen(
            urllib.request.Request(
                f"{BACKEND}/api/auth/register",
                data=json.dumps({
                    "username": "demo_student",
                    "password": "demo12345",
                    "birth_year": 2011,
                    "grade_level": 7,
                    "interests": ["games", "space"],
                }).encode(),
                headers={"Content-Type": "application/json"},
            ),
            timeout=5,
        )
    except Exception:
        pass


def seed_exercises():
    try:
        urllib.request.urlopen(
            urllib.request.Request(f"{BACKEND}/api/admin/seed-exercises", method="POST"),
            timeout=20,
        )
    except Exception as e:
        print("seed skipped:", e)


def login(driver, username: str, password: str):
    driver.get(f"{FRONTEND}/login")
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2.5)


def shot(driver, name: str):
    path = SHOTS / name
    driver.save_screenshot(str(path))
    print(f"wrote {path}")


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--hide-scrollbars")
    opts.add_argument("--force-device-scale-factor=1")
    return webdriver.Chrome(options=opts)


def main():
    ensure_test_accounts()
    seed_exercises()

    driver = make_driver()
    try:
        # 1. Login page
        driver.get(f"{FRONTEND}/login")
        time.sleep(1.5)
        shot(driver, "01_login.png")

        # 2. Register page (student tab)
        driver.get(f"{FRONTEND}/register")
        time.sleep(1.5)
        shot(driver, "02_register_student.png")

        # Register page (teacher tab)
        driver.find_elements(By.CSS_SELECTOR, "button[type='button']")[1].click()
        time.sleep(0.8)
        shot(driver, "03_register_teacher.png")

        # 3. Student dashboard
        login(driver, "demo_student", "demo12345")
        driver.get(f"{FRONTEND}/dashboard")
        time.sleep(2)
        shot(driver, "04_student_dashboard.png")

        # 4. Exercise page (first exercise)
        links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/exercise/']")
        if links:
            links[0].click()
            time.sleep(3)
            shot(driver, "05_student_exercise.png")

        # 5. Settings
        driver.get(f"{FRONTEND}/settings")
        time.sleep(1.5)
        shot(driver, "06_settings.png")

        # 6. Log out, log in as teacher
        driver.get(f"{FRONTEND}/login")
        time.sleep(1)
        # clear localStorage
        driver.execute_script("localStorage.clear();")
        login(driver, "demo_teacher", "demo12345")

        driver.get(f"{FRONTEND}/teacher")
        time.sleep(2)
        shot(driver, "07_teacher_dashboard.png")

        driver.get(f"{FRONTEND}/teacher/exercises")
        time.sleep(2)
        shot(driver, "08_teacher_exercises.png")

        # Student detail (first visible row)
        driver.get(f"{FRONTEND}/teacher")
        time.sleep(2)
        view_links = driver.find_elements(By.LINK_TEXT, "View")
        if view_links:
            view_links[0].click()
            time.sleep(2)
            shot(driver, "09_teacher_student_detail.png")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
