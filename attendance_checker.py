from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import requests

# --- Configuration ---
USERNAME = "***********"
PASSWORD = "**********"
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
TELEGRAM_BOT_TOKEN = "7376143818:AAEITJMoZvvp5WpRbOLKgeN5yBbh8VAwaeY"
TELEGRAM_CHAT_ID = "8001500966"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(url, data=payload)
        resp.raise_for_status()
        print("✅ Telegram message sent.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending Telegram message: {e}")
        if resp is not None:
            print(f"   Response from Telegram API: {resp.text}")

def run_attendance_check():
    telegram_output_messages = []

    options = Options()
    options.add_argument("--headless")  # Run Chrome in hidden mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = None

    try:
        print("🚀 Starting WebDriver...")
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20)

        telegram_output_messages.append("🚀 Starting attendance check script...")
        print("🌐 Opening login page...")
        driver.get("https://login.vardhaman.org/")

        print("🔑 Logging in...")
        wait.until(EC.presence_of_element_located((By.ID, "txtuser"))).send_keys(USERNAME)
        driver.find_element(By.ID, "txtpass").send_keys(PASSWORD)
        driver.find_element(By.ID, "btnLogin").click()
        print("✅ Login submitted.")
        telegram_output_messages.append("✅ Login submitted.")

        # Handle first popup
        try:
            popup1 = wait.until(EC.element_to_be_clickable(
                (By.ID, "ctl00_ContentPlaceHolder1_PopupCTRLMain_btnClose")))
            popup1.click()
            print("✅ Popup 1 closed.")
            telegram_output_messages.append("✅ Popup 1 closed.")
        except:
            print("ℹ️ Popup 1 not found.")
            telegram_output_messages.append("ℹ️ Popup 1 not found or already closed.")

        # Handle second popup
        try:
            popup2 = wait.until(EC.element_to_be_clickable(
                (By.ID, "ctl00_ContentPlaceHolder1_PopupCTRLMain_btnClose")))
            popup2.click()
            print("✅ Popup 2 closed.")
            telegram_output_messages.append("✅ Popup 2 closed.")
        except:
            print("ℹ️ Popup 2 not found.")
            telegram_output_messages.append("ℹ️ Popup 2 not found or already closed.")

        print("📄 Navigating to Attendance page...")
        driver.get("https://student.vardhaman.org/Attendance.aspx")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "date-inr")))
        print("✅ Attendance page loaded.")
        telegram_output_messages.append("✅ Attendance page loaded.")

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        today_str = datetime.today().strftime("%d %b %Y")
        attendance_sections = soup.select("div.col-md-6")

        today_section = None
        for section in attendance_sections:
            date_div = section.find("div", class_="date-inr")
            if date_div and date_div.text.strip() == today_str:
                today_section = section
                break

        if not today_section:
            msg = f"⚠️ <b>Attendance for today ({today_str}) not found.</b>"
            telegram_output_messages.append(msg)
            print(msg)
        else:
            present_classes = []
            absent_classes = []

            attendance_list = today_section.select_one("div.atten-sub.bus-stops ul")
            if attendance_list:
                for li in attendance_list.find_all("li"):
                    subject = li.select_one("div.stp-detail h5").text.strip()
                    timing = li.select_one("div.stp-detail p").text.strip()
                    status_div = li.select_one("div.fac-status div.status")
                    if status_div:
                        classes = status_div.get("class", [])
                        if "btn-success" in classes:
                            present_classes.append(f"{subject} ({timing})")
                        else:
                            absent_classes.append(f"{subject} ({timing})")

            attendance_summary = [f"\n<b>📊 Attendance for {today_str}:</b>"]
            if present_classes:
                attendance_summary.append(f"<b>✅ Present ({len(present_classes)}):</b>")
                attendance_summary += [f"  • {cls}" for cls in present_classes]
            else:
                attendance_summary.append("<b>✅ Present (0)</b>")

            if absent_classes:
                attendance_summary.append(f"<b>❌ Absent ({len(absent_classes)}):</b>")
                attendance_summary += [f"  • {cls}" for cls in absent_classes]
                telegram_output_messages.append(f"⚠️ <b>You were absent for {len(absent_classes)} class(es).</b>")
            else:
                attendance_summary.append("<b>❌ Absent (0):</b> Great job attending all classes!")
                telegram_output_messages.append("🎉 <b>No absences today!</b>")

            telegram_output_messages.extend(attendance_summary)

    except Exception as e:
        msg = f"❌ Script error: {e}"
        print(msg)
        telegram_output_messages.append(msg)

    finally:
        final_msg = "\n".join(telegram_output_messages)
        print("\n📤 Sending summary to Telegram...")
        send_telegram_message(final_msg)
        if driver:
            print("🧹 Closing browser...")
            driver.quit()
        print("✅ Script finished.")
if __name__ == "__main__":
    run_attendance_check()
