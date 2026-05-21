import re

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


# ─── TEXT EXTRACTION ────────────────────────────────────────────────────────

def extract_text(file_path):
    text = ""
    lower_path = file_path.lower()

    if lower_path.endswith('.pdf') and HAS_PYPDF2:
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"
        except Exception as e:
            print(f"[PDF Error] {e}")

    elif lower_path.endswith('.docx') and HAS_DOCX:
        try:
            doc = DocxDocument(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"[DOCX Error] {e}")

    elif lower_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"[TXT Error] {e}")

    return text


# ─── CATEGORY DEFINITIONS ───────────────────────────────────────────────────

JOB_CATEGORIES = {
    "Software Engineering": [
        "java", "c++", "c#", "python", "oop", "data structures", "algorithms",
        "software engineer", "system design", "debugging", "git", "github",
        "version control", "problem solving", "coding", "object oriented",
        "agile", "scrum", "junit", "unit testing", "microservices"
    ],
    "Web Development": [
        "html", "css", "javascript", "react", "angular", "vue", "django",
        "flask", "node", "express", "bootstrap", "frontend", "backend",
        "full stack", "api", "rest", "web developer", "responsive design",
        "typescript", "webpack", "graphql", "next.js", "tailwind"
    ],
    "Data Science": [
        "machine learning", "data science", "deep learning", "nlp", "pandas",
        "numpy", "matplotlib", "tensorflow", "keras", "scikit", "statistics",
        "data analysis", "data visualization", "model training", "regression",
        "classification", "clustering", "pytorch", "jupyter", "sql", "bigquery"
    ],
    "UI/UX Design": [
        "figma", "ui design", "ux design", "user interface", "user experience",
        "wireframe", "prototype", "mockup", "adobe xd", "sketch",
        "usability", "interaction design", "design system", "visual design",
        "user research", "information architecture", "zeplin", "invision"
    ],
    "Mechanical Engineering": [
        "mechanical", "mechanical engineer", "autocad", "solidworks", "catia",
        "ansys", "manufacturing", "cnc", "lathe", "thermodynamics",
        "fluid mechanics", "heat transfer", "production", "design engineer",
        "machine design", "cad", "cam", "fea", "maintenance", "tooling"
    ],
    "Electrical Engineering": [
        "electrical", "circuit", "power systems", "transformer",
        "control systems", "plc", "scada", "electronics",
        "voltage", "current", "wiring", "substation", "matlab", "embedded"
    ],
    "Civil Engineering": [
        "civil", "construction", "structural", "site engineer",
        "autocad civil", "surveying", "concrete", "estimation",
        "building", "infrastructure", "project management", "staad"
    ],
    "Cyber Security": [
        "cyber security", "network security", "penetration testing",
        "ethical hacking", "kali linux", "firewall", "encryption",
        "vulnerability", "security analyst", "siem", "soc", "ids", "ips"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "devops",
        "ci/cd", "jenkins", "linux", "shell scripting", "cloud computing",
        "deployment", "terraform", "ansible", "monitoring", "helm"
    ],
    "Mobile Development": [
        "android", "ios", "flutter", "react native", "mobile app",
        "kotlin", "swift", "app development", "firebase", "xcode"
    ],
    "Supply Chain Management": [
        "supply chain", "logistics", "procurement", "inventory", "warehouse",
        "distribution", "vendor management", "supply planning", "demand planning",
        "erp", "sap", "operations", "shipment", "freight", "transportation",
        "material management", "stock control", "purchasing", "lean", "six sigma"
    ],
    "BPO / Customer Support": [
        "bpo", "call center", "customer support", "customer service",
        "voice process", "non voice process", "inbound", "outbound",
        "telecalling", "crm", "client handling", "email support",
        "chat support", "ticketing system", "service desk", "technical support"
    ],
}

RESUME_SIGNALS = [
    "education", "experience", "skills", "projects", "resume", "summary",
    "objective", "certification", "internship", "employment", "qualification",
    "achievement", "profile", "career", "work history"
]


# ─── ANALYSIS FUNCTIONS ─────────────────────────────────────────────────────

def is_resume(text):
    lower = text.lower()
    return sum(1 for w in RESUME_SIGNALS if w in lower) >= 2


def predict_category(text):
    lower = text.lower()
    best_match = "General"
    max_count = 0
    all_scores = {}

    for category, keywords in JOB_CATEGORIES.items():
        count = sum(1 for word in keywords if word in lower)
        all_scores[category] = count
        if count > max_count:
            max_count = count
            best_match = category

    total_kw = len(JOB_CATEGORIES.get(best_match, []))
    match_pct = round((max_count / total_kw) * 100) if total_kw > 0 else 0
    match_pct = min(match_pct, 100)

    return best_match, match_pct, all_scores


def extract_skills(text):
    lower = text.lower()
    skills_found = []
    for keywords in JOB_CATEGORIES.values():
        for skill in keywords:
            if skill in lower and skill not in skills_found:
                skills_found.append(skill)
    return skills_found


def missing_skills(text, category):
    lower = text.lower()
    required = JOB_CATEGORIES.get(category, [])
    return [skill for skill in required if skill not in lower]


def keyword_match(text, keywords):
    lower = text.lower()
    matched = [kw for kw in keywords if kw.lower() in lower]
    missing = [kw for kw in keywords if kw.lower() not in lower]
    score = round((len(matched) / len(keywords)) * 100) if keywords else 100
    return matched, missing, score


def full_analysis(text, hr_keywords=None, category_filter=None):
    """Run complete resume analysis and return structured result dict."""
    category, match_pct, all_scores = predict_category(text)
    skills = extract_skills(text)
    missing = missing_skills(text, category)

    result = {
        'category': category,
        'match_pct': match_pct,
        'all_scores': all_scores,
        'skills': skills,
        'missing': missing[:8],
        'is_resume': is_resume(text),
    }

    if hr_keywords:
        kw_matched, kw_missing, kw_score = keyword_match(text, hr_keywords)
        # Weighted final score: 60% category match + 40% keyword match
        if category_filter and category != category_filter:
            adj_match = max(0, match_pct - 20)
        else:
            adj_match = match_pct
        final_score = round((adj_match * 0.6) + (kw_score * 0.4))
        result.update({
            'kw_matched': kw_matched,
            'kw_missing': kw_missing,
            'kw_score': kw_score,
            'final_score': final_score,
        })
    else:
        result['final_score'] = match_pct

    return result
