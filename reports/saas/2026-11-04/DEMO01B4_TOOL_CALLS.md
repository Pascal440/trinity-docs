# DEMO-01B.4 — Diagnostic des appels d’outils

**NO-GO.** V1 a reçu HTTP 200, puis le relais a atteint son délai de lecture du flux avant de valider un événement de fin. La trace réelle contient `stream_deadline`, aucun sous-code d’appel d’outil. L’échec B.3 reste indéterminé au-delà de sa catégorie `incompatible_tool_calls`. Aucun appel d’outil exécuté ni livrable généré n’a été observé. V2 n’a pas été envoyée.

## Contrat et correctif

Le SDK officiel représente le flux avec des choix comportant un `delta`, des appels d’outils facultatifs et un usage facultatif. Son type d’outil prévoit un index numérique, un identifiant, un type fonction et des chaînes pour le nom et les arguments. La documentation confirme les appels multiples. Les exemples consultés n’établissent pas la cadence exacte d’émission de l’identifiant ni la fragmentation du nom pour Qwen3.8 Flash. [Type SSE du SDK](https://github.com/togethercomputer/together-py/blob/main/src/together/types/chat/chat_completion_chunk.py) · [Type outil du SDK](https://github.com/togethercomputer/together-py/blob/main/src/together/types/tool_choice.py) · [Documentation Together](https://docs.together.ai/docs/inference/function-calling/overview)

Le relais distingue les neuf sous-codes demandés. Les diagnostics se limitent aux noms de champs connus, à leurs types JSON et aux index bornés. Un identifiant peut être fourni sur un seul fragment. Un identifiant conflictuel est refusé. Les fragments du nom et des arguments sont assemblés par index. Le nom final doit correspondre exactement à un outil déclaré dans la requête WebUI et les arguments doivent former un objet JSON complet. La normalisation des index numériques intégraux, comme `1.0`, a été ajoutée après l’essai à partir du type officiel et vérifiée localement. Le test réel utilisait encore des index strictement entiers.

Cinq tests locaux passent. Ils couvrent les neuf sous-codes, les appels uniques, fragmentés et multiples, l’usage final avec `choices: []`, la fin SSE, le rejet d’un autre modèle et l’absence de raisonnement dans la restitution. Les fixtures sont synthétiques. Le flux réel n’a fourni aucune structure d’outil validée à publier. Aucun argument, prompt ni événement brut ne figure dans ce rapport.

## Recette et budget

| Mesure | Observation |
| --- | --- |
| V1 | HTTP 200, `stream_deadline`, 61,775 s côté relais et 62,63 s dans WebUI |
| V2 | Non envoyée |
| Fichiers | Seuls les trois documents d’entrée étaient présents |
| Réservation antérieure | 0,66772760 USD |
| Nouvelle réservation | 0,16692512 USD, enregistrée avant l’appel |
| Total prudent suivi | 0,83465272 USD, soit 2,50395816 € au facteur 3 EUR/USD |
| Appels comptabilisés | 6 sur 8, appel opérateur compris |
| Usage et débit de V1 | Inconnus. Aucun usage final validé |

Le laboratoire et le relais ont été arrêtés et les verrous conservés. Aucune sonde de connectivité ni nouvelle tentative après l’échec.
