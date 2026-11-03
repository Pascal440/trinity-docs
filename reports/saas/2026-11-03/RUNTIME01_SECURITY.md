# RUNTIME-01 — Cloisonnement, ressources et exploitation

3 novembre 2026, contrôles en UTC. Dépôt documentaire `Pascal440/trinity-docs`, branche `reports/runtime01-lab`, base `reports/launch06-release-candidate` / `5f1f6072bcbd5ca587b18fac84250e497fed8b12`. Aucun dépôt technique publié/modifié. Code Gateway consulté : `f79ff7f4ca938e0610a6e753b4b107dd4edc7437` ; référence Infra inchangée `5bd6fee98a468191613766e0093bdcda8de59099` et Portal LAUNCH-06 `6df4b5a338ac84bd928610292981962eeedd9ee6`. Scripts de laboratoire locaux séparés ; SHA documentaire final fourni dans la PR/livraison.

## Frontière réellement mise en place

Deux conteneurs dédiés, sans source de développement ni volume client/hôte monté. Terminal en `--network none`, WebUI dans ce même namespace isolé ; interfaces réseau du terminal : loopback uniquement. Les données WebUI et le home Terminal sont sur des tmpfs distincts. Aucun accès aux bases, secrets ou volumes D8 depuis le terminal. Seule l’audit opérateur a effectué les SELECT de métadonnées Gateway explicitement autorisés par Maya ; pas de lecture de clé API, de hash ou de données personnelles client.

Chaque processus applicatif tourne UID/GID **1000:1000**, rootfs en lecture seule, `cap-drop ALL`, `no-new-privileges`, aucun mode privilégié, device hôte, socket Docker ou réseau hôte. `sudo -n id` échoue. L’image contient des clients Docker/SSH, mais aucun socket, clé hôte ou chemin réseau vers le VPS ne leur est donné. Le serveur est lancé par Python normal, pas la copie de Python porteuse de cap_setgid prévue pour le mode multi-utilisateur. Aucune commande d’installation, de filtrage iptables ou d’ajout de privilège à l’entrypoint amont n’est exécutée.

Tests de connexion depuis le terminal : Internet, métadonnées et pont hôte injoignables ; escalade sudo refusée, socket absent. Le root visuel du navigateur de fichiers **n’est pas une prison de fichiers** : les commandes peuvent lire le filesystem public de leur propre image, jamais le filesystem privé du VPS qui n’est pas monté. [Contrôles](runtime01-evidence/runtime-checks.json), [état final effectif](runtime01-evidence/final-security-state.json).

Le namespace est partagé entre les deux composants de laboratoire : le terminal peut joindre l’HTTP interne WebUI, protégé par authentification, pas les services hôtes/D8. L’absence d’autorisation est rejetée sur l’API de fichiers et le compte de démo ne peut pas administrer les connexions. Le terminal partagé en mode simple utilisateur n’isole pas les fichiers du compte opérateur de ceux du compte de démo ; ces deux comptes sont dans **un seul périmètre de confiance fictif**. Aucun second client. Le mode multi-utilisateur Open Terminal est désactivé ; aucune promesse d’isolation commerciale multi-tenant.

## Accès privé et secrets

Aucun port Docker publié. Un relais opérateur borné n’écoute que `127.0.0.1:18760` et relaie des octets vers l’HTTP WebUI du conteneur connu. Sa commande Docker est constante ; aucune commande hôte fournie par le terminal/LLM. L’administration Docker nécessaire à la création/arrêt du labo reste côté opérateur, aucun droit transmis à l’application.

Accès depuis le poste de l’opérateur, avec sa connexion SSH déjà autorisée :

```sh
ssh -N -L 18760:127.0.0.1:18760 <alias-SSH-du-VPS>
# Navigateur du poste : http://127.0.0.1:18760
```

Le compte client est non administrateur, connexion système partagée explicitement à ce seul compte ; inscriptions publiques et APIs modèles désactivées. Mot de passe opérateur, mot de passe démo, clé Terminal et clé applicative sont nouveaux et privés au labo, jamais publiés. Fichiers de secrets locaux sous répertoire 0700 ; aucun .env préexistant lu/exporté. Le relais CDP provisoire de test est retiré : seule l’écoute UI ci-dessus demeure. Aucun tunnel public, changement SSH, domaine, certificat ou proxy D8.

Chrome utilise l’option sans sandbox interne de l’image officielle, nécessaire ici sous les restrictions Docker retenues. La frontière demeure le conteneur non privilégié ; cela **ne protège pas les fichiers/processus du même terminal d’une page malveillante**. Tests limités à la page fictive locale, pas de navigation Internet. Le bureau est un Xvnc virtuel propre au laboratoire, aucune capture du bureau, presse-papiers ou session SSH de l’hôte.

## Bornes observées et durée

| Ressource | WebUI | Terminal |
| --- | --- | --- |
| Mémoire | 1 GiB | 2 GiB |
| CPU | 1 | 1 |
| Processus/threads | 384 | 512, après échec observé à 384 |
| Fichiers persistants de session | Data tmpfs 512 MiB | Home tmpfs 512 MiB |
| Temporaire | tmpfs 128 MiB | tmpfs 256 MiB ; shm 256 MiB |
| Taille individuelle | RLIMIT_FSIZE 64 MiB | RLIMIT_FSIZE 64 MiB |
| Ports publics / egress | Aucun | Aucun |

Plafond de 4 terminaux interactifs, logs de processus bornés à 2 Mo et rétention 2 h, logs Docker 2×5 Mo par conteneur. Les limites sont réellement présentes dans Docker. La limite documentaire WebUI est 25 Mo ; elle ne remplace pas les bornes OS des fichiers Terminal. Un remplissage de workspace échouerait dans son tmpfs, pas dans un volume client.

**Arrêt automatique du seul labo à 17:59:13 UTC le 3 novembre 2026**, ou MemAvailable <1 GiB, contrôle toutes les 10 s. Garde actif vérifié ; l’échéance future n’est pas encore observée au moment du rapport. Aucun redémarrage automatique. `OPEN_TERMINAL_EXECUTE_TIMEOUT=5` borne l’attente de réponse, **pas la durée du processus** : la borne d’exécution effective générale est la session de deux heures. Les commandes et clients natifs peuvent rester en arrière-plan jusque-là. Un timeout strict par commande, une borne de tours d’outils plus petite que la valeur amont et la tenue prolongée/récolte des processus sont à qualifier avant une recette LLM ou un usage continu ; ne pas confondre ce prototype borné avec un service d’exécution commercial durci.

Le navigateur auxiliaire de contrôle consommait aussi des processus dans le terminal ; après sa fermeture, environ 345 processus/1,01 GiB sont observés pour le terminal et 325 MiB pour WebUI. Aucun OOM, environ 180 GiB de disque libre et plusieurs GiB de mémoire disponibles pendant les contrôles. Ce sont des observations ponctuelles, pas un dimensionnement de production. Le garde stoppe le labo si la réserve manque ; pas de nettoyage LAUNCH-06 pour libérer des ressources.

## Persistance, nettoyage et reprise

Les chats/configurations et fichiers survivent dans cette session, **pas à son arrêt/recréation**. Les trois entrées fictives originales, scripts et preuves sont conservés localement hors conteneurs ; les rapports expurgés et preuves retenues sont publiés dans trinity-docs. Aucun dump de base ni secret publié. Pour de futurs résultats LLM, exporter les fichiers/traces avant arrêt ; ne pas prétendre qu’ils sont sauvegardés par la sauvegarde D8.

La reprise utilise uniquement les références et objets runtime01 dédiés : recréer explicitement ce laboratoire, compte neuf et grants, réinjecter les entrées fictives et vérifier ressources/limites. Ne pas réutiliser les répertoires historiques ni les volumes D8. Arrêt/effacement éventuel limité aux IDs enregistrés du labo ; aucune commande prune globale. Les conteneurs arrêtés ne sont pas automatiquement supprimés et les archives existantes restent intactes.

Les 13 conteneurs préexistants sont comparés en lecture seule avant/après : images, dates de démarrage et compteurs identiques, 12 healthchecks sains, registre sans healthcheck. Cette observation ne prétend pas comparer byte à byte leurs bases, et ne nécessite aucun accès aux données clientes.
