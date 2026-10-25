# Recommandation d'Articles & Deploiement Serverless Azure

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Azure Functions](https://img.shields.io/badge/Microsoft%20Azure-Functions%20Serverless-0089D6?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI%20Interactive-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Certification-AI%20Engineer%20Project%209-success?style=flat-square)](#)

Preuve de concept (POC) d'un moteur de recommandation d'articles personnalises pour une application mobile de presse, alimente par une architecture cloud serverless sous Microsoft Azure.

---

## Objectifs du Projet

L'application de lecture d'articles a pour objectif d'augmenter l'engagement utilisateur avec des recommandations ciblees :

1. Recommander 5 articles adaptes a chaque utilisateur selon son historique de lecture.
2. Comparer deux approches de recommandation : filtrage base sur le contenu (Content-Based) et filtrage collaboratif (Collaborative Filtering).
3. Deployer le modele sur une architecture cloud serverless avec une Azure Function accessible via API REST.
4. Fournir une interface interactive Streamlit pour tester les recommandations en direct par identifiant utilisateur.

---

## Architecture

```text
[Interface Streamlit] ---> HTTP GET/POST (user_id) ---> [Azure Function Serverless]
        ^                                                         |
        |                                                         v
        +<--------- Reponse JSON (Top-5 scores) <--------- [Moteur d'Inference IA]
```

---

## Modélisation

### 1. Filtrage base sur le contenu (Content-Based Filtering)
* Utilise les embeddings textuels d'articles pour representer les sujets abordes.
* Calcule la similarite cosinus entre le vecteur profil moyen de l'utilisateur et l'ensemble des articles.
* Permet de recommander des articles recents sans historique prealable (mitigation du cold-start).

### 2. Filtrage collaboratif (Collaborative Filtering)
* Exploite la matrice d'interactions utilisateurs-articles.
* Entraine des modeles de factorisation matricielle (SVD) et de plus proches voisins (k-NN) pour identifier des groupes d'utilisateurs aux comportements similaires.
* Permet de decouvrir des contenus au-dela des themes habituels de l'utilisateur.

### 3. Approche Hybride
* Combine les scores de similarite thematique et comportementale.
* Trie et renvoie les 5 articles les plus pertinents avec leur score associe.

---

## Deploiement Serverless (Azure Function)

Le moteur d'inference est encapsule dans une Azure Function HTTP Trigger (Python) :
* Point d'entree : Endpoint HTTP recevant le parametre `user_id` (en query string `?user_id=...` ou dans le corps JSON).
* Format de reponse :
  ```json
  {
      "Article N 68866": "(similarity score = 0.892)",
      "Article N 12480": "(similarity score = 0.845)",
      "Article N 23412": "(similarity score = 0.812)",
      "Article N 58921": "(similarity score = 0.798)",
      "Article N 91024": "(similarity score = 0.774)"
  }
  ```
* Avantages : Facturation a l'usage, mise a l'echelle automatique lors des pics de charge, gestion d'infrastructure simplifiee.

---

## Structure du Repertoire

```text
.
├── AF/                                                # Projet Azure Functions
│   └── serverLessFunc/
│       ├── HttpTriggerFunc/
│       │   ├── __init__.py                            # Logique de la fonction et inference
│       │   └── function.json                          # Configuration des bindings
│       ├── host.json
│       ├── local.settings.json                        # Variables d'environnement locales
│       ├── requirements.txt                           # Dependances Azure
│       └── sorted_recomendations.pckl                 # Matrice de recommandations
├── Guitarian_Guillaume_1_scripts_012023.ipynb         # Notebook d'analyse et de modelisation
├── Guitarian_Guillaume_2_application_Streamlit_012023.py # Interface web Streamlit
├── Guitarian_Guillaume_4_présentation_012023.pdf      # Support de presentation
├── collaborative_filtering_recommandations.pckl       # Modele collaboratif serialise
├── content_base_filtering_recommandations.pckl        # Modele content-based serialise
├── sorted_recomendations.pckl                         # Recommandations precalculees
└── README.md                                          # Documentation du projet
```

---

## Demarrage et Execution Locale

### 1. Cloner le depot et installer les dependances
```bash
git clone https://github.com/ImRobot777/OCR_IA_P9.git
cd OCR_IA_P9
python3 -m venv .venv
source .venv/bin/activate
pip install -r AF/serverLessFunc/requirements.txt streamlit pandas requests
```

### 2. Demarrer l'Azure Function en local
*(Necessite Azure Functions Core Tools)* :
```bash
cd AF/serverLessFunc
func start
```
L'API locale sera accessible sur : `http://localhost:7071/api/HttpTriggerFunc?user_id=123`

### 3. Lancer l'application Streamlit
Dans un second terminal, depuis la racine du depot `OCR_IA_P9` :
```bash
source .venv/bin/activate
streamlit run Guitarian_Guillaume_2_application_Streamlit_012023.py
```
L'interface s'ouvre sur `http://localhost:8501/`.

---

## Auteur & Certification

* **Etudiant :** Guillaume Guitarian
* **Cursus :** OpenClassrooms - Ingenieur IA (Projet 9)
* **Date :** Janvier 2023
