# DEMO-01B.5 — Délais SSE et exécution Atelier Boréal

**NO-GO.** Le flux V1 a franchi l’ancienne limite de 60 s. Le relais l’a ensuite fermé à 208,851 s sur `tool_id_invalid_or_conflicting`, avant la remise de l’appel d’outil à WebUI. Aucun outil n’a été exécuté dans Open Terminal, aucun fichier n’a été généré et V2 n’a pas été envoyée.

## Correctif

Le [relais](demo01b-kit/together_relay.py) utilise un minuteur système pendant l’appel amont. Il interrompt aussi une lecture bloquante. Le délai de 60 s est recalculé à partir du dernier événement utile. Les fragments de texte, de raisonnement ou d’outils et les marqueurs de fin ou d’usage comptent comme activité. Les commentaires SSE et événements vides ne le réinitialisent pas. La durée totale de 240 s couvre l’appel, connexion comprise, sous le plafond de session de 20 min. Les deux motifs d’expiration sont distincts.

Le relais attend la validation complète des appels d’outils avant de restituer le SSE à WebUI. Ce choix évite de transmettre une commande partielle ou non autorisée. Le délai standard de 300 s du client HTTP WebUI couvre les 240 s du relais. Le pilote de recette suit le résultat d’un tour jusqu’à 570 s et attend la vérification des fichiers V1 avant d’autoriser V2. Les [sept tests locaux](demo01b-kit/test_native_sse.py) passent, dont les deux expirations sur une socket sans données et le comptage sans conservation du raisonnement.

## Flux V1 observé

| Mesure | Résultat |
| --- | --- |
| HTTP | 200 |
| Premier événement SSE | 1,698 s |
| Durée jusqu’au rejet | 208,851 s côté relais, 209,81 s jusqu’au constat WebUI |
| Événements | 4 904 |
| Temps depuis le dernier événement, et le dernier utile | 0,000 s chacun à l’arrondi |
| Fragments texte, raisonnement, outils | 15, 4 886, 2 |
| Index d’outils distincts | 1 |
| Marqueur de fin, usage final, `[DONE]` | Absents au moment du rejet |
| Motif | `incompatible_tool_calls` / `tool_id_invalid_or_conflicting` |

Le fragment rejeté contenait un index entier à 0, un champ `id` de type chaîne, un champ `type` de type chaîne et un champ `function` de type objet. Le sous-code couvre un identifiant vide ou incompatible avec celui déjà reçu pour l’index 0. La valeur a été écartée, et le diagnostic ne distingue pas ces deux cas. L’activité SSE observée jusqu’à l’arrêt écarte une expiration d’inactivité pour cet appel. Aucun prompt, raisonnement, argument ou identifiant d’outil brut n’est publié.

## Budget et arrêt

| Poste | Valeur |
| --- | --- |
| Historique | 0,83465272 USD, six appels dont l’appel opérateur |
| V1 B.5 | Réservation 0,16692512 USD écrite avant l’envoi |
| Cumul prudent | 1,00157784 USD, soit 3,00473352 € au facteur 3 EUR/USD |
| Consommation confirmée | Seuls les 68 tokens d’entrée et 36 de sortie de l’appel opérateur sont connus. Tarif estimé 0,00002712 USD, débit inconnu |
| Coût réel de V1 B.5 | Inconnu. Aucun usage final validé et aucune déduction de réservation |
| Plafond de reprise | 10 appels cumulés, maximum 1,50235320 USD au rythme des réservations, soit 4,50705960 € |

Le contrôle en USD a été ajusté à 1,51 USD pour permettre au plus quatre nouvelles réservations au départ, tout en vérifiant la borne de 5 € avant chaque appel. La session s’est arrêtée au premier rejet. Le laboratoire, le relais et le répertoire de session ont été retirés. Les verrous et réservations historiques sont conservés.
