# DEMO-01B.3 — Streaming Together et recette Atelier Boréal

**NO-GO pour la démonstration commerciale.** Together a accepté la requête V1 en streaming natif et a répondu HTTP 200. Le relais a ensuite fermé la session sur `incompatible_tool_calls`, avant l’exécution d’un outil par le modèle. V2 n’a pas été envoyée. Aucun des quatre fichiers attendus n’a été généré.

## Preuves et limites

- L’opérateur a obtenu `connexion OK` avec 68 tokens d’entrée et 36 de sortie. Cette preuve est déclarée par l’opérateur. Aucun appel de connectivité supplémentaire n’a été effectué.
- Le [relais](demo01b-kit/together_relay.py) envoie `stream: true`, lit les événements progressivement et recompose le texte et les arguments d’outils par index. Il vérifie le modèle, le nom des outils, la présence du marqueur `[DONE]` et l’usage avant de restituer un SSE regroupé à WebUI. Le raisonnement est écarté de la restitution et de la journalisation. Cette restitution après validation évite de remettre un appel partiel à WebUI. Elle ne restitue pas le texte en temps réel.
- Les [trois tests locaux](demo01b-kit/test_native_sse.py) utilisent une fixture synthétique inspirée du résultat opérateur et une fixture d’outil. Ils vérifient le texte fragmenté, les arguments JSON fragmentés, l’usage intermédiaire nul, l’usage final avec choix vide, le rejet d’un outil non autorisé, l’arrêt sans `[DONE]`, le rejet d’un autre modèle et le retrait du raisonnement.
- Dans le laboratoire réel Open WebUI 0.13.0 et Open Terminal 0.16.0, les trois sources fictives étaient accessibles au Terminal et WebUI a interrogé son catalogue d’outils. La demande V1 a référencé les trois fichiers existants dans l’espace de travail. Aucun appel d’outil par le modèle n’a été exécuté et seuls les fichiers d’entrée étaient présents à l’arrêt.
- La trace identifie la validation des appels d’outils, mais plusieurs contrôles y partagent le même code, dont la structure des fragments et la validation du nom assemblé. Aucun corps brut n’a été conservé. La condition précise et l’usage de V1 sont donc inconnus.

## Mesures et budget

| Poste | Observation |
| --- | --- |
| Trois réservations historiques | 0,50077536 USD |
| Appel CURL opérateur | 68 + 36 tokens. 0,00002712 USD estimés au tarif catalogue, débit réel inconnu |
| Appel V1 | HTTP 200, `incompatible_tool_calls`. 9,037 s jusqu’au rejet par le relais, 10,21 s jusqu’au constat dans WebUI |
| Réservation V1 | 0,16692512 USD. Aucun usage validé ni coût réel connu |
| Total prudent suivi | 0,66772760 USD, soit 2,00318280 € au facteur conservateur 3 EUR/USD |
| Compteur | 5 appels comptabilisés sur 8, dont l’appel opérateur |

```json
{"call":5,"reserved_usd":"0.66772760","seconds":9.037,"category":"incompatible_tool_calls","http_status":200}
```

Les marqueurs historiques et le verrou de reprise sont conservés. Le relais et le laboratoire temporaire ont été arrêtés et leurs sockets retirées. Aucune relance n’a été effectuée après le rejet.
