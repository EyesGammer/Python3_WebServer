# Python3 WebServer
This is a simple webserver using Python3.

This project is using :
- threading
- sockets
- re _(Regular Expressions)_

## Files
- main.py : Run the main webserver

| Argument      | Abbreviation | Default   | Meaning                         |
| ------------- | ------------ | --------- | ------------------------------- |
| host          | h            | localhost | Host to access webserver        |
| port          | p            | 80        | Port to access webserver        |
| accept        | a            | 5         | Max number of clients at once   |
| show-requests | sr           | True      | Show received socket to console |
- settings.py :
  * predefined : Set HTML file rendered by the URL
  * errors : Errors HTML depending on HTTP error code
  * files : Use dynamic renderer for specified files
- functions.py : Functions that can be used for dnamic rendering
