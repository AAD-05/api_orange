from flask import Flask, request, Response, jsonify

from flask import  redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc
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

    occasion=db.Column(db.Integer)
    stock= db.Column(db.Integer)
    lien_photo=db.Column(db.Text)


    def __repr__(self):
        return '<telephone: {}>'.format(self.code)

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
    prix= db.Column(db.Float)


    def __repr__(self):
        return '<forfait: {}>'.format(self.code)



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


    def __repr__(self):
        return '<utilisateur: {}>'.format(self.code)

  


class Interaction(db.Model):

    __tablename__ = 'interaction'
    id=db.Column(db.Integer, primary_key=True)
    localisation =db.Column(db.String(100))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    id_utilisateur = db.Column(db.Integer)


    def __repr__(self):
        return '<interaction: {}>'.format(self.code)



class Panier(db.Model):

    __tablename__ = 'panier'
    id=db.Column(db.Integer, primary_key=True)
    statut =db.Column(db.String(60))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    id_utilisateur = db.Column(db.Integer)


    def __repr__(self):
        return '<panier: {}>'.format(self.code)



class Avis(db.Model):

    __tablename__ = 'avis'
    id=db.Column(db.Integer, primary_key=True)
    note =db.Column(db.Integer)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    id_interaction=db.Column(db.Integer)
    id_utilisateur = db.Column(db.Integer)


    def __repr__(self):
        return '<avis: {}>'.format(self.code)


class Panier_produit(db.Model):

    __tablename__ = 'panier_produit'
    id=db.Column(db.Integer, primary_key=True)
    id_produit = db.Column(db.Integer)
    type_produit = db.Column(db.Integer)
    nombre=db.Column(db.String(60))
    id_interaction=db.Column(db.Integer)
    via_bot = db.Column(db.Integer, default=0)


    def __repr__(self):
        return '<panier_produit: {}>'.format(self.code)


class Etablissement(db.Model):

    __tablename__ = 'etablissement'
    id=db.Column(db.Integer, primary_key=True)
    effectif =db.Column(db.Integer)
    localisation=db.Column(db.String(60))
    id_utilisateur=db.Column(db.Integer)


    def __repr__(self):
        return '<etablissement: {}>'.format(self.code)


class Etablissement_produit(db.Model):

    __tablename__ = 'etablissement_produit'
    id=db.Column(db.Integer, primary_key=True)
    id_produit = db.Column(db.Integer)
    type_produit = db.Column(db.Integer)
    nombre=db.Column(db.String(60))


    def __repr__(self):
        return '<etablissement_produit: {}>'.format(self.code)



class Commercial(db.Model):

    __tablename__ = 'commercial'
    id=db.Column(db.Integer, primary_key=True)
    nom =db.Column(db.String(60))

    def __repr__(self):
        return '<commercial: {}>'.format(self.code)


class Rdv(db.Model):

    __tablename__ = 'rdv'
    id=db.Column(db.Integer, primary_key=True)
    id_commercial = db.Column(db.Integer)
    id_interaction=db.Column(db.Integer)
    besoin_client = db.Column(db.Text)
    date=db.Column(db.DateTime)
    disponibilite=db.Column(db.Text)

    def __repr__(self):
        return '<rdv: {}>'.format(self.code)







"""
    Créons une requête pour modifier le statut d'une commande 
"""    

@app.route('/bonjour', methods=['GET'])
def bonjour():
    return 'bonjour'


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

#Requete de récupération d'un téléphone par sa marque
@app.route('/produitTelephone', methods=['POST'])
def getTelephone():
    donnee = request.get_json()
    telephoneDemande = donnee['conversation']['memory']['phone']['value']

    liste = Telephone.query.filter(Telephone.stock > 0)
    #liste = Telephone.query.filter(Telephone.prix >= 0)
    telephones = []
    for p in liste:
        if(telephoneDemande.lower() in p.modele.lower()):
            telephones.append({
                "title": p.modele,
                "subtitle": p.prix,
                "imageUrl": "https://boutiquepro.orange.fr/catalog/product/static/8/9988/9988_250x460_1_0.jpg",
                "buttons": [
                    {
                        "value": "https://boutiquepro.orange.fr/telephone-mobile-xiaomi-mi-10t-noir-128go.html?id="+str(p.id),
                        "title": "ajouter au panier",
                        "type": "web_url"
                    }
                ]
            })
        
    return jsonify(
    status=200,
    replies=[{
      'type': 'carousel',
      'content': telephones
    }]
  )


#Requete de récupération d'un forfait par son nom
@app.route('/getForfait', methods=['POST'])
def getForfait():
    donnee = request.get_json()
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
                        "value": "https://boutiquepro.orange.fr/telephone-mobile-xiaomi-mi-10t-noir-128go.html",
                        "title": "lien",
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





#Requete de récupération de tous les forfaits
@app.route('/forfaits', methods=['POST'])
def getAllForfaits():

    listeForfaits=Forfait.query.filter(Forfait.prix > 0)
    forfaits=[]
    for f in listeForfaits:
        forfaits.append({
            "title": f.description,
            "subtitle": f.prix,
            "imageUrl": "https://www.francemobiles.com/actualites/image-orange-320-000-ventes-nettes-de-forfaits-mobiles-au-3eme-trimestre-2017-2017-17648-francemobiles.jpg",
            "buttons": [
                {
                    "value": "https://boutiquepro.orange.fr/telephone-mobile-xiaomi-mi-10t-noir-128go.html",
                    "title": "lien",
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
                "imageUrl": "https://boutiquepro.orange.fr/catalog/product/static/8/9988/9988_250x460_1_0.jpg",
                "buttons": [
                    {
                        "value": "https://jambot-api.herokuapp.com/addToCart/"+str(p.id),
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
@app.route('/addToCart/<int:id>', methods=['POST'])
def addToCart(id):
 
    return "success "+str(id)
  



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


@app.route('/ajouterForfait', methods=['POST'])
def addForfait():


    donnee = request.get_json()
    print("donnees",donnee)
    Forfait=  Forfait( description=donnee['description'],  is_engagement=donnee['is_engagement'], giga_4g=donnee['giga_4g'], giga_5g=donnee['giga_5g'] , description_complete= donnee['description_complete'], prix=donnee['prix'] )

    db.session.add(Forfait)
    db.session.commit()

    return 'succes'


@app.route('/ajouterTelephone', methods=['POST'])
def addTelephone():


    donnee = request.get_json()
    print("donnees",donnee)
    Telephone= Telephone( marque=donnee['marque'],  description=donnee['description'], prix=donnee['prix'], note_design=donnee['note_design'] , note_ap= donnee['note_ap'], note_connection=donnee['note_connection'] ,note_batterie=donnee['note_batterie'], note_puissance=donnee['note_puissance'], occasion=donnee['occasion'], stock=donnee['stock'], lien_photo=donnee['lien_photo'])

    db.session.add(Telephone)
    db.session.commit()

    return 'succes'




@app.route('/ajouterAvis', methods=['POST'])
def addAvis():


    donnee = request.get_json()
    print("donnees",donnee)
    #avis=donnee['nlp']['entities']['number'][0]['raw']
    avis=donnee['conversation']['memory']['rating']['scalar']
    id_util = Utilisateur.query.filter_by( email= donnee['conversation']['memory']['email']).first()
    b = Avis(note=avis,id_interaction=id_util,id_utilisateur=id_util)

    db.session.add(b)
    db.session.commit()

    return 'succes'





@app.route('/listeRV', methods=['POST'])
def showRV():
   
   
   d = request.get_json()
   ALL_RV=Rdv.query.filter_by(disponibilite='disponible').all()
   donnee=[] 
   for rv in ALL_RV:
       do={"value" :str(rv.id), "title": str(rv.date)}
       donnee.append(do)
    
   ut = Utilisateur.query.filter_by( email= d['conversation']['memory']['email']).first()
   return jsonify(
   status=200,
   replies=[{
      "type": "quickReplies",
      "content": {
        "title": "liste des rendez vous disponibles M./Mme " + str(ut.nom),
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



#db.create_all()

if __name__ == '__main__':
    app.run(debug=False)
