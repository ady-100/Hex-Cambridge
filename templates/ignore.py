from bottle import Bottle, template, request

app = Bottle()

@app.route('/', method="POST")
def formhandler():
    """Handle the form submission"""

    email = request.forms.get('email')
    query = request.forms.get('query')

    message = "Hello, thank you for your query: " + first + "  We will get back to you shortly at " + last + "."

    return template("contact.html", message=message)
