from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/getRecommended')
def hello_world():
    return jsonify({'movies': ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Inception', 'The Dark Knight Rises'  ]  })

# @app.route('likeMovie/<movie_id>')
# def like_movie():
#     id = request.params.get('movie_id')
#     return jsonify({'movies': ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Inception', 'The Dark Knight Rises'  ]  })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
