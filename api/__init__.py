from flask import Flask
from api.days import solutions_blueprint

app = Flask(__name__)


@app.route('/')
def hello_world():
    return {
        "test": "hello-world"
    }


app.register_blueprint(solutions_blueprint, url_prefix='/days')

if __name__ == '__main__':
    app.run()
