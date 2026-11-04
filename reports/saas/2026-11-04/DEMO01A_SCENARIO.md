# DEMO-01A — Scénario Atelier Boréal

**Préparation hors ligne. Une seule recette complète après autorisation du modèle, du budget et du relais.**

Les entrées fictives préservées sont `01_ventes_fictives.xlsx`, `02_brief_fictif.docx` et `03_couts_fictifs.pdf`. Utiliser les trois fichiers originaux du [kit](demo01a-kit/inputs/) et vérifier leurs [empreintes](demo01a-kit/inputs-manifest.json). Les fichiers `SMOKE_NOT_LLM` sont des contrôles opérateur séparés.

| Référence indépendante | T1 2026 | T2 2026 |
| --- | ---: | ---: |
| Chiffre d’affaires | 125 000 € | 145 000 € |
| Coûts | 79 000 € | 92 000 € |
| Marge | 46 000 € | 53 000 € |

Variation du CA de +20 000 €, soit +16 %. Marge T2 de 36,5517 %. Objectif T2 de 150 000 € et écart de −5 000 €. Le taux de marge cible de 35 % est atteint. Garder les valeurs de référence côté opérateur pour une vérification indépendante des réponses. [Calcul RUNTIME-01](demo01a-kit/independent-reference.json).

## Déroulement

1. **Importer.** Ouvrir une conversation neuve avec le compte de démonstration, sélectionner le modèle autorisé et le terminal, puis joindre les trois entrées depuis le navigateur de fichiers. Vérifier le rattachement du terminal au premier message.
2. **Analyser et produire.** Envoyer le premier message ci-dessous. Observer l’utilisation réelle des outils natifs et l’apparition du XLSX et du PDF dans l’espace de travail.
3. **Vérifier.** Télécharger V1, conserver ses empreintes et ouvrir le PDF d’analyse. Produire l’aperçu Calc séparé, afficher le graphique et confronter formules, totaux et conclusions à la référence.
4. **Modifier.** Envoyer le second message dans le même chat et le même espace de travail. Vérifier la lecture des livrables V1, la création de V2 et la conservation de V1. L’écart absolu ou une correction doit être justifié par les sources.
5. **Livrer.** Télécharger le XLSX original V2, le PDF d’analyse V2 et son aperçu Calc séparé. Vérifier l’ouverture et les octets avant de fermer la session.

> Analyse les trois documents fictifs Atelier Boréal. Crée Synthese-v1.xlsx avec les données par région, les totaux calculés, la marge et un graphique comparatif. Crée Rapport-v1.pdf avec les conclusions, les écarts aux objectifs et les recommandations. Enregistre les deux fichiers dans le dossier livrables et indique leurs chemins.

> Dans le même espace de travail, relis les fichiers V1 et les trois sources. Ajoute une comparaison T1/T2 en valeur et en pourcentage, ainsi que l’écart à l’objectif et le taux de marge T2. Corrige les écarts de calcul éventuels et explique les changements. Enregistre Synthese-v2.xlsx et Rapport-v2.pdf en conservant V1.

## Critères d’acceptation de la recette

- Les outils ont réellement lu les trois sources et produit les fichiers. Les formules calculent les valeurs de référence à l’arrondi annoncé et le graphique représente les bonnes séries. Les recommandations distinguent le manque à l’objectif de CA et l’objectif de marge atteint.
- V2 résulte de la demande suivante dans le même chat. Conserver les empreintes et fichiers V1/V2. Une recalculation de contrôle ne modifie que la copie d’aperçu. Toute intervention opérateur est consignée, y compris la conversion PDF.
- L’opérateur consigne résultats, erreurs, nombre d’appels et d’actions d’outils, latence, tokens effectivement rapportés, coûts mesurés ou inconnus et interventions. Les prompts et preuves restent fictifs et expurgés. Aucune mesure LLM n’existe au stade DEMO-01A.
- Stopper si le budget, le temps ou le plafond d’appels est atteint, si un autre fournisseur intervient ou si les contrôles de réseau échouent. Soumettre le résultat de cette unique recette à Maya avant toute suite.
