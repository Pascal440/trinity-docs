# OPS-01 — Décisions proposées

- **DEMO-01B en attente de la clé dédiée.** Kit RUNTIME-01 recréé depuis DEMO-01A, frontière réseau de la variante split et refus du relais contrôlés localement. Avant un seul scénario, confirmer catalogue authentifié, tarifs et facteur tout compris. Aucun accès fournisseur actif, coût d’inférence de 0 €.
- **Dockhand suspendu sur le démon D8.** Image officielle épinglée et procédure privée préparée. La sécurité des services existants exige une frontière d’autorisation au niveau du moteur. Préférer un démon dédié pour la gestion, ou un inventaire explicitement filtré si la lecture suffit.
- **Accès commerciaux.** Conserver la route client Portal publique déjà existante et les administrations dans le périmètre opérateur privé. Les sondes anonymes et sources embarquées établissent les routes et protections. L’ouverture des données d’un client n’était pas autorisée.

## Console commerciale à arbitrer

Proposer une première vue opérateur en lecture seule dans le périmètre administratif privé du Portal. Une ligne par organisation avec état d’abonnement et Stripe issu du Portal, plan et limites issus du Gateway, solde/disponible/réservé et consommations du ledger Gateway, état et référence de l’instance issus du provisionneur. Afficher l’origine, la fraîcheur et les écarts de rapprochement. Éviter les copies de secrets et de reçus complets.

Faire le rapprochement via l’UUID d’organisation, le lien Gateway vérifié et la référence de provisionnement existante. Les correspondances manquantes restent visibles comme telles. Utiliser des lectures explicites, paginées et auditées, avec rôle opérateur, séparation des tenants et accès par SSH privé ou chemin d’administration autorisé. Le détail renvoie aux consoles propriétaires des opérations. Évaluer l’ajout de commandes d’écriture seulement dans une mission autorisée et avec la comptabilisation existante.

Les 13 conteneurs existants ont conservé leurs identités, images, dates de démarrage et compteurs depuis la dernière observation DEMO-01A. Les conteneurs temporaires ont tous été retirés.

Aucune console nouvelle développée ou déployée dans OPS-01. La documentation seule est publiée dans `Pascal440/trinity-docs`, branche `reports/demo01b-ops01` depuis `reports/demo01a-preparation`. Pas de lancement automatique de la suite.
