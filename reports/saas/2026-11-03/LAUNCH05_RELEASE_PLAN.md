# LAUNCH-05 — Dossier de mise en service non exécuté

3 novembre 2026, Europe/Paris. Ce plan décrit une future mission soumise à autorisation. **Il n’autorise aucune commande sur D8, aucune clé live, migration active, recette réelle ou encaissement.**

## 1. Sources et artefacts

| Rôle | Commit / image |
| --- | --- |
| Portal LAUNCH-04, base et fallback source compatible | 76a11ded222395633efe5fcc7c14a11c293c1e68 |
| Portal LAUNCH-05 candidat | feature/launch05-commercial-qualification ; SHA final indiqué par la PR technique et les rapports centraux |
| Portal D8 historique | b9c84b5de9671c1be73f8e8cb3198bea3cfec855 ; image sha256:50173a5cf60b06f87ac392b8187b1bd4d47387feb89c05301a488e99754aa4f5 |
| Gateway D7 conservé | f79ff7f4ca938e0610a6e753b4b107dd4edc7437 ; image sha256:71d466513a1b85539313d47f6928da0159dbb52a964a1895f68becacf7453852 |
| Infrastructure D8 conservée | 5bd6fee98a468191613766e0093bdcda8de59099 |
| Provisionneur runtime D2 conservé dans D8 | image sha256:2e5be0ec0d8a2fc170fca7068ad4d354dc0429ce8859ead9e0e8228a5623e061 |
| MySQL 8.4.7 de qualification | mysql@sha256:0426ec38c7a10aa45ba383887df7878f74ee70e2fd589c7b69207f3577901903 |
| Runtime PHP de qualification | image Portal D8 50173a5c ci-dessus, nouvelles sources montées uniquement dans des conteneurs jetables |
| Image commerciale LAUNCH-05 | NON CONSTRUITE : nom/digest/SBOM/build/runtime à fournir dans une mission autorisée |
| Image de retour compatible LIVE | NON CONSTRUITE : source LAUNCH-04 qualifiée comme base, artefact à produire et vérifier |

Les images applicatives existantes proviennent d’un registre privé local ; les digests exacts sont observés via métadonnées d’image, sans publication d’une adresse externe d’exploitation. Le runtime PHP D8 utilisé pour tester les sources ne contient pas le code LAUNCH-05 comme image de release : ne jamais confondre ces deux artefacts.

Aucune obligation de fusionner toutes les PR empilées ou les prototypes FRONT n’est introduite. La direction doit approuver les sources et la stratégie de release exactes, sans considérer main comme la référence fonctionnelle.

## 2. Inventaire et ordre des migrations

La chaîne complète validée en MySQL est :

1. 0001_01_01_000000_create_users_table.php
2. 0001_01_01_000001_create_cache_table.php
3. 0001_01_01_000002_create_jobs_table.php
4. 2026_10_30_000001_create_portal_domain.php
5. 2026_10_30_000002_create_onboardings.php
6. 2026_10_30_000003_add_provisioner_v2.php
7. 2026_10_31_000001_create_billing.php
8. 2026_10_31_000002_create_stripe_adapter.php
9. 2026_11_03_000001_add_stripe_fiscal_evidence.php

Sur un D8 conforme, seule la neuvième est nouvelle. Vérifier la table de migrations réelle avant toute décision ; ne pas rejouer des migrations antérieures ni accepter une dérive de schéma. La neuvième ajoute sept colonnes nullable aux factures et un trigger immuable mode/compte. Aucun backfill ou conversion TEST→LIVE. Pas de migration LAUNCH-05 supplémentaire.

MySQL effectue des commits implicites pour certains DDL : la réussite transactionnelle des données ne garantit pas une migration DDL tout-ou-rien. Préparer sauvegarde, droits ALTER/CREATE TRIGGER, contrôle des verrous, détection d’un DDL partiel et réparation en avant. Les migrations de preuve sont forward-only : ne pas lancer migrate:rollback/down ou effacer tables/triggers pour revenir d’image.

## 3. Ordre de mise en service proposé, jamais exécuté ici

| Étape future | Critère avant de passer à la suivante |
| --- | --- |
| Préparer les artefacts | PR revue ; images candidat et retour compatibles construites depuis SHA épinglés, dépendances/absence de caches de tests vérifiées, digests enregistrés et bootstrap/tests d’image réussis |
| Vérifier le cadre commercial | Vendeur/compte, fiscalité/justificatifs, offre/crédit/quota, support, domaine, données et fournisseur validés ; clés réelles toujours absentes tant que la direction n’autorise pas leur usage |
| Préparer une pause contrôlée | Bloquer nouveaux Checkout et processing, traiter les opérations déjà envoyées comme ambiguës tant que non rapprochées ; maintenir l’ingestion signée si son profil reste autorisé ; définir une fenêtre d’indisponibilité et un retour de secours |
| Sauvegarder avant schéma | Snapshot cohérent SQL Portal/Gateway/provisionneur, volumes WebUI/états, images/manifeste et clés de déchiffrement ; copie externe de récupération et restauration isolée pertinente qualifiées ; jamais publier ces données |
| Migrer le portail | Vérification D8 réelle, sauvegarde acquise, workers empêchés d’agir ; appliquer uniquement la migration additive autorisée puis vérifier colonnes/trigger, anciennes références et déchiffrement sans afficher de corps |
| Déployer le portail et scheduler ensemble | Même image candidate et configuration contrôlée, processing fermé ; conserver Gateway/Infra/provisionneur et leurs identités/volumes, aucun nouveau ledger |
| Contrôler sans encaisser | Health/boot HTTPS, schema, contexte, restrictions de route, flags, conservation des reçus/refs, chiffrement et scheduler ; vérifier une image propre sans cache Laravel de test |
| Examiner le backlog | Reçus non rapprochés, needs_review, payloads persistés anciens et opérations inflight examinés en privé ; pas de crédit manuel ni de reset d’intention |
| Arbitrer l’ouverture | Nouvelle autorisation direction/opérateur, profil complet approuvé et expiration surveillée ; recette réelle explicitement bornée dans une autre mission |
| Vérifications de recette autorisée ultérieure | Paiement réellement permis, facture remise, grant unique, activation et consommation/retour contrôlés ; ne jamais les déduire des seules simulations présentes |

Cet ordre ne réinstalle pas D8 et ne modifie pas les autres dépôts. Si une dérive réelle impose un changement Gateway/Infra ou un autre contrat, arrêter et soumettre une mission distincte.

## 4. Workers, reçus et opérations ambiguës

Séparer réception, processing Stripe, billing et autorisations Gateway. Un scheduler en cours d’exécution n’est pas la preuve que ces tâches sont autorisées. Les processus doivent partager les bons verrous/caches et utiliser le même profil ; les jobs/reconcile/controls sont cloisonnés par compte/mode. Un profil par processus et une identité financière par organisation restent les limites de LAUNCH-04.

Ne pas réécrire un payload Checkout, une clé d’idempotence, une référence de grant ou une quantité de période en attente. Après une réponse perdue, relire/réconcilier le même objet et la même opération ; après la limite de rétention de 23 h, aucune nouvelle création aveugle. Une réception ACK est seulement une preuve de stockage, pas de paiement ou de crédit.

L’expiration de l’approbation LIVE bloque également l’ingestion : un POST refusé n’est pas un reçu durable local. Après réautorisation séparée, vérifier les livraisons/relectures manquantes côté fournisseur selon une mission autorisée et reprendre les mêmes IDs. Ne pas répondre artificiellement 200 ni marquer processed un événement non rapproché.

## 5. Surveillance et procédure d’erreur préparées

stripe:health est un diagnostic de lecture sans API Stripe. Sortie JSON non personnelle ; code 1 pour autorisation invalide, jobs needs_review, bindings needs_review/unknown ou attente de plus de cinq minutes ; compteurs et processing_enabled distincts. ready n’est ni un GO commercial ni la preuve d’un traitement financier activé.

Le raccorder à la supervision externe et faire vérifier une livraison d’alerte avant ouverture. Rien n’est installé par LAUNCH-05. Sur alerte :

1. Identifier en privé le profil et les références existantes ; conserver reçus chiffrés et codes d’erreur, sans exporter clés/corps/données clients.
2. Si autorisation expirée/refusée : ne pas contourner ; décision d’autorisation distincte puis restauration d’une configuration concordante, avant toute reprise.
3. Si donnée incertaine/incompatible : garder l’état financier confirmé, bloquer l’opération et résoudre le fait autoritatif. Les limites et l’expiration ordinaires restent appliquées par Portal/Gateway.
4. Après confirmation : utiliser la réconciliation et la reprise des jobs existants (stripe:reconcile / stripe:retry, selon diagnostic et autorisation), puis les workers ; jamais un second Checkout/create/grant pour effacer l’incertitude.
5. Contrôler unicité, outbox, audit et solde en lecture autorisée ; consigner la résolution et l’absence de double attribution.

Aucune commande de ce plan n’a été exécutée sur la préproduction. Les compteurs cinq minutes constituent un seuil de diagnostic proposé, pas un engagement SLA.

## 6. Retour applicatif conservant les preuves

Avant retour : fermer les nouvelles créations/processing, repérer opérations engagées et conserver la réception lorsque le profil est encore autorisé ; sauvegarder l’état et vérifier la compatibilité de l’image de retour. Conserver schéma additif, triggers, clés de déchiffrement, mappings, références, reçus et historique Gateway. Aucun rollback financier implicite ou remboursement par retour d’image.

Le retour cible un binaire compatible LAUNCH-04 ou ultérieur et le schéma à neuf migrations. **Portal D8 est test-only : il ne constitue pas un fallback sûr après introduction de données stripe_live**, car son worker ne reconnaît pas cette source pour le rapprochement. Ne pas redéployer D8 sur de telles données, ne pas convertir leur mode et ne pas enlever le trigger.

En l’absence d’une image de retour compatible vérifiée, garder une mise en maintenance/processing fermé et corriger en avant plutôt que perdre la traçabilité. Après retour, rapprocher les mêmes opérations avec les mêmes références, contrôler le déchiffrement et les jobs ; aucune nouvelle écriture financière tant que le doute subsiste.

## 7. Conditions de refus et contrôles après installation future

Refuser l’ouverture si : image/digest/rollback non qualifiés ; schéma réel divergent ; backup ou récupération non maîtrisés ; autorisation absente/expirée/incohérente ; compte/mode/catalogue étranger ; vendeur/offre/TVA non validés ; traitements ou dotations Portal/Gateway discordants ; backlog non expliqué ; alerte externe non livrée ; erreurs de bootstrap ou d’isolation ; tentative de contourner une référence TEST existante. Un seul flag ne vaut jamais autorisation.

Après installation autorisée, avant paiement : vérifier les digests chargés, schema/trigger, HTTPS/cookies/horloges, clés privées correctement montées sans lecture dans les logs, lecture des anciennes preuves, health et supervision, cadence/flags des workers, contrôles de route du profil opposé et absence d’effet sur D8. Après recette réelle autorisée : rapprocher paiement/facture, grant unique, activation, consommation, quota, annulation/reprise et sauvegarde des nouvelles données selon le périmètre expressément permis.

Le dossier est prêt pour revue ; l’image finale, les opérations réelles, les décisions commerciales et les vérifications d’exploitation restent à autoriser et exécuter séparément.

## Livraison et références GitHub

Portal feature/launch05-commercial-qualification : commit 679d3738cfb5a724bd0125cca52786cfc2d25545 ; [PR technique #14 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/14), base feature/launch04-stripe-live / 76a11ded222395633efe5fcc7c14a11c293c1e68. Les preuves nouvelles expurgées sont [consultables à ce commit](https://github.com/Pascal440/trinity-saas-portal/tree/679d3738cfb5a724bd0125cca52786cfc2d25545/docs/launch05/evidence). Aucune image commerciale candidate construite ou déployée.

Branche documentaire reports/launch05-commercial-qualification depuis reports/launch04-stripe-live / edb4b84ad14e7716682ae640d18e82a57dc7b2ff. Le SHA documentaire final est fourni par la PR et le livrable de mission.
