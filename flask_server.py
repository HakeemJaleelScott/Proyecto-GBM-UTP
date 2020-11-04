import os
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
# app.debug = True
app.config['MONGO_URI'] = 'mongodb://localhost:27017/GBM'
mongo = PyMongo(app)


"""We then use the route() decorator to tell Flask what URL should trigger our function.
establece la ruta dentro del servidor donde consultar la data
"""


@app.route('/', methods=['POST', 'GET'])
def home():
    #flag = True
    if request.method == 'POST':
        uid = request.form['id']
        data =list(mongo.db.ClientesPA.find({'name':{'$regex': uid, '$options':'i'}}))
        if data:
            print ('found by name')
            return render_template('show.html', data=data) 
        elif not data:
            data = list(mongo.db.ClientesPA.find({'_id':{'$regex': uid}}))
            if data:
                print('found by id')
                return render_template('show.html', data=data)
            else:
                return render_template('not found.html')
            
            

    
                

    else:
        return render_template('start.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        uid = request.form['id']
        name = request.form['name']

        mongo.db.ClientesPA.insert_one({'_id': uid, 'name': name })

        #mongo.db.ClientesPA.find_one({'_id': uid})
        return redirect(url_for('create'))
    else:
        return render_template('create.html')


@app.route('/add/<uid>/<name>', methods=['POST', 'GET'])
def add(uid, name):
    if request.method == 'POST':
        uid = uid
        name = name
        model = request.form['model']
        devType = request.form['devType']
        serial = request.form['serial']
        sysName = request.form['sysName']
        location = request.form['location']
        env = request.form['env']
        config = request.form['config']
        os = request.form['os']

        mongo.db.ClientesPA.update({'_id': uid}, {'$push': {'HW':
                                                                        {'modelo': model,
                                                                         'tipo': devType,
                                                                         'serie': serial,
                                                                         'sysName': sysName,
                                                                         'ubicacion': location,
                                                                         'ambiente': env,
                                                                         'config': config,
                                                                         'os': os}

                                                                        }
                                                              }
                                               )
        return redirect(url_for('add', uid=uid, name=name))

    else:
        return render_template('add.html', uid=uid, name=name)

@app.route('/addsw/<uid>/<name>', methods=['POST', 'GET'])
def addsw(uid, name):
    if request.method == 'POST':
        uid = uid
        name = name
        plataforma = request.form['plataforma']
        version = request.form['version']
        SO = request.form['SO']
        solucion = request.form['solucion']
        

        mongo.db.ClientesPA.update({'_id': uid}, {'$push': {'SW':
                                                                        {'plataforma': plataforma,
                                                                         'version': version,
                                                                         'SO': SO,
                                                                         'solucion': solucion}

                                                                        }
                                                              }
                                               )
        return redirect(url_for('addsw', uid=uid, name=name))

    else:
        return render_template('addsw.html', uid=uid, name=name)

@app.route('/read/<uid>', methods=['POST', 'GET'])
def read(uid):
    if request.method == 'POST':
        uid = request.form['id']
        data = mongo.db.ClientesPA.find_one({'_id': uid})

        return render_template('read.html', data=data)

    else:
        data = mongo.db.ClientesPA.find_one({'_id': uid})
        return render_template('read.html', data=data)


@app.route('/build')
def build():
    return render_template('addsw.html')


@app.route('/update/<uid>/<index>', methods=['POST', 'GET'])
def update(uid, index):
    
    index1 = int(index)
    index2= str(index)
    if request.method == 'POST':
        model = request.form['model']
        devType = request.form['devType']
        serial = request.form['serial']
        sysName = request.form['sysName']
        location = request.form['location']
        env = request.form['env']
        config = request.form['config']
        os = request.form['os'] 
        index
    
        mongo.db.ClientesPA.update_one({'_id': uid}, {'$set': {'HW.'+index2+'.modelo': model,
                                                                         'HW.'+index2+'.tipo': devType,
                                                                         'HW.'+index2+'.serie': serial,
                                                                         'HW.'+index2+'.sysName': sysName,
                                                                         'HW.'+index2+'.ubicacion': location,
                                                                         'HW.'+index2+'.ambiente': env,
                                                                         'HW.'+index2+'.config': config,
                                                                         'HW.'+index2+'.os': os},
                                                    
                                                                        }
                                               )
        return redirect(url_for('read', uid=uid))
    else:
        data = mongo.db.ClientesPA.find_one({'_id': uid})
        return render_template('update.html', data=data, HW=index1)


@app.route('/delete')
def delete():
    return 0


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
