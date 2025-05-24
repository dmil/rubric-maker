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
    ```
4.  Run the application.

## Environment Variables

The application uses the following environment variables, which should be defined in a `.env` file:

-   `CANVAS_ACCESS_TOKEN`: Your Canvas API access token.
-   `CANVAS_SUBDOMAIN`: The Canvas subdomain for your institution (e.g., `courseworks2.columbia.edu`).
-   `CANVAS_COURSE_ID`: The Canvas course ID.