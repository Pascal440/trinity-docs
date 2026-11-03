# LAUNCH-06 — Release candidate commerciale

**GO construction et qualification isolée. GO conditionnel pour une future recette explicitement autorisée. NO-GO déploiement D8, activation LIVE et paiement réel.**

Date : 3 novembre 2026. Portal `feature/launch06-release-candidate`, base LAUNCH-05 `679d3738cfb5a724bd0125cca52786cfc2d25545`. Packaging exact des images : `91d47437df0a86063b9c68354c805c987dd83382`. Qualification, preuves et documentation Portal : `6df4b5a338ac84bd928610292981962eeedd9ee6`, [PR #15 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/15) ; base LAUNCH-05 non fusionnée. Gateway D7 `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` et Infra D8 `5bd6fee98a468191613766e0093bdcda8de59099` consultés sans modification. Docs : branche `reports/launch06-release-candidate`, base `reports/launch05-commercial-qualification` / `0a1d0706105ed6e27b68b7071197fe4b09dd94db`.

## Résultat confirmé

Deux images finales, candidate LAUNCH-05 et secours LAUNCH-04, ont été construites chacune deux fois sans cache ni réseau, avec égalité des digests manifest et config OCI. Elles ont été chargées puis utilisées par les tests, sans montage de sources applicatives. Les références exactes sont dans [le manifeste](LAUNCH06_IMAGE_MANIFEST.md). Aucun push de registre, y compris le registre D8.

La qualification effectue 41 contrôles enregistrés. MySQL 8.4.7 et le Gateway D7 exécutent leurs véritables migrations, modèles et ledger dans un réseau sans sortie. Stripe et le provisionneur sont simulés. Des fixtures TEST signées passent par Apache ; le processeur Portal et le ledger Gateway attribuent un seul crédit de 10 unités monétaires de fixture, sans second crédit au rejeu. Aucun paiement ni appel API Stripe réel.

La migration additive passe de huit migrations D8 synthétiques à neuf. Les anciennes références et reçus chiffrés restent identiques ; aucune fiscalité ancienne n’est inventée. Redémarrage du seul candidat jetable et retour vers l’image LAUNCH-04 sur la même base à neuf migrations conservent les empreintes financières et le déchiffrement. Le secours rejoue la fixture TEST sans double attribution ; aucun rollback SQL.

Un nouveau dépôt restic local chiffré a sauvegardé les deux bases synthétiques, la clé applicative synthétique et le volume représentatif WebUI ; `check --read-data` et restauration indépendante réussissent. La base restaurée est relue par l’image candidate ; le volume restauré conserve son SQLite et son upload. Ce volume contient une petite fixture user/chat, **pas une instance réelle Open WebUI ni son schéma complet**. Aucun dépôt de sauvegarde opérationnel ni destination S3 n’a été écrit.

## Changements nécessaires, périmètre limité

Packaging multi-stage utilisant les runtimes déjà disponibles, dépendances PHP production vérifiées contre composer.lock, assets Vite construits hors réseau, image finale aplatie pour exclure l’ancien code des couches basses. Démarrage sans migration, clé générée ni activation financière ; flags TEST-processing, LIVE et billing désactivés par défaut. Lanceurs CLI et scheduler sous www-data, secrets runtime séparés des images, health SQL/cache/session fourni. Aucun moteur Stripe, Gateway, quota ou provisionneur redéveloppé.

L’essai initial a détecté un défaut réel de droits : des caches Laravel créés par une CLI root n’étaient pas lisibles par Apache. Le lanceur CLI a été corrigé pour utiliser l’identité web ; les images retenues ont ensuite été reconstruites et requalifiées. Les builds antérieurs ne sont pas des releases retenues. Les erreurs de harnais et limites sont détaillées dans [les résultats](LAUNCH06_TEST_RESULTS.md).

## État de livraison et continuité

Code et preuves expurgées publiés en PR brouillon Portal depuis LAUNCH-05 ; cinq rapports centraux et index en PR brouillon documentaire depuis LAUNCH-05. Les SHA finaux et liens figurent dans les PR et le livrable de mission. Les images et archives restent locales, sous références LAUNCH06 distinctes. Aucune fusion, migration active, modification d’instance cliente, écriture de base D8, redémarrage actif, changement réseau global, déploiement ou encaissement.

Les 13 services existants ont été observés en lecture seule. Leur identité, démarrage et compteur de redémarrages ont été comparés avant/après la qualification finale ; aucun redémarrage provoqué. Cette comparaison n’équivaut pas à un audit des contenus des bases D8, qui ne sont pas inspectées par ce harnais.

## Preuves et suites proposées

[Tests](LAUNCH06_TEST_RESULTS.md) · [Écarts et procédures](LAUNCH06_OPERATIONAL_GAPS.md) · [Décision](LAUNCH06_DECISION.md). La [CI Portal #21](https://github.com/Pascal440/trinity-saas-portal/actions/runs/41659123376) est réussie : 212 tests / 2 135 assertions, build, style et audits. Les preuves machine expurgées sont dans Portal `docs/launch06/evidence/`, le mode opératoire dans `docs/launch06/README.md`. Les scénarios LAUNCH-05 déjà prouvés ne sont pas exécutés de nouveau sans raison ; la nouveauté est ici la forme de livraison, son bootstrap, ses droits, sa migration et son retour compatible.

L’autorisation présente n’inclut aucune mission suivante.
