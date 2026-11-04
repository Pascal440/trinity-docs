# DEMO-01B.2 — Requête minimale bornée

**NO-GO pour Atelier Boréal.** La sonde unique a reçu HTTP 400. Le diagnostic expurgé identifie le paramètre `stream` dans le message de validation de Together. La requête corrigée omettait ce champ. Le diagnostic ne conserve pas assez de détails pour établir quelle valeur ou quel mode Together exige. Il ne permet pas non plus d’attribuer rétrospectivement le même motif aux deux appels précédents.

## Comparaison avec l’exemple officiel

| Champ | Exemple Qwen3.8 Flash | Sonde B.1 | Sonde B.2 |
| --- | --- | --- | --- |
| `model` | `Qwen/Qwen3.8-Flash` | Identique | Identique |
| `messages` | Un message utilisateur | Un message utilisateur court | Identique à B.1 |
| `max_tokens` | Omis | 64 | 64 |
| `stream` | Omis | `false` injecté | Omis |
| `n` | Omis | `1` injecté | Omis |
| Autres champs | Aucun | Aucun | Aucun |

La fiche du modèle montre un appel minimal sans ces trois options et annonce le streaming. Le contrat générique documente le plafond `max_tokens` et les options `stream` et `n`. Cela ne prouve pas que le service de ce modèle accepte le mode non streamé. La destination TLS est restée celle du relais pour isoler le changement de JSON. L’exemple officiel utilise un autre nom d’hôte Together. [Fiche du modèle](https://www.together.ai/models/qwen3-8-flash) · [Contrat Chat Completions](https://docs.together.ai/reference/chat-completions)

## Résultat observé

| Mesure | Résultat |
| --- | --- |
| Nouveaux appels d’inférence | 1 |
| Statut et catégorie | HTTP 400, `provider_http` |
| Code et paramètre expurgés | `invalid_request_error`, `stream` |
| Latence amont | 0,063 s |
| Tokens et coût réel | Inconnus, aucun usage validé |
| Réservations antérieures | 0,33385024 USD |
| Réservation cumulative | 0,50077536 USD, soit une borne de 1,50232608 € à 3 EUR/USD |

Le relais inspecte le message fournisseur en mémoire et conserve uniquement une reformulation fixe et un nom de paramètre autorisé. Cette règle écarte également les détails utiles qui ne correspondent à aucun motif prévu. Le fichier local du diagnostic est privé. Les tests locaux ont vérifié le JSON normalisé, le plafond de sortie, les rejets hors périmètre, l’expurgation et la reprise du compteur historique. La première invocation locale a échoué à la compilation d’une expression régulière avant tout accès fournisseur. Après correction, une seule sonde a été envoyée.

Les verrous historiques ont été conservés. Le marqueur de cette sonde a été écrit avant l’envoi. Aucun nouvel essai, laboratoire ou scénario V1/V2 n’a été lancé après le refus.
