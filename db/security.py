import re
import cgi

class Sanitisation:
    def isValidEmail(email):
        if re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return True
        else:
            return False

    def sanitise(string):
        return cgi.escape(string)
