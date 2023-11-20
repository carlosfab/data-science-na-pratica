# importar os pacotes necessários
import numpy as np
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from joblib import load

# instanciar Flask object
app = Flask(__name__)

# api
api = Api(app)

# carregar modelo
model = load('model/model.joblib')


class PrecoImoveis(Resource):
    def get(self):
        return {'Nome': 'Carlos Melo'}

    def post(self):
        args = request.get_json(force=True)
        input_values = np.asarray(list(args.values())).reshape(1, -1)
        predict = model.predict(input_values)[0]

        return jsonify({'previsao': float(predict)})


api.add_resource(PrecoImoveis, '/')


if __name__ == '__main__':
    app.run()