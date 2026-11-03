# LAUNCH-04 — Résultats de tests

Date : 3 novembre 2026, Europe/Paris. Résultats exécutés pendant cette mission, distincts des preuves D7/D8.

| Vérification | Résultat / portée |
| --- | --- |
| Suite PHPUnit complète | 209 tests, 2 111 assertions, zéro échec/erreur, PHP 8.4.24 / PHPUnit 11.5.57 |
| Base des tests | SQLite mémoire ; migration additive exécutée uniquement dans ces bases synthétiques |
| Transport | Http::fake et preventStrayRequests, conteneur réseau none ; zéro appel réel Stripe, Gateway, provisionneur ou WebUI |
| Nouveaux cas | 30 tests de profil LIVE synthétique + 1 test préservant la clé d’idempotence TEST D8 |
| Compatibilité | Suite D8 rejouée ; une attente catalogue ajustée explicitement au refus sans état financier fabriqué |
| MySQL 8.4.7 | Texte exact du trigger compilé ; UPDATE ordinaire accepté, changement mode/compte refusé, contexte préservé ; cinq contrôles réussis |
| Limite MySQL | Test SQL ciblé seulement, pas de suite Laravel/MySQL complète ; conteneur jetable sans réseau/port/volume persistant supprimé |
| Style | Pint --test, 117 fichiers, réussi |
| Syntaxe PHP | Tous les PHP app/bootstrap/config/database/routes/tests/scripts passent php -l |
| Build Vite | Réussi, 799 modules ; aucune publication des assets compilés |
| Diff / publication | diff --check et contrôle des fichiers sélectionnés, secrets et artefacts exclus |

## Couverture ajoutée

Les trente scénarios LIVE couvrent profil autorisé synthétique ; absence de grant au retour navigateur ; modes, clés et comptes croisés ; routes webhook croisées ; signatures invalides ; type/mode imbriqué et metadata ; catalogue et Product étrangers ; autorisation absente/expirée/modifiée, seller incomplet, prix/dotation/taxes différents ; UI bloquée ; doublons et rejeux ; réponse perdue Stripe et Gateway ; rétention d’idempotence ; renouvellement sans report ; impayé/régularisation/reprise propriétaire ; annulation ; remboursements synthétiques ; deux organisations ; fiscalité HT/taxe/TTC et URLs chiffrées ; trigger de contexte ; refus de conversion d’un binding TEST ; files et worker d’autre profil ; refus de dispatch d’un crédit en attente après expiration ; absence de publication financière sur metadata incompatibles après paiement.

Les scénarios de cycle financier réutilisent les fixtures et assertions existantes avec un mode LIVE synthétique ; ils n’exécutent aucun appel externe ni l’instance D8. Le simulateur est explicite sur son livemode et son compte, pas un second moteur financier. La fixture commune est abstraite pour éviter de compter les tests d’origine deux fois par héritage.

Le test TEST supplémentaire vérifie les clés HTTP d’idempotence brutes historiques. LIVE utilise une dérivation mode+compte+UUID persisté, vérifiée dans les tests ; un retry conserve cette valeur.

## Échecs initiaux et corrections

La première suite avant build a exécuté 178 tests et rencontré huit erreurs de rendu dues au manifest Vite absent. Le build isolé a fourni ce prérequis ; la suite finale de 209 tests passe. Aucun contournement de contrôle financier pour obtenir ce résultat. L’option Pint --dirty ne fonctionne pas dans l’image sans binaire Git ; formatage des chemins concernés puis contrôle global --test réussi.

L’ancienne attente « une divergence produit une suspension financière synthétique » est remplacée conformément à LAUNCH-04 par « revue sans nouveau snapshot financier ». Les impayés autoritatifs, la neutralisation et la reprise après régularisation restent testés.

## Preuves et limites

La preuve agrégée et la liste des tests de profil sont dans [docs/launch04/TEST_RESULTS.json](https://github.com/Pascal440/trinity-saas-portal/blob/76a11ded222395633efe5fcc7c14a11c293c1e68/docs/launch04/TEST_RESULTS.json) du dépôt technique. Les XML PHPUnit détaillés et journaux bruts restent dans l’espace isolé ; aucune clé synthétique, .env ou dump n’est publiée. Aucune donnée d’exploitation réelle utilisée.

Non exécutés : LIVE réel, Stripe authentifié, carte/SCA réelle, Stripe Tax réel, DNS/TLS/publication, migration du VPS, activation réelle, navigateur E2E, restauration ou charge. Les paiements D7 et l’inférence D8 restent des preuves historiques, pas des tests LAUNCH-04. Les dépendances ont été reprises de copies existantes ; l’installation propre des lockfiles est aussi vérifiée par la CI si elle réussit, dont le statut sera fourni séparément.

Les garde-fous applicatifs ne remplacent pas une future autorisation humaine ni l’isolation et la supervision d’une release commerciale. Aucun paiement ni service client modifié.

## Références de livraison GitHub

Dépôt technique : Pascal440/trinity-saas-portal ; branche feature/launch04-stripe-live ; commit 76a11ded222395633efe5fcc7c14a11c293c1e68 ; [PR #13 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/13), base fix/launch023d8-owner-activation. Aucun déploiement ni activation LIVE.

Dépôt documentaire : Pascal440/trinity-docs ; branche reports/launch04-stripe-live issue de reports/launch03-commercial au commit e0878a2b1bd24a3f943291a37d3c6a205f838281. Le SHA documentaire final est fourni par la PR et le livrable de mission.
