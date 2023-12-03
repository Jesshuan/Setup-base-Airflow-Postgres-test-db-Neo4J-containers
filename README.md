## DEEPMICROBIOT - GRAPH DB
## PROOF OF CONCEPT

(en construction)

#### Architecture

3 Folders:
- AIRFLOW
- POSTGRES
- NEO4J

Les trois dossiers correspondent à trois containers distincts pour cette phase de test.
Chaque container est à même de communiquer en local, hors d'un réseau interne Docker.

#### Lancement des containers en local

##### 1 - POSTGRES DB DE TEST:

- Dans le fichier docker compose, il est possible de changer préalablement le password du user. Par défaut : 'my_pass'

- Lancement du container avec la commande :
```
$ cd POSTGRES_DB

$ docker compose up
```


Précisions:

- Le port de sortie côté localhost est volontairement défini sur 5433 (et pas 5432), pour éviter tout conflit avec la database d'Airflow en local et/ou une base de données Postgres en local

- Selon l'interface, la database par défault est "postgres-db"

- le user par défaut en postgres est "postgres"

Visualisation :

- une interface adminer de visualisation est également lancée et peut être visible via l'adresse : "http://localhost:8090"



##### 2 - NEO4J:

- Avant de lancer le container pour la première fois, il est important de vérifier que tout le dossier "NEO4J" soit clean de tout autre dossier ou fichier que le fichier "docker-compose.up"... En effet, Neo4j a besoin d'écrire dans des dossier de config en étant propriétaire de ces dossiers. Veillez donc à supprimer, s'ils sont présents, les dossiers conf, data, import, logs et plugins...

- Lancement du container avec la commande :
```
$ cd NEO4J

$ docker compose up
```

Visualisation :

Deux interfaces de visualisations sont possibles:

- se connecter à l'adresse locale : "http://localhost:7474" 

- Utiliser "Neo4j Desktop" si le logiciel est présent sur l'ordinateur. Une fois le logiciel lancé, "Add" => "Remote connection". Nommer la nouvelle base de données.

Définition du mot de passe :

La définition d'un nouveau mot de passe pour Neo4j se fait normalement lors d'une première connection à l'interface.
Initialement, l'id_user par défaut est : neo4j
Et le mot de passe est : neo4j

À la première connexion, il est possible de redéfinir ce user et  mot de passe.


##### 3 - AIRFLOW :

- (Optionnel ) Sous Linux, il est possible d'enlever un message d'alerte en accordant les bons droits users au moment de la création des sous-dossiers :

 La commande est (depuis le dossier 'AIRFLOW' à la racine):
'
$ mkdir -p ./dags ./logs ./plugins
$ echo -e "AIRFLOW_UID=$(id -u)" > .env
'

Hors Linux, les dossiers dags, logs, plugins... sont créés automatiquement.
Il est posible d'ajouter un fichier .env à la main à la racine du dossier avec :
'AIRFLOW_UID=50000'

(voir encart 'Setting the right Airflow user' on https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

- lancer la commande : ' docker compose up airflow-init ' car il faut initialiser en premier lieu ce container

- lancer ensuite la commande : 'docker compose up ' pour lancer tous les autres containers

- L'interface airflow est visible en local à l'adresse localhost par défaut : 'http://localhost:8080'

- Connection à la Database POSTGRES :

Il faut ajouter une nouvelle Connection "Postgres" sous Airflow (Admin -> Connections) avec les paramètres suivants :
```
Connection Id : postgres_local
Host : 172.17.0.1 (sous Linux, sous Windows et Mac -> essayer "host.docker.internal" )
Login : postgres
Password : ('my_pass' par défault si non changé dans le fichier docker-compose de Postgres)
Port : 5433
```

Puis: enregistrer la nouvelle Connection

- Connection à la Database NEO4J :

Il faut ajouter une nouvelle Connection "Neo4j " sous Airflow (Admin -> Connections) avec les paramètres suivants :
```
Connection Id : neo4j_local
Host : 172.17.0.1 (sous Linux, sous Windows et Mac -> essayer "host.docker.internal" )
Login : neo4j
Password : (défini par l'utilisateur au lancement de la DB NEO4J, à la première connection)
Port : 7687
```

Solution alternative en cas de problème :
Dans Airflow -> backend_files, il y a un fichier de connection défini dans conn.json dans lequel il est possible de spécifier une nouvelle connection.
Il est ensuite possible de créer un Neo4JHook à partir de cette connection.

Puis: enregistrer la nouvelle Connection

- Lancer le DAG 'init_extract_files_to_db_dag' pour commencer une première extraction depuis les bases de données vers la DatabasePostgres

- Après écriture dans la base de données Postgres, lancer le dag 'generate_all_neo4j_graph' pour générer les noeuds et relations dans le graph Neo4j


#### Développement en local / Database Neo4j en Remote

Dans l'optique d'une phase intermédiaire de développement, où les développeurs continuent à travailler en local... (via les containers POSTGRES et AIRFLOW) mais le résultat (NEO4J) doit être visible pour d'autres équipes.

La base de données NoSQL orientée graphe sous Neo4J doit être hébergé sur un serveur de l'entreprise, ou sur le cloud.
Un outil gratuit AuraDB est directement proposé par Neo4j pour cette hébergement. (il est cependant limité à 200k neouds et 400k relations). Cet outil peut également être débloqué en version payante (AuraDB Professional) pour ne pas être limité. (https://neo4j.com/pricing/).
Le grand avantage de rester avec AuraDB est une simplification de la maintenance et une optimisation des performances.
Il existe également des interface de gestion sur la plupart des plateformes cloud connus (AWS, GCP...).


Dans l'hypothèse, où par exemple, nous avons mis en place une instance distance via AuraDB :

À la création de l'instance il est proposé de récupérer les infos : URI, ID, PASSWORD de la base de donnée...

Il faut alors changer la connection dans Airflow de la manière suivante :

```
Connection Id : neo4j_remote
Host : <ID>.databases.neo4j.io (l'URI fourni par l'instance, sans le "neo4j+s://" ou le "bolt:// devant")
Login : neo4j
Password : (fourni par l'instance)
Port : 7687
Extra : {"encrypted":true} (cet ajout est indispensable pour les shémas type "neo4j+s" au moment d'écrire ces lignes)
```

- Ne pas oublier de changer l'hypervariable dnas le DAG de génération du graphe Neo4j. (CONNECTION_NEO4J = "neo4j_remote") pour basculer du local au remote