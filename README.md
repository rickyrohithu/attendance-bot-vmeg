# 🕵️‍♂️ Automated Attendance Checker Bot

This is a Python-based automation bot that logs into the **Vardhaman College student portal**, checks your **attendance for the current day**, and **sends a Telegram alert** if you're marked absent. It helps you stay informed without manually logging in every time.

---

## 🚀 Features

- 🔐 Logs into your college portal using credentials  
- 📅 Scrapes today’s attendance records  
- ✅ Counts total classes attended and missed today  
- 📲 Sends an alert via **Telegram Bot** if you were absent  
- 🕔 Designed to run automatically every day at **5 PM**  

---

## 🛠 Tech Stack

- **Python**  
- **Selenium** for browser automation  
- **BeautifulSoup** for HTML parsing  
- **Telegram Bot API** for alerts  
- **Cron (Mac/Linux)** for daily scheduling  

---

## 🧠 How It Works

1. Uses `selenium` to open the login page:  
   `https://login.vardhaman.org/`
2. Logs in using your username & password  
3. Navigates to the attendance page:  
   `https://student.vardhaman.org/Attendance.aspx`
4. Parses today’s date and marks:
   - ✅ Present: `btn-success`
   - ❌ Absent: any other status
5. Counts total present & absent  
6. Sends a Telegram alert if absent  

---

## 📂 Project Structure

```
attendance_checker.py         # Main Python script  
README.md                     # Project documentation  
```

---

## 📦 Requirements

Install these Python packages first:

```bash
pip install selenium
pip install beautifulsoup4
```

You’ll also need:
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (installed and in PATH)  
- A Telegram Bot Token and Chat ID

---

## 🧪 How to Run

```bash
python3 attendance_checker.py
```

---

## 🕒 Automation (Daily Cron Job at 5 PM)

Edit your crontab:

```bash
crontab -e
```

Add:

```bash
0 17 * * * /usr/bin/python3 /Users/rohithsomireddy/Documents/AttendanceBot/attendance_checker.py
```

---

## 🔒 Note

- Keep your credentials secure — avoid uploading them to GitHub!  
- You can use `.env` files or input fields to enhance security.

---

## 📬 Telegram Alert Format

```
📢 Attendance Alert – 20 July 2025
✅ Attended: 4
❌ Absent: 2

⚠️ You were marked absent today.
```

---

## 🙌 Contribution

Pull requests and suggestions welcome! Built with ❤️ to help students automate boring stuff.

---

## 📎 License

MIT License
