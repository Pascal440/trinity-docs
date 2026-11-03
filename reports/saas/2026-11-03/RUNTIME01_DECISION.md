# RUNTIME-01 — Décision proposée à Maya

**GO laboratoire technique isolé. NO-GO démonstration client présentée comme génération autonome complète ; NO-GO déploiement commercial.**

3 novembre 2026, contrôles en UTC. Dépôt documentaire `Pascal440/trinity-docs`, branche `reports/runtime01-lab`, base `reports/launch06-release-candidate` / `5f1f6072bcbd5ca587b18fac84250e497fed8b12`. Aucun dépôt technique publié/modifié. Code Gateway consulté : `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` ; référence Infra inchangée `5bd6fee98a468191613766e0093bdcda8de59099` et Portal LAUNCH-06 `6df4b5a338ac84bd928610292981962eeedd9ee6`. Scripts de laboratoire locaux séparés ; SHA documentaire final fourni dans la PR/livraison.

## Acquis

Open WebUI 0.13.0 et Open Terminal 0.16.0 officiels sont épinglés, leurs contrats mécaniques exercés : onglets, terminal, quatre formats en aperçu/téléchargement, bureau virtuel et Chrome avec actions natives. Le compte de démo est non administrateur. Les ressources et l’accès sont bornés, aucun accès privilégié hôte depuis le terminal, D8 et ses quatre previews inchangés. Les trois entrées fictives et le contrôle numérique indépendant sont prêts. Aucun coût d’inférence externe engagé par cette mission.

## Non acquis, sans simulation

TN-27Q est une référence fonctionnelle GIPS acceptée ; on ne recommence pas son benchmark de capacité isolée. Il manque **son accès autorisé depuis ce labo** : aucune identité RUNTIME-01/démo identifiée par les critères audités, aucune clé utilisable confirmée et aucun fournisseur actif déclarant explicitement les identifiants TN-27Q/Qwen3.8 examinés. Pas d’appel à GIPS et pas de conclusion sur sa disponibilité intrinsèque.

Les trois essais et la génération/modification dans le même chat sont non exécutés. Qualité, exactitude des livrables IA, corrections autonomes, latence et tokens/coût sont non mesurés. Les contrôles opérateur ne remplacent pas ces preuves. Les limites Excel (formules sans cache et graphique dans l’aperçu) et de durée/ressources restent visibles.

## Proposition concrète d’accès, à autoriser avant exécution

1. Identifier formellement un accès **déjà dédié et autorisé**, s’il existe sous un autre nom ; sinon autoriser un client distinct `runtime01-demo`, un plan de quota et une clé distincte, sans reprise d’une clé GIPS/production ni d’un client D8.
2. Identifier le **public_id et provider key exacts** du routage TN-27Q approuvé. Les allowed_models/allowed_providers doivent contenir uniquement ces valeurs, jamais une liste vide. Si ce routage exige une modification Gateway ou GIPS, stopper cette étape et obtenir son autorisation séparée ; aucune configuration n’est changée dans RUNTIME-01.
3. Plafonds initiaux proposés pour arbitrage, non appliqués : 6 requêtes/minute, 60/heure, 120/jour et 120/mois pour cette identité éphémère ; `tokens_per_request=4096`, 500 000 tokens/jour et mois ; une requête à la fois côté démo ; expiration de clé après 2 h de recette, révocation après export des preuves. Chat via l’interface de démo seulement, autres fonctionnalités désactivables du plan à false ; aucun fournisseur payant de secours. Le code partage can_use_chat avec embeddings : une restriction HTTP du raccordement devra être vérifiée avant d’annoncer une clé limitée au chat. **Budget externe inchangé : 0 €.** Si le plafond empêche trois essais, consigner l’arrêt et demander arbitrage, sans le relever silencieusement.
4. Conserver la clé en fichier secret opérateur/WebUI, jamais dans le terminal, les rapports, l’URL ou les conversations. Raccorder WebUI à ce seul endpoint par un flux applicatif approuvé tout en maintenant l’egress Terminal fermé. Le relais UI actuel ne fournit **aucun** flux vers le modèle ; ce raccordement n’est pas déjà actif.
5. Avant les essais, régler et vérifier borne d’itérations d’outils, durée de commande et accès financier selon le profil Gateway effectif. Ne pas désactiver un contrôle global, attribuer des crédits à un client existant ou contourner le ledger. Puis appliquer le [protocole des trois essais](RUNTIME01_DEMO_RESULTS.md), dans des sessions jetables séparées et séquentielles.

## Mécanismes existants réutilisables et pièges constatés

`GatewayApiKeyService::generateForClient`, `GatewayApiKey` et le contrôleur admin émettent une clé aléatoire et stockent son SHA256. Le clair est disponible au moment d’émission, pas récupérable à partir du hash ; aucune tentative de récupération de clé existante. `expires_at` et sa validation existent, mais l’émission admin examinée met cette date à null : une clé générée par défaut **n’est pas automatiquement éphémère**. Expiration explicite à inclure dans toute opération future autorisée.

`GatewayClientPlan` / `GatewayPlanLimit` et `PlanAccessManager` portent le plan actif, les modèles/fournisseurs permis et les fonctionnalités ; absence de plan/limites refuse l’accès. `QuotaManager` gère fenêtres de requêtes et tokens, SQL ou Redis selon configuration, et `GatewayRequestRecorder` conserve mesures de tokens/coûts et leur statut. Aucun de ces mécanismes n’est réécrit.

**Attention aux conventions existantes :** une limite numérique nulle ou ≤0 est non bornée, pas « budget nul » ; une liste de modèles/fournisseurs vide autorise tous. Le budget externe 0 € est ici respecté par l’absence de fournisseur/clé d’inférence activés, pas par des quotas numériques mis à zéro. `tokens_per_request` compare le max_tokens demandé, pas toute la longueur du contexte ; les totaux journaliers reposent sur l’usage enregistré et ne constituent pas une garantie de plafond monétaire strict à la requête près. Les valeurs proposées ne sont pas une preuve de dimensionnement de TN-27Q.

## Arbitrage demandé

Valider ou fournir l’identité dédiée, ses plafonds et le routage exact, puis autoriser explicitement le raccordement et la recette interne bornée. Together AI reste une option non activée ; aucun modèle externe payant ou budget nouveau n’est autorisé. Ne pas commander de GPU.

Les cinq rapports et preuves sont proposés en PR documentaire brouillon depuis LAUNCH-06. Les éléments techniques restent dans le répertoire local de laboratoire ; aucune publication Gateway/Infra/Portal et aucune fusion. L’interface privée expire automatiquement le 3 novembre à 17:59:13 UTC ; les rapports GitHub restent consultables. **Aucune correction Gateway, nouvelle identité, recette LLM, DEMO-01 ou mission suivante lancée automatiquement.**
