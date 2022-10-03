#!/usr/bin/python3
"""
--------------------------------------------------
Module pour aider à la création d'une page web cgi
--------------------------------------------------
Auteur : Franck Ayrault, ENM
V0 (mai 2016) : fonctions tracer_erreurs_web, requete et repondre
V1 (mai 2016) : remplacement de tracer_erreurs_web par tracer, recherche de compatibilité avec python 3
V2 (4/11/16) : ajout de repondre_json et de la fonction vue pour construire des parties de la page
V3 (9/12/16) : ajout de la possibilité de récupérer les variables d'environnement de la requete
V4 (23/11/17) : évolution majeure, perte de la compatibilité python 2 (utiliser la V3 pour toute application en python 2) afin de simplifier la maintenance
  - mise en cache des vues
  - suppression de la fonction tracer (traçage des erreurs systématiques, compte tenu de l'objectif pédagogique de ce module)
  - renommages de repondre en renvoyer, de repondre_json en servir, et de requete en valeur
  - ajout des accès aux web services (générateur service et fonction objet)
  - garantie des entrées-sorties en utf-8
V5 (6/02/18) : ajout de la réception de fichier depuis un formulaire web (fonction reception)
V6 (20/04/18) : ajout de paramètres optionnels dans les fonctions service et objet pour compléter l'url
V7 (29/03/19) : correction de bugs sur la fonction reception et sur la fonction valeur (cas sans argument)
V8 (13/05/20) : ajout de fournir, compatibilité python 3.8, débogage (mettre DEBUG = False si ça pose problème, en particulier pour faire un web service)
V1.0.0 (04/01/21) : changement de paradigme (inversion d'appel), perte de la compatibilité ascendante, utilisation du décorateur app, ajout d'un exemple
V1.0.1 (21/01/21) : correctifs (récupération de l'environnement via **env et forçage utf8)

NB : le forçage utf8 n'est garanti que si l'import de ce module est placé avant tout autre import !
"""


# Forçage utf8 pour le traitement correct des caractères accentués

import locale
locale.setlocale(locale.LC_CTYPE, 'fr_FR.utf8')
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
import sys
if sys.stdout.encoding not in ["utf-8", "UTF-8"] :
    def _write(data) :
        sys.stdout.buffer.write(data.encode("utf-8", errors='surrogateescape'))
    sys.stdout.write = _write


# Modules de la bibliothèque standard

import os
import cgi
import cgitb
import html
import json
import urllib.request
import inspect


# Correctifs apportés aux modules cgi et cgitb - ne pas utiliser directement en dehors du module

class _FieldStorage(cgi.FieldStorage) :
    def make_file(self) :
        self._binary_file = True
        return cgi.FieldStorage.make_file(self)


def _reset() :
    return 'Content-Type: text/html\n\n<!DOCTYPE html>\n<html lang="fr">\n<head><meta charset="UTF-8" /></head>\n'
cgitb.reset = _reset


# Fonctionnalités privées - ne pas utiliser directement en dehors du module

def _data(requete) :   # données envoyées par une requête AJAX POST
    try :
        data = requete.file.read().decode("utf-8")
        try :
            return json.loads(data)
        except :
            return html.escape(data)
    except :
        return None


def _param(nom, requete) :   # paramètre de la requête (GET ou POST)
    champ = requete[nom]
    if champ.filename :
        return champ   # représente un fichier uploadé
    else :
        return html.escape(champ.value)   # sécurité contre l'injection de code


def _type(sortie) :   # analyse la sortie pour déterminer le type de contenu de la réponse http
    if type(sortie) in [list, dict] :
        return "application/json"
    else :
        try :
            debut = sortie[:30]   # on analyse les 30 premiers caractères pour déterminer le type
            if any(c in debut for c in ["<!DOCTYPE html>", "<!--", "<html", "<head", "<body"]) :
                return "text/html"
            else :
                return "text/plain"
        except :
            return "application/json"


def _finalisation(sortie, type_de_contenu) :   # finalisation de la réponse http
    if type_de_contenu == "application/json" :
        return json.dumps(sortie, ensure_ascii = False, indent = 2)
    elif type_de_contenu == "text/plain" :
        return html.unescape(sortie)
    else :
        return sortie


def _entete(type_de_contenu) :   # entête http
    return "Content-type: " + type_de_contenu + "; charset=utf-8\n"


def _cgi(fonction, debug = True) :   # surcouche cgi
    if debug :        
        cgitb.enable()
    requete = _FieldStorage()   # paramètres de la requête web, transmis par la passerelle cgi
    params = {}
    for param in inspect.signature(fonction).parameters.values() :
        nom = param.name
        if param.kind == param.VAR_KEYWORD :   # cas du paramètre **env
            params.update(os.environ)   # tout l'environnement
        elif nom == "__data__" :   # données reçues d'une requête AJAX
            params[nom] = _data(requete)
        else :
            try :
                params[nom] = _param(nom, requete)   # paramètre trouvé dans la requête
            except :
                try :
                    params[nom] = os.environ[nom]   # paramètre trouvé dans l'environnement
                except :
                    pass    # on laisse la valeur par défaut faute d'avoir trouvé le paramètre quelque part
    sortie = fonction(**params)   # exécution de la fonction
    type_de_contenu = _type(sortie)
    for output in [_entete(type_de_contenu), _finalisation(sortie, type_de_contenu)] :
        sys.stdout.write(output + "\n")


_cache = {}   # vues mises en cache pour éviter des accès disque répétés


# Fonctions publiques pour construire une application web

def vue(fichier, **args) :
    """Retourne la vue (une chaîne de caractères) résultant du 'peuplement' du fichier squelette.
       **args associe clefs et valeurs pour substitution des zones de type {clef} dans le squelette.
       Exemple : web.vue("bonjour.html", nom = "Dupont", prenom = "Jean")
                 --> retourne le contenu de bonjour.html en remplaçant {nom} par Dupont et {prenom} par Jean
    """
    if fichier in _cache :
        squelette = _cache[fichier]   # le fichier a déjà été lu, son contenu est dans le dictionnaire cache
    else :
        with open(fichier) as f :
            squelette = f.read()   # chaîne de caractères contenant tout le fichier
            _cache[fichier] = squelette   # mise en cache
    return squelette.format(**args)


def enregistrer(fichier, dossier = ".", sortie = None, ext = None) :
    """Enregistre le fichier soumis via le formulaire html appelant, et retourne son nom côté serveur.
       Le formulaire appelant doit être soumis via la méthode POST et en multipart/form-data :
       <form action="script.py" method="post" enctype="multipart/form-data">
       Le fichier à recevoir est nommé via l'attribut name dans le formulaire html appelant :
       <input type="file" name="fichier" />
       Le fichier reçu est enregistré côté serveur dans le dossier courant par défaut,
       sous le nom résultant de la concaténation de sortie et ext,
       par exemple image.jpg si sortie == "image" et ext == ".jpg"
       Si sortie est absent, le nom du fichier côté serveur sera identique au nom côté client.
       Si ext est absent (conseillé), l'extension sera automatiquement récupérée du nom du fichier côté client.
       Si fichier ne désigne pas un fichier uploadé, cette fonction renvoie None et aucun fichier n'est créé côté serveur.
    """
    if hasattr(fichier, "filename") and fichier.filename :
        nom = fichier.filename.rsplit(".", maxsplit = 1)   # exemple : nom = ["NORMALES", "data"] pour le fichier NORMALES.data
        if not sortie :
            sortie = nom[0]
        if not ext :
            try :
                ext = "." + nom[1]
            except IndexError :
                ext = ""
        with open((dossier + "/" + sortie + ext).encode("utf-8"), "wb") as f :   # copie et enregistrement du fichier (en mode binaire)
            f.write(fichier.file.read())
        return sortie + ext


def app(fonction) :
    """Décorateur transformant la fonction en application web.
       Les paramètres de la fonction sont lus dans la requête web,
       ou à défaut dans l'environnement (exemple : REMOTE_ADDR --> IP du client),
       ou à défaut :
       **env --> tout l'environnement (sous forme de dictionnaire)
       __data__ --> données envoyées par une requête AJAX POST
       Il est recommandé de donner une valeur par défaut à chaque paramètre de la fonction.
    """
    _cgi(fonction)


# Fonctions publiques pour accéder à un service web

def service(url, **args) :
    """Accède au web service désigné par l'url, avec les paramètres **args.
       service("http://site.fr/serv", a = 1, b = "2,3") est équivalent à service("http://site.fr/serv?a=1&b=2,3")
       Ce générateur renvoie le flux de lignes généré par l'url (à convertir en liste ou à parcourir par une boucle for).
       Exemple d'utilisation : for data in web.service("http://...") : ...
    """
    if args :
        url = url + "?" + "&".join(clef + "=" + str(args[clef]) for clef in args)
    for ligne in urllib.request.urlopen(url) :
        yield ligne.decode('utf-8').strip()


def objet(url, **args) :
    """Accède au web service désigné par l'url (url renvoyant un objet au format json), avec les paramètres **args.
       objet("http://site.fr/serv.json", a = 1, b = "2,3") est équivalent à objet("http://site.fr/serv.json?a=1&b=2,3")
       Cette fonction retourne l'objet python résultant du décodage de l'objet json renvoyé par l'url.
    """
    return json.loads("".join(service(url, **args)))


# Exemple : cloud basique (dépôt/téléchargement dans un dossier)

if __name__ == "__main__" :

    # Vues html (fichiers virtuels ici)
    _cache["page.html"] = '''<!DOCTYPE html>
                             <html lang="fr">
                               <head>
                                 <meta charset="UTF-8" />
                                 <title>Nuage test</title>
                               </head>
                               <body>
                                 <table>
                                   {liste}
                                 </table>
                                 <form action="web.py" method="post" enctype="multipart/form-data">
                                   <label for="fic">Ajouter un fichier</label>
                                   <input type="file" name="nouveau" id="fic"/>
                                   <button>Envoyer</button>
                                 </form>
                                 <p><a href="web.py?out=json">Voir la liste des fichiers sous forme de web service json</a></p>
                                 <p><a href="web.py?out=txt">Voir le liste des fichiers sous forme de texte brut</a></p>
                               </body>
                             </html>
                          '''
    _cache["fic.html"] = '''<tr>
                              <td>
                                <a href="fichiers/{fic}">{fic}</a>
                              </td>
                              <td>
                                <form action="web.py" method="delete">
                                  <button name="suppression" value="{fic}">Supprimer</button>
                                </form>
                              </td>
                            </tr>
                         '''

    # Dossier de stockage (nuage) - ce dossier doit déjà être créé sur le serveur avec tous les droits pour tous (777)
    DOSSIER = "fichiers"

    # Contrôleur
    @app
    def nuage(out = "html", nouveau = None, suppression = None) :
        """Application web affichant le contenu du dossier DOSSIER.
           out : format de sortie (html, json ou txt)
           nouveau : représente le fichier à déposer dans DOSSIER
           suppression : nom du fichier à supprimer dans DOSSIER
        """
        enregistrer(nouveau, dossier = DOSSIER)
        try :
            os.remove((DOSSIER + "/" + suppression).encode("utf-8"))
        except :
            pass
        ls = os.listdir(DOSSIER)
        if out == "html" :
            ls_html = ""
            for fic in ls :
                ls_html = ls_html + vue("fic.html", fic = fic)
            return vue("page.html", liste = ls_html)
        elif out == "json" :
            return {"liste des fichiers" : ls}
        else :
            return "Liste des fichiers :\n" + "\n".join(ls)

