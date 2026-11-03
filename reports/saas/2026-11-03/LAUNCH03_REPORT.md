# LAUNCH-03 — Qualification du lancement commercial

Date : 3 novembre 2026, observations vers 12 h 15–12 h 25 Europe/Paris.
Destinataire : Maya. Priorité P0 : première vente AI Workspace Pro, 49 € HT/mois.

## 1. Décision proposée

**NO-GO pour encaisser aujourd’hui via le parcours SaaS D8. GO pour préparer un pilote commercial assisté, conditionné à la levée des blocages P0 ci-dessous.** Ce GO de préparation n’autorise aucune correction, activation ou opération financière.

Le paiement TEST → crédit unique → activation → conversation IA est déjà démontré historiquement. Le principal développement manquant est une évolution bornée de l’adaptateur Stripe vers un mode live explicitement séparé : le code D8 refuse volontairement les clés live, les événements live et les sessions live. Un changement de variables ne suffit pas. Il n’est pas nécessaire de reconstruire le portail, le provisionneur, WebUI ou le ledger.

Les autres décisions P0 sont : identité du vendeur et cadre fiscal/contractuel vérifiés ; contenu exact de l’offre et marge ; configuration live du compte/catalogue/webhook ; traitements permanents et plan non limité à la recette ; support et récupération des données ; qualification ciblée des écarts live et du cycle impayé/régularisation. Le nom commercial définitif et la finalisation FRONT ne sont pas sur ce chemin critique.

### Arbitrages immédiats à rendre par Maya et l’opérateur

1. Vendeur légal, régime fiscal et premier segment autorisé. Proposition pour raccourcir : un premier professionnel en France, accompagné, sans promettre une ouverture internationale ou B2C.
2. Crédit EUR d’usage inclus, modèles autorisés, quotas, durée du plan, délai d’activation et support. Ne pas adopter le crédit D7 de 1 EUR ou les 10 requêtes D8 comme offre définitive.
3. Autoriser dans une mission distincte l’extension live du Stripe existant et sa qualification, avec conservation des protections compte/mode/idempotence.
4. Choisir un profil commercial isolé des identités TEST, en réutilisant les composants D8 ; autoriser séparément sa mise en service après les preuves requises.

## 2. Périmètre, sources et limites de preuve

Audit en lecture seule des dépôts techniques et de métadonnées de l’hôte. Seules écritures de livraison : ce rapport et l’index dans Pascal440/trinity-docs. Aucun paiement, appel API Stripe authentifié, changement Stripe, migration, redémarrage, déploiement, fusion ou changement de configuration. Aucune requête aux bases, aucune lecture des conversations, aucune action sur une instance cliente ou les crédits. Aucun test historique rejoué ; pas de développement dans les anciens répertoires.

Les copies d’audit techniques ont été clonées dans un nouvel espace distinct. Aucun fichier .env, clé, mot de passe ou contenu de fichier secret ouvert. Les paramètres runtime ont été filtrés dans le processus de lecture avant affichage ; seuls flags non secrets et états de présence utiles ont été retenus. Les adresses d’exploitation, clients, identifiants Stripe, ressources de stockage et chemins privés sont volontairement omis du rapport publié.

### Références Git examinées

| Dépôt | Branche / référence | SHA | PR / rôle |
| --- | --- | --- | --- |
| trinity-docs | reports/workspace02-saas, base de cette mission | d08adefa270a1c5a66e07f5e389cae9adfd673e3 | [#1](https://github.com/Pascal440/trinity-docs/pull/1), ouverte en brouillon |
| trinity-saas-infra | ops/launch023d8-first-ai-client | 5bd6fee98a468191613766e0093bdcda8de59099 | [#15](https://github.com/Pascal440/trinity-saas-infra/pull/15), brouillon, base D7 |
| trinity-saas-portal | fix/launch023d8-owner-activation | b9c84b5de9671c1be73f8e8cb3198bea3cfec855 | [#8](https://github.com/Pascal440/trinity-saas-portal/pull/8), brouillon, base D7 |
| trinity-gateway | fix/launch023d7-noninteractive-financial-actor | f79ff7f4ca938e0610a6e753b4b107dd4edc7437 | [#9](https://github.com/Pascal440/trinity-gateway/pull/9), brouillon, base LAUNCH 02.2 |

Le rapport ne confond pas main et la référence D8. Les chaînes de PR restent empilées. Une intégration/release revue est nécessaire avant ouverture commerciale ; fusionner toutes les PR ou reprendre les branches FRONT n’est pas un préalable technique à la première vente. Une future livraison doit épingler ses sources et images, sans modifier les PR de cette mission.

Sources primaires du projet :

- [D6 — réception signée et migration Endive](https://github.com/Pascal440/trinity-saas-infra/blob/5bd6fee98a468191613766e0093bdcda8de59099/LAUNCH023D6_REPORT.md).
- [D7 — Checkout sandbox et crédit unique](https://github.com/Pascal440/trinity-saas-infra/blob/5bd6fee98a468191613766e0093bdcda8de59099/LAUNCH023D7_REPORT.md).
- [D8 — activation, inférence et restauration D7](https://github.com/Pascal440/trinity-saas-infra/blob/5bd6fee98a468191613766e0093bdcda8de59099/LAUNCH023D8_REPORT.md).
- [Politique financière V1](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/docs/launch021/POLICY.md), [tests Stripe historiques](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/docs/launch022/TEST_RESULTS.md), [prérequis commerciaux](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/docs/launch022/COMMERCIAL_PREREQUISITES.md).

Les rapports sources peuvent comporter des références opérationnelles historiques ; elles ne sont pas recopiées ici. Les réserves anciennes « aucun paiement sandbox qualifié » sont levées pour le scénario D7, sans être interprétées comme une qualification du live ou de tous les événements.

## 3. Parcours commercial reconstitué

| Étape | Déjà démontré | Limite / observation LAUNCH-03 |
| --- | --- | --- |
| Inscription et vérification du propriétaire | D7 : inscription normale, mot de passe choisi par l’opérateur, vérification par SMTP et approbation commerciale applicative | Historique ; aucun nouvel email ou utilisateur créé. L’approbation préalable fait partie du parcours, ce n’est pas un achat totalement autonome. |
| Checkout Stripe TEST | D7 : Checkout normal, paiement de 49 EUR en sandbox, facture paid et lecture Stripe autoritative | Ce n’est pas un encaissement réel ni une validation de TVA ; aucun objet Stripe relu aujourd’hui. |
| Webhooks | D6 : premier événement réel signé accepté et reçu durable après redémarrage. D7 : événements abonnement/Checkout/facture traités et deux rejeux réels HTTP 200 | Réception TEST seule déclarée aujourd’hui ; l’ACK prouve la réception, pas l’attribution ni l’activation. |
| Attribution de crédits | D7 : exactement un topup de 1 EUR d’usage via outbox et worker, inchangé après rejeux | Dotation de recette, pas politique tarifaire. Aucun solde actuel relu. |
| Provisionnement WebUI | D8 : instance dédiée par les contrats existants, réseau/volume propres, HTTPS | Instance healthy observée dans Docker ; aucune requête à l’instance, aucun nouveau provisionnement. |
| Activation du propriétaire | D8 : ticket, identité récente et mot de passe fourni par le propriétaire ; job succeeded, onboarding active ; correction owner également admin | Image Portal D8 retrouvée. Aucun statut métier actuel vérifié en DB. |
| Première conversation IA | D8 : réponse fournisseur réelle depuis WebUI et persistance après redémarrage ; trois consommations dont un appel auxiliaire | Aucun appel IA répété ; conversation actuelle non ouverte. |
| Comptabilisation de consommation | D8 : 0,00096512 EUR débités en trois appels, réserves soldées, zéro réserve restante et un seul topup historique | Mesure réelle historique, différente du coût fournisseur estimé. Le solde actuel n’est pas affirmé. |
| Suspension et reprise après régularisation | LAUNCH 02.1/02.2 : états versionnés, neutralisation asynchrone, reprise après confirmation et nouvelle action propriétaire ; tests synthétiques réussis, dont test_payment_failure_regularization_and_fresh_owner_resume_are_technically_confirmed | Aucun cycle complet impayé Stripe réel → suspension de l’instance → règlement → reprise réelle n’est démontré par D6/D7/D8. Les phases antérieures prouvent des briques techniques, pas l’assemblage Stripe réel. |
| Renouvellement / annulation / remboursement | Implémentés et testés historiquement, notamment doublons, perte de réponse, clôture sans report et remboursement conservateur | Pas de renouvellement mensuel réel D7 arrivé à échéance ; aucune qualification financière complète live. Ne pas annoncer ces fonctions comme absentes à redévelopper. |

D8 limite la recette à 10 requêtes, avec 2/minute, 10/heure/jour/mois et 2 048 tokens de sortie. Le plan expire le **3 novembre 2026 à 16 h 48 min 20 s Paris**, d’après son manifeste et son rapport. Cette échéance n’a pas été relue dans la base aujourd’hui ; elle reste la dernière durée documentée et ne permet aucune promesse d’un mois commercial. Le crédit test D7 avait une période distincte, jusqu’au mois suivant : crédit disponible et autorisation technique valide sont deux conditions différentes.

## 4. État effectivement observable pendant cet audit

### Services et HTTPS

Treize conteneurs présents : douze healthy et un registre actif sans healthcheck annoncé. Les sept services centraux et l’instance WebUI sont en cours d’exécution. Les quatre previews FRONT sont séparées ; aucune n’est nécessaire au paiement D8.

Images observées : Portal sha256:50173a5cf60b06f87ac392b8187b1bd4d47387feb89c05301a488e99754aa4f5 et Gateway sha256:71d466513a1b85539313d47f6928da0159dbb52a964a1895f68becacf7453852, cohérentes avec D8/D7. Cela ne prouve pas l’état métier ou le contenu des bases.

Le domaine du portail indiqué par le manifeste public résout. Une poignée de main TLS depuis l’hôte valide le nom et la chaîne de confiance, en TLS 1.3 ; échéance du certificat : 31 janvier 2027 à 11 h 34 min 58 s Paris. Aucune requête HTTP applicative, aucune session ni visite WebUI. Ce contrôle n’est pas un test d’accessibilité depuis un réseau extérieur indépendant. HTTPS et domaine existent : il n’y a pas à les reconstruire. Leur emploi commercial, leur maîtrise et le renouvellement du certificat doivent être confirmés par l’opérateur ; changer de marque/domaine n’est pas imposé par la technique.

### Paramètres déclarés des conteneurs

| Paramètre non secret | Observation |
| --- | --- |
| STRIPE_TEST_ENABLED | true, Portal et scheduler |
| STRIPE_TEST_PROCESSING_ENABLED | false, Portal et scheduler |
| STRIPE_BILLING_MODE | test |
| STRIPE_TEST_UNIT_AMOUNT | 4900 centimes EUR |
| STRIPE_TEST_AUTOMATIC_TAX | false |
| BILLING_ENABLED | false |
| BILLING_MONTHLY_CREDIT | vide |
| FINANCIAL_ENABLED | false, Gateway |
| FINANCIAL_MONTHLY_CREDIT | vide, Gateway |
| APP_ENV / APP_DEBUG | production / false sur les conteneurs observés |

Ces valeurs viennent uniquement de Config.Env via docker inspect. Aucun boot Laravel ou lecture de cache contenant potentiellement des secrets n’a été effectué ; l’effectivité exacte après entrypoint/cache n’est pas certifiée. Elles concordent avec le profil réception seule documenté. APP_ENV=production ne signifie pas paiements live. Le moteur de consommation sur la période existante est distinct des traitements administratifs financiers désactivés.

### Sauvegarde et alertes

Le dernier enregistrement externe indique une fin réussie le **3 novembre à 03 h 20 min 43 s Paris** : exit code 0, dump SQL, chiffrement, destination hors VPS et contrôle d’intégrité déclarés ; six écrivains et une instance cliente quiescés. Les dernières exécutions systemd backup/monitor ont Result=success. Aucun backup ou restore lancé pendant cette mission.

Ce dernier enregistrement porte full_data_read=false, restoration_from_s3_verified=false et password_custody_off_vps_verified=false. Cela indique que cette exécution ne certifie pas ces contrôles, sans annuler les restaurations D5/D6/D7 historiques. D8 démontre la restauration isolée D7 avec copie externe du mot de passe. Les snapshots D8 incluant la conversation et le volume client ne sont pas annoncés comme restaurés. Une restauration ciblant ce nouveau périmètre constitue une nouvelle preuve utile ; il n’y a aucune raison de rejouer la restauration D7 identique.

Le fichier privé attendu par le notifier de sauvegarde est absent (existence seulement contrôlée). Le code prévoit alors une file durable, sans envoi email. Le SMTP fonctionnel du portail D7 ne prouve donc pas les alertes d’exploitation. Le monitor peut réussir tout en restant incapable de prévenir l’opérateur à l’extérieur de l’hôte.

## 5. Ce qui est réutilisable sans nouvelle architecture

- Portail : comptes, organisations, propriétaire/admin, approbation, session récente, parcours d’activation et états d’erreur.
- Provisionneur : v2 signé, idempotence, tickets, scopes organisation/session, suspension et reprise, volume WebUI dédié.
- Stripe : Checkout hébergé à prix serveur, vérification compte et catalogue, HMAC sur corps brut, reçus chiffrés, jobs durables, reprise et rapprochement autoritatif.
- Finance : périodes, autorisation versionnée, outbox, grant unique, clôture des reliquats, refus de crédit sur simple retour navigateur ; ledger et réserves dans Gateway, pas de seconde comptabilité.
- Exploitation : images immuables, HTTPS existant, sauvegarde S3 chiffrée, procédures de restauration, scheduler et commandes de reprise.

Ces composants n’ont pas besoin d’être réécrits pour la première vente. Les tests historiques ne sont pas réexécutés dans LAUNCH-03. Les améliorations live futures devront réutiliser ces tests et ajouter uniquement les assertions modifiées, les cas mode/compte croisés et les parcours non encore assemblés.

## 6. Blocages et classement des écarts

P0 = bloquant avant premier paiement ; P1 = nécessaire avant élargissement commercial ; P2 = amélioration ultérieure. Un élément « non vérifié » est une preuve manquante à lever, pas une affirmation d’absence.

| ID | Écart et preuve | Classe | Résolution minimale / responsable |
| --- | --- | --- | --- |
| B1 | Adaptateur D8 test-only, refus live dans code, bindings et UI | P0 — confirmé | Codex, mission distincte : évolution live bornée et explicite, refus des mélanges de mode, compte, price et metadata ; garder les contrats financiers. |
| B2 | Compte vendeur Stripe live, activation/KYC, capacité d’encaissement et versement non vérifiés ; catalogue/destination live non inspectés | P0 — preuve manquante | Opérateur : vérifier compte légal et habilitations, puis préparer Product/Price mensuel EUR 49 HT exclusive et webhook live versionné dans une mission autorisée. Ne pas réutiliser les objets TEST. |
| B3 | Traitements administratifs déclarés arrêtés ; quantité mensuelle vide des deux côtés | P0 — confirmé comme configuration déclarée | Décider quantité d’usage, configuration concordante Portal/Gateway et fonctionnement permanent des workers/scheduler. Prévoir pause des nouveaux achats et reprise des mêmes références sans arrêter les preuves. |
| B4 | Plan D8 limité à la recette et échéance du jour, quotas non commerciaux | P0 — dernière référence documentée | Maya : plan et quotas mensuels explicites pour le futur client, modèle viable, budget fournisseur ; opérateur configure plus tard par les chemins applicatifs existants. Ne pas prolonger le pilote dans cet audit. |
| B5 | Identité juridique du vendeur, régime TVA, obligations de facturation, CGV/conditions et traitement des données non établis par les sources | P0 — preuve manquante | Opérateur/Maya avec conseil compétent : valider le vendeur, cas B2B initial, prix/taxes, justificatif et contrat. Le nom de marque peut rester provisoire si le vendeur légal est correctement identifié. |
| B6 | Automatic tax désactivé ; collecte adresse présente mais mise à jour du Customer et collecte identifiant fiscal non présentes dans le payload examiné ; justificatif fiscal complet non démontré | P0 pour le traitement fiscal retenu | Qualifier un seul cas fiscal initial ; adaptation ciblée si nécessaire ; fournir facture conforme, identité client, montant HT/taxe/TTC et accès au justificatif, éventuellement assisté. Ni 49 EUR TEST ni un reçu de paiement ne prouvent la conformité. |
| B7 | Cycle réel assemblé impayé → neutralisation → régularisation → reprise non prouvé ; refus live encore volontaire | P0 pour ouvrir un abonnement récurrent | Étendre les preuves dans un environnement isolé avec la future version : cas ciblés manquants, sans agir sur la recette D8. Réutiliser les assertions existantes ; pas de nouveau moteur de cycle de vie. |
| B8 | Canal externe d’alerte backup absent ; contact support, délai et procédure d’activation ambiguë non validés commercialement | P0 — exploitation minimale | Support humain nommé et joignable, revue des jobs/reçus/erreurs ; un canal externe d’alerte réellement livré. Un outil de tickets ou une astreinte 24/7 ne sont pas requis pour un pilote explicitement assisté. |
| B9 | Restauration historique D7 réussie, mais volume/conversation D8 et accès de secours complets non requalifiés | P0 — preuve minimale de récupérabilité du service vendu | Restauration isolée ciblée du périmètre nouveau WebUI + correspondances SQL/états/clé ; accès externe aux secrets de récupération et procédure opérateur. Définir RPO/RTO et interruptions ; ne pas rejouer D7 sans changement. |
| B10 | Accès administratifs historiques à durcir, filtrage fournisseur et accès de secours non requalifiés ; santé Docker seule insuffisante | P0 — clôture ciblée du risque d’exploitation | Opérateur : valider accès administratifs protégés, secours indépendant et exposition limitée aux routes prévues, sans refonte réseau. Les détails d’accès sensibles sont omis ici. |
| E1 | Offre multi-modèle, internationale ou B2C, remises/proratas/crédits de balance hors contrat V1 | P1 si souhaités | Restreindre le premier pilote au contrat existant ; qualifier chaque extension avant la vendre. Ne pas développer ces cas pour une première vente simple. |
| E2 | Charge, deuxième client réel, dimensionnement et isolation sous concurrence non qualifiés globalement | P1 | Mesure et essai d’isolation supplémentaires avant augmentation des clients, limites de capacité et coût de stockage ; le pilote doit être borné. |
| E3 | Supervision durable, vieillissement des files, rapprochements paginés, réserves ambiguës, revue des sauvegardes et mises à jour | P1 au-delà de la surveillance humaine initiale | Automatiser progressivement les contrôles déjà disponibles ; conserver immédiatement une surveillance humaine explicite sur ces points. |
| E4 | Reprise après remboursement et souscription suivante limitée par la politique terminale V1 | P1 si cette promesse commerciale est requise | Assumer une revue humaine et l’expliquer avant vente ; ne pas promettre un remboursement proratisé ou une réouverture automatique. |
| A1 | Nom commercial, animations/sculpture et fusion FRONT | P2 | Aucun blocage technique au premier client accompagné ; identité légale et offre honnête restent P0. |
| A2 | Haute disponibilité, nouvelle architecture, SSO complet, portail support avancé | P2 pour un pilote aux engagements limités | Évolution selon engagements et demande, pas préalable systématique au premier abonnement. |

### B1 — Portée exacte de l’évolution live

Le refus est distribué, donc retirer une regex ou changer un flag serait insuffisant :

| Code D8 | Garde observée | Conséquence |
| --- | --- | --- |
| [Secrets.php L11](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Stripe/Secrets.php#L11) | mode doit être test | live bloqué avant accès à Stripe |
| [Client.php L24/L41](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Stripe/Client.php#L24) | livemode=false et clé test | objets et clé live refusés |
| [Inbox.php L59](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Stripe/Inbox.php#L59) et Contract/Processor | événement et reçu attendus en test | réception/traitement live à rendre cohérents, sans mélange |
| [Checkout.php L28/L135](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Stripe/Checkout.php#L135) | source stripe_test, mode/metadata test et session cs_test | création/récupération live non disponibles |
| [Identity.php](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Stripe/Identity.php) | binding et metadata environnement test | identités TEST non convertibles implicitement |
| [Reconciler.php L223](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Stripe/Reconciler.php#L223) et [Billing/Worker.php L32](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/app/Services/Billing/Worker.php#L32) | source stripe_test dans publication/relecture | ne pas contourner le rapprochement avec une nouvelle source mal reconnue |
| [StripeBilling.vue L15](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/resources/js/Pages/StripeBilling.vue#L15) | mention permanente bac à sable sans paiement réel | UI commerciale à aligner sur le mode réellement servi |

La politique source et les contraintes des tables doivent être vérifiées avant de décider si une migration additive est nécessaire ; cet audit ne l’affirme ni ne l’autorise. Les organisations, reçus, abonnements et crédits TEST existants ne doivent pas devenir des données live par simple changement de valeur. L’espace client D8 doit rester intact. La séparation peut s’appuyer sur les profils et contrôles existants ; aucun nouveau microservice ou nouvelle comptabilité n’est justifié ici.

### B5/B6 — Taxes, facture et vendeur

Constat code : Catalog impose EUR mensuel, tax_behavior=exclusive, prix serveur ; Checkout demande billing_address_collection=required et possède un flag automatic_tax. Reconciler vérifie le sous-total HT attendu puis la cohérence amount_paid/amount_due/total/InvoicePayment/PaymentIntent/Charge ; il ne force pas le total payé à 49 EUR quand une taxe s’ajoute. Les contrôles financiers sont donc réutilisables. La collecte adresse seule ne prouve ni régime fiscal ni conformité des factures.

Checkout crée auparavant un Customer avec metadata, sans adresse ni identité fiscale dans ce payload, et ne transmet pas customer_update.address ou tax_id_collection dans la création de session examinée. La documentation Stripe recommande customer_update.address=auto pour utiliser l’adresse collectée sur un Customer existant avec le calcul automatique : c’est un point d’intégration à qualifier sur le contrat Endive épinglé, pas une erreur API reproduite pendant LAUNCH-03. L’identifiant fiscal n’est requis que selon les cas vendus, pas uniformément pour tous les clients. [Stripe Tax — Checkout](https://docs.stripe.com/tax/checkout/page).

La page existante propose le règlement d’une facture ouverte et l’annulation en fin de période ; aucun parcours complet d’accès au justificatif d’une facture déjà payée n’a été identifié dans les fichiers examinés. La remise d’une facture conforme peut être assurée manuellement au premier client si elle est traçable ; développer un historique PDF dans le portail n’est pas indispensable à la première vente.

Les mentions vendeur/client, numérotation, description, dates et traitement HT/TVA/TTC doivent être validés pour le cas retenu. Aucun taux universel n’est déduit d’un prix de 49 € HT ; si le taux légal applicable retenu est 20 %, le total est 58,80 €, mais ce n’est pas une décision fiscale de cette mission. [Service Public — mentions des factures](https://entreprendre.service-public.gouv.fr/vosdroits/F31808?lang=fr).

En novembre 2026, la réception des factures électroniques est déjà une obligation applicable aux entreprises entrant dans le champ de la réforme ; pour les PME/micro-entreprises, l’émission concernée est prévue au 1er septembre 2027. Le statut exact du vendeur et le calendrier applicable doivent être vérifiés, sans imposer une nouvelle plateforme de facturation interne. Un PDF Stripe n’établit pas à lui seul la conformité au dispositif français. [Service Public — mise en conformité](https://entreprendre.service-public.gouv.fr/vosdroits/F39785).

Si le service traite des données personnelles pour le compte du client, les rôles, instructions, sous-traitants et contrat correspondant doivent être cadrés ; le fournisseur IA et les transferts éventuels sont à examiner avant de promettre une résidence ou confidentialité particulière. Aucune conclusion sur leur conformité ou non-conformité actuelle n’est tirée sans leurs contrats. [CNIL — article 28](https://cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4).

## 7. Plan minimal ordonné, à autoriser séparément

| Ordre | Action future | Réutilisation | Critère de sortie |
| --- | --- | --- | --- |
| 1 | Maya et opérateur figent une fiche pilote : vendeur, segment, 49 HT, taxe, dotation EUR d’usage, modèle/quotas, durée, support, conditions et annulation | Offre unique AI_WORKSPACE_PRO et politique V1 | Décisions explicites et marge bornée ; aucune promesse illimitée, aucun nom de marque exigé pour retarder l’identité légale. |
| 2 | Opérateur vérifie la capacité live du compte vendeur, fiscalité/facture, domaine existant et autorisations fournisseur | Compte/processus Stripe et HTTPS existants | Preuves de capacité d’encaisser, facturer et verser ; objets live distincts préparés seulement après autorisation. Les secrets restent hors rapport. |
| 3 | Codex fait une évolution live ciblée de l’adaptateur D8 et UI, avec revue des sources, compte/mode, contraintes, metadata et reprises | Client Stripe, inbox, jobs, catalog, contrats 02.1, ledger, provisioning et activation | PR révisable, tests nouveaux live/test croisés et non-régression des garde-fous ; aucune adoption de données TEST en live. Ne pas refaire une intégration Stripe parallèle. |
| 4 | Qualifier seulement les écarts : fiscalité retenue, configuration live admissible/refusée, renouvellement et cycle réel sandbox impayé/régularisation avec WebUI de test isolé | Suites existantes et protocole D7/D8 | Pour les changements de mode : tests de contrat isolés ; pour le cycle non démontré : nouveau parcours sandbox autorisé. Succès technique après observation, pas ACK seul. Aucun test contre l’instance D8. |
| 5 | Fermer le minimum d’exploitation : support humain, alertes externes, contrôle des accès, restauration isolée du nouveau volume WebUI et rapprochement SQL/états | Backup S3, scripts de restauration et procédures v2 | Récupération documentée sans reset/destruction ; RPO/RTO et coupure backup acceptés ; opérateur reçoit l’alerte et dispose des accès de secours. |
| 6 | Préparer puis faire approuver une release commerciale épinglée et un profil sans échéance de recette | Images/Compose/manifeste existants et scheduler | Source/image/config approuvées, monthly credit identique Portal/Gateway, workers actifs au bon rythme, seuils de revue/rollback. Déploiement distinct explicitement autorisé ; D8 préservé. |
| 7 | Première souscription d’un client réel, accompagné, après GO opérateur/Maya | Parcours normal inscription → approbation → Checkout → webhook → grant → activation → conversation | Paiement réel du client, facture remise, exactement un grant conforme, service actif, coût borné. Aucun paiement artificiel de qualification ni recharge SQL. Chaque action financière est autorisée séparément. |
| 8 | Suivre la première période et son renouvellement ; rester assisté avant d’élargir | Réconciliation, annulation et support existants | Écarts traités, continuité et économie vérifiées ; élargissement seulement après la preuve manquante correspondante. |

Les étapes de code et d’exploitation peuvent être préparées en parallèle organisationnel, mais aucun paiement n’est ouvert avant leurs critères P0. Cette séquence n’est pas un lancement automatique de corrections. Aucun délai chiffré n’est inventé : les décisions vendeur/TVA/compte live peuvent conditionner le chemin davantage que le code.

### Une facture externe ou un Payment Link permet-il de vendre immédiatement ?

Pas de voie de livraison déjà prête démontrée. Le cœur 02.1 accepte des snapshots provenant d’adaptateurs de confiance, mais la seule commande simulateur est bloquée hors local/testing ; la réconciliation D8 reconnaît stripe_test. Un paiement externe ne doit pas être transformé en crédit par SQL, par simulateur en production, par faux statut paid ou par activation manuelle non auditée.

Une première vente assistée hors Checkout pourrait être une décision commerciale distincte, mais demanderait un adaptateur d’encaissement vérifié, ses preuves et ses procédures de cycle de vie. Son économie de travail n’est pas établie ; elle n’est donc pas recommandée comme raccourci acquis. Le chemin proposé conserve le Stripe déjà développé.

## 8. Risques financiers et opérationnels à accepter ou résoudre

- 49 € HT est un prix de service, pas 49 € de crédits ni une garantie de marge. Déduire frais de paiement, infra, stockage/sauvegarde, fournisseur et support ; réserver un budget maximum par période. La dotation D7 de 1 EUR et la conversion de recette sans majoration ne fixent aucune politique durable.
- D8 montre qu’un appel avec raisonnement peut atteindre 2 048 tokens sans réponse finale utile, et qu’un appel auxiliaire WebUI consomme aussi budget et quota. L’offre doit expliquer ce qui compte ; un réglage de modèle ou sa sélection est à décider, sans promettre un nombre de réponses à partir des seuls tokens.
- Aucun découvert, report ou recharge automatique selon V1. Une réserve ou tentative fournisseur ambiguë peut bloquer la clôture de période : support et réconciliation doivent conserver la référence, pas re-créditer au hasard.
- Le remboursement de paiement déclenche une suspension et revue, récupère le reliquat après résolution des réserves et conserve la consommation déjà payée au fournisseur. La perte résiduelle, l’avoir et la relation client restent à décider ; aucun remboursement automatique au prorata n’est promis.
- Réactiver les workers sans examiner les reçus/intents pendants peut produire des effets différés. D7 a traité son ancien QA D6, mais aucun état actuel des files n’est certifié ici. La future activation doit contrôler les cas en attente avant toute ouverture.
- Les sauvegardes quiescent des services et une instance cliente : interruptions à annoncer dans les engagements. Une réussite de sauvegarde n’équivaut pas à une restauration testée ; les données WebUI ajoutent un périmètre distinct du dump D7.
- Préproduction, données de recette, previews et registre vivent sur le même hôte ; aucune capacité commerciale ou isolation de charge globale n’est prouvée par un healthcheck. Un pilote limité peut réutiliser cet hôte après validation explicite, sans obligation d’une nouvelle architecture ; ne pas promettre une HA ou un SLA non démontré.
- Disponibilité fournisseur, résidence des données, conditions de sous-traitance et politique de sécurité des versions doivent correspondre aux engagements du premier client. Les tarifs/modèles D8 sont des observations datées, pas des prix actuels revalidés dans cette mission.

### Support minimal d’une activation échouée

Réutiliser [les procédures v2 existantes](https://github.com/Pascal440/trinity-saas-portal/blob/b9c84b5de9671c1be73f8e8cb3198bea3cfec855/docs/phase612/OPERATIONS.md) : demande et référence existantes, observation du job, nouvelle authentification propriétaire si session expirée ; nouveau ticket si échec/expiration autorisés. Après résultat final perdu, relire le job sans rejouer le mot de passe. Le mode recover demande le mot de passe déjà choisi ; compte ambigu ou mot de passe perdu = investigation conservant données et états. Aucun reset du volume, faux auth_time, second create ou second grant. En cas de paiement confirmé mais service non délivré, suivre un dossier client jusqu’à activation ou décision financière explicite.

## 9. Vérifications réellement faites et travail non fait

Réalisé : lecture des rapports D6/D7/D8 et PR ; inspection statique du code D8 Stripe/finance/UI/procédures ; SHA des clones et branches ; santé Docker et IDs d’images ; extraction filtrée des flags ; résolution DNS et validation TLS du portail ; métadonnées locales de sauvegarde et résultat systemd ; existence de configuration du notifier ; consultation de sources officielles Stripe/Service Public/CNIL le 3 novembre 2026.

Non réalisé : tests unitaires/builds/navigateurs, test de carte ou paiement réel, GET Stripe authentifié, scan extérieur, requête aux bases, lecture des files métiers ou des soldes, nouvelle conversation, interrogation WebUI, sauvegarde/restauration, essai d’alerte/email, vérification KYC/compte bancaire, audit juridique complet, changement de secret ou de configuration. Aucune preuve historique rejouée pour la seule raison de refaire un audit.

Sources officielles utilisées pour cadrer les prérequis, et non pour affirmer l’état du compte de l’opérateur : [Stripe — compte live](https://docs.stripe.com/get-started/account/set-up), [checklist live](https://docs.stripe.com/get-started/checklist/go-live), [taxes Checkout](https://docs.stripe.com/tax/checkout/page), [factures françaises](https://entreprendre.service-public.gouv.fr/vosdroits/F31808?lang=fr), [facturation électronique](https://entreprendre.service-public.gouv.fr/vosdroits/F39785), [CNIL article 28](https://cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4). Les prescriptions générales ne remplacent pas l’examen du cas fiscal/contractuel du vendeur.

## 10. État de livraison et arbitrage

Livraison documentaire seulement : branche reports/launch03-commercial issue de reports/workspace02-saas au commit d08adefa270a1c5a66e07f5e389cae9adfd673e3 ; PR en brouillon ciblant cette base. Aucun code technique modifié, committé ou poussé ; aucun service déployé ou modifié. Le SHA documentaire final et le lien PR sont fournis dans le livrable et les métadonnées GitHub pour éviter une référence au propre commit du rapport.

Maya peut décider une suite bornée « pilote live assisté » en réutilisant D8, avec B1 à B10 comme portes de sortie P0 ; le niveau de preuve requis est détaillé, sans exiger une refonte ni redévelopper les mécanismes existants. Aujourd’hui : **NO-GO premier encaissement par D8 ; GO conditionnel pour un premier pilote après fermeture des P0.** Aucune correction lancée automatiquement.
