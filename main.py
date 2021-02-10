from flask import Flask, request, Response, jsonify,render_template
from apscheduler.schedulers.background import BackgroundScheduler

import json
from json import JSONEncoder
import urllib.request

from flask import  redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc, func, text
from datetime import datetime
import os
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#'postgresql://postgres:root@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jknjknc6v468v86v354'

#port = int(os.environ["PORT"])

db = SQLAlchemy(app)
migrate = Migrate()
migrate.init_app(app, db)




class Telephone(db.Model):

    __tablename__ = 'telephone'
    id=db.Column(db.Integer, primary_key=True)
    marque =db.Column(db.String(60))
    modele=db.Column(db.String(60))
    description=db.Column(db.Text)
    prix= db.Column(db.Float)
    
    note_design=db.Column(db.Float)
    note_ap=db.Column(db.Float)
    note_connection=db.Column(db.Float)
    note_batterie=db.Column(db.Float)
    note_puissance=db.Column(db.Float)
    point=db.Column(db.Integer)
    occasion=db.Column(db.Integer)
    stock= db.Column(db.Integer)
    
    lien_photo=db.Column(db.Text)


    def __repr__(self):
        return '<telephone: {}>'.format(self.id)

class Forfait(db.Model):

    __tablename__ = 'forfait'
    id=db.Column(db.Integer, primary_key=True)
    type=db.Column(db.Integer)
    description=db.Column(db.Text)
    is_engagement=db.Column(db.Integer)
    zone=db.Column(db.String(60))
    giga_4g=db.Column(db.Integer)
    giga_5g=db.Column(db.Integer)
    description_complete=db.Column(db.Text)
    point=db.Column(db.Integer)
    prix= db.Column(db.Float)
    lien_photo=db.Column(db.Text)

    def __repr__(self):
        return '<forfait: {}>'.format(self.id)


class Utilisateur(db.Model):

    __tablename__ = 'utilisateur'
    id=db.Column(db.Integer, primary_key=True)
    numero_telephone=db.Column(db.String(60))
    siret = db.Column(db.String(60))
    telephone_actuel = db.Column(db.String(180))
    forfait_actuel= db.Column(db.String(180))
    nom =db.Column(db.String(60))
    prenom=db.Column(db.String(60))
    email=db.Column(db.String(60))
    metier=db.Column(db.String(100))


    def __repr__(self):
        return '<utilisateur: {}>'.format(self.id)

  


class Interaction(db.Model):

    __tablename__ = 'interaction'
    id=db.Column(db.Integer, primary_key=True)
    localisation =db.Column(db.String(100))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    id_utilisateur = db.Column(db.Integer)


    def __repr__(self):
        return '<interaction: {}>'.format(self.id)



class Panier(db.Model):

    __tablename__ = 'panier'
    id=db.Column(db.Integer, primary_key=True)
    statut =db.Column(db.String(60))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    id_utilisateur = db.Column(db.Integer)


    def __repr__(self):
        return '<panier: {}>'.format(self.id)



class Avis(db.Model):

    __tablename__ = 'avis'
    id=db.Column(db.Integer, primary_key=True)
    note =db.Column(db.Integer)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    id_interaction=db.Column(db.Integer)
    id_utilisateur = db.Column(db.Integer)


    def __repr__(self):
        return '<avis: {}>'.format(self.id)


class Panier_produit(db.Model):

    __tablename__ = 'panier_produit'
    id=db.Column(db.Integer, primary_key=True)
    id_produit = db.Column(db.Integer)
    type_produit = db.Column(db.String(60))
    nombre=db.Column(db.Integer)
    id_interaction=db.Column(db.Integer)
    via_bot = db.Column(db.Integer, default=0)


    def __repr__(self):
        return '<panier_produit: {}>'.format(self.id)


class Etablissement(db.Model):

    __tablename__ = 'etablissement'
    id=db.Column(db.Integer, primary_key=True)
    effectif =db.Column(db.Integer)
    localisation=db.Column(db.String(60))
    id_utilisateur=db.Column(db.Integer)


    def __repr__(self):
        return '<etablissement: {}>'.format(self.id)


class Etablissement_produit(db.Model):

    __tablename__ = 'etablissement_produit'
    id=db.Column(db.Integer, primary_key=True)
    id_produit = db.Column(db.Integer)
    type_produit = db.Column(db.Integer)
    nombre=db.Column(db.String(60))


    def __repr__(self):
        return '<etablissement_produit: {}>'.format(self.id)



class Commercial(db.Model):

    __tablename__ = 'commercial'
    id=db.Column(db.Integer, primary_key=True)
    nom =db.Column(db.String(60))

    def __repr__(self):
        return '<commercial: {}>'.format(self.id)


class Rdv(db.Model):

    __tablename__ = 'rdv'
    id=db.Column(db.Integer, primary_key=True)
    id_commercial = db.Column(db.Integer)
    id_interaction=db.Column(db.Integer)
    besoin_client = db.Column(db.Text)
    date=db.Column(db.DateTime)
    disponibilite=db.Column(db.Text)

    def __repr__(self):
        return '<rdv: {}>'.format(self.id)


class Option(db.Model):

    __tablename__ = 'option'
    id=db.Column(db.Integer, primary_key=True)
    type=db.Column(db.Text)
    point=db.Column(db.Integer)
    description=db.Column(db.Text)
    description_complete=db.Column(db.Text)
    prix= db.Column(db.Float)


    def __repr__(self):
        return '<option: {}>'.format(self.id)


def maj_dashboard():
    # db.session.execute("CALL insertcalendrier();")
    #     db.session.execute(sqlalchemy.text("CALL my_proc(:param)"), param='something')

    db.session.execute(text("CALL insertimplantation()"))
    db.session.execute(text("CALL insertclient()"))
    db.session.execute(text("CALL insertproduit()"))
    db.session.execute(text("CALL insertcalendrier()"))
    db.session.execute(text("CALL insertfait()"))
    db.session.commit()

# For the scheduler, automatisation pour la BDD
sched = BackgroundScheduler(daemon=True)
sched.add_job(maj_dashboard,'cron',hour=4)
sched.start()


"""
    Créons une requête pour modifier le statut d'une commande 
"""
@app.route('/accueil', methods=['GET'])
def bonjour():
    maj_dashboard()
    return render_template('accueil.html')


@app.route('/test', methods=['GET'])
def testeur():
    return "hohoho"




@app.route('/getInfoTelephone/<string:tel>', methods=['GET'])
def info_telephone(tel):
    ut = Telephone.query.filter(Telephone.modele.like("%"+tel+"%")).first()
    return ut.description



@app.route('/getTelephonegiga/<int:giga>', methods=['GET'])
def info_telephone_giga(giga):
    ut = Telephone.query.filter(Telephone.modele.like("%"+giga+"%")).first()
    return ut.description



@app.route('/getForfait/<string:forf>', methods=['GET'])
def info_forfait(forf):
    ut = Forfait.query.filter(Forfait.description.like("%"+forf+"%")).first()
    return "Le forfait "+forf+" dispose de "+str(ut.giga_4g)+"giga en 4G."


@app.route('/getForfaitGiga/<int:taille>', methods=['GET'])
def liste_forfait_giga(taille):
    liste=""
    ut = Forfait.query.filter(Forfait.giga_4g >= taille).all()
    for u in ut:
        liste=liste+str(u.description)+","
    return "les forfaits disposant de plus de "+str(taille)+" giga de connexion en 4G sont : "+liste



@app.route('/getForfaitPosition/<string:forf>', methods=['GET'])
def info_forfait_position(forf):

    ut = Forfait.query.filter(Forfait.description.like("%"+forf+"%")).first()
    zone=str(ut.zone).replace(" ",",")
    return "Le forfait "+forf+" est disponible sur la zone : "+zone+"."

@app.route('/getForfaitMetier/<string:metier>', methods=['GET'])
def info_forfait_metier(metier):
    liste=""
    ut = Utilisateur.query.filter_by(metier=metier).all()
    for u in ut:
        liste=str(u.telephone_actuel)
    return "Nous vous recommandons le téléphone "+liste+" car à l'heure actuel , la plupart des "+metier+" chez Orange l'utilise."





@app.route('/jambot', methods=['GET'])
def jambot():

    email = request.args.get('email')
    return render_template('jambot.html',email=email)



@app.route('/panier/<string:email>', methods=['GET'])
def panier_page(email):
    
    ut= Utilisateur.query.filter_by(email=email)
    if ut is not None:
        ut=ut.first()
    else:
        ut=None
    produits=None
    liste=[]
    listef=[]
    panier = Panier.query.filter_by(statut="En cours",id_utilisateur=ut.id).first()
    if panier is not None:
        produits=Panier_produit.query.filter_by(id=panier.id).with_entities(Panier_produit.id, Panier_produit.id_produit, Panier_produit.id_interaction, Panier_produit.type_produit, Panier_produit.nombre, Panier_produit.via_bot).all()
        for p in produits:
            tel=Telephone.query.filter_by(id=p[1]).first()
            forfait=Forfait.query.filter_by(id=p[1]).first()
            if tel is not None:
                temp=[p,Telephone.query.filter_by(id=p[1]).first()]
                liste.append(temp)
            elif forfait is not None:
                temp=[p,Forfait.query.filter_by(id=p[1]).first()]
                listef.append(temp)
    return render_template('panier.html',ut=ut,panier=produits, liste=liste , listef=listef)






@app.route('/Dashboard', methods=['GET'])
def dashboard():
    total_interactions = db.session.query(func.public.total_interactions()).all()
    total_interactions_abouties = db.session.query(func.public.total_interactions_abouties()).all()
    print(total_interactions)
    ratio = round(total_interactions_abouties[0][0]/total_interactions[0][0], 3)
    CA = db.session.query(func.public.total_ca()).all()
    doughnut_abouties = (total_interactions_abouties[0][0]/total_interactions[0][0])*100
    doughnut_non_abouties = ((total_interactions[0][0] - total_interactions_abouties[0][0])/total_interactions[0][0])*100

    # print(data[0][0])
    return render_template('dashboard.html', CA=CA[0][0], ratio=ratio, total_interactions_abouties=total_interactions_abouties[0][0], total_interactions=total_interactions[0][0], doughnut_datas=[doughnut_abouties, doughnut_non_abouties])


@app.route('/id_conv', methods=['POST'])
def check_id_conv():
    
    donnee = request.get_json()
    return jsonify(
        status=200,
        replies=[{
        'type': 'text',
        'content': donnee['conversation']['memory']['Nom']
        }]
    )



# @app.route('/telephones', methods=['POST'])
# def telephones():
#     donnee = request.get_json()
#     prix_max = donnee['conversation']['memory']['money_max']['amount']

#     #print("\n prix_max is : \n", prix_max)
#     liste = Telephone.query.filter(Telephone.prix <= prix_max)
#     #print("Lisssssssst",liste)
#     #List=Telephone.query.all()
#     table_telephones = []
#     for p in liste:
#         if(p.stock > 0):
#             table_telephones.append({
#                 "title": p.modele,
#                 "subtitle": p.prix,
#                 "imageUrl": "https://boutiquepro.orange.fr/catalog/product/static/8/9988/9988_250x460_1_0.jpg",
#                 "buttons": [
#                     {
#                         "value": "https://boutiquepro.orange.fr/telephone-mobile-xiaomi-mi-10t-noir-128go.html",
#                         "title": "lien",
#                         "type": "web_url"
#                     }
#                 ]
#             })
        
#     return jsonify(
#     status=200,
#     replies=[{
#       'type': 'carousel',
#       'content': table_telephones
#     }]
#   )

#Requete de récupération d'un téléphone d'occasion par son modèle
@app.route('/occasionTelephone', methods=['POST'])
def getTelephoneOccasion():
    donnee = request.get_json()
    telephoneDemande = donnee['conversation']['memory']['phone_occasion']['value']
    prix_max = donnee['conversation']['memory']['max']['amount']
    #ut= Utilisateur.query.filter_by(email=donnee['conversation']['memory']['email']).first()
    ut= Utilisateur.query.filter_by(id=45).first()

    liste = Telephone.query.filter(Telephone.prix <= prix_max)
    #liste = Telephone.query.filter(Telephone.prix >= 0)
    telephones = []
    for p in liste:
        if(telephoneDemande.lower() in p.modele.lower()):
            if(p.occasion is not None and p.occasion != 1):
                telephones.append({
                    "title": p.modele,
                    "subtitle": p.prix,
                    "imageUrl": p.lien_photo,
                    "buttons": [
                        {
                            "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id)+"/"+str(ut.email),
                            "title": "ajouter au panier",
                            "type": "web_url"
                        }
                    ]
                })
        
    if(len(telephones)!=0):
        return jsonify(
            status=200,
            replies=[{
                'type' : 'carousel',
                'content' : telephones
            }]
        )
    else:
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': "Désolé "+telephoneDemande+" n'est pas dans notre catalogue"
            }]
        )


#Requete de récupération d'un téléphone neuf par son modèle
@app.route('/nouveauTelephone', methods=['POST'])
def getTelephoneNeuf():
    donnee = request.get_json()
    telephoneDemande = donnee['conversation']['memory']['phone_occasion']['value']
    prix_max = donnee['conversation']['memory']['max']['amount']
    #ut= Utilisateur.query.filter_by(email=donnee['conversation']['memory']['email']).first()
    ut= Utilisateur.query.filter_by(id=45).first()

    liste = Telephone.query.filter(Telephone.prix <= prix_max)
    #liste = Telephone.query.filter(Telephone.prix >= 0)
    telephones = []
    for p in liste:
        if(telephoneDemande.lower() in p.modele.lower()):
            if(p.occasion is not None and p.occasion != 0):
                telephones.append({
                    "title": p.modele,
                    "subtitle": p.prix,
                    "imageUrl": p.lien_photo,
                    "buttons": [
                        {
                            "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id)+"/"+str(ut.email),
                            "title": "ajouter au panier",
                            "type": "web_url"
                        }
                    ]
                })
        
    if(len(telephones)!=0):
        return jsonify(
            status=200,
            replies=[{
                'type' : 'carousel',
                'content' : telephones
            }]
        )
    else:
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': "Désolé "+telephoneDemande+" n'est pas dans notre catalogue"
            }]
        )

#Requete de récupération d'un téléphone par sa marque
@app.route('/produitTelephone', methods=['POST'])
def getTelephone():
    donnee = request.get_json()
    telephoneDemande = donnee['conversation']['memory']['phone']['value']
    #ut= Utilisateur.query.filter_by(email=donnee['conversation']['memory']['email']).first()
    ut= Utilisateur.query.filter_by(id=45).first()

    liste = Telephone.query.filter(Telephone.stock > 0)
    #liste = Telephone.query.filter(Telephone.prix >= 0)
    telephones = []
    for p in liste:
        if(telephoneDemande.lower() in p.modele.lower()):
            telephones.append({
                "title": p.modele,
                "subtitle": p.prix,
                "imageUrl": p.lien_photo,
                "buttons": [
                    {
                        "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id)+"/"+str(ut.email),
                        "title": "ajouter au panier",
                        "type": "web_url"
                    }
                ]
            })
        
    if(len(telephones)!=0):
        return jsonify(
            status=200,
            replies=[{
                'type' : 'carousel',
                'content' : telephones
            }]
        )
    else:
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': "Désolé "+telephoneDemande+" n'est pas dans notre catalogue"
            }]
        )


#Requete de récupération d'un téléphone avec les besoins du client
@app.route('/proposerTelephone', methods=['POST'])
def proposerTelephone():
    donnee = request.get_json()
    #ut= Utilisateur.query.filter_by(email=donnee['conversation']['memory']['email']).first()
    ut= Utilisateur.query.filter_by(id=45).first()
    #domaine = donnee['conversation']['memory']['domaine']['value']
    try:
        prix = donnee['conversation']['memory']['money_max']['scalar']
    except:
        prix = donnee['conversation']['memory']['money_max']['amount']


    nombre = donnee['conversation']['memory']['nombre']['scalar']
    #localisation = donnee['conversation']['memory']['localisation']['value']
    n_design = donnee['conversation']['memory']['note_design']['scalar']
    n_appareil = donnee['conversation']['memory']['note_appareil']['scalar']
    n_connection = donnee['conversation']['memory']['note_connection']['scalar']
    n_batterie = donnee['conversation']['memory']['note_batterie']['scalar']
    n_puissance = donnee['conversation']['memory']['note_puissance']['scalar']
    occasion = donnee['conversation']['memory']['occasion']['slug']
    print(type(occasion))

    #liste = Telephone.query.filter(Telephone.stock > nombre and Telephone.prix <= prix and Telephone.note_design >= n_design and Telephone.note_ap >= n_appareil and Telephone.note_connection >= n_connection and Telephone.note_batterie >= n_batterie and Telephone.note_puissance >= n_puissance)
    f_stock = Telephone.query.filter(Telephone.stock > nombre)
    
    telephones = []
    for p in f_stock:
        if(p.prix <= prix):
            if(p.note_ap is not None and p.note_ap >= n_appareil):
                if(p.note_connection is not None and  p.note_connection >= n_connection):
                    if(p.note_batterie is not None and  p.note_batterie >= n_batterie):
                        if(p.note_puissance is not None and  p.note_puissance >= n_puissance):
                            if(p.note_design is not None and  p.note_design >= n_design):
                                #Partie occasion ou pas
                                if(occasion == 'yes' and p.occasion == 1):
                                    telephones.append({
                                        "title": p.modele,
                                        "subtitle": p.prix,
                                        "imageUrl": p.lien_photo,
                                        "buttons": [
                                            {
                                                "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id)+"/"+str(ut.email),
                                                "title": "ajouter au panier",
                                                "type": "web_url"
                                            }
                                        ]
                                    })
                                elif(occasion == 'no' and p.occasion == 0):
                                    telephones.append({
                                        "title": p.modele,
                                        "subtitle": p.prix,
                                        "imageUrl": p.lien_photo,
                                        "buttons": [
                                            {
                                                "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id)+"/"+str(ut.email),
                                                "title": "ajouter au panier",
                                                "type": "web_url"
                                            }
                                        ]
                                    })
        
    if(len(telephones)!=0):
        return jsonify(
            status=200,
            replies=[{
                'type' : 'carousel',
                'content' : telephones
            }]
        )
    else:
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': "Désolé aucun de nos téléphones ne correspond à votre demande"
            }]
        )



#Requete de récupération d'un forfait par le besoin client
@app.route('/proposerForfait', methods=['POST'])
def proposerForfait():
    donnee = request.get_json()

    #domaine = donnee['conversation']['memory']['domaine']['value']
    ut= Utilisateur.query.filter_by(id=45).first()
    try:
        prix = donnee['conversation']['memory']['money_max']['scalar']
    except:
        prix = donnee['conversation']['memory']['money_max']['amount']
    nombre = donnee['conversation']['memory']['nombre']['scalar']
    #localisation = donnee['conversation']['memory']['localisation']['value']
    t_giga = donnee['conversation']['memory']['type_giga']['value']
    n_giga = donnee['conversation']['memory']['nombre_giga']['scalar']
    try:
        zone = donnee['conversation']['memory']['zone']['value']
    except:
        zone = donnee['conversation']['memory']['localisation']['value']

    f_prix = Forfait.query.filter(Forfait.prix <= prix)
    forfaits = []
    for f in f_prix:
        if(t_giga == "4g"):
            if(f.giga_4g is not None and f.giga_4g >=  n_giga):
                if(f.zone is not None and zone.lower() in f.zone.lower()):
                    forfaits.append({
                        "title": f.description +" disponible en "+ f.zone,
                        "subtitle": str(f.giga_4g) + "Go à "+str(f.prix) + " €",
                        "imageUrl": "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
                        "buttons": [
                            {
                                "value": "https://jambot-api.herokuapp.com/addToCart/"+str(f.id)+"/"+str(ut.email),
                                "title": "ajouter au panier",
                                "type": "web_url"
                            }
                        ]
                    })
        elif(t_giga == "5g"):
            if(f.giga_5g is not None and f.giga_5g >=  n_giga):
                if(f.zone is not None and zone.lower() in f.zone.lower()):
                    forfaits.append({
                        "title": f.description +" disponible en "+ f.zone,
                        "subtitle": str(f.giga_5g) + "Go à "+str(f.prix) + " €",
                        "imageUrl": "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
                        "buttons": [
                            {
                                "value": "https://boutiquepro.orange.fr/telephone-mobile-xiaomi-mi-10t-noir-128go.html",
                                "title": "lien",
                                "type": "web_url"
                            }
                        ]
                    })
        
    if(len(forfaits)!=0):
        return jsonify(
            status=200,
            replies=[{
                'type' : 'carousel',
                'content' : forfaits
            }]
        )
    else:
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': "Désolé aucun de nos forfaits ne correspond à votre demande"+t_giga
            }]
        )



#Requete de récupération d'un forfait par son nom
@app.route('/getForfait', methods=['POST'])
def getForfait():
    donnee = request.get_json()
    
    ut= Utilisateur.query.filter_by(id=45).first()
    forfaitDemande = donnee['conversation']['memory']['forfait-variable']['value']

    listeForfaits = Forfait.query.filter(Forfait.prix > 0)
    forfaits = []
    for f in listeForfaits:
        if(forfaitDemande.lower() in f.description.lower()):
            forfaits.append({
                "title": f.description,
                "subtitle": f.prix,
                "imageUrl": "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
                "buttons": [
                    {
                        "value": "https://jambot-api.herokuapp.com/addToCart/"+str(f.id)+"/"+str(ut.email),
                        "title": "ajouter au panier",
                        "type": "web_url"
                    }
                ]
            })
        
    if(len(forfaits)!=0):
        return jsonify(
            status=200,
            replies=[{
                'type' : 'carousel',
                'content' : forfaits
            }]
        )
    else:
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': "Désolé "+forfaitDemande+" n'est pas dans notre catalogue"
            }]
        )





#Requete de récupération de tous les forfaits
@app.route('/forfaits', methods=['POST'])
def getAllForfaits():
    ut= Utilisateur.query.filter_by(id=45).first()
    listeForfaits=Forfait.query.filter(Forfait.prix > 0)
    forfaits=[]
    for f in listeForfaits:
        forfaits.append({
            "title": f.zone,
            "subtitle": f.giga_5g,
            "imageUrl": "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
            "buttons": [
                {
                        "value": "https://jambot-api.herokuapp.com/addToCart/"+str(f.id)+"/"+str(ut.email),
                        "title": "ajouter au panier",
                        "type": "web_url"
                }
            ]
        })
        
    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': forfaits
    }]
  )




@app.route('/telephones', methods=['POST'])
def telephones():
    donnee = request.get_json()
    #ut= Utilisateur.query.filter_by(email=donnee['conversation']['memory']['email']).first()
    ut= Utilisateur.query.filter_by(id=45).first()
    prix_max = donnee['conversation']['memory']['money_max']['amount']

    #print("\n prix_max is : \n", prix_max)
    liste = Telephone.query.filter(Telephone.prix <= prix_max)
    #print("Lisssssssst",liste)
    #List=Telephone.query.all()
    table_telephones = []
    for p in liste:
        if(p.stock > 0):
            table_telephones.append({
                "title": p.modele,
                "subtitle": p.prix,
                "imageUrl": p.lien_photo,
                "buttons": [
                    {
                        "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id)+"/"+str(ut.email),
                        "title": "ajouter au panier",
                        "type": "web_url"
                    }
                ]
            })
        
    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': table_telephones
    }]
  )



#Requete de récupération d'un forfait par son nom
@app.route('/addToCart/<int:id>/<string:email>', methods=['GET'])
def addToCart(id,email):
    ut=Utilisateur.query.filter_by(email=email).first()
    panier = Panier.query.filter_by(statut="En cours",id_utilisateur=ut.id).first()
    if panier is None:
        panier=Panier(statut= "En cours", id_utilisateur=ut.id)
        db.session.add(panier)
        db.session.commit()
        panier=Panier.query.filter_by(statut="En cours",id_utilisateur=ut.id).first()

    test=Panier_produit.query.filter_by(id=panier.id, id_produit=id).first()
    if(test is None):
        tel=Telephone.query.filter_by(id=id).first()
        forfait=Forfait.query.filter_by(id=id).first()
        if tel is not None:
            panier_produit=Panier_produit(id=panier.id,id_produit=id,type_produit="telephone",nombre=1,id_interaction=0,via_bot=1)    
            db.session.add(panier_produit)
            db.session.commit()
        elif forfait is not None:        
            panier_produit=Panier_produit(id=panier.id,id_produit=id,type_produit="forfait",nombre=1,id_interaction=0,via_bot=1)    
            db.session.add(panier_produit)
            db.session.commit()
    else:
        Panier_produit.query.filter_by(id=panier.id,id_produit=id).update({Panier_produit.nombre: Panier_produit.nombre+1 })
        db.session.commit()
    
    return ""

#Requete de récupération d'un forfait par son nom
@app.route('/validerPanier/<string:email>', methods=['GET'])
def validerPanier(email):

    util = Utilisateur.query.filter_by( email= email).first()
    Panier.query.filter_by(statut="En cours",id_utilisateur=util.id).update({Panier.statut: "Valider" })
    db.session.commit()

    return render_template('validation.html')


@app.route('/validerPanierVP/<string:email>', methods=['GET'])
def validerPanierPV(email):

    util = Utilisateur.query.filter_by( email= email).first()
    Panier.query.filter_by(statut="En cours",id_utilisateur=util.id).update({Panier.statut: "Valider" })
    db.session.commit()

    return render_template('validation.html')
    

#Requete de récupération d'un forfait par son nom
@app.route('/panier/<string:email>', methods=['POST'])
def getPanier(email):
    
    donnee = request.get_json()
    util = Utilisateur.query.filter_by( email= email).first()
    panier = Panier.query.filter_by(statut="En cours",id_utilisateur=util.id).first()
    liste=[]
    listef=[]
    produit=[]
    if panier is not None:
        produits=Panier_produit.query.filter_by(id=panier.id).with_entities(Panier_produit.id, Panier_produit.id_produit, Panier_produit.id_interaction, Panier_produit.type_produit, Panier_produit.nombre, Panier_produit.via_bot).all()
        for p in produits:
            tel=Telephone.query.filter_by(id=p[1]).first()
            forfait=Forfait.query.filter_by(id=p[1]).first()
            if tel is not None:
                liste.append(Telephone.query.filter_by(id=p[1]).first())
            elif forfait is not None:
                listef.append(forfait.query.filter_by(id=p[1]).first())
            
        for p in liste:
                produit.append({
                    "title": p.modele,
                    "subtitle": str(p.prix)+" X "+str(Panier_produit.query.filter_by(id=panier.id,id_produit=p.id).first().nombre) ,
                    "imageUrl": p.lien_photo,
                    "buttons": [
                        {
                            "value": "https://jambot-api.herokuapp.com/validerPanier/damendiaye@gmail.com",
                            "title": "Valider mon panier avec carte bancaire",
                            "type": "web_url"
                        },
                        {
                            "value": "https://jambot-api.herokuapp.com/validerPanierVP/damendiaye@gmail.com",
                            "title": "Valider mon panier avec des points",
                            "type": "web_url"
                        }
                    ]
                })
        for f in listef:
                produit.append({
                    "title": f.description +" disponible en "+ f.zone,
                    "subtitle": str(f.giga_4g) + "Go à "+str(f.prix) + " €",
                    "imageUrl":  "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
                    "buttons": [
                        {
                            "value": "https://jambot-api.herokuapp.com/validerPanier/damendiaye@gmail.com",
                            "title": "Valider mon panier avec carte bancaire",
                            "type": "web_url"
                        },
                        {
                            "value": "https://jambot-api.herokuapp.com/validerPanierVP/damendiaye@gmail.com",
                            "title": "Valider mon panier avec des points",
                            "type": "web_url"
                        }
                    ]
                })
    else:
        produit.append('Vous n\' avez pas de panier en cours')

    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': produit
    }]
  )


#Requete de récupération d'un forfait par son nom
# @app.route('/testpanier/<string:email>', methods=['POST'])
# def getPanierAAD(email):
    
#     donnee = request.get_json()
#     util = Utilisateur.query.filter_by( email= email).first()
#     panier = Panier.query.filter_by(statut="En cours",id_utilisateur=util.id).first()
#     liste=[]
#     # testAAD1=Panier_produit.query.filter_by(id=panier.id).with_entities(Panier_produit.id_produit, Panier_produit.id_interaction, Panier_produit.type_produit, Panier_produit.nombre, Panier_produit.via_bot).all()
#     # print(testAAD1)
#     # print(testAAD1[0][1])
    
#     if panier is not None:
#         produits=Panier_produit.query.filter(Panier_produit.id == panier.id)
#         for p in produits:
#             print(str(p.id_produit)+"\n")
#             liste.append(Telephone.query.filter_by(id=p.id_produit).first())
#     produit=[]
#     for p in liste:
#             produit.append({
#                 "title": p.modele,
#                 "subtitle": p.prix,
#                 "imageUrl": p.lien_photo,
#                 "buttons": [
#                     {
#                         "value": "",
#                         "title": "panier",
#                         "type": "web_url"
#                     }
#                 ]
#             })

#     return jsonify(
#     status=200,
#     replies=[{
#       'type': 'carousel',
#       'content': produit
#     }]
#   )
  

#Requete de récupération d'une option par son nom
@app.route('/getOption', methods=['POST'])
def getOption():
    donnee = request.get_json()
    optionDemandee = donnee['conversation']['memory']['option-variable']['value']

    listeOptions = Option.query.filter(Option.prix > 0)
    options = []
    for o in listeOptions:
        if(optionDemandee.lower() in o.description.lower()):
            options.append({
                "title": "Nom: " + o.description_complete,
                "subtitle": 'Prix: ' + str(o.prix) + '€',
                "buttons": [
                    {
                        "value": "https://boutiquepro.orange.fr/telephone-mobile-business-everywhere-flex-sans-engagement.html",
                        "title": "Voir",
                        "type": "web_url"
                    }
                ]
            })   
        
    return jsonify(
    status=200,
    replies=[{
      'type': 'list',
      'content': options
    }]
  )


#Requete de récupération de toutes les options
@app.route('/options', methods=['POST'])
def getAllOptions():

    listeOptions=Option.query.filter(Option.prix > 0)
    options=[]
    for o in listeOptions:
        options.append({
            "title": "Nom: " + o.description_complete,
            "subtitle": 'Prix: ' + str(o.prix) + '€',
            "buttons": [
                {
                    "value": "https://boutiquepro.orange.fr/telephone-mobile-business-everywhere-flex-sans-engagement.html",
                    "title": "Voir",
                    "type": "web_url"
                }
            ]
        })   
    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': options
    }]
  )



# @app.route('/allbots', methods=['GET'])
# def getBots():
    
#     List=Bot.query.all()
#     table_bot = []
#     for b in List:
#         json_com={
#             'id': b.id,
#             'notation': b.notation,
#             'client': b.Client_id,
#             'date': b.date,
#             }
#         table_bot.append(json_com)
#     response = jsonify({"Bots" : table_bot})

#     return response.json



# @app.route('/allclients', methods=['GET'])
# def getClients():
    
#     List=Client.query.all()
#     table_client = []
#     for c in List:
#         json_com={
#             'id': c.id,
#             'nom': c.nom,
#             'prenom': c.prenom,
#             'localisation': c.localisation,
#             'effectif': c.effectif,
#             'domaine':c.domaine
#             }
#         table_client.append(json_com)
#     response = jsonify({"Clients" : table_client})

#     return response.json


# @app.route('/getClient_by_id/<int:id_c>', methods=['GET'])
# def getClient(id_c):
    
#     c=Client.query.filter_by(id=id_c).first()
#     json_com={
#             'id': c.id,
#             'nom': c.nom,
#             'prenom': c.prenom,
#             'localisation': c.localisation,
#             'effectif': c.effectif,
#             'domaine':c.domaine
#             }
#     response = jsonify({"Client" : json_com})

#     return response.json


# @app.route('/ajouterProduit', methods=['POST'])
# def addProduit():
    
    
#     donnee = request.get_json()

#     description=donnee['description']
    
#     prix=donnee['prix']
    
#     type_produit=donnee['type']
    

#     niveau=0
#     n=Produit.query.order_by(desc(Produit.id)).first()
#     if n != None:
#         niveau=n.id+1


#     b = Produit(id=niveau,description=description,prix=prix,type_produit=type_produit)

#     db.session.add(b)
#     db.session.commit()

#     return 'succes'





@app.route('/recupInfo/<string:siret>', methods=['POST'])
def recupInfo(siret):
    req_info = urllib.request.urlopen("https://entreprise.data.gouv.fr/api/sirene/v3/etablissements/"+str(siret)+"/").read()
    info = json.loads(req_info.decode('utf-8'))
    


    return jsonify(
    status=200,
    conversation={"memory":{"Etablissement":info.etablissement.denomination ,"localisation":info.etablissement.geo_adresse ,"effectif":info.etablissement.tranche_effectifs}}
    )





@app.route('/ajouterForfait', methods=['POST'])
def addForfait():


    donnee = request.get_json()
    print("donnees",donnee)
    forfait=  Forfait( description=donnee['description'],  is_engagement=donnee['is_engagement'], giga_4g=donnee['giga_4g'], giga_5g=donnee['giga_5g'] , description_complete= donnee['description_complete'], prix=donnee['prix'] )

    db.session.add(forfait)
    db.session.commit()

    return 'succes'


@app.route('/ajouterTelephone', methods=['POST'])
def addTelephone():


    donnee = request.get_json()
    print("donnees",donnee)
    telephone= Telephone( marque=donnee['marque'],  description=donnee['description'], prix=donnee['prix'], note_design=donnee['note_design'] , note_ap= donnee['note_ap'], note_connection=donnee['note_connection'] ,note_batterie=donnee['note_batterie'], note_puissance=donnee['note_puissance'], occasion=donnee['occasion'], stock=donnee['stock'], lien_photo=donnee['lien_photo'])

    db.session.add(telephone)
    db.session.commit()

    return 'succes'




@app.route('/ajouterAvis', methods=['POST'])
def addAvis():
    donnee = request.get_json()
    print("donnees",donnee)
    avis=donnee['conversation']['memory']['rating']['scalar']
    id_util = Utilisateur.query.filter_by( id=45).first().id
    b = Avis(note=avis,id_interaction=id_util,id_utilisateur=id_util)

    db.session.add(b)
    db.session.commit()
    return jsonify(
        status=200,
        replies=[{
        'type': 'list',
        'content': 'Merci ! A bientôt!'
        }]
    )


@app.route('/recommandForfait', methods=['POST'])
def recommandForfait():

    donnee = request.get_json()
    
    ut= Utilisateur.query.filter_by(id=45).first()
    phone = donnee['conversation']['memory']['phone']['value']
    listeUtilisateurs = Utilisateur.query.all()
    forfaitsEntiers = []
    for val in listeUtilisateurs:
        if phone in val.telephone_actuel.lower():
            val.forfait_actuel = val.forfait_actuel.replace('g',' g')
            val.forfait_actuel = val.forfait_actuel.split(" ",1)
            lettre = val.forfait_actuel[0]
            nombre = int(lettre)
            forfaitsEntiers.append(nombre)
    values = []
    for x in forfaitsEntiers:
        listeForfaits = Forfait.query.filter(Forfait.giga_4g == x)
        for l in listeForfaits:
            values.append({
                "title": l.description,
                "subtitle": l.giga_4g,
                "imageUrl": "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
                "buttons": [
                    {
                        "value": "https://jambot-api.herokuapp.com/addToCart/"+str(l.id)+"/"+str(ut.email),
                        "title": "ajouter au panier",
                        "type": "web_url"
                    }
                ]
            })
    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': values
    }])
    
@app.route('/recommandTel', methods=['POST'])
def recommandTel():

    donnee = request.get_json()
    ut= Utilisateur.query.filter_by(id=45).first()
    forfait = donnee['conversation']['memory']['forfait-variable']['value']
    listeforfaits = Forfait.query.all()
    forfaitsvalues = []
    for val in listeforfaits:
        if forfait in val.description.lower():
            forfaitsvalues.append(val.giga_4g)
    values = []
    for x in forfaitsvalues:
        x = str(x) + 'go'
        listeTel = Utilisateur.query.filter(Utilisateur.forfait_actuel == x)
        for l in listeTel:
            #telephones = Telephone.query.filter(l.telephone_actuel.lower() in Telephone.modele.lower())
            telephones = Telephone.query.all()
            for t in telephones:
                if(l.telephone_actuel.lower() in t.modele.lower()):
                    values.append({
                    "title": t.modele,
                    "subtitle": t.prix,
                    "imageUrl": t.lien_photo,
                    "buttons": [
                        {
                            "value": "https://jambot-api.herokuapp.com/addToCart/"+str(t.id)+"/"+str(ut.email),
                            "title": "ajouter au panier",
                            "type": "web_url"
                        }
                    ]
                })
    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': values
    }])




@app.route('/listeRV', methods=['POST'])
def showRV():
   
   d = request.get_json()
   ALL_RV=Rdv.query.filter_by(disponibilite='disponible').all()
   donnee=[]
#    donnee.append({"value": "https://pro.orange.fr/contacts/",
#                         "title": "Chat spontanté",
#                         "type": "web_url"})
   for rv in ALL_RV:
       do={"value" :str(rv.id), "title": str(rv.date)}
       donnee.append(do)
    
   ut = Utilisateur.query.filter_by( id=45).first()
   return jsonify(
   status=200,
   replies=[{
      "type": "quickReplies",
      "content": {
        "title": "pour un entretient immédiat \n Rendez vous sur :\n https://pro.orange.fr/contacts/ \n.Liste des rendez vous disponibles M./Mme " + str(ut.nom),
        "buttons": donnee
      }
    
    }]
  )



@app.route('/allrdv', methods=['GET'])
def getAllRdv():    
    List=Rdv.query.all()
    table_rdv = []
    for c in List:
        json_com={
            'id': c.id,
            'client': c.id_interaction,
            'disponibilite': c.disponibilite,
            }
        table_rdv.append(json_com)
    response = jsonify({"Rdv" : table_rdv})

    return response.json



@app.route('/takeRdv', methods=['POST'])
def takeRV():

    donnee = request.get_json()
    rdv=int(donnee['nlp']['source'])
    id = Utilisateur.query.filter_by( email= donnee['conversation']['memory']['email']).first().id
    Rdv.query.filter_by(id=rdv).update({Rdv.disponibilite: 'indisponible', Rdv.id_interaction: id})
    db.session.commit()
    return "succes"



@app.route('/addrdv', methods=['POST'])
def addRV():

    donnee = request.get_json()
    id=donnee['id']
    id_commercial =donnee['id_commercial']
    id_interaction=donnee['id_interaction']
    besoin_client =donnee['besoin_client']
    disponibilite =donnee['disponibilite']
    date=donnee['date']
    b = Rdv(id=id, id_commercial=id_commercial, id_interaction=id_interaction, besoin_client= besoin_client , date=date,disponibilite=disponibilite)

    db.session.add(b)
    db.session.commit()

    return 'success'


@app.route('/supAllRdv', methods=['POST'])
def supRV():

    c=Rdv.query.all()
    for i in c:
        db.session.delete(i)
    db.session.commit()

    return 'success'


@app.route('/addCommercial', methods=['POST'])
def addCommercial():

    donnee = request.get_json()
    id=donnee['id']
    nom=donnee['nom']
    b = Commercial(id=id,nom=nom)

    db.session.add(b)
    db.session.commit()

    return 'success'

@app.route('/addUser', methods=['POST'])
def addUser():

    donnee = request.get_json()
    id=donnee['id']
    nom=donnee['nom']
    prenom=donnee['prenom']
    email=donnee['email']
    numero_telephone="hohooho"
    siret = "hohooho"
    telephone_actuel ="hohooho"
    forfait_actuel= "hohooho"
    
    b = Utilisateur(id=id,nom=nom,prenom=prenom,email=email,numero_telephone=numero_telephone, siret=siret,telephone_actuel=telephone_actuel,forfait_actuel=forfait_actuel)

    db.session.add(b)
    db.session.commit()

    return 'success'

# @app.route('/ajouterClient', methods=['POST'])
# def addClient():
     
    
#     donnee = request.get_json()

#     nom=donnee['nom']
#     prenom=donnee['prenom']
    
#     localisation=donnee['localisation']
    
#     effectif=donnee['effectif']
    
#     domaine=donnee['domaine']
#     niveau=0
#     n=Client.query.order_by(desc(Client.id)).first()
#     if n != None:
#         niveau=n.id+1

#     b = Client(id=niveau, nom=nom,prenom=prenom,localisation=localisation,effectif=effectif,domaine=domaine)

#     db.session.add(b)
#     db.session.commit()

#     return 'succes'


@app.route('/', methods=['POST'])
def index():
  data = request.get_json()
  #print("data : \n" + jsonify(data))
  # FETCH THE CRYPTO NAME
  crypto_name = data["nlp"]["entities"]["crypto_name"][0]["raw"]
  #print(crypto_name)
  # FETCH BTC/USD/EUR PRICES
  r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': 'The price of %s is %f BTC and %f USD' % (crypto_name, r.json()['BTC'], r.json()['USD'])
    }]
  )


@app.route('/loc-effectif', methods=['POST'])
def get_localisation_effectif():
    data = request.get_json()
    #print("data : \n" + jsonify(data))
    # FETCH THE CRYPTO NAME

    num_tel = data["conversation"]["memory"]["numero_telephone"]["number"]
    siret = data["conversation"]["memory"]["siret"]["raw"]
    memory = dict(data["conversation"]["memory"])

    #print(crypto_name)
    # FETCH BTC/USD/EUR PRICES
    r = requests.get("https://entreprise.data.gouv.fr/api/sirene/v3/etablissements/"+siret)
    print("R \n:", r)
    print("R.json() \n:", r.json())

    memory['localisation'] = r.json()['etablissement']['libelle_commune']
    memory['effectif'] = r.json()['etablissement']['tranche_effectifs']



    return jsonify(
    status=200,
    conversation={"memory": dict(memory)}
    )

#Requete de récupération de tous les forfaits
@app.route('/interaction', methods=['POST'])
def addInteraction():

    inter=Interaction(localisation="Rouen",date=datetime.now(),id_utilisateur=45)
    db.session.add(inter)
    db.session.commit()
        
    return jsonify(
    status=200,
    replies=[{
    'type': 'text',
    'content': 'je vais bien et vous! Comment puis-je vous aidez ?'
    }]
    
    
    
  )

 

#db.create_all()

if __name__ == '__main__':
    app.run(debug=False)




