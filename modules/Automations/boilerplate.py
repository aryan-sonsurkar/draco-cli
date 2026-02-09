import os
from datetime import date

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

    <h1>{project}</h1>
    <p>Project initialized by Draco.</p>

</body>
</html>
"""

CSS_TEMPLATE = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
}
"""

README_TEMPLATE = """# {project}

 Project generated using **Draco**

## Tech Stack
- HTML
- CSS

## Created On
{date}
"""

def create_web_project(name):
    if os.path.exists(name):
        return "Project already exists."

    os.makedirs(f"{name}/css")
    os.makedirs(f"{name}/assets")

    with open(f"{name}/index.html", "w") as f:
        f.write(HTML_TEMPLATE.format(project=name))

    with open(f"{name}/css/style.css", "w") as f:
        f.write(CSS_TEMPLATE)

    with open(f"{name}/README.md", "w") as f:
        f.write(README_TEMPLATE.format(
            project=name,
            date=date.today()
        ))

    with open(f"{name}/.gitignore", "w") as f:
        f.write("node_modules/\n.env\n")

    return f"Web project '{name}' created successfully."


def create_python_project(name):
    if os.path.exists(name):
        return "Project already exists."

    os.makedirs(name)

    with open(f"{name}/main.py", "w") as f:
        f.write("# Entry point\n")

    with open(f"{name}/README.md", "w") as f:
        f.write(f"# {name}\n\nGenerated using Draco.\n")

    return f"Python project '{name}' created successfully."
