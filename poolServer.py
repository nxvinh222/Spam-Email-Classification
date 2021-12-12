from flask import Flask, jsonify, request
import math
app = Flask(__name__)

pools = []


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works!'})


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    if len(pools) == 0:
        pools.append(data)
        return jsonify({"status": "inserted"})
    for index, pool in enumerate(pools):
        if data['poolId'] == pool['poolId']:
            pools[index]['poolValues'].extend(data['poolValues'])
            return jsonify({"status": "appended"})
        if index == len(pools) - 1:
            pools.append(data)
            return jsonify({"status": "inserted"})


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    poolValues = []
    for pool in pools:
        if data['poolId'] == pool['poolId']:
            poolValues = pool['poolValues']
    print(poolValues)
    poolValues.sort()
    index = len(poolValues)*data['percentile']/100
    if index.is_integer():
        quantile = (poolValues[index-1]+poolValues[index])/2
    else:
        quantile = poolValues[math.ceil(index)-1]
    return jsonify({'quantile': quantile, 'total': len(poolValues)})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
