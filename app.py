from flask import Flask, jsonify, request, render_template
import pandas as pd
import math
import pickle


app = Flask(__name__)
#Loads frame for the model input
with open('frame', 'rb') as f:
    frame = pickle.load(f)
#laods model
with open('model', 'rb') as f:
    pred_model = pickle.load(f)

columns = frame.columns
columns_old=["year", "km"] + [i for i in range(1081)]
dictionary = dict(zip(columns, columns_old))

X = frame.append(pd.DataFrame({'year':[2021], "km":[20000], "brand_Audi":[1]})).fillna(0)

X = X.rename(columns=dictionary)

print(X.head())
preds = pred_model.predict(X)


brand = [s for s in frame if "brand" in s]
model = [s for s in frame if "model" in s]
colour = [s for s in frame if "colour" in s]
fuel = [s for s in frame if "fuel" in s]
engine = [s for s in frame if "engine" in s]
transmision = [s for s in frame if "transmision" in s]
cartype = [s for s in frame if "type" in s]
city = [s for s in frame if "city" in s]


features_dict={'brand':brand, 'model':model, 'colour':colour, 'fuel':fuel, 'engine':engine, 'transmision':transmision, 'type':cartype, 'city':city}



list_all = [i for i in frame.columns]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars', methods=['GET'])
def cars():
    return jsonify({"all":list_all})

@app.route('/predict', methods=['GET'])
def carpredict():
    return jsonify({"pred":preds[0]})

# allow both GET and POST requests
@app.route('/input', methods=['GET', 'POST'])
def input():
# handle the POST request
    if request.method == 'POST':
        km = request.form.get('km')
        year = request.form.get('year')
        brand = request.form.get('brand')
        model = request.form.get('model')
        colour = request.form.get('colour')
        fuel = request.form.get('fuel')
        engine = request.form.get('engine')
        transmision = request.form.get('transmision')
        cartype = request.form.get('type')
        city = request.form.get('city')

        X = frame.append(pd.DataFrame({'year':year, "km":km, brand:[1], colour:[1], model:[1], fuel:[1], engine:[1], transmision:[1], cartype:[1], city:[1]})).fillna(0)

        X = X.rename(columns=dictionary)

        preds = pred_model.predict(X)
        return '''
                  <h1 class="content">The value is: {} $ARS</h1>'''.format(int(preds[0]))


    if request.method == 'GET':
        return render_template('default.html', brand=features_dict['brand'], model=features_dict['model'], colour=features_dict['colour'], fuel=features_dict['fuel'], engine=features_dict['engine'], transmision=features_dict['transmision'], cartype=features_dict['type'], city=features_dict['city'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)