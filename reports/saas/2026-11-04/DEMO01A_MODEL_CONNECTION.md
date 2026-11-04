# DEMO-01A — Raccordement OpenAI-compatible

Le kit livre un profil hors ligne exécutable. `ENABLE_OPENAI_API=false`, Ollama et les connexions directes navigateur désactivés. L’adresse WebUI préparée est `http://127.0.0.1:18081/v1`. Ce port est inutilisé dans le profil livré. Le [gabarit de politique](demo01a-kit/model-policy.example.json) est désactivé et son budget externe vaut 0 €. Aucun fournisseur ni relais sortant mis en service.

## Schéma retenu pour la mise en service autorisée

Conserver les deux conteneurs en `--network none` dans des namespaces distincts pour cette variante. La séparation permet de réserver le listener modèle au loopback de WebUI. Deux sockets Unix de session distinctes servent de frontière applicative.

| Flux | Transport et frontière |
| --- | --- |
| Poste opérateur → WebUI | Tunnel SSH et listener hôte loopback. Relais à cible fixe vers le port 8080 **dans WebUI** pour la variante à namespaces séparés. |
| WebUI → Terminal | Adaptateur loopback WebUI sur 8000 vers une socket Unix dédiée. Serveur de socket dans Terminal vers son propre 8000. Authentification Terminal existante et transfert HTTP/WebSocket conservés. |
| WebUI → fournisseur | Adaptateur loopback WebUI sur 18081 vers une seconde socket Unix. Celle-ci est créée par un relais applicatif de l’hôte et montée uniquement dans WebUI. La socket Terminal ne relaie que vers le port local du Terminal. |

Les deux adaptateurs sont à mettre en service et à vérifier lors de la recette autorisée. Le lancement hors ligne livré ne crée ni ces montages ni ces sockets. L’opérateur installe les adaptateurs uniquement dans les objets temporaires de la variante, sans changement réseau global. Chaque dossier de socket est réservé à la session, avec accès local explicite. Aucun montage de secret fournisseur dans Terminal, aucun proxy générique, aucun chemin `CONNECT`, aucune publication TCP du Terminal. Le modèle ne doit recevoir ni identifiant administrateur WebUI, ni jeton du relais. Une mesure réseau depuis Terminal doit confirmer qu’il ne voit pas le listener modèle, sa socket ou un chemin Internet. Tester aussi les WebSocket du Terminal et du bureau après séparation, puisque cette topologie diffère de celle déjà qualifiée.

## Règles du relais fournisseur

- Une seule base HTTPS exacte, fixée côté relais par l’opérateur après approbation. TLS vérifié, redirections refusées, cible et port non dérivés des requêtes. Aucun choix d’URL côté WebUI, aucun proxy d’environnement ni repli automatique. En cas de changement du DNS ou de cible, vérifier la destination approuvée avant de reprendre.
- Autoriser uniquement `GET /v1/models` et `POST /v1/chat/completions` au chemin exact. Filtrer le catalogue sur un identifiant unique, rejeter tout autre modèle, route, requête hors limite ou clé locale absente. Conserver le streaming SSE si requis par l’interface et borner taille, temps et concurrence. Le relais ne transmet que les en-têtes nécessaires et injecte lui-même la clé amont.
- Configurer des plafonds positifs avant activation, une échéance et un plafond monétaire validé avec l’opérateur. Débiter le nombre d’appels à l’admission et couper si les compteurs, le budget ou la mesure d’usage deviennent indisponibles. Éviter les relances et tâches auxiliaires. Le plafond de tours d’outils du kit vaut 8 par réponse. Une réponse WebUI avec outils peut produire plusieurs requêtes amont.
- Conserver la clé amont dans le processus du relais ou dans un secret opérateur temporaire protégé, séparé du jeton local WebUI. Exclure les clés, corps et autorisations des journaux. Expirer le relais et supprimer ses accès à la fin de la recette.

## Configuration WebUI après validation des frontières

Dans le WebUI neuf, ouvrir **Administration → Paramètres → Connexions** et configurer une connexion OpenAI-compatible unique vers `http://127.0.0.1:18081/v1`, avec son jeton local et l’identifiant exact approuvé. Activer cette connexion seulement après les contrôles négatifs locaux. Sélectionner le modèle et ses appels de fonctions natifs dans le compte démo. Garder les tâches de titre, tags et relances désactivées. Une sortie autorisée enregistre uniquement les métriques utiles à la recette. L’arrêt du relais doit rendre le modèle indisponible.

**Option Together AI via Trinity Gateway.** La destination approuvée serait la base HTTPS de Trinity Gateway. Le modèle sélectionné dans WebUI serait l’ID public exposé par Gateway, confirmé par un catalogue autorisé. Faire confirmer par l’opérateur Gateway le fournisseur Together autorisé et l’absence de repli payant, les quotas et l’identité dédiée. Cette option ne suppose ni disponibilité d’un modèle précis ni modification de Gateway pendant DEMO-01A. Aucun accès GIPS réutilisé. L’essai direct TN-27Q préparé antérieurement n’est pas un prérequis et ne doit pas être exécuté pour cette préparation.
