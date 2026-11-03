# LAUNCH-05 — Qualification intégrée et préparation de release

3 novembre 2026 — Europe/Paris. Destinataire : Maya.
**Qualification technique réussie sur les sources ; GO conditionnel pour préparer une recette commerciale contrôlée. Aucune autorisation de recette, déploiement ou encaissement réel.**

## Références exactes

| Composant | Référence |
| --- | --- |
| Portal base obligatoire | feature/launch04-stripe-live, 76a11ded222395633efe5fcc7c14a11c293c1e68, PR #13 |
| Branche livrée | feature/launch05-commercial-qualification, créée dans un nouveau clone depuis cette base |
| Gateway utilisé sans modification | D7, f79ff7f4ca938e0610a6e753b4b107dd4edc7437, PR #9 |
| Infra de compatibilité, non modifiée | D8, 5bd6fee98a468191613766e0093bdcda8de59099, PR #15 |
| Portal de compatibilité | D8, b9c84b5de9671c1be73f8e8cb3198bea3cfec855, PR #8 |
| Base documentaire | reports/launch04-stripe-live, edb4b84ad14e7716682ae640d18e82a57dc7b2ff, PR #3 |

L’ascendance Portal D8 → LAUNCH-04 est conservée. Gateway est chargé depuis un snapshot de ce commit épinglé en lecture seule ; son clone est contrôlé propre avant exécution et après qualification. Aucun changement de code ou de configuration dans Gateway/Infra. Les SHA finaux et PR sont référencés dans le livrable et les copies centrales, sans référence circulaire dans le propre commit du rapport.

## Preuves nouvelles

| Suite réellement exécutée | Résultat | Portée |
| --- | --- | --- |
| Upgrade MySQL 8.4.7 | 21 contrôles réussis | Huit migrations Laravel D8, données synthétiques payées/reçus/intentions préexistantes, puis neuvième migration LAUNCH-04 |
| Intégration TEST | 33 contrôles réussis ; 23 sous-processus métiers concurrents | Portal/MySQL et réel Gateway HTTP à quatre workers ; Stripe et provisionneur simulés |
| Intégration LIVE simulé | 38 contrôles réussis ; 23 sous-processus métiers concurrents | Même moteur et vrai Gateway, y compris expiration d’autorisation et événements en attente |
| Suite PHPUnit | 212 tests / 2 135 assertions, réussite | SQLite mémoire, trois tests de politique/alerte nouveaux et suite LAUNCH-04 complète |
| Autres contrôles | Syntaxe PHP, Pint sur 123 fichiers, compilation Python, build Vite 799 modules, diff | Réussis dans les environnements isolés |

Les contrôles d’intégration ne sont pas additionnés aux assertions PHPUnit comme s’il s’agissait de la même métrique. Les 23 sous-processus comptent les courses ingest/process/billing du harnais, pas tous les processus Docker/PHP. Les résultats D7/D8 de paiement TEST et conversation réelle restent historiques : aucun scénario client D8 n’est rejoué ici.

## Isolation et provenance

MySQL neuf, réseau none, aucun port hôte, données sur tmpfs. Le runtime PHP est un conteneur neuf à réseau none ; il joint le seul MySQL par socket Unix temporaire et son propre Gateway par HTTP loopback. Aucune route vers Stripe ou les réseaux Docker actifs n’est utilisée. Le code Gateway, ses dépendances copiées de l’image D7 et ses contrôleurs/services financiers sont inchangés. Le wrapper de qualification réside uniquement dans le portail.

L’image de production ne contient pas les factories de développement : le wrapper ajoute leurs classes depuis les dépendances de test dans le processus jetable et charge le helper Faker conditionnel. Ce n’est pas une modification du runtime actif ou du moteur financier. Le fixture Gateway existant a été repris dans les tests Portal avec chemins de bootstrap et diagnostics expurgés adaptés ; les routes et classes financières réelles sont chargées depuis Gateway D7.

Tous les tokens, comptes et autorisations utilisés sont synthétiques. Les fixtures d’approbation LIVE simulée n’existent qu’en tmpfs, sous APP_ENV=testing, avec clés aléatoires sans valeur chez Stripe, et sont détruites avec le conteneur. Aucun artefact d’approbation commerciale réutilisable n’est publié ou installé. Aucun secret réel, .env de déploiement ou base existante n’est ouvert. Les conteneurs temporaires ont été supprimés, les services actifs préservés.

## Upgrade depuis D8

Le test exécute réellement le migrateur Laravel jusqu’aux huit migrations D8, puis crée des données synthétiques représentatives : organisation/propriétaire, abonnement payé, période granted, outbox succeeded, binding TEST, facture, reçu chiffré et job processed. C’est un seed contrôlé dans la base jetable, pas une copie d’un client réel et pas une preuve de paiement.

Après migration LAUNCH-04, les valeurs et références des huit tables métier examinées sont identiques sur leurs colonnes préexistantes. Les sept nouveaux champs fiscaux sont null sur l’ancienne facture, sans donnée inventée ; l’ancien reçu reste déchiffrable. Les triggers mode/compte, l’append-only des reçus et les contraintes d’unicité sont exercés sur MySQL. La référence financière et le period_id sont aussi testés indépendamment des autres identifiants. Une écriture fiscale interrompue est rollbackée ; HT/taxe/TTC et URL chiffrée sont relus ; un nouveau migrate est sans effet.

Aucune nouvelle migration LAUNCH-05. La migration LAUNCH-04 reste la seule différence de schéma à appliquer depuis D8, dans une mission ultérieure autorisée. La liste complète et l’ordre figurent dans LAUNCH05_RELEASE_PLAN.md.

## Contrats financiers intégrés

Le harnais réutilise le Checkout, l’inbox, le Processor, Reconciler, Worker et Gateway/WalletService existants. Aucune deuxième comptabilité ou wallet fictif n’est employé pour la preuve MySQL : les grants, clôtures, réserves et soldes sont lus dans le vrai schéma Gateway jetable.

Sont démontrés : Checkout des deux profils ; refus d’un webhook signé de mode opposé et de signature invalide ; réception atomique et déduplication concurrentes ; rollback d’une transaction financière interrompue puis reprise d’un job resté processing ; un grant par période ; perte du corps HTTP après commit SQL Gateway ; récupération de la même référence sans double crédit ; renouvellement clôturant le reliquat sans report ; isolation des deux organisations ; remboursement synthétique avec réserve engagée puis règlement et récupération du reliquat, sans refund d’usage.

La facture synthétique vérifie 4 900 centimes HT, 735 de taxe et 5 635 TTC, sans imposer de taux français. Les preuves fiscales sont relues après les traitements/rejeux sur MySQL et les liens sont chiffrés.

L’impayé confirmé de la seconde organisation bloque réellement l’admission financière Gateway, clôture le reliquat échu sans nouveau grant et conduit à une suspension technique confirmée par le provisionneur simulé. La régularisation autoritative donne un seul crédit et exige une nouvelle reprise propriétaire. Le contrôleur et les assertions v2 existants sont exercés avec une session propriétaire synthétique récente ; la reprise reste resuming jusqu’à opération succeeded et observation active simulées. Le rejeu ne crédite pas une deuxième fois.

**Limite de preuve :** les classes financières Gateway et MySQL/HTTP sont réelles ; les opérations de provisionnement, l’observation WebUI et l’API Stripe restent simulées. La session propriétaire est préparée par le harnais, pas par un nouveau test de login SMTP/navigateur. Il ne s’agit ni d’une qualification Stripe LIVE réelle, ni d’un nouveau cycle physique de conteneur WebUI.

## Arbitrage financier vérifié

Une anomalie de devise sur la période suivante d’une organisation déjà payée marque needs_review, sans nouvel événement financier, intention, grant, clôture ni renouvellement. Les derniers droits confirmés demeurent admis par la classe FinancialPeriods du Gateway jusqu’à leur échéance normale ; cette même classe refuse l’admission à l’échéance, sans fabriquer un impayé. La protection CommercialGate du portail est également testée avant/après échéance en PHPUnit.

Une autorisation LIVE synthétique expirée avec reçus en attente refuse Processor et Worker. Les états financiers, outbox, ledger et audit d’autorisation Gateway ne changent pas ; le reçu reste pending. Après rétablissement de la même autorisation synthétique, le même événement devient processed sans second grant. Aucun Checkout ou nouveau create n’est relancé aveuglément.

La politique LAUNCH-04 est donc conservée : données non fiables → revue/inconnu et opération bloquée ; seules les données autoritatives confirmées déclenchent attribution, impayé, remboursement et régularisation. Les droits préalables ne sont pas prolongés par une anomalie ni révoqués sur une information incompatible.

## Alerte et résolution

Ajout ciblé de stripe:health : lecture seule, sans appel Stripe, sans sortie d’identifiant client ou secret. Le JSON et le code de sortie signalent autorisation invalide/expirée, jobs needs_review, bindings needs_review/unknown et attente supérieure à cinq minutes ; le filtrage porte sur le mode/compte sélectionnés. Le champ processing_enabled est exposé séparément : ready n’est pas une autorisation commerciale ni une preuve que les traitements sont activés.

Les tests vérifient l’alerte d’expiration avec un événement pending, l’absence de modification du job et le cloisonnement des comptes/profils. La commande est prête à être raccordée à la supervision dans une mission d’exploitation ; aucun timer, envoi email ou service d’alerte n’a été installé. La procédure de résolution est détaillée dans le dossier de release : inspecter les erreurs, confirmer les faits, reprendre les mêmes IDs/références ; aucun crédit manuel ni nouvel objet aveugle.

## Échecs de harnais traités sans modifier D8

Les essais intermédiaires ont identifié : attente trop tôt sur le MySQL temporaire d’initialisation ; montage vendor impossible sous un répertoire source read-only sans mountpoint ; factories/helper Faker manquants dans les dépendances runtime ; résultat CLI Laravel d’erreur retournant sans JSON mais avec exit code 0 ; session utilisateur synthétique à rebinder pour le contrôleur ; permissions de journaux du nouveau clone après un lancement root.

Ces points sont corrigés dans l’orchestration/bootstrap des seuls tests. Le runner exige désormais une preuve JSON passed, le serveur MySQL définitif, le commit Gateway exact et propre ; il charge un snapshot read-only avec points de montage préparés, utilise l’utilisateur 1000 et protège les logs. Aucun échec intermédiaire n’est compté comme succès. Les résultats finaux ci-dessus sont issus d’une exécution complète figée des trois suites.

## État de livraison et limites restantes

Source technique committée/poussée sur la branche LAUNCH-05, PR en brouillon vers LAUNCH-04 ; quatre rapports centraux et index sur branche issue de reports/launch04-stripe-live, PR en brouillon. Aucun merge, migration D8, déploiement, paiement ou activation réelle.

Le code est prêt à être proposé pour une recette contrôlée **après** décision distincte et préparation d’une release. L’image commerciale LAUNCH-05 et son fallback compatible ne sont pas construits : leurs digests restent à établir et qualifier. La compatibilité MySQL/intégration financière est démontrée ; elle ne remplace pas le contrôle de l’image finale, du KYC/catalogue/compte live, du vendeur, de l’offre/dotation, de la fiscalité, des sauvegardes et alertes externes. Les limitations multi-compte/une identité par organisation et collisions globales refusées de LAUNCH-04 restent inchangées.

Aucun changement Gateway ou Infra indispensable n’a été identifié. Aucune mission suivante démarrée.

## Livraison et références GitHub

Portal feature/launch05-commercial-qualification : commit 679d3738cfb5a724bd0125cca52786cfc2d25545 ; [PR technique #14 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/14), base feature/launch04-stripe-live / 76a11ded222395633efe5fcc7c14a11c293c1e68. Les preuves nouvelles expurgées sont [consultables à ce commit](https://github.com/Pascal440/trinity-saas-portal/tree/679d3738cfb5a724bd0125cca52786cfc2d25545/docs/launch05/evidence). Aucune image commerciale candidate construite ou déployée.

Branche documentaire reports/launch05-commercial-qualification depuis reports/launch04-stripe-live / edb4b84ad14e7716682ae640d18e82a57dc7b2ff. Le SHA documentaire final est fourni par la PR et le livrable de mission.

## CI GitHub finale

[Portal CI 41644554393](https://github.com/Pascal440/trinity-saas-portal/actions/runs/41644554393), sur 679d3738cfb5a724bd0125cca52786cfc2d25545 : completed / success. Installation Composer/npm, validation, syntaxe, Pint, tests PHP, build, audits et scan de release réussis selon les métadonnées de job vérifiées. Les suites MySQL/HTTP sont les preuves locales isolées ci-dessus, distinctes de la CI applicative ; aucun nombre supplémentaire de tests CI n’est déduit de ce statut.
