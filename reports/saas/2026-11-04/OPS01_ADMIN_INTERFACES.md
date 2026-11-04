# OPS-01 — Interfaces commerciales actives sur IONOS

Vérification en lecture seule à partir du routage Traefik actif, des images et sources embarquées, et de GET anonymes sans suivre les redirections. Les essais ne se sont pas authentifiés et n’ont pas ouvert de contenu client ni exécuté d’action métier.

| Interface | Adresse effective | Identité de l’image active | Observation HTTP |
| --- | --- | --- | --- |
| Portal SaaS | `https://portal.linesoft.fr` | `sha256:50173a5cf60b06f87ac392b8187b1bd4d47387feb89c05301a488e99754aa4f5`, PHP 8.4.24, Laravel 12.70.2. Pas de label révision applicative constaté. | Accueil 200 via Traefik |
| Administration Portal | `/admin` sur loopback Apache **dans le conteneur Portal** | Même image | 404 via l’URL publique. 302 vers la connexion depuis le loopback applicatif |
| Facturation client Portal | `https://portal.linesoft.fr/billing/stripe` | Même image | 302 anonyme vers `/login` |
| Administration Gateway | `http://gateway.localhost/gateway-admin` est la base configurée interne. Service port 80 sur le réseau Docker privé, sans port hôte publié. | `sha256:71d466513a1b85539313d47f6928da0159dbb52a964a1895f68becacf7453852`, révision `f79ff7f4ca938e0610a6e753b4b107dd4edc7437`, PHP 8.4.24, Laravel 13.30.0. | Racine admin 302, login 200. Login également joignable depuis le VPS vers l’adresse Docker privée |

La route Traefik Portal exclut le préfixe `/admin`. Apache applique `Require local` à ce chemin. Une redirection SSH directe vers l’IP Docker Portal n’est donc pas un accès navigateur valide à l’admin. Le point d’entrée confirmé est un accès opérateur au conteneur et à son loopback. L’ouverture privée dans un navigateur demanderait un relais éphémère vers **ce loopback**, avec test du login, des cookies et de l’origine avant usage. Aucun relais Portal créé. L’application exige également un compte vérifié et `is_admin`.

Gateway n’a pas de route Traefik centrale publique dans la configuration observée. `/gateway-admin` à travers le domaine Portal renvoie 404. Un tunnel SSH Gateway est possible vers l’adresse Docker privée courante, à relever côté opérateur dans `docker inspect`. Depuis son poste, remplacer le paramètre par cette adresse et utiliser le compte Gateway autorisé existant.

```sh
ssh -N -L 18772:<adresse-docker-privee-gateway>:80 <alias-vps>
```

URL navigateur prévue `http://127.0.0.1:18772/gateway-admin/login`. L’HTTP 200 du login a été vérifié depuis le VPS vers le service privé. Le tunnel depuis le poste et la session authentifiée n’ont pas été testés. Le code protège les écrans via `auth` et `trinity.gateway.web-admin`.

## Écrans confirmés dans les conteneurs

| Domaine | Code embarqué | Observation et limite |
| --- | --- | --- |
| Organisations et instances Portal | `Admin.vue`, `Organization.vue`, dashboard et instance. Administration des organisations, membres, onboarding, demandes, événements et références d’instance. | Route locale atteinte et protégée. Aucun affichage authentifié de données clients. |
| Abonnement Stripe Portal | `StripeBilling.vue` et `StripeBillingController`. État abonnement/financier, checkout, fin de période, réconciliation et facture. | Propriétaire vérifié exigé. Actions sensibles protégées par confirmation du mot de passe. 302 anonyme observé, ni checkout ni activation testés. |
| Clients Gateway | `/gateway-admin/clients` et détail client. Vues de liste et fiche, utilisateurs, clés, état, association conteneur et indicateurs d’usage. | 302 anonyme et contrôleur/vues présents. |
| Plans et quotas Gateway | `/gateway-admin/plans` et `/gateway-admin/plans/{plan}/limits`. Édition des limites du plan dans le code actif. | 302 pour l’index. Écran d’édition identifié par la route, aucune modification. |
| Crédits Gateway | `/gateway-admin/wallets` et détail. Solde, disponible, réserves, journal, consommation et remboursements. | 302 anonyme, vues actives présentes. |
| Consommation Gateway | `/gateway-admin/usage` et détail client. Requêtes, tokens, estimation coût fournisseur et prix client. | 302 anonyme et vues actives présentes. Valeurs réelles non consultées. |

Aucun écran global réunissant abonnements Stripe et Gateway/instances n’a été identifié dans ces routes ou vues déployées. L’existence d’une vue dans une branche de développement, d’une route client ou d’une table de facturation ne confirme pas une console globale déployée. Les références LAUNCH-06 et les branches FRONT restent des références historiques distinctes des images actives ci-dessus.
