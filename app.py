from flask import Flask, request, make_response,render_template
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # Add your logic here
    return render_template('GPCE-frontend.html')




if __name__ == '__main__':
     app.run(debug=True)