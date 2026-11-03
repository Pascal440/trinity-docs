# LAUNCH-05 — Résultats exécutés et preuves

3 novembre 2026, Europe/Paris. Les preuves JSON se trouvent dans [docs/launch05/evidence](https://github.com/Pascal440/trinity-saas-portal/tree/679d3738cfb5a724bd0125cca52786cfc2d25545/docs/launch05/evidence) du dépôt technique ; les liens immuables figurent dans les copies centrales. Les logs privés et XML bruts ne sont pas publiés.

| Preuve nouvelle | Résultat |
| --- | --- |
| upgrade.json | MySQL 8.4.7, 21 contrôles ; migrateur Laravel D8 (8 migrations), seed synthétique représentatif, upgrade LAUNCH-04 (9 migrations), intégrité et fiscalité |
| test.json | 33 contrôles, 23 sous-processus métiers ; vrai HTTP Gateway D7 et MySQL ; mode Stripe TEST simulé |
| live.json | 38 contrôles, 23 sous-processus métiers ; mêmes contrats réels ; mode Stripe LIVE simulé, refus/expiration et reprise |
| phpunit.json | 212 tests / 2 135 assertions, PHP 8.4.24, PHPUnit 11.5.57, SQLite mémoire ; aucune requête externe |
| Autres contrôles | Pint 123 fichiers, php -l complet, compilation Python, Vite 799 modules, diff --check et sélection de publication |

## Couverture MySQL

Création des tables via la chaîne Laravel complète ; état D8 préexistant avec période payée, mapping TEST, références, outbox et reçu chiffré ; conservation des colonnes et références anciennes de huit tables ; champs fiscaux anciens non fabriqués ; immutabilité de compte/mode ; append-only ; unicité indépendante de financial_reference et period_id ; déchiffrement du reçu ancien ; rollback d’une écriture interrompue ; conservation et relecture de champs fiscaux et URL chiffrée ; migrate répété sans effet.

Le seed payé est une préparation synthétique, pas un ancien paiement réel importé. Seule la base jetable est migrée. Les clés de chiffrement du seed sont synthétiques, temporaires et détruites avec les conteneurs.

## Couverture financière intégrée

Les deux profils font tourner les mêmes classes Portal et Gateway, avec bases dédiées et HTTP réel dans l’espace réseau isolé. La signature des webhooks, les objets Stripe et les réponses provisionneur sont synthétiques. Le test vérifie :

- Rejet de signature/mode croisés avant stockage ; concurrence ingest et déduplication des reçus/jobs.
- Transaction financière MySQL interrompue avec rollback complet, puis reprise d’un job processing dans un autre processus.
- Grant unique par période ; perte de réponse après vrai commit Gateway ; retries concurrents et récupération de la même référence.
- Deux organisations, soldes indépendants, renouvellement sans report et clôture du reliquat avant nouveau grant.
- Anomalie de période suivante : aucun nouvel état/credit/close ; droit payé admis avant échéance et refusé par la vraie classe d’admission Gateway à échéance.
- Facture réellement impayée dans l’API simulée : refus réel d’admission Gateway, suspension confirmée par observation simulée ; régularisation avec un seul grant, nouvelle action propriétaire via contrôleur et contrat v2, attente de l’opération et de l’observation actives simulées.
- Remboursement simulé avec réserve engagée réelle en SQL Gateway : clôture retardée, consommation réglée, retrait du reliquat et conservation ledger/solde, aucun refund d’usage.
- LIVE : autorisation synthétique expirée avant traitement, puis avec période payée et événement pending ; aucun changement financier ou audit d’autorisation Gateway ; alerte health ; restauration synthétique et rejeu du même événement sans double crédit.

Les tests ne sont pas une preuve d’isolement réseau de deux nouveaux conteneurs WebUI ; aucune instance cliente n’est créée. Les assertions v2 sont produites par le code Portal mais le provisionneur est simulé : la vérification cryptographique et le fonctionnement WebUI réel ne sont pas nouvellement qualifiés ici.

## Suite applicative

Les 209 tests LAUNCH-04 sont rejoués pour compatibilité, avec trois nouveaux scénarios de droits avant/après expiration, d’alerte d’autorisation et de cloisonnement du diagnostic. Les nouvelles fonctionnalités ne nécessitent pas de nouvelle migration LAUNCH-05 ni de modification Gateway/Infra. Le moteur de finance n’est pas réécrit.

Un essai PHPUnit a été bloqué par le fichier de log root du nouveau clone ; droits harmonisés dans le seul clone puis suite complète réussie. Les autres erreurs initiales de montage, readiness MySQL, bootstrap factories et session sont listées dans le rapport. Les logs d’échec restent privés et ne sont pas présentés comme des preuves réussies.

## Reproduction et limites

Voir [docs/launch05/README.md](https://github.com/Pascal440/trinity-saas-portal/blob/679d3738cfb5a724bd0125cca52786cfc2d25545/docs/launch05/README.md) et scripts/run-launch05-isolated.py. Il faut un checkout Gateway D7 propre et épinglé, ses dépendances runtime provenant de l’image identifiée, les dépendances de développement Portal et les deux images locales exactes. Aucun pull/install implicite : le runner utilise --pull=never, --network none, tmpfs et un socket temporaire. Le harnais refuse un autre commit Gateway ou un résultat sans preuve JSON passed. Ne jamais l’exécuter depuis des sources en exploitation.

Non exécutés : Stripe LIVE authentifié, paiement réel, carte/SCA, impôts/Stripe Tax réels, login SMTP/navigateur, nouveau provisionnement WebUI physique, sauvegarde/restauration du VPS, image commerciale finale, déploiement et activation. Les 21/33/38 contrôles sont des checks de harnais, pas des tests PHPUnit supplémentaires. Les 23 sous-processus par profil excluent les autres processus d’orchestration.

Aucune autorisation LIVE utilisable hors test n’a été créée ; les artefacts synthétiques sont uniquement dans le tmpfs des conteneurs détruits. Les compteurs locaux ne préjugent pas du résultat CI, signalé séparément lorsqu’il est vérifié.

## Livraison et références GitHub

Portal feature/launch05-commercial-qualification : commit 679d3738cfb5a724bd0125cca52786cfc2d25545 ; [PR technique #14 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/14), base feature/launch04-stripe-live / 76a11ded222395633efe5fcc7c14a11c293c1e68. Les preuves nouvelles expurgées sont [consultables à ce commit](https://github.com/Pascal440/trinity-saas-portal/tree/679d3738cfb5a724bd0125cca52786cfc2d25545/docs/launch05/evidence). Aucune image commerciale candidate construite ou déployée.

Branche documentaire reports/launch05-commercial-qualification depuis reports/launch04-stripe-live / edb4b84ad14e7716682ae640d18e82a57dc7b2ff. Le SHA documentaire final est fourni par la PR et le livrable de mission.
