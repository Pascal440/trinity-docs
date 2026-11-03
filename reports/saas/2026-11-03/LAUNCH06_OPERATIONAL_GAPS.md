# LAUNCH-06 — Écarts d’exploitation et procédures proposées

Date : 3 novembre 2026. Portal `feature/launch06-release-candidate`, base LAUNCH-05 `679d3738cfb5a724bd0125cca52786cfc2d25545`. Packaging exact des images : `91d47437df0a86063b9c68354c805c987dd83382`. Qualification, preuves et documentation Portal : `6df4b5a338ac84bd928610292981962eeedd9ee6`, [PR #15 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/15) ; base LAUNCH-05 non fusionnée. Gateway D7 `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` et Infra D8 `5bd6fee98a468191613766e0093bdcda8de59099` consultés sans modification. Docs : branche `reports/launch06-release-candidate`, base `reports/launch05-commercial-qualification` / `0a1d0706105ed6e27b68b7071197fe4b09dd94db`.

## Avant tout déploiement autorisé

1. Revue des PR empilées LAUNCH-04→05→06 et des digests ; ne pas repartir de main ni remplacer le runtime D8 implicitement. Conserver images candidate/secours et entrées de build dans un stockage approuvé distinct du registre D8 avant toute opération. Leur transfert et leur conservation durable ne sont pas exécutés ici.
2. Fixer la fenêtre opérateur, les objectifs de récupération/perte de données et un déclencheur de retour ; vérifier capacité, espace, accès de secours et détenteur des clés. Les objectifs commerciaux RPO/RTO restent à arbitrer, aucun SLA inventé.
3. Effectuer **dans une mission autorisée** la sauvegarde pré-migration avec les outils Infra existants `backup-private.py` / `backup-ionos.py` : verrou existant, inventaire du profil réellement actif et des writers, arrêt cohérent contrôlé, dump des bases/archives des volumes, clés applicatives et secrets nécessaires en archive chiffrée, `restic check --read-data`, preuve de snapshot et remise en route du seul état initial. Ne pas exécuter ces scripts contre D8 pendant LAUNCH-06.
4. Restaurer ce snapshot dans un nouvel environnement sans réseau de production, avec secrets de récupération protégés, puis vérifier migrations, déchiffrement des reçus, périodes/ledger/références et santé. Restaurer le vrai volume de la nouvelle instance WebUI et la même version de l’application, sans réutiliser ses identifiants/API ni routes publiques. LAUNCH-06 ne prouve que les fixtures commerciales et le volume représentatif.
5. Qualifier paramètres SQL à privilèges minimaux, droits des volumes/tmpfs et flux strictement nécessaires. Le candidat demande les emplacements runtime indiqués dans le README Portal ; pas de source montée ni de migration à l’entrypoint.

## Surveillance minimale, sans nouvelle plateforme

Réutiliser `stripe:health` LAUNCH-05, en lecture seule, exécuté périodiquement dans le processus du bon profil/compte : JSON + code retour ; pas d’appel Stripe ni identifiants client. Alerter si `oldest_pending_seconds > 300`, `review_jobs > 0`, `uncertain_bindings > 0` ou autorisation invalide/expirée dans `authorization_error`. Observer aussi `processing_enabled` selon l’état approuvé : un profil volontairement désactivé n’est pas une panne, mais un traitement attendu désactivé doit être signalé.

Conserver un heartbeat scheduler, la santé SQL/cache/session, l’ancienneté des sauvegardes et la capacité disque. L’expiration d’autorisation doit déclencher une alerte avant/à échéance, sans prolonger l’autorisation automatiquement ni reprendre un job sans décision opérateur. Les scénarios d’expiration et anomalies métier sont historiquement prouvés en LAUNCH-05 ; le raccordement opérationnel est restant.

L’outil existant `notify_backup.py` et son moniteur savent déjà mettre en file des alertes expurgées de sauvegarde. Son fichier privé de configuration SMTP est **absent lors de ce contrôle**. Ne pas supposer que la messagerie applicative remplit ce rôle. Raccordement minimal proposé : config privée root0600, serveur/port/TLS, expéditeur et destinataire opérateur validés, authentification via fichier secret si nécessaire ; test d’un message synthétique après autorisation. L’outil actuel n’accepte que les catégories de sauvegarde : adapter son petit routage ou ajouter un wrapper pour les seuls signaux de `stripe:health` nécessitera une future autorisation d’écriture Infra. Ne pas envoyer le JSON métier brut, ni données clients, reçus ou secrets. Aucun service global installé ni message envoyé ici.

Au retour vers LAUNCH-04, `stripe:health` est absent : prévoir un contrôle externe expurgé compatible ou un backport revu avant l’opération. Le health SQL/cache/session reste présent dans le packaging des deux images ; il ne remplace pas la surveillance financière.

## Accès de secours et reprise

Prévoir un opérateur avec accès SSH de secours/console VPS vérifié séparément et accès à la clé de déchiffrement sauvegardée hors du serveur. Aucun login de secours, rotation ou lecture/export des secrets existants n’est effectué. Conserver les références d’image et l’état des writers avant intervention. En cas d’activation échouée : analyser le reçu/job et l’état du provisionneur, reprendre les mécanismes idempotents existants après décision, ne pas attribuer manuellement un second crédit et ne pas supprimer les traces.

Retour applicatif proposé : désactiver les traitements selon procédure approuvée, sélectionner le **secours LAUNCH-04** par digest, conserver le schéma à neuf migrations et la même clé, vérifier santé et empreintes avant reprise. Aucun rollback destructif, retour vers Portal D8 test-only ou restauration d’un vieux dump sur des écritures plus récentes. Si des écritures postérieures rendent la compatibilité incertaine, arrêter l’étape et arbitrer ; ne pas effacer une période ni un reçu.

## Ressources observées

Hôte : disque 232 GiB, environ 194 GiB libres avant les derniers artefacts, RAM ~7,9 GiB dont ~5,1 GiB disponibles, pas de swap. En fin de qualification et conservation des archives : environ 188 GiB libres. Valeurs ponctuelles, pas de garantie de charge. Qualification bornée : MySQL 768 MiB, chaque web/Gateway 512 MiB, scheduler 256 MiB, 1 CPU et 256 PIDs par conteneur. Pas de publication de port, pas de création de bridge global ; namespace network-none partagé entre fixtures. Contrôler à nouveau la capacité avant toute recette réelle et définir une rétention approuvée des archives ; aucun nettoyage global exécuté.

## Protocole court de prochaine recette, à autoriser

1. Nouveau tenant de test et nouveau provisionnement isolé, budget IA et domaine/HTTPS fixés, snapshot préalable et plan de retour validés. Aucun client D8 utilisé.
2. Un Checkout Stripe **TEST réel** est justifié pour l’assemblage de la nouvelle image, ses paramètres d’adresse/fiscalité et son webhook réel : un abonnement de test, webhook signé reçu, attribution unique vérifiée par références Portal/Gateway. Pas de nouvelle preuve LIVE ni répétition du catalogue de scénarios LAUNCH-05 sans écart constaté.
3. Provisionneur existant : une instance WebUI neuve physiquement créée, activation propriétaire avec mot de passe choisi par lui ; contrôler la récupération d’un lien/échec sans divulgation de secret.
4. Une conversation IA réelle et débit Gateway correspondant, en comptant les éventuels appels auxiliaires ; vérifier quotas et crédits avant/après, sans crédit manuel ajouté.
5. Scénario de suspension/régularisation **TEST explicitement autorisé**, refus effectif de service puis reprise propriétaire et technique, aucun double crédit.
6. Restaurer une sauvegarde du nouveau tenant dans une autre instance isolée, vérifier vraie application WebUI, conversation/upload et données financières, ne pas réutiliser ses routes ou jetons externes. Test d’alerte synthétique et procédure support avec opérateur identifié.
7. Consigner les preuves/limites puis arrêter et demander l’arbitrage suivant. Cette mission future n’est ni lancée ni autorisée par LAUNCH-06.

## Classement commercial restant

Avant premier paiement réel : validation vendeur/offre 49 € HT/mois, quotas/coûts, domaine/HTTPS commercial, compte Stripe LIVE et versements/catalogue, justificatifs/taxes et conditions applicables, approbation LIVE explicite, sauvegarde/restauration opérationnelle et support/alertes minimaux, décision de déploiement. Ces contrôles restent des validations distinctes ; aucun de leurs réglages réels n’a été modifié. Avant élargissement : charge/capacité, exercices de reprise périodiques, supervision et support étendus. Améliorations : automatisation supplémentaire seulement si un besoin mesuré le justifie.
