# """Task 4 helper: creates a starter Jupyter notebook and README."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for folder in ("data", "notebooks", "reports", "src"):
    (ROOT / folder).mkdir(exist_ok=True)

README = """# Week 1 Assessment — Python & Data Engineering

## Setup
1. Create a virtual environment: `python -m venv .venv`
2. Activate it: Windows `.venv\\Scripts\\activate`; macOS/Linux `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run Task 1, Task 2, and Task 3 scripts separately.
5. Open `notebooks/week1_analysis.ipynb` in Jupyter.

## Findings
- The source dataset contains 8 employees across four departments.
- Five employees earn more than 50,000.
- IT has three employees and the highest average salary in the supplied data.
- Chennai employees are Arun, Priya, Divya, and Suresh.
- Marketing is listed as a department but has no employees.

## Git submission
Create branch `feature/analysis`, commit in small steps, open and merge a Pull Request,
resolve a deliberate README conflict, and capture `git log --oneline --graph`.
These GitHub account actions must be completed in your own repository.
"""
(ROOT / "README.md").write_text(README, encoding="utf-8")
(ROOT / "requirements.txt").write_text(
    "requests\npython-dotenv\npandas\nmatplotlib\nnumpy\nnotebook\nnbconvert\nnbformat\n",
    encoding="utf-8",
)
(ROOT / ".gitignore").write_text(
    ".env\n.venv/\n__pycache__/\n.ipynb_checkpoints/\n*.pyc\n", encoding="utf-8"
)

try:
    import nbformat as nbf
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("# Week 1 Assessment Analysis\n\n## Load and inspect employee data"),
        nbf.v4.new_code_cell("import pandas as pd\ndf = pd.read_csv('../data/employees.csv')\ndf.info()\ndf.describe()"),
        nbf.v4.new_markdown_cell("## Department summary"),
        nbf.v4.new_code_cell("df.groupby('department').agg(headcount=('id','count'), average_salary=('salary','mean'), maximum_salary=('salary','max'))"),
        nbf.v4.new_markdown_cell("## Timing example"),
        nbf.v4.new_code_cell("%timeit df['salary'].mean()"),
    ]
    nbf.write(nb, ROOT / "notebooks" / "week1_analysis.ipynb")
    print("Created notebooks/week1_analysis.ipynb")
except ImportError:
    print("Install nbformat to generate the notebook.")
print("Created README.md, requirements.txt, .gitignore and project folders.")
print("Finish the GitHub branch, commits, PR, merge, and screenshot manually.")
