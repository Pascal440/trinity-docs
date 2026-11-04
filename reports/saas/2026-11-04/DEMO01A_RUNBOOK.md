# DEMO-01A — Runbook du laboratoire

Le [kit](demo01a-kit/) contient le profil hors ligne, les manifests, les scripts et les entrées fictives. Versions retenues Open WebUI 0.13.0 slim et Open Terminal 0.16.0 complet sur linux/amd64. Références officielles par digest et identifiants Docker dans le [manifeste](demo01a-kit/image-manifest.json).

## Vérification et démarrage

Sur le VPS autorisé, se placer dans le dossier `demo01a-kit`. Le lanceur vérifie au moins quatre CPU, 4 Gio de RAM disponible, 20 Gio libres, le port local 18760, les deux images locales épinglées et les trois empreintes d’entrée. Si une image manque, son téléchargement par digest est une opération opérateur distincte, à évaluer avec les ressources disponibles. Si la capacité est insuffisante, arrêter la préparation sur cet hôte.

```sh
sudo python3 start.py --check
sudo python3 start.py
```

La première commande crée les deux conteneurs, prépare le compte et les entrées, vérifie le catalogue vide et retire les conteneurs. La seconde maintient la session au premier plan, au maximum deux heures depuis le lancement. L’écoute UI se limite à `127.0.0.1:18760`. Le lanceur affiche un chemin privé sous `/dev/shm` contenant les identifiants temporaires à consulter côté opérateur.

```sh
ssh -N -L 18760:127.0.0.1:18760 <alias-ssh-vps>
```

Ouvrir `http://127.0.0.1:18760` depuis le poste opérateur, utiliser le compte non administrateur et sélectionner **Atelier Boréal — Terminal**. Les entrées sont dans `runtime01/inputs` du Terminal. Le compte admin sert uniquement au paramétrage local.

Le lanceur utilise UID/GID 1000, racines en lecture seule, capacités supprimées, no-new-privileges et init Docker. Plafonds de 1 CPU par conteneur, WebUI 1 Gio et 384 processus, Terminal 2 Gio et 512 processus. Les données et le home sont des tmpfs distincts de 512 Mio. WebUI partage le namespace network none du Terminal dans ce profil hors ligne. Aucun socket Docker ou volume client monté et aucun port Docker publié. Le relais UI utilise une cible fixe et douze connexions simultanées au maximum.

## Export Excel et préparation des téléchargements

1. Télécharger le XLSX original depuis l’onglet Fichiers vers un répertoire opérateur distinct. Choisir un nom de PDF dédié, différent du PDF d’analyse.
2. Sur l’hôte de laboratoire, lancer la conversion sur la copie téléchargée. Le script exige 2 Gio de mémoire disponible, une destination neuve et un XLSX d’au plus 25 Mio.
3. Réimporter le PDF d’aperçu dans le dossier de livrables du Terminal par le navigateur de fichiers. Ouvrir ce PDF dans WebUI. Laisser le XLSX original et le PDF d’analyse disponibles au téléchargement.

```sh
sudo python3 preview.py /chemin/demo/Synthese-v1.xlsx /chemin/demo/Synthese-v1-apercu.pdf
```

Le worker utilise LibreOffice et UNO de l’image Terminal épinglée. Il ouvre une copie en lecture seule, demande l’interdiction des macros et des mises à jour de liens, appelle `calculateAll()` puis exporte une page par feuille. Le réseau est fermé, les échanges transitent par stdin/stdout sans montage, et les limites sont 768 Mio, 1 CPU, 128 processus et 60 secondes côté lanceur. L’export est manuel et distinct du rendu natif. Contrôler les feuilles exportées, le zoom, les valeurs et le graphique avant présentation. Un [exemple opérateur](demo01a-kit/preview-example/SMOKE_NOT_LLM-apercu.pdf) accompagne le [classeur de contrôle](demo01a-kit/preview-example/SMOKE_NOT_LLM-cache-faux.xlsx).

## Arrêt et reprise

Exporter les livrables et les preuves utiles avant l’arrêt. Ctrl-C ou SIGTERM retire les deux conteneurs du lancement et efface ses fichiers temporaires. Le superviseur de session ferme l’écoute à l’échéance ou sous 1 Gio de mémoire disponible. Cette durée de session ne constitue pas un timeout par commande Terminal. Le chemin de fermeture sur interruption brutale du superviseur ou de Docker relève de l’opérateur.

En cas d’interruption brutale, inspecter uniquement les objets de démo. Après vérification des IDs et du label, retirer les objets de ce lancement par leurs IDs explicites.

```sh
sudo docker ps -a --filter label=mission=demo01a
sudo docker rm -f <id-webui-demo01a> <id-terminal-demo01a>
```

Les données de session disparaissent au retrait. Reprendre à partir du kit et des entrées originales avec une nouvelle vérification des ressources.
