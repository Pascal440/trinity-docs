# DEMO-01B — Résultats de recette

**Scénario réel non exécuté.** La clé Together dédiée est absente. L’ID public `Qwen/Qwen3.8-Flash` reste un candidat à confirmer sur catalogue authentifié. Aucun remplacement de modèle, aucune instance GPU réservée.

| Mesure demandée | État |
| --- | --- |
| Conversations réelles / appels d’inférence | 0 / 0 |
| V1 Excel / PDF | Non produits |
| V2 dans le même chat | Non exécutée |
| Exactitude des livrables | Non évaluée |
| Tokens et latence modèle | Non mesurés |
| Coût de la mission | 0 € d’inférence |
| Interventions opérateur pendant le scénario | Sans objet |
| Erreurs | Absence de clé dédiée. Premier contrôle split bloqué par les permissions de la socket de test, corrigé. |

Référence indépendante réutilisée pour la future recette. CA 125 000 € et 145 000 €, coûts 79 000 € et 92 000 €, marges 46 000 € et 53 000 €, variation CA +16 %, marge T2 36,5517 %, écart à l’objectif T2 −5 000 €. Les valeurs viennent des trois entrées fictives historiques, pas d’une production LLM. [Référence source](demo01a-kit/independent-reference.json).

Contrôles exécutés localement. Recréation du kit #7, démarrage avec namespaces distincts, accès Terminal de WebUI, réponse locale sur socket modèle réservée à WebUI, refus d’accès depuis Terminal, refus de sortie réseau du Terminal. Le test HTTP du garde vérifie le jeton, les routes, le modèle exact, les outils locaux et la limite de huit admissions. Les tokens fictifs du test du garde ne sont pas comptés dans la recette ni dans le coût.

À remplir après l’unique scénario autorisé. Traces V1/V2 dans le même chat, SHA256 des originaux téléchargés, validation du graphique et des formules, actions Terminal, appels fournisseur, tokens rapportés, coût facturé ou estimé, latence de bout en bout, corrections autonomes et interventions. Arrêt du relais vérifié après export.
