import functions
# Errors pages
errors = {
        404: "errors/404.html"
        }
# Indexed pages
predefined = {
        "index": "index.html",
        "list-dir": "predef/list.html"
        }
# Makes pages more dynamics ( in this example, the string '{{test}}' is remplaced by the return of the function plus from the functions.py )
files = {
        "index.html": {"test": functions.plus()}
        }
