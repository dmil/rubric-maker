# Rubric Maker
Talk to AI, Make Rubric, Upload to CourseWorks

## Setup

1.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
2.  Create a `.env` file in the root directory.
3.  Add your environment variables to the `.env` file:

    ```
    CANVAS_ACCESS_TOKEN=your_canvas_access_token
    CANVAS_SUBDOMAIN=your_canvas_subdomain
    CANVAS_COURSE_ID=your_canvas_course_id
    # Optionally, add CANVAS_ASSIGNMENT_ID if you want to attach the rubric to a specific assignment
    ```
4.  Edit `rubric.json` to define your rubric criteria and ratings.  
    The file should be a JSON array of criterion objects. See the provided `rubric.json` for an example structure.
5.  Run the application:

    ```bash
    python make-rubric.py
    ```

## Environment Variables

The application uses the following environment variables, which should be defined in a `.env` file:

-   `CANVAS_ACCESS_TOKEN`: Your Canvas API access token.
-   `CANVAS_SUBDOMAIN`: The Canvas subdomain for your institution (e.g., `courseworks2.columbia.edu`).
-   `CANVAS_COURSE_ID`: The Canvas course ID.
-   `CANVAS_ASSIGNMENT_ID` (optional): The Canvas assignment ID to attach the rubric to.

## Rubric Definition

Rubric criteria and ratings are defined in `rubric.json`.  
Each criterion should include a description, long description, points, criterion_use_range, and a list of ratings.  
Each rating should include a description, points, and long description.

Example structure:

```json
[
  {
    "description": "Criterion Title",
    "long_description": "Detailed explanation.",
    "points": 3,
    "criterion_use_range": false,
    "ratings": [
      {
        "description": "Excellent",
        "points": 3,
        "long_description": ""
      },
      {
        "description": "Needs Improvement",
        "points": 2,
        "long_description": ""
      },
      {
        "description": "Unacceptable",
        "points": 0,
        "long_description": ""
      }
    ]
  }
]
```

Edit `rubric.json` to match your grading needs before running the script.