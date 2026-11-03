# LAUNCH-06 — Arbitrage proposé à Maya

**GO qualification isolée des images. GO conditionnel pour préparer une recette limitée séparément autorisée. NO-GO déploiement D8, Stripe LIVE et paiement réel.**

Date : 3 novembre 2026. Portal `feature/launch06-release-candidate`, base LAUNCH-05 `679d3738cfb5a724bd0125cca52786cfc2d25545`. Packaging exact des images : `91d47437df0a86063b9c68354c805c987dd83382`. Qualification, preuves et documentation Portal : `6df4b5a338ac84bd928610292981962eeedd9ee6`, [PR #15 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/15) ; base LAUNCH-05 non fusionnée. Gateway D7 `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` et Infra D8 `5bd6fee98a468191613766e0093bdcda8de59099` consultés sans modification. Docs : branche `reports/launch06-release-candidate`, base `reports/launch05-commercial-qualification` / `0a1d0706105ed6e27b68b7071197fe4b09dd94db`.

## Ce qui est levé

- Images candidate LAUNCH-05 et secours LAUNCH-04 construites deux fois, digests identiques et livraison chargée vérifiée.
- Bootstrap et droits CLI/web, migration additive MySQL, webhook TEST signé, moteur/ledger Gateway réels avec Stripe simulé, grant unique et refus LIVE non autorisé.
- Scheduler sans effet financier lorsqu’il est désactivé, diagnostic health, redémarrage isolé et retour compatible sans rollback SQL ni perte de références.
- Sauvegarde chiffrée restic locale et restauration commerciale indépendante ; intégrité du volume WebUI représentatif.

## Conditions restantes

Le volume WebUI qualifié est une fixture, pas un vrai redémarrage Open WebUI ; une recette physique limitée reste nécessaire. Les archives/images sont locales et leur conservation durable/transfert approuvé restent à organiser. Les preuves ne qualifient ni Stripe LIVE, ni restauration S3 opérationnelle, ni SQL de production à privilèges minimaux, ni alertes externes, ni accès console de secours, ni performance commerciale. Le cadre vendeur/prix/quotas/fiscalité/domaine/conditions reste à valider avant encaissement.

La configuration SMTP d’alerte manque ; `stripe:health` est exploitable mais n’est pas un canal externe déjà raccordé. Son absence dans le secours LAUNCH-04 doit être prise en compte. Aucune modification Gateway/Infra n’a été nécessaire pour les tests ; un futur raccordement de leur exploitation demandera son autorisation propre.

## Chemin minimal proposé

Maya peut faire revoir les deux PR brouillon et choisir une mission de recette TEST réelle sur **nouveau tenant isolé**, couvrant uniquement assemblage Stripe/webhook, provisionnement réel, activation, conversation/débit, suspension/reprise et restauration réelle + support/alerte. Le protocole est dans [les écarts opérationnels](LAUNCH06_OPERATIONAL_GAPS.md). Ensuite seulement, arbitrer les prérequis commerciaux et une mission de déploiement/activation distincte.

L’ancien D8 test-only est exclu du retour après données LIVE ; le secours est explicitement LAUNCH-04 compatible. Pas de nouvelle architecture recommandée, pas de réécriture financière. Aucun lancement automatique de correction, mission suivante, fusion, déploiement ou encaissement.
