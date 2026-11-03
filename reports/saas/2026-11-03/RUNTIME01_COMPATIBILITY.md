# RUNTIME-01 — Compatibilité exacte des versions

3 novembre 2026, contrôles en UTC. Dépôt documentaire `Pascal440/trinity-docs`, branche `reports/runtime01-lab`, base `reports/launch06-release-candidate` / `5f1f6072bcbd5ca587b18fac84250e497fed8b12`. Aucun dépôt technique publié/modifié. Code Gateway consulté : `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` ; référence Infra inchangée `5bd6fee98a468191613766e0093bdcda8de59099` et Portal LAUNCH-06 `6df4b5a338ac84bd928610292981962eeedd9ee6`. Scripts de laboratoire locaux séparés ; SHA documentaire final fourni dans la PR/livraison.

## Images et sources épinglées

| Composant | Variante officielle | Source exacte | Manifest linux/amd64 exécuté |
| --- | --- | --- | --- |
| Open WebUI 0.13.0 | `ghcr.io/open-webui/open-webui:v0.13.0-slim` | `c38885a1a737da4968f157092f304f3b5481d0bf` | `sha256:9c583de5686ed3f92e992a9326a99225e951047176ccc5644fcd4352b77eb959` |
| Open Terminal 0.16.0 | `ghcr.io/open-webui/open-terminal:0.16.0` complet | `6444534c8aa4bd8acf561bf62cd9eef3e29bd24f` | `sha256:28adefe59c450e4010862f25300a4c7e023de463779538dbee8818769911c835` |

Les tags servent uniquement à identifier les publications ; les conteneurs utilisent `image@sha256:…`, pas de tag flottant. Les index multiarchitecture ont été consultés et le manifest amd64 sélectionné. Les IDs Docker effectifs, tailles et labels sont enregistrés dans [image-manifest.json](runtime01-evidence/image-manifest.json). Pas de construction locale ni de publication de registre.

Références primaires : [release WebUI v0.13.0](https://github.com/open-webui/open-webui/releases/tag/v0.13.0), [release Terminal v0.16.0](https://github.com/open-webui/open-terminal/releases/tag/v0.16.0), [README Terminal au commit retenu](https://github.com/open-webui/open-terminal/blob/6444534c8aa4bd8acf561bf62cd9eef3e29bd24f/README.md), [proxy WebUI au commit retenu](https://github.com/open-webui/open-webui/blob/c38885a1a737da4968f157092f304f3b5481d0bf/backend/open_webui/routers/terminals.py). La release GitHub WebUI v0.13.0 est bien publiée le 3 novembre ; aucune qualification 0.12.5 substituée.

## Contrat d’intégration réellement exercé

Configurer **Admin Settings → Integrations → Open Terminal**, pas un serveur d’outils OpenAPI générique. Connexion système avec identifiant, URL privée loopback du terminal, `auth_type=bearer`, clé de laboratoire propre, `enabled=true` et `/openapi.json`. Le backend WebUI conserve la clé et relaie les requêtes utilisateur authentifiées. `GET /api/config` annonce terminal, system, git, events, browser et desktop ; notebooks désactivés volontairement.

Une connexion sans `config.access_grants` est privée aux administrateurs. Le compte de démonstration reçoit un grant `read` explicite, uniquement sur cette connexion. Il accède au terminal et aux fichiers, mais pas à l’administration des connexions. Les contextes d’utilisateur et `X-Session-Id` déterminent les sessions ; `browser/tabs` expose `session_id`, alors que la création expose `id`. Les sélecteurs UI suivent `tab`, `menuitem` et `menuitemradio`. Les références d’éléments du navigateur expirent après rechargement et doivent être relues.

Les appels d’outils par le LLM nécessiteront un modèle réellement raccordé, le mode d’appels natifs et la capacité terminal, puis un test du passage du contexte provisoire vers le premier message sauvegardé. **Ce passage et les outils déclenchés par TN-27Q ne sont pas prouvés ici.** La version 0.16.0 annonce une correction de ce rattachement ; une note de release n’est pas un test d’exécution.

## Résultat par priorité

| Priorité | État confirmé | Limite |
| --- | --- | --- |
| Espace à onglets | Fichiers multiples, plein écran, terminal, Browser et Desktop dans le compte de démo | Pas de conversation LLM sauvegardée ni de preuve de reprise de ses onglets après génération |
| Connexion et outils | Découverte OpenAPI/capabilities, lecture des 3 entrées, commande API et commande terminal UI, sorties réelles | Actions opérateur seulement, pas d’appel LLM |
| Excel | Données visibles et téléchargement intègre ; fichier avec formules et graphique, Calc les ouvre correctement | Aperçu natif ne calcule pas les formules sans cache ; graphique absent de cet aperçu |
| Word | Aperçu UI et téléchargement intègre, rendu serveur PDF disponible | Contrôle sur document fictif simple ; pas toute mise en page avancée |
| PDF | Texte visible dans l’aperçu UI et téléchargement intègre | Pas de test de gros documents, signatures ou OCR |
| PowerPoint | Aperçu UI d’une diapositive et téléchargement intègre ; rendu serveur PDF disponible | Pas une validation exhaustive des animations/graphiques/thèmes |
| Bureau | Desktop virtuel Linux, capture et actions réelles, canvas connecté dans WebUI ; Calc ouvert par l’opérateur | Audio et pilotage visuel par TN-27Q non qualifiés ; aucune capture du bureau hôte |
| Browser | Chrome isolé, page locale, formulaire piloté par API native et visible dans l’onglet du même compte | Réseau externe fermé ; pas de recherche Internet ni de pilotage LLM |
| Générer puis modifier | Protocole et entrées prêts | **Non exécuté : absence d’identité/routage autorisés** |

## Dépendances effectives

Python 3.12.13 ; Chromium 156.0.8078.73 ; LibreOffice 25.2.3.2. Bibliothèques présentes dans l’image complète : openpyxl 3.1.5, python-docx 1.2.0, python-pptx 1.0.2, WeasyPrint 70.0, pandas 3.1.0, matplotlib 3.11.2, pypdf 6.21.4. Aucun apt/pip/npm global sur le VPS ; aucune installation supplémentaire dans les services existants.

La variante WebUI slim réduit les dépendances ; Ollama, APIs modèles et téléchargements de modèles sont désactivés, mode hors ligne. L’extraction documentaire testée est celle d’Open Terminal complet ; aucun RAG local/embedding ou moteur GPU n’est revendiqué. Le code upstream et ses licences restent ceux des images officielles ; aucun changement de marque commerciale réalisé.

**Conclusion : compatibilité mécanique de ces deux images confirmée sur les parcours exercés ; compatibilité agentique TN-27Q et qualité client encore non qualifiées.**
