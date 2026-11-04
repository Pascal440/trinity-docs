# DEMO-01B — Résultats de la recette réelle

4 novembre 2026. Open WebUI 0.13.0 et Open Terminal 0.16.0, images épinglées du kit split. Modèle Together serverless `Qwen/Qwen3.8-Flash`. Les demandes ont été soumises au compte de démonstration via l’API WebUI et suivies dans son historique, sans interaction graphique.

| Contrôle | Résultat observé |
| --- | --- |
| Catalogue authentifié et visibilité dans WebUI | Confirmés après attribution d’un droit au compte de démonstration |
| V1 | 2,15 s entre soumission et constat de l’erreur dans le chat |
| V2 | Même chat. 2,09 s entre soumission et constat de l’échec de connexion au relais fermé |
| Appels amont | 1 réservation et tentative. Le second message n’a pas déclenché de nouvel appel Together |
| Latence fournisseur, tokens et coût réel | Non mesurés. Aucun usage valide enregistré. Les durées WebUI incluent le sondage toutes les 2 s |
| Réservation conservée | 0,16692512 USD, soit 0,50077536 € avec le facteur conservateur 3 EUR/USD. Il s’agit d’une borne, pas d’un montant facturé |
| Lecture des trois sources par le modèle | Non démontrée. Les trois fichiers étaient présents dans le Terminal |
| XLSX, PDF, formules et graphiques V1/V2 | Aucun fichier généré. Seuls les trois fichiers d’entrée étaient présents avant arrêt |
| Arrêt | Relais fermé, deux conteneurs et répertoire de session retirés. Verrou de budget conservé |

Trace du relais expurgée.

```json
{"call": 1, "status": "closed_on_upstream_error", "reserved_usd": "0.16692512"}
```

Le relais regroupe les erreurs HTTP, les erreurs de transport et les réponses non conformes dans le même état. La trace ne permet donc pas d’attribuer la cause exacte ni de conclure sur une éventuelle facturation de la tentative. Les corrections effectuées avant le premier appel se sont limitées au droit de lecture du modèle dans WebUI et au choix du client WebSocket. Le verrou interdit une nouvelle session sous la même autorisation. Le résultat de la démonstration est **non validé**.

## Référence indépendante

CA de 125 000 € et 145 000 €, coûts de 79 000 € et 92 000 €, marges de 46 000 € et 53 000 €, hausse de CA de 16 %, marge T2 de 36,5517 % et écart à l’objectif T2 de −5 000 €. [Calcul indépendant](demo01a-kit/independent-reference.json)

## Reprise DEMO-01B.1

La sonde sans outil a reçu HTTP 400. Atelier Boréal reste en NO-GO. [Diagnostic, correctif et réservation cumulative](DEMO01B1_DIAGNOSTIC.md).

## Reprise DEMO-01B.2

La sonde bornée a reçu HTTP 400. Le diagnostic expurgé identifie le paramètre `stream`. [Comparaison des requêtes et résultat](DEMO01B2_DIAGNOSTIC.md).
