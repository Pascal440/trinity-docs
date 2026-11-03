# LAUNCH-06 — Tests exécutés et preuves historiques

Date : 3 novembre 2026. Portal `feature/launch06-release-candidate`, base LAUNCH-05 `679d3738cfb5a724bd0125cca52786cfc2d25545`. Packaging exact des images : `91d47437df0a86063b9c68354c805c987dd83382`. Qualification, preuves et documentation Portal : `6df4b5a338ac84bd928610292981962eeedd9ee6`, [PR #15 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/15) ; base LAUNCH-05 non fusionnée. Gateway D7 `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` et Infra D8 `5bd6fee98a468191613766e0093bdcda8de59099` consultés sans modification. Docs : branche `reports/launch06-release-candidate`, base `reports/launch05-commercial-qualification` / `0a1d0706105ed6e27b68b7071197fe4b09dd94db`.

## Exécutés pendant LAUNCH-06

| Contrôle | Résultat et portée |
| --- | --- |
| Builds hors réseau sans cache | 2 par image, égalité manifest/config OCI ; image Docker chargée validée par couches et labels |
| Scan runtime | Deux images, chemins de développement/secrets exclus, aucun motif sensible retenu |
| Bootstrap final | Apache `/login`, health SQL/cache/session ; rootfs en lecture seule avec seuls volumes/tmpfs autorisés |
| Upgrade D8 synthétique | 8→9 migrations, empreinte financière et reçus chiffrés conservés ; anciennes taxes nulles |
| Contrats de paiement TEST | Stripe simulé, webhook réellement signé reçu par Apache, Processor/Worker réels, Gateway D7 HTTP et ledger réels, grant unique |
| Rejeux | Doublon et replay sans second reçu ni grant ; route LIVE croisée refusée |
| Profil LIVE | Non autorisé, appel refusé avant fournisseur, aucune clé/approbation LIVE réelle |
| Scheduler | Processus image, heartbeat et absence d’effet financier quand flags processing/billing sont désactivés |
| Diagnostic | `stripe:health` dans l’image candidate ; processing désactivé explicitement visible |
| Redémarrage candidat jetable | Même reçu déchiffrable, périodes/références/ledger conservés |
| Restic | Nouveau dépôt local chiffré, sauvegarde cohérente des seuls writers jetables arrêtés, lecture intégrale de contrôle, restauration SQL identique |
| Restauration indépendante | Nouvelle MySQL + candidate, ancien reçu déchiffré, empreinte financière identique |
| Volume WebUI représentatif | Nouveau volume, SQLite integrity_check=ok, chat et upload conservés ; pas de démarrage WebUI réel |
| Retour LAUNCH-04 | Même base à neuf migrations, empreintes identiques, replay TEST idempotent, health valide |

**41 contrôles enregistrés** dans `IMAGE_QUALIFICATION.json`. Le compteur comprend les contrôles de chaque rôle et les étapes globales ; ce n’est pas un total PHPUnit. Un seul topup réellement comptabilisé dans le Gateway synthétique pour le nouveau client. Aucun appel Stripe réel ni port hôte publié. Toutes les données et clés du scénario sont synthétiques ; le harnais nettoie ses seuls conteneurs et volumes.

PHP/Python : syntaxe des scripts nouveaux vérifiée ; Pint sur les nouveaux fichiers PHP. La [CI de PR #15](https://github.com/Pascal440/trinity-saas-portal/actions/runs/41659123376) est **réussie** : 212 tests / 2 135 assertions, syntaxe, Pint, composer validate, npm ci, build Vite, audits Composer/npm sans avis de vulnérabilité et scan de publication. Exécution automatique sur la référence de merge de PR f81f954a045820b2d8dbc0bfb5198642a6d9d5ce, tête 6df4b5a338ac84bd928610292981962eeedd9ee6, base 679d3738cfb5a724bd0125cca52786cfc2d25545 ; aucune fusion effective. PHP CI 8.4.27 et Node 22.23.4 : cette CI source reste distincte du runtime des images et des 41 contrôles Docker. Les tests locaux source ne sont pas substitués aux tests des images.

## Échecs intermédiaires et correction

Les premières tentatives de harnais ont rencontré : identité Docker exposée comme manifest plutôt que config OCI ; copie Docker dans un rootfs déclaré read-only (remplacée par injection stdin dans le tmpfs) ; disponibilité temporaire MySQL d’initialisation (attente de la fin d’init ajoutée) ; chaîne littérale de marqueur de clé dans une bibliothèque (scan resserré sur un bloc PEM complet). Le premier essai de retour a aussi nécessité de réinjecter le pilote de fixture Gateway perdu lors du redémarrage de son tmpfs ; le scénario complet final a été relancé avec ce correctif et un cache restic privé. Ces tentatives ne sont pas comptées comme des succès.

Le premier démarrage HTTP a exposé un défaut de packaging : CLI root + umask privé créaient des caches root illisibles par www-data. Correction committée au packaging `91d47437df0a86063b9c68354c805c987dd83382` : CLI après lecture des secrets descend sous www-data. Les deux images finales ont été reconstruites deux fois puis le scénario complet a été relancé. Les anciennes images intermédiaires ne constituent pas les images retenues.

## Historiques conservés, non revendiqués comme nouveaux

LAUNCH-05 : 21 contrôles MySQL, 33 TEST, 38 LIVE simulé, concurrence et pertes de réponse, impayé/régularisation, expiration d’autorisation, 212 tests / 2 135 assertions et CI source verte à son commit. Ces résultats ne sont pas des paiements LIVE. D6/D7/D8 : parcours et provisionnement réels anciens déjà documentés ; pas de nouvelle instance D8, activation propriétaire ou conversation réelle dans LAUNCH-06.

## Non exécutés et limites

Aucune connexion Stripe LIVE, paiement TEST réel auprès de Stripe, activation réelle, appel fournisseur IA, nouveau provisionnement WebUI, suspension physique, sauvegarde D8/S3, preuve d’accès console opérateur ou alerte externe envoyée. Pas de test de charge ni de validation d’un SQL applicatif à privilèges minimaux ; la fixture MySQL utilise root pour créer/migrer les bases jetables. Les limites mémoire/CPU/PIDs bornent la qualification et ne sont pas un dimensionnement commercial.
