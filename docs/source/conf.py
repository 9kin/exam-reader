pygments_style = 'sphinx'

extensions = ["sphinx.ext.autodoc", "sphinx_autodoc_typehints"]
html_theme = "alabaster"
html_theme_options = {
    "description": "exam-reader",
    "github_user": "9kin",
    "github_repo": "exam-reader",
    "github_button": True,
    "github_type": "star",
    "github_banner": True,
}

project = "exam-reader"
copyright = "2020, 9kin"
author = "9kin"

extensions = []
# templates_path = ["_templates"]
# exclude_patterns = []
html_static_path = ["static"]
# html_theme_options = {"logo_only": True}
