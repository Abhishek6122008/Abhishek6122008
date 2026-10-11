"""Everything personal lives here. Edit this file, re-run `python scripts/render_all.py`."""

USERNAME = "Abhishek6122008"
NAME = "Abhishek Chaudhary"
PROMPT_USER = "abhishek"
PROMPT_HOST = "github"
LEETCODE_USER = "Abhi_1905"
# Left out of the language bar: notebook bytes are mostly saved output, CMake is Flutter scaffolding
HIDE_LANGS = ["Jupyter Notebook", "CMake"]

# Cycled by the typing animation in header.svg
ROLES = [
    "Java Developer",
    "Flutter Developer · Liquid Galaxy",
    "Open Source @ Apache Fineract",
    "DSA Enthusiast · 300+ LeetCode problems",
    "Building consistency, every day",
]

TAGLINE = "Gurgaon, IN  ·  Java, Flutter & a daily dose of DSA"

# neofetch-style rows on info-card.svg. "{...}" placeholders are filled from live data.
INFO_ROWS = [
    ("Role", "Java · Flutter Developer"),
    ("Now", "Flutter apps for Liquid Galaxy"),
    ("OSS", "Apache Fineract · Apicurio Registry"),
    ("Uptime", "{uptime} on GitHub"),
    ("Langs", "{top_langs}"),
    ("Backend", "Java · Spring Boot · Redis"),
    ("Mobile", "Flutter · Dart · Firebase"),
    ("ML", "Python · Jupyter · Deep Learning"),
    ("LeetCode", "{lc_solved} solved  ·  {lc_rating} contest rating"),
    ("Repos", "{public_repos} public  ·  {stars} stars"),
    ("Streak", "{current_streak}d current  ·  {longest_streak}d best"),
    ("Hobbies", "Code · Gym · Books"),
]

# globe.svg: home pin + arcs to the open-source projects you contribute to (lat, lon)
HOME = ("Gurgaon", 28.46, 77.03)
GLOBE_CMD = "./open-source --from gurgaon"

REGIONS = [
    ("Apache Fineract", 39.74, -75.55),
    ("Apicurio", 35.78, -78.64),
    ("Liquid Galaxy", 41.62, 0.62),
]
# tech-sphere.svg: category -> labels (each category gets its own colour)
TECH = {
    "languages": ["Java", "Dart", "Python", "C++", "JavaScript"],
    "mobile": ["Flutter", "Firebase", "Liquid Galaxy", "KML"],
    "backend": ["Spring Boot", "Redis", "REST APIs", "Postman"],
    "ml": ["Jupyter", "Deep Learning", "Gemini"],
    "tools": ["Git", "GitHub Actions", "Linux", "Docker"],
}
