import os, json
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

prueba= Flask (__name__)
#prueba.debug = True
prueba.config['MONGO_URI']= 'mongodb://localhost:27017/prueba'
mongo = PyMongo(prueba)





"""We then use the route() decorator to tell Flask what URL should trigger our function.
establece la ruta dentro del servidor donde consultar la data
"""





@prueba.route('/', methods= ['POST', 'GET'])
def home():
    if request.method=='POST':
        uid =request.form ['id']
        try:
            data=mongo.db.Colection_examp_produc.find_one({'_id':uid})
            return redirect(url_for('add', uid=data['_id'],  name=data['name']))

        except:
            
            return redirect(url_for('create',user=uid))
    
   
    else:
        return render_template('start.html')

@prueba.route('/create/<user>',methods=['POST','GET'])
def create(user):
    if request.method == 'POST':
        uid= user
        name= request.form['name']
        model= request.form['model']
        devType= request.form['devType']
        serial= request.form['serial']
        sysName= request.form['sysName']
        location= request.form['location']
        env= request.form['env']        
        config= request.form['config']
        os= request.form['os']
        

        mongo.db.Colection_examp_produc.insert_one({'_id':uid, 'name':name,
                                                    'sistema':[{'modelo':model,
                                                               'tipo':devType,
                                                               'serie': serial,
                                                               'sysName':sysName,
                                                               'ubicacion':location,
                                                               'ambiente':env,
                                                               'config':config,
                                                               'os':os}]
                                                    })
        
        data=mongo.db.Colection_examp_produc.find_one({'_id':uid})
        return redirect(url_for('add', uid=data['_id'],name=data['name']))
    else:
        return render_template('create.html', uid=user) 
    
@prueba.route('/add/<uid>/<name>', methods= ['POST','GET'])
def add(uid, name):
    if request.method == 'POST':
        uid= uid
        name= name
        model= request.form['model']
        devType= request.form['devType']
        serial= request.form['serial']
        sysName= request.form['sysName']
        location= request.form['location']
        env= request.form['env']        
        config= request.form['config']
        os= request.form['os']
        

        mongo.db.Colection_examp_produc.update({'_id':uid},{'$push':{'sistema':
                                                                            {'modelo':model,
                                                                            'tipo':devType,
                                                                            'serie': serial,
                                                                            'sysName':sysName,
                                                                            'ubicacion':location,
                                                                            'ambiente':env,
                                                                            'config':config,
                                                                            'os':os}
                                                                                    
                                                                        }
                                                            }
                                               )
        return redirect(url_for('add', uid=uid, name=name))
                                                    
    else:
        return render_template('add.html', uid=uid,name=name) 

@prueba.route('/read', methods = ['POST','GET'])
def read():
    if request.method == 'POST':
        uid =request.form ['id']
        data=mongo.db.Colection_examp_produc.find_one({'_id':uid})

        return render_template('read.html',data=data)
    
    else:
        return render_template('start.html')

@prueba.route('/build')
def build():
    return render_template('EUREKA.html')
       
@prueba.route('/update')
def update():
    return 0

@prueba.route('/delete')
def delete():
    return 0

if __name__ == "__main__":
    prueba.run(host='127.0.0.1', port=80, debug= True)
