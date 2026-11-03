# LAUNCH-04 — Configuration LIVE préparée, non activée

Date : 3 novembre 2026. NO-GO activation LIVE maintenu. Ce document ne contient ni secret ni configuration réelle et ne doit pas être appliqué automatiquement.

## Profils et compatibilité

STRIPE_BILLING_MODE accepte exactement test ou live, test par défaut pour compatibilité D8. Un profil par processus, jamais sélectionné par une requête cliente. Les variables historiques STRIPE_TEST_* continuent d’alimenter TEST ; LIVE ne récupère pas les valeurs TEST par défaut.

| Décision / variable LIVE | Défaut | Validation future requise |
| --- | --- | --- |
| STRIPE_LIVE_ENABLED | false | Activation d’intégration distincte et explicite par décision autorisée |
| STRIPE_LIVE_PROCESSING_ENABLED | false | Autorisation supplémentaire des créations/traitements ; false garde la réception si l’approbation reste valide |
| STRIPE_LIVE_ACCOUNT_ID | absent | Compte vendeur approuvé, vérifié avec la clé utilisée |
| STRIPE_LIVE_SECRET_KEY_FILE | absent | Fichier privé, non public, non symlink, permissions sans droits groupe/autres ; clé du mode sélectionné |
| STRIPE_LIVE_WEBHOOK_SECRET_FILE | absent | Secret de la destination LIVE, jamais celui de TEST |
| STRIPE_LIVE_PREVIOUS_WEBHOOK_SECRET_FILE | absent | Ancien secret LIVE uniquement pendant rotation contrôlée |
| STRIPE_LIVE_PRICE_ID | absent | Price LIVE, Product AI_WORKSPACE_PRO, EUR, mois, quantité 1, exclusive |
| STRIPE_LIVE_UNIT_AMOUNT | 4900 | Décision de prix HT ; catalogue doit correspondre strictement |
| STRIPE_LIVE_AUTOMATIC_TAX | false | Régime, immatriculations et configuration Stripe Tax approuvés avant usage |
| STRIPE_LIVE_COLLECT_TAX_IDS | false | Segment et identifiants fiscaux à collecter, sans supposer une obligation uniforme |
| STRIPE_LIVE_APPROVAL_FILE | absent | Artefact privé d’approbation, à créer seulement dans une future mission autorisée |

COMMERCIAL_SELLER_NAME et COMMERCIAL_SELLER_ID proviennent du vendeur légal validé ; aucun nom de prototype. COMMERCIAL_TAX_POLICY_REFERENCE, COMMERCIAL_PLAN_REFERENCE et COMMERCIAL_APPROVAL_REFERENCE identifient les décisions de fiscalité, offre/quota et direction. Toutes sont requises en LIVE. BILLING_MONTHLY_CREDIT doit être une chaîne décimale positive en EUR d’usage ; le prix de 49 EUR n’en détermine pas la valeur. APP_URL fait partie de la configuration approuvée et doit être HTTPS pour Checkout hors test/local.

BILLING_ENABLED et les autorisations/quantités du Gateway restent des prérequis séparés. Les flags Gateway/Infra ne sont pas modifiés ici. Le profil TEST conserve également sa dotation et ses contrôles ; ne pas confondre mode applicatif Laravel production et Stripe live.

## Artefact d’approbation, jamais livré avec des valeurs actives

Schéma attendu, illustratif seulement : mode live, reference correspondant à COMMERCIAL_APPROVAL_REFERENCE, expires_at entier Unix futur, configuration_sha256 égal à Profile::fingerprint(). Aucun exemple de clé ou de compte réel et aucun fichier d’autorisation utilisable fourni.

Le hash lie compte, Price, montant, version API, offre, automatic_tax, collect_tax_ids, identité commerciale complète, dotation mensuelle et APP_URL. Un changement de ces paramètres invalide l’approbation. Le chemin des credentials n’est pas lié pour permettre une rotation contrôlée ; chaque clé reste typée test/live et le compte vérifié avant l’opération.

Il s’agit d’un fichier privé d’autorisation d’exploitation, pas d’une attestation signée par la direction. Aucun endpoint ni commande de cette livraison ne le crée automatiquement. Aucun booléen déclarant à lui seul la validation commerciale ne suffit. Une future mission devra figer la configuration, faire revoir l’empreinte hors réseau, créer/installer l’artefact sous contrôle opérateur et qualifier son expiration. Aucun secret ne doit être inclus dans cet artefact ni copié dans GitHub.

À partir des défauts livrés, modifier seulement STRIPE_BILLING_MODE, seulement enabled, seulement processing_enabled ou seulement un fichier de clé ne peut autoriser des opérations LIVE. Après une future autorisation complète, il faudra gérer explicitement son retrait/expiration : la présence antérieure d’un profil approuvé ne doit pas être assimilée à une nouvelle décision de lancement.

## Endpoint et version

TEST : /stripe/test/webhook. LIVE : /stripe/live/webhook. Le processus refuse la route du profil opposé, même avec une signature valide. Version HTTP et snapshot : 2026-10-28.endive. Seuls les événements plateforme du compte attendu sont admis ; Connect/thin/Managed Payments restent exclus V1. La signature valide permet la réception ; seul le rapprochement autoritatif crée l’état financier.

Pas de diagnostic LIVE authentifié lancé. La commande historique stripe:test-configuration refuse LIVE. Les objets test ne sont ni renommés ni adoptés. Une collision globale d’ID est rejetée ; une organisation existante conserve son binding mode/compte. Plusieurs processus de profils différents devraient disposer de configurations/caches/verrous adaptés et faire l’objet d’une qualification de déploiement séparée ; cela n’est pas installé ici.

## Décisions liées à l’identité juridique / fiscalité

Avant tout paiement : vendeur légal et immatriculation, compte Stripe et versements, segment/pays autorisés, régime TVA/exonérations et références fiscales, politique de facture/numérotation/avoirs, conditions d’abonnement/résiliation/remboursement, conservation des justificatifs et données personnelles, offre et quota, support et délai de service. L’identité fiscale du client et son adresse doivent être correctes ; la collecte de tax_id dépend du cas retenu.

Le payload prépare customer_update.address=auto, une adresse de facturation obligatoire et l’option tax_id_collection. Aucun taux fixe et aucune activation de Stripe Tax par défaut. Les preuves HT/taxe/TTC sont des observations Stripe sous les restrictions V1 : une ligne, pas de prorata/remise/avoir/shipping. L’application ne certifie pas le traitement fiscal à la place du vendeur.

Les liens Stripe de facture/PDF sont validés puis stockés chiffrés ; la remise et la conformité réelle restent à qualifier. Aucun nouveau système de facturation, taux national codé en dur ou vendeur AXENOR n’est ajouté.

## Migration et exploitation futures

Une migration additive est fournie pour preuves fiscales et trigger de contexte immuable, testée seulement en SQLite mémoire et, pour son trigger, en MySQL jetable. Pas de migration de base active. Prévoir dans une mission future sauvegarde/restauration, droits SQL, verrous ALTER et retour d’image sans down destructif.

Prévoir alertes d’expiration d’approbation et de jobs non traités. Une approbation expirée bloque aussi la réception : conserver les traces Stripe et reprendre sous la même identité/référence après décision, sans nouveau crédit manuel. Refuser une donnée incompatible marque revue/inconnu et n’altère pas les derniers droits financiers confirmés ; la période/les limites Gateway existantes restent applicables jusqu’à leur échéance et la revue opérateur reste nécessaire.

Aucune instruction de ce document n’autorise un déploiement, une clé réelle, un paiement ou un remboursement réel. Décision séparée obligatoire après revue de la PR.

## Références de livraison GitHub

Dépôt technique : Pascal440/trinity-saas-portal ; branche feature/launch04-stripe-live ; commit 76a11ded222395633efe5fcc7c14a11c293c1e68 ; [PR #13 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/13), base fix/launch023d8-owner-activation. Aucun déploiement ni activation LIVE.

Dépôt documentaire : Pascal440/trinity-docs ; branche reports/launch04-stripe-live issue de reports/launch03-commercial au commit e0878a2b1bd24a3f943291a37d3c6a205f838281. Le SHA documentaire final est fourni par la PR et le livrable de mission.
