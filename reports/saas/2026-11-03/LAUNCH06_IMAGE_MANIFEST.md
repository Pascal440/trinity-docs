# LAUNCH-06 — Manifeste des images

Date : 3 novembre 2026. Portal `feature/launch06-release-candidate`, base LAUNCH-05 `679d3738cfb5a724bd0125cca52786cfc2d25545`. Packaging exact des images : `91d47437df0a86063b9c68354c805c987dd83382`. Qualification, preuves et documentation Portal : `6df4b5a338ac84bd928610292981962eeedd9ee6`, [PR #15 en brouillon](https://github.com/Pascal440/trinity-saas-portal/pull/15) ; base LAUNCH-05 non fusionnée. Gateway D7 `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` et Infra D8 `5bd6fee98a468191613766e0093bdcda8de59099` consultés sans modification. Docs : branche `reports/launch06-release-candidate`, base `reports/launch05-commercial-qualification` / `0a1d0706105ed6e27b68b7071197fe4b09dd94db`.

### candidate

- Source applicative : `679d3738cfb5a724bd0125cca52786cfc2d25545`.
- Référence locale : `launch06/candidate:679d3738cfb5-91d47437df0a`.
- Manifest OCI / ID Docker sur cet hôte : `sha256:8413d2f78bb2425c6116296173ddbe98e34216b5a3b31dae9fe3b49a83b12503`.
- Config OCI : `sha256:5c3ce728c1a1fc55f50e487646ccf9807f428a892609c9f5699b7224b7cceb31`.
- Archive OCI SHA256 : `d5a822f7569d089b510fa467795a96f157d4791d4e3afea8d2612e8a7673feb9`.
- Archive Docker SHA256 : `44a0e579afed371918076a7782a3203c421a5137ec3039a397c772793983a2ee`.
- PHP 8.4.24, Laravel 12.70.2, Composer 2.9.7 ; dépendances production et absence de dépendances dev vérifiées.
### fallback

- Source applicative : `76a11ded222395633efe5fcc7c14a11c293c1e68`.
- Référence locale : `launch06/fallback:76a11ded2223-91d47437df0a`.
- Manifest OCI / ID Docker sur cet hôte : `sha256:1a3b2fadb66e6143612f64e4674b9534a522f08910f5e03db033b9be47d30043`.
- Config OCI : `sha256:735225d2dad93a116f82480058242cb1061e7183cd3f9a183d0f33427c292373`.
- Archive OCI SHA256 : `47ec6018c58a2efecfb3d4357e0438f044e54c06024f28f414dad55991aa0087`.
- Archive Docker SHA256 : `1a939a69dc03d06b50207e8afd1c2c921fdee8c2babe717e23d437764c2c2870`.
- PHP 8.4.24, Laravel 12.70.2, Composer 2.9.7 ; dépendances production et absence de dépendances dev vérifiées.

## Entrées immuables et reproductibilité

Runtime PHP/Apache/vendor production : `sha256:50173a5cf60b06f87ac392b8187b1bd4d47387feb89c05301a488e99754aa4f5`. Image Node de build : `sha256:a9f5f7c91a432850b2a8a7797adf5eadb6c733ceed61167806cee7ea7fbc29df`. Gateway exécuté : `sha256:71d466513a1b85539313d47f6928da0159dbb52a964a1895f68becacf7453852`. MySQL exécuté : `sha256:0426ec38c7a10aa45ba383887df7878f74ee70e2fd589c7b69207f3577901903`. Le Dockerfile extrait les dépendances du runtime D8 revu, mais remplace le code applicatif et aplatit le rootfs final ; **l’ancien Portal D8 test-only n’est jamais proposé comme secours**.

Quatre builds non cachés, réseau de build désactivé, SOURCE_DATE_EPOCH fixé au commit de source, horodatage des couches réécrit, provenance/SBOM automatiques désactivés pour le contrôle d’identité. Les deux manifest/config de chaque rôle sont égaux ; couches décompressées et labels de l’image chargée concordent avec OCI. Le Docker de cet hôte expose le digest manifest dans `.Id` : il n’est pas confondu avec le digest config, également enregistré.

Le snapshot npm contrôlé est conservé localement, SHA256 `49ad048ad96e9aa95035d61b8e95329bfb921083de2aa2e41548912b2b261f0f`. Versions et intégrités **déclarées** concordent avec les locks ; les deux extras de prototype @axe-core/playwright et axe-core sont exclus uniquement des nouveaux contextes. Il n’y a pas de `npm ci` indépendant dans ce build hors réseau ni de vérification individuelle du contenu contre chaque tarball npm. Reproductibilité démontrée pour les mêmes entrées figées, pas une reconstruction autonome depuis Internet. Conserver les images d’entrée et le snapshot avant toute opération ; leur disponibilité sur une autre machine reste un prérequis.

Les locks SHA256, inventaires complets noms/versions des dépendances PHP et métadonnées runtime figurent dans les JSON expurgés Portal `docs/launch06/evidence/`. Les assets dérivent de package-lock et du snapshot ; node_modules n’est pas embarqué dans l’image livrée. PHP PDO MySQL est présent.

## Migrations communes et compatibilité

Les deux sources possèdent les mêmes neuf migrations :

- `0001_01_01_000000_create_users_table.php`
- `0001_01_01_000001_create_cache_table.php`
- `0001_01_01_000002_create_jobs_table.php`
- `2026_10_30_000001_create_portal_domain.php`
- `2026_10_30_000002_create_onboardings.php`
- `2026_10_30_000003_add_provisioner_v2.php`
- `2026_10_31_000001_create_billing.php`
- `2026_10_31_000002_create_stripe_adapter.php`
- `2026_11_03_000001_add_stripe_fiscal_evidence.php`

La qualification recrée les huit migrations antérieures, y ajoute l’état financier synthétique, puis exécute la neuvième. Retour à l’image LAUNCH-04 en conservant les neuf migrations, sans down ni suppression de colonne. Aucune donnée LIVE réelle n’est créée ; la compatibilité du schéma financier prévu est démontrée avec des données TEST synthétiques, pas un compte LIVE.

## Contrôles de livraison

Scan des deux rootfs exportés : aucun fichier .env, dépôt Git, dossier applicatif tests/docs/scripts/node_modules, dump SQL/SQLite ou cache Laravel PHP embarqué ; aucun motif de secret LIVE/GitHub ni bloc de clé privée détecté. Ceci reste un scan par chemins et motifs, pas une preuve mathématique d’absence de toute donnée sensible. Les secrets obligatoires sont injectés à l’exécution ; aucune clé de client ou de production dans les archives.

Bootstrap HTTP, accès SQL/cache/session, workers métier, scheduler, redémarrage et fallback validés par l’image. `stripe:health` appartient à LAUNCH-05 ; il n’existe pas dans la source LAUNCH-04. Le health SQL/cache/session fourni par le packaging fonctionne sur les deux. Le protocole d’exploitation devra en tenir compte lors d’un retour vers LAUNCH-04.

Stockage exclusivement local LAUNCH06, pas de registre actif ni publication d’archives dans Git. Seuls manifestes, code et preuves expurgées sont publiés. Les chemins privés locaux et paramètres opérationnels sensibles ne sont pas nécessaires dans ce rapport.
