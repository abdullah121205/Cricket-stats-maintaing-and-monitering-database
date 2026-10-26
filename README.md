# 🏏 Cricket Stats Database & Monitoring System

A full-stack cricket statistics management and monitoring platform designed to maintain, track, and analyze cricket data including players, teams, matches, batting/bowling scorecards, and performance leaderboards.

---

## 🌟 Key Features

- **👤 Player Management**: Track player profiles, roles (Batter, Bowler, All-rounder, Wicketkeeper), career batting averages, strike rates, bowling figures, and recent form.
- **🏆 Team Management**: Organize teams, squads, match records, and dynamic win/loss percentages.
- **🏏 Match & Scorecard Tracking**: Schedule matches across Test, ODI, and T20 formats; record innings-by-innings batting and bowling spells.
- **📊 Performance Analytics & Leaderboards**: Instant statistical queries for top run scorers, top wicket takers, highest strike rates, and team standings.
- **⚡ Dual Database Support**: Production-ready for **MySQL 8.0+** with zero-config **SQLite fallback** for immediate local execution.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, FontAwesome, Chart.js
- **Backend**: Python 3.10+, Flask, Flask-CORS, PyMySQL
- **Database**: MySQL / SQLite

---

## 📁 Project Structure

```text
Cricket-stats-maintaing-and-monitering-database/
├── backend/
│   ├── app.py               # Main Flask application & static server
│   ├── config.py            # Environment & database configuration
│   ├── db.py                # Database connection adapter (MySQL/SQLite)
│   └── routes/              # REST API routes (players, teams, matches, venues, stats)
├── frontend/
│   ├── index.html           # KPI dashboard & performance charts
│   ├── players.html         # Player directory & career stats modal
│   ├── teams.html           # Team rosters & win-rate progress
│   ├── matches.html         # Match schedules & scorecard recorder
│   ├── statistics.html      # Top scorers, bowlers & team standings
│   ├── css/style.css        # Sports UI stylesheet
│   └── js/app.js            # Frontend client controller
├── database/
│   ├── schema.sql           # MySQL database schema definition
│   ├── sample_data.sql      # Seed dataset with teams, players & scorecards
│   └── queries.sql          # Analytical SQL queries & leaderboards
├── requirements.txt         # Python dependencies
└── .env.example             # Database configuration template
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database (Optional)
The system runs immediately out of the box with SQLite. To connect to MySQL instead, copy `.env.example` to `.env` and set your credentials:
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cricket_stats
```

### 3. Run the Application
```bash
python backend/app.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 👨‍💻 Team & License

- **Institution**: SRM Institute of Science and Technology
- **License**: Educational & Academic Use
