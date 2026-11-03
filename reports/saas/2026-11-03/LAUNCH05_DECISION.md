# LAUNCH-05 — Décision proposée à Maya

3 novembre 2026 — Europe/Paris.

**GO qualification technique des sources ; GO conditionnel pour préparer une recette commerciale contrôlée. NO-GO déploiement, activation LIVE et paiement réel dans cette mission.**

## Motifs vérifiés

- Migration Laravel complète sur MySQL 8.4.7 depuis un état D8 synthétique : 21 contrôles, données anciennes et références conservées, fiscalité et contraintes prouvées.
- Même moteur TEST/LIVE simulé, avec vrais contrats HTTP et ledger du Gateway D7 : 33 contrôles TEST et 38 LIVE, pertes de réponse et interruptions/rejeux sans double grant.
- Période suivante incompatible : aucun nouvel état financier ; droit antérieur conservé avant échéance puis refusé par la classe réelle d’admission Gateway à échéance.
- Impayé/régularisation confirmés sur objets synthétiques : suspension financière réelle Gateway, reprise Portal par nouveau contexte propriétaire et observations techniques simulées ; aucun second crédit au rejeu.
- Autorisation expirée avec événement pending : aucun mouvement financier ni audit d’autorisation nouveau, alerte exploitable et reprise idempotente après rétablissement synthétique.
- 212 tests / 2 135 assertions ; style, syntaxe et build réussis. Aucun changement requis du code Gateway/Infra.

## Portée exacte du GO

Les écarts MySQL et d’intégration financière identifiés après LAUNCH-04 sont levés dans les conditions isolées documentées. Les sources peuvent être proposées à la revue de release et à la préparation d’une recette contrôlée distincte. Ce résultat ne donne pas un accord d’opération ni une certification de Stripe LIVE.

## Conditions non levées

1. Image commerciale candidate et image de retour compatible non construites/qualifiées ; digests à établir. L’image D8 utilisée comme runtime de test n’est pas la release LAUNCH-05.
2. Stripe LIVE réel, compte/versements/catalogue, clés et fiscalité réelle non inspectés ni utilisés. Les identités/offres/conditions de LAUNCH-03 demandent toujours validation.
3. Aucun nouveau provisionnement/suspension physique WebUI ; le provisionneur, les états techniques et Stripe sont simulés. Les preuves D8 réelles restent historiques.
4. Aucune sauvegarde/restauration de préproduction requalifiée ; aucun canal externe d’alerte installé ou testé. La commande health est prête, pas une notification déjà livrée.
5. Déploiement, migration réelle, permissions SQL/verrous, effets de charge et cohérence de l’image finale non exercés.
6. Limites LAUNCH-04 maintenues : profil par processus, identité financière unique par organisation, collisions globales refusées, expiration d’approbation bloquant aussi l’ingestion.

## Décision minimale demandée, sans exécution automatique

Maya peut autoriser une mission de préparation des images/release et de validation des prérequis commerciaux/opérationnels, puis définir explicitement une recette de bout en bout et ses opérations autorisées. Aucune nouvelle architecture ni réécriture du moteur n’est justifiée par les résultats présents.

Ne pas confondre GO technique des sources, autorisation de déployer et autorisation d’encaisser. Si la direction exige une preuve WebUI réelle ou Stripe réel avant cette étape, elle doit faire l’objet d’un périmètre séparé. LAUNCH-05 n’engage pas cette mission suivante.

## Livraison et références GitHub

Portal feature/launch05-commercial-qualification : commit 679d3738cfb5a724bd0125cca52786cfc2d25545 ; [PR technique #14 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/14), base feature/launch04-stripe-live / 76a11ded222395633efe5fcc7c14a11c293c1e68. Les preuves nouvelles expurgées sont [consultables à ce commit](https://github.com/Pascal440/trinity-saas-portal/tree/679d3738cfb5a724bd0125cca52786cfc2d25545/docs/launch05/evidence). Aucune image commerciale candidate construite ou déployée.

Branche documentaire reports/launch05-commercial-qualification depuis reports/launch04-stripe-live / edb4b84ad14e7716682ae640d18e82a57dc7b2ff. Le SHA documentaire final est fourni par la PR et le livrable de mission.
