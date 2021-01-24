from bottle import Bottle, template, request

app = Bottle()

@app.route('/', method="POST")
def formhandler():
    """Handle the form submission"""

    first = request.forms.get('first')
    last = request.forms.get('last')

    message = "Hello " + first + " " + last + "."

    return template("form.tpl", message=message)
