from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/ignore.py', methods=['GET', 'POST'])
def hello():
    return render_template('contact.html', say=request.form['email'], to=request.form['query'])

if __name__ == "__main__":
    app.run()
