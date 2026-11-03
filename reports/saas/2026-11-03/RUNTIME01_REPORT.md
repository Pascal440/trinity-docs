# RUNTIME-01 — Laboratoire Open WebUI et Open Terminal

**Volet technique qualifié. Démonstration LLM non exécutée faute d’accès dédié autorisé. Le critère final de génération puis modification par l’IA n’est pas atteint.**

3 novembre 2026, contrôles en UTC. Dépôt documentaire `Pascal440/trinity-docs`, branche `reports/runtime01-lab`, base `reports/launch06-release-candidate` / `5f1f6072bcbd5ca587b18fac84250e497fed8b12`. Aucun dépôt technique publié/modifié. Code Gateway consulté : `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` ; référence Infra inchangée `5bd6fee98a468191613766e0093bdcda8de59099` et Portal LAUNCH-06 `6df4b5a338ac84bd928610292981962eeedd9ee6`. Scripts de laboratoire locaux séparés ; SHA documentaire final fourni dans la PR/livraison.

## Périmètre et décision respectés

La mise à jour Maya remplace 0.12.5 par **Open WebUI v0.13.0** ; Open Terminal reste **0.16.0**. L’arbitrage modèle fixe un budget externe de **0 €**, interdit toute clé de production/GIPS implicite et toute création d’identité sans autorisation. Aucun fournisseur alternatif ni serveur Together AI commandé, aucun appel d’inférence lancé par RUNTIME-01.

Deux images officielles sont exécutées par digest, sur linux/amd64 : WebUI slim `sha256:9c583de5686ed3f92e992a9326a99225e951047176ccc5644fcd4352b77eb959` ; Terminal complet `sha256:28adefe59c450e4010862f25300a4c7e023de463779538dbee8818769911c835`. Les versions effectives sont confirmées par API/métadonnées Python. Le code applicatif amont n’est pas modifié ; aucun montage des sources de développement. [Compatibilité détaillée](RUNTIME01_COMPATIBILITY.md).

## Résultats effectivement démontrés

- Connexion système Open Terminal découverte par WebUI, puis partagée explicitement avec un **compte de démonstration non administrateur**. Un compte opérateur distinct administre uniquement ce WebUI neuf.
- Nouvel espace à onglets : fichiers simultanés, plein écran, terminal avec commande réellement exécutée et sortie websocket observée, Desktop avec canvas VNC réel, Browser en mode Chrome. Le navigateur et les actions natives partagent la session du compte de démo avant premier message.
- Excel, Word, PDF et PowerPoint : quatre aperçus UI ouverts ; quatre téléchargements déclenchés depuis l’UI, comparés octet pour octet aux originaux. Les routes d’aperçu et téléchargement du proxy authentifié sont également exercées. Ces documents sont **préparés par l’opérateur et marqués SMOKE_NOT_LLM**, pas des productions IA.
- Bureau virtuel Linux : LibreOffice Calc ouvre le classeur de contrôle, recalcule ses sommes et affiche son graphique dans le contexte opérateur. Le bureau du compte de démo est aussi réellement connecté dans l’interface. Ce n’est pas le bureau du VPS.
- Chrome : formulaire d’une page fictive locale rempli et validé, par les actions natives du même compte que l’onglet. Ni visite publique ni accès au serveur hôte.
- Les trois véritables documents **d’entrée** fictifs sont lus par `read_file` ; `run_command` exécute une commande de contrôle. Le script indépendant calcule la référence numérique à partir des entrées. Aucun résultat LLM n’a été évalué.

## Blocage modèle confirmé

Lecture SQL directe, limitée à des compteurs de métadonnées, sans bootstrap Laravel ni appel d’inférence : aucune identité nommée RUNTIME-01/démonstration trouvée par les critères nom/slug, aucune clé active correspondante, aucun fournisseur actif déclarant explicitement TN-27Q ou Qwen3.8 dans `supported_models`. Aucune clé API, hash de clé ou donnée personnelle client extraite. Cette recherche ne certifie pas l’absence d’un accès connu sous un autre nom et ne teste pas GIPS ; elle ne fournit **aucun accès autorisé utilisable** au laboratoire.

Les mécanismes existants d’émission SHA256, plan, quotas, modèles/fournisseurs autorisés et journalisation sont examinés en lecture seule. [Proposition concrète soumise à Maya](RUNTIME01_DECISION.md). Ni identité, clé, plan, crédit ni route créés ; aucun réglage Gateway/GIPS modifié. WebUI conserve ses API modèles désactivées. Aucun modèle factice, aucune fausse conversation et aucun fournisseur payant de remplacement.

## Ressources et continuité

Avant création : environ 188 GiB libres, 5,1 GiB de RAM disponibles sur 7,9 GiB, 4 CPU, sans swap. Images ajoutées : environ 0,87 Go WebUI et 7,24 Go Terminal décompressés ; environ 180 GiB libres ensuite. Plafonds : WebUI 1 GiB/1 CPU/384 processus, Terminal 2 GiB/1 CPU/**512 processus**, sans swap supplémentaire. Mesure après fermeture du navigateur auxiliaire : environ 325 MiB WebUI et 1,01 GiB Terminal ; valeurs ponctuelles, pas un test de charge.

Les 13 conteneurs préexistants conservent leurs images, dates de démarrage et compteurs de redémarrage ; les 12 avec healthcheck sont sains. D8, son instance cliente, ses volumes et les quatre previews FRONT ne sont pas modifiés. Archives LAUNCH-06 conservées ; aucun nettoyage de volumes anciens, changement global Docker/réseau/SSH, migration commerciale ou déploiement.

## Accès, persistance et fin de session

Seule écoute de laboratoire : loopback `127.0.0.1:18760`, à utiliser par **tunnel SSH privé** vers le VPS existant ; aucun port Docker publié, DNS ou proxy D8 modifié. Le relais CDP temporaire de qualification est retiré et son navigateur auxiliaire fermé. Les identifiants restent dans un fichier privé local remis à l’opérateur, jamais dans GitHub.

État WebUI et home Terminal sur des tmpfs distincts bornés : persistance pendant la session seulement, arrêt = perte de ces états. Le garde local arrête uniquement ces deux conteneurs à **17:59:13 UTC le 3 novembre 2026**, ou si MemAvailable passe sous 1 GiB. Cette date n’est pas prolongée par la publication. Scripts, trois entrées fictives originelles et preuves locales sont conservés séparément ; une reprise après expiration nécessite une recréation explicite du seul laboratoire. Aucune nouvelle mission automatiquement lancée.

## Limites déterminantes

Les sommes Excel sans cache restent vides dans l’aperçu natif et son graphique n’y est pas rendu ; Calc calcule et affiche le graphique. Les mises en page avancées, audio, navigation Internet, charge et isolement entre plusieurs clients ne sont pas qualifiés. Les trois essais LLM et la modification dans une conversation persistée sont **bloqués/non exécutés**. [Résultats](RUNTIME01_DEMO_RESULTS.md) · [Sécurité](RUNTIME01_SECURITY.md) · [Décision](RUNTIME01_DECISION.md).
