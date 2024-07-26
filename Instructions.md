# Instructions

## Running the server

1. Ensure Python is installed

2. Open terminal and navigate to the project directory.
This can be done by right clicking the contents of the folder and selecting `Open terminal here` on Windows.


3. Run the following commands in order (assuming OS is Windows):

```bash
py -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
```

If the second command fails, try:
`.venv\Scripts\activate.bat`
or
`.venv\Scripts\activate`

Then, for a single time, create the database using:
`python init_db.py`

To run the server, run: `flask --app api run`

To quit the server, tap Ctrl + C

## Paths

- All files (html, css, js) are to be placed in the `static/` folder
- All paths must be in the form `/static/{filename}`. For example, to link the css file `opt.css`, the `href` of `link` will be having the value `/static/opt.css`