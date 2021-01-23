import datetime

from flask import Flask, render_template, request


# Configure application
app = Flask(__name__)

# The homepage
@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

# The about page
@app.route("/about")
def about():
    """Show about us section"""
 
    return render_template("about.html")

@app.route('/test_form')
def test_form():

    return render_template('test_form.html')

@app.route('/data', methods=['POST'])
def data():
    # get data from the test HTML form, at URL /test_form, sending data to /data, with name="form_name"
    # how to display/do something useful with this?
    print("This is the python output of the form you just filled in. Will make it so it doesn't automatically go to this page")
    print("Your input was:")
    input = request.form['form_name']
    print(input)
    return input
    


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
