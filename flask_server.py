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
    #flag = True
    if request.method == 'POST':
        uid = request.form['id']
        data =list(mongo.db.Colection_examp_produc.find({'name':{'$regex': uid, '$options':'i'}}))
        if data:
            print ('found by name')
            return render_template('show.html', data=data) 
        elif not data:
            data = list(mongo.db.Colection_examp_produc.find({'_id':{'$regex': uid}}))
            if data:
                print('found by id')
                return render_template('show.html', data=data)
            else:
                return render_template('not found.html')
            
            

    
                

    else:
        return render_template('start.html')


@prueba.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        uid = request.form['uid']
        name = request.form['name']

        mongo.db.Colection_examp_produc.insert_one({'_id': uid, 'name': name })

        data = mongo.db.Colection_examp_produc.find_one({'_id': uid})
        return redirect(url_for('add', uid=data['_id'], name=data['name']))
    else:
        return render_template('create.html')


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
        #TODO
        #A ver que pex aqui... :'D
        mongo.db.Colection_examp_produc.update_one({'_id': uid}, {'$set': {'sistema.'+index2+'.modelo': model,
                                                                         'sistema.'+index2+'.tipo': devType,
                                                                         'sistema.'+index2+'.serie': serial,
                                                                         'sistema.'+index2+'.sysName': sysName,
                                                                         'sistema.'+index2+'.ubicacion': location,
                                                                         'sistema.'+index2+'.ambiente': env,
                                                                         'sistema.'+index2+'.config': config,
                                                                         'sistema.'+index2+'.os': os},
                                                    
                                                                        }
                                               # {arrayFilters:index,upsert:False}
                                               )
        return redirect(url_for('read', uid=uid))
    else:
        data = mongo.db.Colection_examp_produc.find_one({'_id': uid})
        return render_template('update.html', data=data, sistema=index1)


@prueba.route('/delete')
def delete():
    return 0


if __name__ == "__main__":
    prueba.run(host='127.0.0.1', port=80, debug=True)
