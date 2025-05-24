import requests
from dotenv import load_dotenv
import os

# ─── LOAD CREDENTIALS ───────────────────────────────────────────────────────────
load_dotenv()
API_TOKEN   = os.getenv("CANVAS_ACCESS_TOKEN")
SUBDOMAIN   = os.getenv("CANVAS_SUBDOMAIN")           # e.g. courseworks2.columbia.edu
COURSE_ID   = os.getenv("CANVAS_COURSE_ID")           # string or int is fine
ASSIGNMENT_ID = os.getenv("CANVAS_ASSIGNMENT_ID")     # optional; leave blank to create
                                                     # rubric at course level only
BASE_URL = f"https://{SUBDOMAIN}/api/v1"
HEADERS  = {"Authorization": f"Bearer {API_TOKEN}"}

# ─── RUBRIC DEFINITION (✱ THIS IS THE ONLY PART THAT CHANGED) ──────────────────
rubric = [
    {
        "description": "Story Potential",
        "long_description": "Is the idea newsworthy, original, and compelling?",
        "points": 3,
        "criterion_use_range": False,
        "ratings": [
            {
                "description": "✅ / 🤯 Strong, original, timely story idea",
                "points": 3,
                "long_description": ""
            },
            {
                "description": "⚠ / 🤔 Some story potential; needs sharper focus, relevance, or originality",
                "points": 2,
                "long_description": ""
            },
            {
                "description": "⛔ Story idea is weak, stale, or not clearly connected to real-world issues",
                "points": 0,
                "long_description": ""
            }
        ]
    },
    {
        "description": "Use of Data",
        "long_description": "Has the regression meaningfully informed the story idea or the reporter’s thinking?",
        "points": 3,
        "criterion_use_range": False,
        "ratings": [
            {
                "description": "✅ / 🤯 Thoughtful connection between analysis and story development",
                "points": 3,
                "long_description": ""
            },
            {
                "description": "⚠ / 🤔 Connection between analysis and story is weak, vague, or unclear",
                "points": 2,
                "long_description": ""
            },
            {
                "description": "⛔ Misinterpretation of regression; major misunderstanding of the data",
                "points": 0,
                "long_description": ""
            }
        ]
    },
    {
        "description": "Next Steps",
        "long_description": "Is there a clear plan for strengthening the analysis or further developing the reporting?",
        "points": 3,
        "criterion_use_range": False,
        "ratings": [
            {
                "description": "✅ / 🤯 Clear and thoughtful next steps outlined",
                "points": 3,
                "long_description": ""
            },
            {
                "description": "⚠ / 🤔 Plan is vague, thin, or missing important elements",
                "points": 2,
                "long_description": ""
            },
            {
                "description": "⛔ No awareness of what still needs work; missing critical steps",
                "points": 0,
                "long_description": ""
            }
        ]
    },
    {
        "description": "Clarity and Writing",
        "long_description": "Is the pitch clear, logical, easy to understand, and professional?",
        "points": 3,
        "criterion_use_range": False,
        "ratings": [
            {
                "description": "✅ / 🤯 Clear, engaging, appropriate writing for journalism",
                "points": 3,
                "long_description": ""
            },
            {
                "description": "⚠ / 🤔 Writing is somewhat unclear, unfocused, or too technical",
                "points": 2,
                "long_description": ""
            },
            {
                "description": "⛔ Pitch is confusing, sloppy, or inappropriate in tone",
                "points": 0,
                "long_description": ""
            }
        ]
    }
]

# ─── BUILD FORM-ENCODED PAYLOAD ────────────────────────────────────────────────
rubric_payload = {
    "rubric[title]": "Data Journalism Pitch Rubric (Emoji Version)",
    "rubric[free_form_criterion_comments]": "true",
    "rubric_association[association_type]": "Assignment" if ASSIGNMENT_ID else "Course",
    "rubric_association[association_id]": ASSIGNMENT_ID or COURSE_ID,
}

for idx, criterion in enumerate(rubric):
    rubric_payload[f"rubric[criteria][{idx}][description]"]       = criterion["description"]
    rubric_payload[f"rubric[criteria][{idx}][long_description]"]  = criterion["long_description"]
    rubric_payload[f"rubric[criteria][{idx}][points]"]            = criterion["points"]
    rubric_payload[f"rubric[criteria][{idx}][criterion_use_range]"] = str(criterion["criterion_use_range"]).lower()

    for r_idx, rating in enumerate(criterion["ratings"]):
        rubric_payload[f"rubric[criteria][{idx}][ratings][{r_idx}][description]"]      = rating["description"]
        rubric_payload[f"rubric[criteria][{idx}][ratings][{r_idx}][points]"]           = rating["points"]
        rubric_payload[f"rubric[criteria][{idx}][ratings][{r_idx}][long_description]"] = rating["long_description"]

# ─── API CALL ──────────────────────────────────────────────────────────────────
resp = requests.post(
    f"{BASE_URL}/courses/{COURSE_ID}/rubrics",
    headers=HEADERS,
    data=rubric_payload
)

if resp.status_code in (200, 201):
    created = resp.json()
    print(f"✅ Rubric created! Canvas rubric ID: {created['rubric']['id']}")
    if ASSIGNMENT_ID:
        print(f"   (Attached to assignment {ASSIGNMENT_ID})")
else:
    print("⛔ Failed to create rubric:")
    print(resp.status_code, resp.text)
