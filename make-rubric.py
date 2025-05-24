import requests
from dotenv import load_dotenv
import os
import json

# ─── LOAD CREDENTIALS ───────────────────────────────────────────────────────────
load_dotenv()
API_TOKEN   = os.getenv("CANVAS_ACCESS_TOKEN")
SUBDOMAIN   = os.getenv("CANVAS_SUBDOMAIN")           # e.g. courseworks2.columbia.edu
COURSE_ID   = os.getenv("CANVAS_COURSE_ID")           # string or int is fine
ASSIGNMENT_ID = os.getenv("CANVAS_ASSIGNMENT_ID")     # optional; leave blank to create
                                                     # rubric at course level only
BASE_URL = f"https://{SUBDOMAIN}/api/v1"
HEADERS  = {"Authorization": f"Bearer {API_TOKEN}"}

# ─── LOAD RUBRIC FROM JSON FILE ────────────────────────────────────────────────
with open("rubric.json", "r", encoding="utf-8") as f:
    rubric = json.load(f)

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
