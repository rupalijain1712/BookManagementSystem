#  AI-Powered Book Management System

A full-stack web application for intelligent book management with CRUD operations, Google Gemini AI recommendations, and cloud deployment on Render.com — built with Python Flask, SQLite3, and the `google-genai` SDK.

>  Fully Cloud-Deployed &nbsp;|&nbsp;  Gemini AI Powered &nbsp;|&nbsp;  SQL Injection Protected &nbsp;|&nbsp;  Zero External DB Server

---

##  Features

###  Google Gemini AI Recommendations
- Accepts **free-form natural language** input (e.g. "I love sci-fi thrillers")
- Prompts Gemini with an **expert librarian persona** to generate 5 curated book picks
- Each recommendation includes: Book Name, Author, Difficulty Level, and Why Recommended
- Every AI response is **persisted in SQLite** for future analytics and trending insights
- Uses `gemini-3-flash-preview` — sub-second responses on Render's free tier

###  Full CRUD Operations
- **Create** — Add new books with title, author, and category via a validated form
- **Read** — View the complete book catalog in a responsive card-based layout
- **Search** — Find a book by title with a live fuzzy `LIKE` query
- **Update** — Edit any field for an existing book by ID
- **Delete** — Remove a book record by ID with immediate DB commit

###  Live Dashboard (Home Page)
- Displays **total books** in the library at a glance
- Shows **unique category count** and lists all available categories
- Stats are computed in real time from the database on every page load

###  Security — SQL Injection Prevention
- All database operations use **parameterized queries** (`?` placeholders with tuples)
- No raw string formatting in SQL — safe against injection by design
- Sensitive API keys loaded via **environment variables**, never hardcoded

###  Cloud Deployment on Render.com
- Deployed via **Gunicorn WSGI server** using a `Procfile`
- Linked directly to a **GitHub repository** for automatic re-deploy on push
- Comes with automatic **HTTPS/SSL** and is accessible 24/7 from any device
- Environment variable `GEMINI_API_KEY` configured securely in Render's dashboard

---

##  Project Structure

| File / Folder | Purpose |
|---|---|
| **`app.py`** | Flask application — defines all 7 routes and wires templates to logic |
| **`database.py`** | SQLite data layer — all CRUD functions and table creation |
| **`gemini_service.py`** | Google Gemini AI service — prompt engineering and API call |
| **`/templates/`** | 8 Jinja2 HTML templates for every page |
| **`/static/style.css`** | Custom CSS — responsive card layout and page styling |
| **`requirements.txt`** | Python dependencies: Flask, gunicorn, google-genai |
| **`Procfile`** | Render.com deployment command: `web: gunicorn app:app` |
| **`books.db`** | Auto-created SQLite database file on first run |

---

##  Database Schema

### `books` table
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incremented unique identifier |
| `title` | TEXT | Book title (required) |
| `author` | TEXT | Author name (required) |
| `category` | TEXT | Genre or subject category |
| `created_at` | DATETIME | Timestamp of record creation (IST offset) |
| `updated_at` | DATETIME | Timestamp of last update (IST offset) |

### `recommendations` table
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incremented unique identifier |
| `interest` | TEXT | The user's original interest input |
| `ai_response` | TEXT | Full recommendation text from Gemini |

---

##  How It Works

```
User Submits Interest (e.g. "dark fantasy novels")
        ↓
Flask Route POST /recommend
        ↓
gemini_service.get_book_recommendation(interest)
        ↓
Gemini Flash generates 5 curated picks with author + difficulty
        ↓
Response saved → database.save_recommendation(interest, text)
        ↓
Jinja2 renders result on recommend.html
        ↓
User sees formatted recommendations instantly
```

---

##  Routes Overview

| Route | Method(s) | Function | Template |
|---|---|---|---|
| `/` | GET | Loads live stats (total books, categories) | `home.html` |
| `/add` | GET, POST | Form to add a new book to the DB | `add_book.html` / `success.html` |
| `/view` | GET | Fetches and displays all books | `view_books.html` |
| `/search` | GET, POST | Searches books by title (`LIKE` query) | `search_book.html` |
| `/update` | GET, POST | Updates title, author, category by ID | `update_book.html` / `success.html` |
| `/delete` | GET, POST | Deletes a book record by ID | `delete_book.html` / `success.html` |
| `/recommend` | GET, POST | Calls Gemini AI and saves the response | `recommend.html` |

---

##  Functions Reference

| Function | File | Purpose |
|---|---|---|
| `create_tables()` | `database.py` | Creates `books` and `recommendations` tables if they don't exist |
| `add_book(title, author, category)` | `database.py` | Inserts a new book row with a parameterized `INSERT` |
| `get_all_books()` | `database.py` | Returns all rows from the `books` table |
| `search_book(title)` | `database.py` | Fetches a single book using `SELECT ... WHERE title LIKE ?` |
| `update_book(id, title, author, category)` | `database.py` | Updates all editable fields for a given book ID |
| `delete_book(id)` | `database.py` | Deletes a book record by primary key |
| `get_page_stats()` | `database.py` | Returns total book count, unique category count, and category list |
| `save_recommendation(interest, ai_response)` | `database.py` | Persists Gemini output to the `recommendations` table |
| `get_book_recommendation(user_interest)` | `gemini_service.py` | Sends engineered prompt to Gemini, returns recommendation text |

---

##  Getting Started

**Requirements:**
- Python 3.10 or later
- A Google AI Studio API key (free tier available at [aistudio.google.com](https://aistudio.google.com))
- Git

**Local Setup:**

```bash
# 1. Clone the repository
git clone https://github.com/cloudsony999/BookManagement_FLASK_SQLITE

# 2. Navigate to the project folder
cd BookManagement_FLASK_SQLITE

# 3. Install dependencies
pip install Flask gunicorn google-genai

# 4. Set your Gemini API key
# Windows
set GEMINI_API_KEY=your_api_key_here

# macOS / Linux
export GEMINI_API_KEY=your_api_key_here

# 5. Run the app
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000`

>  The `books.db` file is created automatically on first run. Do not delete it while the app is running.

---

##  Deploying to Render.com

| Step | Action |
|---|---|
| **1** | Push your code to a public GitHub repository |
| **2** | Log in to [Render.com](https://render.com) and click **New Web Service** |
| **3** | Connect your GitHub repository |
| **4** | Set **Build Command**: `pip install -r requirements.txt` |
| **5** | Set **Start Command**: `gunicorn app:app` *(auto-detected from Procfile)* |
| **6** | Add environment variable: `GEMINI_API_KEY = your_key_here` |
| **7** | Click **Deploy** — your app goes live with a public HTTPS URL |

---

##  Use Cases

- Personal or institutional book catalog management
- AI-assisted reading list generation for students and librarians
- Educational project showcasing Flask + SQLite + LLM integration
- Beginner-friendly template for full-stack Python web development
- Learning prompt engineering with real API integration
- Portfolio project demonstrating cloud deployment skills

---

##  Future Improvements

- **User Authentication** — Flask-Login with role-based access and bcrypt password hashing
- **Analytics Dashboard** — Category trends, top-searched books, and Plotly/Chart.js visualizations
- **AI Chat Assistant** — Multi-turn conversational interface for interactive reading guidance
- **PostgreSQL Migration** — SQLAlchemy ORM for production-grade concurrency and scalability
- **REST API + Mobile App** — Flask-RESTful endpoints for an Android/iOS front end
- **Advanced Search & Filter** — Filter by author, category, price range, and pagination
- **Book Cover Images** — Auto-fetch covers via Open Library or Google Books API
- **Email Alerts** — Flask-Mail with Gmail SMTP or SendGrid for new book notifications

---

##  Tech Stack

| Technology | Role | Why Chosen |
|---|---|---|
| **Python 3** | Core language | Readable syntax, vast ecosystem, platform-independent |
| **Flask** | Web framework | Lightweight, easy routing with `@app.route`, Jinja2 built-in |
| **SQLite3** | Database | Serverless, zero config, single `.db` file — perfect for this scale |
| **Google Gemini AI** | AI recommendations | State-of-the-art LLM, simple `google-genai` SDK, free tier for students |
| **Jinja2** | HTML templating | Flask built-in, clean logic/UI separation, dynamic rendering |
| **Gunicorn** | WSGI server | Production-grade Python server, required by Render.com |
| **Render.com** | Cloud hosting | Free tier, native Python/Flask support, Procfile-based deployment |

---

## ⭐ Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

##  Developers

Rupali Jain
Sayar Sekhar Ghosh
