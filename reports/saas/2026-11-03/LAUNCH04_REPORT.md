# LAUNCH-04 — Extension contrôlée Stripe TEST / LIVE

Date : 3 novembre 2026, Europe/Paris. Destinataire : Maya.
**GO développement réalisé ; NO-GO activation LIVE maintenu.**

## Références et périmètre

Dépôt technique autorisé : Pascal440/trinity-saas-portal. Base exacte : fix/launch023d8-owner-activation, b9c84b5de9671c1be73f8e8cb3198bea3cfec855. Branche indépendante : feature/launch04-stripe-live. Ancêtres vérifiés avant modification : D8 → D7 12ef3933e13b3fef72d28b6436cf0398d117ee41 → D6 824ad1796fced672a2e49823dae35d963667ca25 → LAUNCH 02.2 ad88d19942504604f5544eef3b57eab113e53247. Les dépendances fonctionnelles D8 sont conservées ; les prototypes FRONT ne font pas partie de cette branche.

Nouveau clone isolé, sans réutilisation des sources montées ou du clone historique sale. Aucune écriture dans Gateway/Infra, aucune lecture/modification des bases actives, aucune action sur l’instance cliente D8, aucun déploiement/redémarrage/fusion. Aucun accès Stripe authentifié ni clé LIVE réelle utilisée. Les formes de clés créées par les tests sont purement aléatoires et synthétiques ; tous les appels HTTP sont interceptés et le conteneur n’a pas de réseau.

## Résultat fonctionnel

Le même client, inbox, processeur, Checkout, réconciliateur et worker financier acceptent désormais les contextes test et live explicitement sélectionnés, avec paramètres et autorités séparés. Un seul profil est actif par processus ; aucune sélection de mode depuis le navigateur ou depuis le corps d’un webhook.

TEST conserve les anciennes variables plates et les mêmes clés d’idempotence envoyées à Stripe : les demandes D8 déjà en vol ne sont pas réécrites. LIVE utilise ses propres variables, désactivées par défaut, et ses clés HTTP d’idempotence sont dérivées du mode live, du compte attendu et de la référence persistée. La reprise conserve toujours cette référence, y compris après une réponse perdue ; pas de second create aveugle après 23 heures.

Profile centralise la sélection. LIVE exige simultanément : sélection live, enabled explicite, compte attendu, identité commerciale complète, dotation mensuelle positive et fichier privé d’approbation valide/expirant lié à l’empreinte exacte de la configuration. Les POST et workers exigent en plus processing_enabled ; la couche finance conserve BILLING_ENABLED et les contrôles Gateway existants. Aucun fichier d’approbation ni clé live ni valeur commerciale réelle n’est livré. Un changement isolé de mode ou de flag à partir des valeurs livrées ne suffit pas à autoriser LIVE.

L’approbation est un artefact d’exploitation privé à permissions restreintes, pas une signature cryptographique de Maya et pas une défense contre un administrateur malveillant ou un backend compromis. Sa création et son installation futures doivent relever d’une mission autorisée. Le code vérifie sa référence, son expiration et son hash de configuration ; il ne peut pas vérifier une décision humaine externe. Les chemins de clés peuvent tourner sans changer le hash : chaque credential sélectionné reste vérifié par format de mode et GET /account dans le client.

## Séparation et garde-fous conservés

- Clé API test en contexte live et inverse : refus avant envoi ; contrôle du compte par /account avec la même clé que l’opération ; API Endive épinglée.
- Objets Price/Product/Customer/Subscription/Invoice/PaymentIntent/Charge/Event validés sur leur type et livemode ; catalogue actif, EUR mensuel, prix serveur, tax_behavior exclusive et offer_code contrôlés.
- Metadata organisation, référence d’abonnement, référence Checkout, mode et offre strictes. Customer vérifié sur environnement et liens organisation/abonnement. Aucun binding étranger adopté.
- Deux routes webhook explicites, /stripe/test/webhook et /stripe/live/webhook, chacune refusant le mode opposé. HMAC du corps brut, fenêtre de signature, rotation, contrôle version et refus Connect/context thin conservés. Le compte des événements plateforme sans champ account est rattaché à la destination configurée, puis confirmé avant effets métier par la relecture de l’événement sur le compte attendu ; une signature seule ne vaut jamais preuve de paiement.
- Reçus append-only, compte/mode persistés, identité d’événement, chiffrement et ACK après commit du job. Le worker vérifie aussi le compte/mode du reçu et la version/famille du snapshot autoritatif relu.
- Sources financières stripe_test et stripe_live distinctes dans le portail. Le worker reconnaît les deux comme exigeant le même rapprochement Stripe avant toute opération ; il ignore le profil opposé et n’envoie pas un grant déjà en attente si l’autorisation n’est plus valide.
- Balayage des jobs, réconciliation et contrôles bornés au compte/mode sélectionnés. La commande historique stripe:test-configuration reste exclusivement TEST, pour ne pas la transformer implicitement en diagnostic live authentifié.
- Aucun grant au retour navigateur, avant facture payée autoritativement, sur crédit de balance/hors Stripe ou sur un événement au contexte incompatible. Outbox, réserves, ledger Gateway et reprise v2 inchangés dans leurs contrats.

## Refus sans effet financier : ajustement explicite D8

D8 pouvait convertir une erreur de schéma/catalogue/metadata en snapshot past_due synthétique via failClosed. LAUNCH-04 exige le refus des états ambigus/incompatibles sans effet financier : le réconciliateur marque désormais needs_review ou unknown et conserve le dernier état financier confirmé, sans publier un nouvel événement financier. Le worker s’arrête sur cette erreur et n’exécute pas l’outbox.

Une attente de test D8 a donc été volontairement remplacée : la divergence de quantité/catalogue exige une revue sans suspension financière fabriquée. Les tests vérifient que les événements/outbox/grants existants ne changent pas dans ce cas, y compris après un paiement antérieur. Une facture réellement impayée ou un remboursement réellement confirmé restent des faits autoritatifs et suivent les états financiers et procédures de suspension/reprise existants.

Conséquence opérationnelle : une incompatibilité seule ne révoque pas un droit antérieurement payé. Les limites et l’échéance existantes du Gateway restent applicables ; la revue humaine doit traiter l’alerte. Le renouvellement ou un nouveau grant ne peut avancer sans rapprochement valide. Ce changement de politique est signalé à Maya pour revue dans la PR, sans déploiement implicite.

## SQL et migration additive

2026_11_03_000001_add_stripe_fiscal_evidence.php ajoute sept colonnes nullable à stripe_invoices : subtotal_excluding_tax, tax_amount, total_amount, currency, invoice_number et deux URLs de justificatifs chiffrées. Les anciennes lignes restent null ; aucune donnée de recette n’est convertie ou remplie artificiellement. L’enrichissement intervient seulement lors d’un futur rapprochement autoritatif valide.

Le même fichier ajoute un trigger SQLite/MySQL interdisant le changement mode/account_id d’un binding existant. Une organisation conserve une seule identité financière Stripe ; une ancienne organisation TEST ne devient pas une organisation LIVE par changement de variables ou UPDATE. La migration est forward-only et son down refuse de retirer les preuves.

Contraintes globales D8 conservées : event_id unique, Customer/Checkout/Subscription uniques, invoice_id primaire, période unique par organisation et références financières UUID uniques. Une collision de même identifiant externe entre deux contextes est refusée, jamais fusionnée : ce choix conservateur limite la coexistence dans une même base si Stripe fournit effectivement des IDs identiques entre contextes. Il n’est pas présenté comme un routage multi-compte simultané. Le traitement de ces collisions nécessiterait une évolution dédiée ; aucune re-clé primaire massive n’est introduite ici.

La migration n’a été exécutée que dans les bases SQLite mémoire des tests. Le texte exact du trigger MySQL a été compilé et exercé dans un MySQL 8.4.7 jetable, sans réseau ni port ni volume persistant : UPDATE ordinaire accepté, changement de mode et de compte refusés, état initial conservé. Cela ne constitue pas une intégration Laravel/MySQL complète ni une migration du VPS. Le conteneur de test a été supprimé ; aucun service actif utilisé.

Toute application de cette migration sur un environnement réel reste à autoriser, après sauvegarde et contrôle de privilèges CREATE TRIGGER/ALTER TABLE, temps de verrouillage, compatibilité des images et procédure de retour applicatif conservant les données.

## Fiscalité et interface

Le prix reste mensuel EUR côté serveur et tax_behavior=exclusive. Checkout collecte une adresse, prépare customer_update.address=auto et une option indépendante de collecte d’identifiant fiscal ; automatic_tax et collect_tax_ids sont faux par défaut dans LIVE, et leur changement invalide l’approbation de configuration. Aucun taux fixe ni activation automatique de Stripe Tax.

Reconciler conserve sous-total HT, total et différence taxe en unités monétaires entières, devise et numéro de facture. Aucun taux n’est supposé ; la fixture vérifie une taxe synthétique de 735 centimes sur 4 900 centimes HT. Les remises/avoirs et le shipping restent hors contrat V1 ; incohérences de total refusées. Cette différence est une observation arithmétique sous les restrictions V1, pas une certification de la fiscalité appliquée par le vendeur. Les champs fiscaux, numéros et URLs participent à la relecture de stabilité ; URLs Stripe autorisées validées avant stockage chiffré.

Les références et liens de justificatifs sont conservés, sans nouveau générateur de facture ni nouvel écran d’historique PDF. La page existante de facture impayée reste disponible selon son contrat. La conformité du justificatif et la remise au client restent à qualifier avec l’identité juridique et le cas fiscal retenus.

StripeBilling affiche le bac à sable en TEST ; en LIVE il affiche le vendeur configuré seulement dans un profil commercial autorisé, sinon l’indisponibilité. Aucun nom AXENOR codé en dur comme vendeur. Le contrôle serveur, et non ce libellé, bloque Checkout. Voir LAUNCH04_LIVE_CONFIGURATION.md pour toutes les décisions encore manquantes.

## Tests réellement exécutés

- PHP 8.4.24 / PHPUnit 11.5.57 : 209 tests, 2 111 assertions réussies, SQLite mémoire et Http::fake/preventStrayRequests dans un conteneur --network none.
- 30 scénarios LIVE synthétiques supplémentaires et une assertion de compatibilité de clés TEST, en plus de la suite D8. Les helpers ont été extraits dans une fixture abstraite commune ; aucun test D8 n’est compté deux fois par héritage.
- Rejets clé/mode, compte, routes/événements croisés, session et metadata, catalogue/product, approbation absente/expirée/incohérente, mélange de reçus, files d’autre contexte, impossibilité d’adopter un binding TEST ; simulations doublons, réponse perdue, renouvellement, impayé/régularisation, reprise propriétaire et absence de double grant.
- Preuve SQL MySQL ciblée : cinq contrôles réussis, pas une intégration applicative complète.
- Syntaxe PHP complète réussie ; Pint --test sur 117 fichiers réussi ; build Vite portail réussi, 799 modules ; diff --check et scan des seuls fichiers publiés.

La première invocation de PHPUnit avant le build a produit huit erreurs de rendu dues au manifest Vite absent ; aucune n’était un paiement ou une erreur financière. Après build et changements ciblés, la suite finale ci-dessus réussit. Pint --dirty n’était pas utilisable dans l’image PHP sans Git ; les chemins concernés ont été formatés explicitement puis le contrôle global --test a réussi. Ces résultats ne sont pas masqués par les chiffres finaux.

D7/D8 restent des preuves historiques de paiement TEST et service réel. LAUNCH-04 n’ajoute aucune preuve de transaction Stripe réelle, d’activation commerciale ou de service livré à un nouveau client. Tests navigateur, carte, compte live, Stripe Tax réel, SCA réelle, reprise WebUI réelle et performance/charge non exécutés. Les dépendances déjà disponibles ont été copiées dans le clone isolé sans installation/mise à jour sur l’hôte ; une installation indépendante du lockfile relève aussi de la CI.

## Contrats inter-dépôts et limites

Gateway et Infra ne nécessitent pas de changement de code identifié : les contrats existants transportent autorisation/période/référence/quantité d’usage, pas une nouvelle comptabilité Stripe. L’exploitation future devra valider les identités financières, le matching de la quantité mensuelle Portal/Gateway, les flags et le profil de déploiement dans une mission distincte. Aucune configuration de ces dépôts n’a été modifiée.

L’approbation expirée bloque aussi l’ingestion LIVE : les livraisons extérieures devront être reprises après autorisation renouvelée. Une future ouverture doit surveiller l’expiration et vérifier la reprise des reçus, sans compter une réception rejetée comme persistée. Les opérations déjà envoyées avec résultat ambigu gardent leur référence et exigent réconciliation ; une pause ne les annule pas.

Les blocages commerciaux LAUNCH-03 autres que le code restent ouverts : vendeur et compte live, cadre fiscal, offre/quota/marge, support et alertes, récupérabilité et décision de release. La présente PR n’est ni une autorisation ni une procédure d’activation LIVE automatique.

## Livraison

Code committé/poussé sur feature/launch04-stripe-live avec PR en brouillon vers la référence D8 ; aucun merge ni déploiement. Documentation expurgée publiée sur une branche issue de reports/launch03-commercial dans trinity-docs avec PR en brouillon. Les liens et SHA exacts de livraison figurent dans le livrable et la copie centrale du rapport ; le fichier contenu dans son propre commit ne prétend pas connaître son SHA.

Décision attendue : revue du code et de l’ajustement de refus, puis décision séparée d’activation et de futurs essais de bout en bout. Aucune mission suivante démarrée.

## Références de livraison GitHub

Dépôt technique : Pascal440/trinity-saas-portal ; branche feature/launch04-stripe-live ; commit 76a11ded222395633efe5fcc7c14a11c293c1e68 ; [PR #13 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/13), base fix/launch023d8-owner-activation. Aucun déploiement ni activation LIVE.

Dépôt documentaire : Pascal440/trinity-docs ; branche reports/launch04-stripe-live issue de reports/launch03-commercial au commit e0878a2b1bd24a3f943291a37d3c6a205f838281. Le SHA documentaire final est fourni par la PR et le livrable de mission.

## Vérification CI GitHub finale

[Portal CI 41631339121](https://github.com/Pascal440/trinity-saas-portal/actions/runs/41631339121), sur le commit 76a11ded222395633efe5fcc7c14a11c293c1e68 : completed / success. Les étapes d’installation Composer et npm, validation Composer, syntaxe, Pint, tests PHP, build, audits Composer/npm et scan de release sont toutes success d’après les métadonnées de job consultées. Les 209 tests / 2 111 assertions ci-dessus sont les compteurs locaux mesurés ; aucun compteur supplémentaire n’est inventé depuis ce statut CI.
