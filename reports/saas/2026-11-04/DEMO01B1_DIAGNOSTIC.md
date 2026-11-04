# DEMO-01B.1 — Diagnostic ciblé Together AI

## Conclusion

**NO-GO pour Atelier Boréal.** Le catalogue authentifié confirme le modèle et les tarifs, mais la sonde sans outil a été rejetée par Together AI. Le scénario V1/V2 n’a pas repris et aucun nouveau laboratoire n’a été démarré.

## Cause établie et limite

Le premier échec historique reste indéterminé. Le relais d’origine journalisait le même état pour un refus HTTP, une rupture de transport, une erreur JSON et une réponse incompatible. La sonde de reprise a été rejetée avant toute validation locale de `model`, `usage`, `choices` ou des appels d’outils. Son code `invalid_request_error` ne permet pas d’identifier le paramètre ou la condition que Together a refusé. La sonde utilise le même modèle et la même destination TLS, sans outil, avec un message court et 64 tokens de sortie au maximum.

| Observation | Résultat |
| --- | --- |
| Appels d’inférence de reprise | 1 |
| HTTP et code fournisseur expurgé | 400, `invalid_request_error` |
| Catégorie et classe | `provider_http`, `UpstreamError` |
| Durée de l’appel amont | 1,912 s |
| Tokens et coût réel | Inconnus pour les deux tentatives. Aucun usage validé |
| Réservation historique conservée | 0,16692512 USD |
| Réservation ajoutée | 0,16692512 USD |
| Réservation cumulée | 0,33385024 USD, soit une borne de 1,00155072 € au facteur conservateur 3 EUR/USD |

Le verrou historique est intact. Un marqueur privé de reprise a enregistré la réservation avant l’envoi. Le marqueur de réussite est absent et le relais refuse le scénario. La limite reste de huit réservations cumulées, soit 4,00620288 € au facteur retenu. Ces montants sont des bornes de réservation, pas des débits constatés.

## Correctif et vérifications

Le [correctif Python](demo01b-kit/together_relay.py) sépare HTTP, TLS, timeout, transport, JSON et incompatibilités de réponse. Il journalise uniquement des métadonnées et des codes autorisés par liste fermée. Il maintient l’égalité stricte de l’ID, les plafonds de tokens et le nombre de choix, puis contrôle le format des appels d’outils et vérifie que leurs noms figurent dans la requête. La destination réseau et les plafonds restent identiques. [Contrat Together Chat Completions](https://docs.together.ai/reference/chat-completions)

Les tests sur réponses locales ont vérifié la classification, l’expurgation d’un code arbitraire, les rejets de modèle, usage et choix invalides, ainsi qu’un événement SSE contenant un outil indexé suivi de `data: [DONE]`. Le test de budget a vérifié le refus après huit réservations cumulées. Ces vérifications ne démontrent pas le fonctionnement du flux SSE en session réelle avec Together.

La première invocation de la sonde s’est arrêtée avant toute requête d’inférence parce que la validation du verrou traitait son texte comme un secret sans espaces. La correction sépare la lecture d’un fichier privé de la validation du format d’une clé. L’invocation suivante a effectué le seul POST réel autorisé. Aucun nouvel essai n’a suivi son rejet.
