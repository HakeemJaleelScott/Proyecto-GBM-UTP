import os
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

prueba = Flask(__name__)
# prueba.debug = True
prueba.config['MONGO_URI'] = 'mongodb://localhost:27017/prueba'
mongo = PyMongo(prueba)


"""We then use the route() decorator to tell Flask what URL should trigger our function.
establece la ruta dentro del servidor donde consultar la data
"""


@prueba.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        uid = request.form['id']
        try:
           data = mongo.db.Colection_examp_produc.find_one({'_id': uid})
           return redirect(url_for('read', uid=data['_id']))

        except:
            # data = mongo.db.Colection_examp_produc.find_one({'name':{'$regex': uid}})
            data =list(mongo.db.Colection_examp_produc.find({'name':{'$regex': uid, '$options':'i'}}))
            for i in data:
                print(i)
            return render_template('show.html', data=data)

             #return redirect(url_for('create', user=uid))

    else:
        return render_template('start.html')


@prueba.route('/create/<user>', methods=['POST', 'GET'])
def create(user):
    if request.method == 'POST':
        uid = user
        name = request.form['name']
        model = request.form['model']
        devType = request.form['devType']
        serial = request.form['serial']
        sysName = request.form['sysName']
        location = request.form['location']
        env = request.form['env']
        config = request.form['config']
        os = request.form['os']

        mongo.db.Colection_examp_produc.insert_one({'_id': uid, 'name': name,
                                                    'sistema': [{'modelo': model,
                                                                 'tipo': devType,
                                                                 'serie': serial,
                                                                 'sysName': sysName,
                                                                 'ubicacion': location,
                                                                 'ambiente': env,
                                                                 'config': config,
                                                                 'os': os}]
                                                    })

        data = mongo.db.Colection_examp_produc.find_one({'_id': uid})
        return redirect(url_for('add', uid=data['_id'], name=data['name']))
    else:
        return render_template('create.html', uid=user)


@prueba.route('/add/<uid>/<name>', methods=['POST', 'GET'])
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

        mongo.db.Colection_examp_produc.update({'_id': uid}, {'$push': {'sistema':
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


@prueba.route('/read/<uid>', methods=['POST', 'GET'])
def read(uid):
    if request.method == 'POST':
        uid = request.form['id']
        data = mongo.db.Colection_examp_produc.find_one({'_id': uid})

        return render_template('read.html', data=data)

    else:
        data = mongo.db.Colection_examp_produc.find_one({'_id': uid})
        return render_template('read.html', data=data)


@prueba.route('/build')
def build():
    return render_template('EUREKA.html')


@prueba.route('/update/<uid>/<index>', methods=['POST', 'GET'])
def update(uid, index):
    
    index = int(index)
    if request.method == 'POST':
        model = request.form['model']
        devType = request.form['devType']
        serial = request.form['serial']
        sysName = request.form['sysName']
        location = request.form['location']
        env = request.form['env']
        config = request.form['config']
        os = request.form['os'] 
        #TODO
        #A ver que pex aqui... :'D
        mongo.db.Colection_examp_produc.update_one({'_id': uid}, {'$set': {'sistema':
                                                                        {'modelo': model,
                                                                         'tipo': devType,
                                                                         'serie': serial,
                                                                         'sysName': sysName,
                                                                         'ubicacion': location,
                                                                         'ambiente': env,
                                                                         'config': config,
                                                                         'os': os},
                                                    
                                                                        }
                                                              },
                                               # {arrayFilters:index,upsert:False}
                                               )
        return redirect(url_for('read', uid=uid))
    else:
        data = mongo.db.Colection_examp_produc.find_one({'_id': uid})
        return render_template('update.html', data=data, sistema=index)


@prueba.route('/delete')
def delete():
    return 0


if __name__ == "__main__":
    prueba.run(host='127.0.0.1', port=80, debug=True)
