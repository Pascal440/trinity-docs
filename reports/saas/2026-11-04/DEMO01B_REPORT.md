# DEMO-01B — Préparation de l’essai Together AI

4 novembre 2026, heure de Paris. Base documentaire `reports/demo01a-preparation` au commit `205e230919f366ad349c9788a6b7ef6a81323151`, [PR DEMO-01A #7](https://github.com/Pascal440/trinity-docs/pull/7).

**Recette réelle tentée. Le relais s’est fermé au premier appel amont et aucun livrable n’a été généré.**

L’opérateur a autorisé l’utilisation d’une copie privée de la clé existante et confirmé la désactivation de la recharge automatique. Le catalogue authentifié a accepté le modèle et les tarifs attendus. Le modèle a été rendu visible uniquement au compte de démonstration par un droit local. Les deux messages ont été envoyés via l’API de conversation d’Open WebUI et ont le même identifiant de chat. Les métriques et la limite du diagnostic sont consignées dans les [résultats](DEMO01B_RESULTS.md). Les deux conteneurs temporaires et l’accès fournisseur ont été retirés après collecte. Le verrou de budget a été conservé.

## Préparation historique

Lors de la préparation, aucun accès Together utilisable n’avait été trouvé et aucune inférence n’avait été lancée.

La recherche s’est limitée à la présence de `TOGETHER_API_KEY`, de `/run/secrets/together_api_key` et de `/home/codex/.config/demo01b/together.key`. Aucun accès utilisable dans ce périmètre. L’opérateur doit déposer une clé autorisée pour cette mission dans le dernier fichier, appartenant à `codex` et en mode `0600`. Une notification lui a indiqué le chemin. Aucun appel au catalogue authentifié. Together publie `Qwen/Qwen3.8-Flash` comme ID serverless, à confirmer dans le catalogue actif de l’identité fournie. Le tarif public consulté est 0,15 USD/M tokens d’entrée et 0,47 USD/M de sortie. [Fiche modèle](https://www.together.ai/models/qwen3-8-flash) · [Tarifs](https://www.together.ai/pricing).

## Recréation et frontière réseau

Le `--check` du kit publié est passé sur les deux images épinglées, le compte de démo, le grant, le catalogue vide et les trois empreintes d’entrées. La [variante split](demo01b-kit/start_split.py) a également démarré et passé les contrôles de séparation. Les deux conteneurs ont chacun leur namespace Docker `none`. WebUI joint le Terminal par une socket d’API dédiée. Une autre socket, réservée à WebUI, relaie vers le modèle. La réponse de contrôle locale n’est pas un modèle et n’a pas été utilisée dans une conversation. Depuis Terminal, l’accès au listener modèle et à Internet échoue. Le dossier modèle et le socket Docker y sont absents. Aucun port Docker publié. Les deux lots temporaires ont été retirés.

La première tentative split joignait le Terminal, mais la socket de contrôle modèle appartenait à root. La correction attribue la socket de test à l’UID 1000, puis le contrôle complet passe. Aucun changement de privilège des applications. Le fonctionnement des WebSocket de bureau et la chaîne d’outils avec un vrai modèle restent à observer dans cette variante. Les validations mécaniques RUNTIME-01 restent historiques.

## Relais et borne

Le [relais](demo01b-kit/together_relay.py) écoute sur une socket Unix privée. Il contrôle le jeton local, confirme l’ID exact, le type chat, le contexte et les tarifs par le catalogue authentifié avant d’ouvrir la socket. Les seules routes sont `GET /v1/models` et `POST /v1/chat/completions`. Destination TLS fixe `api.together.xyz:443`, aucune redirection ni URL fournie par l’appelant. Corps textuel limité à 256 Kio, fonctions locales seulement, une réponse par requête, un appel à la fois, délai d’admission de 20 minutes et aucune relance. L’appel amont est non streamé. Une réponse SSE groupée est restituée si WebUI la demande. Le contrat SSE a été contrôlé sur réponse locale, pas en session réelle WebUI/Together.

Le relais réserve **avant envoi** un contexte maximal de 1 100 000 tokens et 4 096 tokens de sortie, soit 0,16692512 USD par appel aux plafonds retenus. Huit réservations donnent 1,33540096 USD. Avec un facteur tout compris confirmé au plus à 3 EUR par USD facturé, la borne est **4,00620288 €**, sous 5 €. Un plafond USD indépendant vaut 1,50. Ni un change de marché ni une taxe n’ont été présumés. Confirmer la borne tout compris et l’absence de frais fixes ou de facturation additionnelle avant le lancement. Si catalogue, frais ou plafonds ne peuvent être qualifiés, garder le relais fermé. Une erreur ou un usage absent/incohérent ferme la session et conserve la réservation. Le marqueur de budget fixe interdit un redémarrage sous la même autorisation.

Les contrôles HTTP Unix avec une fonction amont locale ont refusé un appel anonyme, une route et un modèle hors liste, un outil hébergé et un neuvième appel. Ils ont également contrôlé le format SSE. Ce sont des preuves du garde local, pas une preuve de facturation Together.

## Reprise opérateur conditionnelle

1. Déposer la clé dédiée en mode 0600 et confirmer le facteur tout compris documenté. Garder le chemin de verrou ci-dessous identique pour la mission. Vérifier à nouveau les ressources avant de lancer le split. Le serveur est au premier plan et borné à 20 minutes, avec arrêt si la réserve mémoire tombe sous 1 Gio.

   ```sh
   cd demo01b-kit
   sudo env PYTHONDONTWRITEBYTECODE=1 python3 start_split.py
   ```

2. Prendre le répertoire de session indiqué par le lanceur. Depuis la session SSH de `codex`, créer un jeton local aléatoire dans ce répertoire et démarrer le relais au premier plan. `FACTOR` doit porter la borne opérateur confirmée, pas un taux estimé sans justificatif.

   ```sh
   umask 077
   python3 -c 'import secrets; print(secrets.token_urlsafe(32))' > "$SESSION/model.token"
   python3 together_relay.py --key-file /home/codex/.config/demo01b/together.key \
     --local-token-file "$SESSION/model.token" --socket "$SESSION/model/api.sock" \
     --budget-lock /home/codex/.config/demo01b/budget.lock \
     --eur-per-usd-inclusive "$FACTOR" --confirm-one-session
   ```

3. Depuis le tunnel privé `ssh -N -L 18760:127.0.0.1:18760 <alias-vps>`, ajouter dans l’administration du WebUI neuf la connexion unique `http://127.0.0.1:18081/v1` et son jeton local. Vérifier le catalogue filtré. Activer les appels de fonctions natifs et sélectionner le modèle exact avec le compte démo. Conserver les générations auxiliaires et connexions directes désactivées. Exécuter une seule fois le [scénario Atelier Boréal](DEMO01A_SCENARIO.md), V1 puis V2 dans le même chat, avec conservation des originaux et empreintes. Stopper si le plafond est atteint, sans autre modèle ni second essai.
4. Exporter les preuves et mesurer les valeurs de [résultats](DEMO01B_RESULTS.md). Arrêter le relais et la session, vérifier la disparition des sockets, écoute et conteneurs. Laisser le marqueur de budget pour l’audit. L’opérateur retire l’accès de mission de son stockage dédié ou révoque la clé selon sa politique. Le code ne supprime pas une clé de l’opérateur.

Aucun accès fournisseur n’a été activé pendant cette mission. Les contrôles effectués portent sur les objets DEMO-01B et les accès anonymes des consoles existantes.
