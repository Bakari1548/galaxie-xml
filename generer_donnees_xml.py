from lxml import etree
from random import choice
import json



def extaire_deputes_depuis_json(fichier_json):
    """
    Extraction des députés de la 15eme législature depuis le fichier JSON
    deputes.json et retourne une liste de dictionnaires.
    """
    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    allDeputes = []

    for i in data:
        deputes = data[i]['deputies']
        for depute in deputes:
            allDeputes.append(depute)
    print(f"Nombre total de députés extraits : {len(allDeputes)}")

    with open('./dataJSON/deputes_extraits.json', 'w', encoding='utf-8') as wf:
        json.dump(allDeputes, wf, ensure_ascii=False, indent=4)
    return allDeputes



def extraire_lois_depuis_json(fichier_json):
    """
    Extraction des projet lois de la 15eme législature (2024-2029) depuis le fichier JSON
    prjet_loi.json et retourne une liste de dictionnaires.
    """

    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    projetsDeLoi = []

    lois = data[0]
    for loi in lois:
        projetsDeLoi.append(loi)
    print(f"Nombre total de lois extraits : {len(projetsDeLoi)}")

    return projetsDeLoi


def extraire_commissions_depuis_json(fichier_json):
    """
    Extraction des commissions depuis le fichier JSON
    avec les membre de bureau de chaque commission.
    """
    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    commissions = []
    commisonJSON = data[0]

    # print("Commissions depuis JSON : ", commisonJSON)

    for commission in commisonJSON:
        commissions.append(commission)
    print(f"Nombre total de commissions extraits : {len(commissions)}")

    return commissions


def generer_commissions_json(fichier_json):
    """
    Génération des commissions depuis le fichier JSON
    commissions.json et retourne une liste de dictionnaires
    avec le bureau de chaque commission.
    """
    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # commissions = []
    commissions = data

    print(f"Nombre total de commissions extraits : {len(commissions)}")

    # print("Commissions : ", commissions[0])

    return commissions


def generer_donnees_xml(nom_fichier, nbr_donnees):
    
    BATIMENT_CHOICES = ['A', 'B', 'C', 'D']

    allDeputes = extaire_deputes_depuis_json('./dataJSON/deputes.json')
    projetsDeLoi = extraire_lois_depuis_json('./dataJSON/projet_loi.json')
    allCommissions = generer_commissions_json('./dataJSON/commissions.json')

    # print("Commissions : ", commissions)

    # 'with' garantit la fermeture propre du fichier
    with etree.xmlfile(nom_fichier, encoding='utf-8') as xf:
        xf.write_declaration()
        # On définit l'élément racine
        with xf.element('assemblee_nationale'):

            # ========= Génération des informations generales de l'assemblee ========

            informations_generales = etree.Element('informations_generales')
            pays = etree.SubElement(informations_generales, 'pays')
            pays.text = 'Sénégal'
            legislature = etree.SubElement(informations_generales, 'legislature')
            legislature.text = '15ème législature (2024-2029)'
            annee_debut_legis = etree.SubElement(informations_generales, 'annee_debut_legis')
            annee_debut_legis.text = '2022-07-30'
            siege = etree.SubElement(informations_generales, 'siege')
            siege.text = 'Dakar'
            description = etree.SubElement(informations_generales, 'description')
            description.text = """
                L'Assemblée nationale est l'institution législative qui représente le peuple et exerce 
                le pouvoir législatif. Elle est composée de plusieurs organes essentiels assurant son 
                bon fonctionnement et la mise en œuvre de ses missions républicaines.
            """
            nombre_deputes = etree.SubElement(informations_generales, 'nombre_deputes')
            nombre_deputes.text = str(nbr_donnees)
            
            xf.write(informations_generales)
            
            # ======== Génération des députés ========
            deputes = etree.Element('deputes')
            
            for i in range(nbr_donnees):
                # Création d'un depute
                depute = etree.SubElement(deputes, 'depute', id=f"DPT{allDeputes[i]['id']}")
                # les sous-element identifiant d'un depute
                identifiant = etree.SubElement(depute, 'identifiant')

                nom = etree.SubElement(identifiant, 'nom')
                nom.text = allDeputes[i]['first_name']
                prenom = etree.SubElement(identifiant, 'prenom')
                prenom.text = allDeputes[i]['last_name']
                date_naissance = etree.SubElement(identifiant, 'date_naissance')
                date_naissance.text = allDeputes[i]['birth_date']
                lieu_naissance = etree.SubElement(identifiant, 'lieu_naissance')
                lieu_naissance.text = allDeputes[i]['birth_place']

                # Sous element parti d'un depute
                parti = etree.SubElement(depute, 'parti')
                parti.text = allDeputes[i]['party']['name']

    
                profession = etree.SubElement(depute, 'profession')
                profession.text = allDeputes[i]['profession']

                # Sous element contact d'un depute
                contact = etree.SubElement(depute, 'contact')
                email = etree.SubElement(contact, 'email')
                email.text = allDeputes[i]['email']
                telephone = etree.SubElement(contact, 'telephone')
                telephone.text = f'77{1000000 + i}'
                adresse_bureau = etree.SubElement(contact, 'adresse_bureau')
                adresse_bureau.text = f'Batiment {choice(BATIMENT_CHOICES)} Bureau {i + 1}'

                reseaux_sociaux = etree.SubElement(contact, 'reseaux_sociaux')
                twitter = etree.SubElement(reseaux_sociaux, 'twitter')
                twitter.text = f'@{allDeputes[i]["last_name"].lower()}_{allDeputes[i]["first_name"].lower()}'
                facebook = etree.SubElement(reseaux_sociaux, 'facebook')
                facebook.text = f'facebook.com/{allDeputes[i]["last_name"].lower()}.{allDeputes[i]["first_name"].lower()}'
                linkedin = etree.SubElement(reseaux_sociaux, 'linkedin')
                linkedin.text = f'linkedin.com/in/{allDeputes[i]["last_name"].lower()}.{allDeputes[i]["first_name"].lower()}'
                # xf.write(depute)

            xf.write(deputes)

            # ======== Génération des lois ========
            lois = etree.Element('lois')
            for loi in projetsDeLoi:
                projet_loi = etree.SubElement(lois, 'projet_loi', id=f"LOI{loi['id']}")
                titre = etree.SubElement(projet_loi, 'titre')
                titre.text = loi['title']
                description_loi = etree.SubElement(projet_loi, 'description_loi')
                description_loi.text = loi['description']
                date_publication = etree.SubElement(projet_loi, 'date_publication')
                date_publication.text = loi['publish_date']
                statut = etree.SubElement(projet_loi, 'statut')
                statut.text = loi['status']
                # document = etree.SubElement(projet_loi, 'document')
                # titre_document = etree.SubElement(document, 'titre_document')
                # titre_document.text = loi['fichiers']['name']
                # fichier_pdf = etree.SubElement(document, 'fichier_pdf')
                # fichier_pdf.text = loi['fichiers']['full_path']
            
            xf.write(lois)

            # ======== Génération des commissions ========
            commissions = etree.Element('commissions')
            for commission in allCommissions:
                # print("Titre Commissions: ", commission['title'])
                title_commission = commission['title']
                description_commission = commission['description']
                president_commission = commission['bureau']['president_id']
                vice_presidents_commission = commission['bureau']['vice_president_id']

                commission = etree.SubElement(commissions, 'commission', id=f"COM{commission['id']}")
                
                titre_com = etree.SubElement(commission, 'titre_com')
                titre_com.text = title_commission
                
                description_com = etree.SubElement(commission, 'description_com')
                description_com.text = description_commission
                
                bureau = etree.SubElement(commission, 'bureau')
                
                president_id = etree.SubElement(bureau, 'president_id')
                president_id.text = president_commission
                
                for i in range(len(vice_presidents_commission)):
                    vice_president_id = etree.SubElement(bureau, 'vice_president_id')
                    vice_president_id.text = vice_presidents_commission[i]
                # vice_president_id = etree.SubElement(bureau, 'vice_president_id')
                # vice_president_id.text = commission['bureau']['vice_president_id']
            xf.write(commissions)

    print(f"Fichier '{nom_fichier}' généré avec {nbr_donnees} députés, {len(projetsDeLoi)} lois et {len(allCommissions)} commissions.")



# extaire_deputes_depuis_json('deputes.json')
# extraire_lois_depuis_json('projet_loi.json')
# extraire_commissions_depuis_json('projet_loi.json')
generer_donnees_xml('assemblee_nationale.xml', 165)
