# OPS-01 — Dockhand

**Installation suspendue sur le démon Docker D8.** L’inventaire des conteneurs, y compris arrêtés, et des noms de services système n’a trouvé ni Dockhand, Portainer, Yacht, Dockge, Rancher ou Cockpit. Aucun listener détecté sur les ports usuels inspectés 3000, 9000, 9443, 2375, 2376 et 18770. Les quatre previews FRONT, D8 et le registre sont déjà présents.

Image officielle préparée pour linux/amd64, version `v1.0.55`. Index `sha256:039fbb65899f5ecc1d63083736d94587306b35736bca666eca623416859ddaa5`. Manifest exécutable `fnsys/dockhand@sha256:d15656246d6d8f2caf12743236c88ad1b728e2a2b918e1858ae116d05f8875a9`. Le registre a fourni les digests. Aucun conteneur ni volume Dockhand n’a été créé. [Release officielle](https://github.com/Finsys/dockhand/releases/tag/v1.0.55) · [Manuel officiel](https://dockhand.pro/manual/).

Sur IONOS, `/var/run/docker.sock` est en mode 0660, UID 0, GID 986. Un processus pouvant s’y connecter via le groupe ou root reçoit les droits de l’API Docker du démon partagé, qui incluent création de conteneurs avec montages hôte, arrêt, exec et retrait. Monter le socket avec `:ro` ne filtre pas les méthodes HTTP sur cette socket. L’isolation de D8 ne peut donc pas être garantie par le port loopback, un volume séparé ou l’authentification Dockhand seuls. L’amont démarre avec authentification désactivée. La version candidate est postérieure au correctif d’authentification WebSocket 1.0.34, ce qui ne change pas la portée du socket. [Manuel officiel](https://dockhand.pro/manual/) · [Avis de sécurité amont](https://github.com/Finsys/dockhand/security/advisories/GHSA-f6q3-chhc-4hxm).

## Préparation conditionnelle

VPS observé avec environ 5 Gio de RAM disponible, quatre CPU et 179 Gio libres. Refaire le contrôle de capacité et l’inspection de la version Docker avant toute installation. Utiliser un démon ou un hôte distinct de D8, ou une passerelle dont les opérations et objets autorisés sont appliqués côté serveur et vérifiés. Un proxy Docker limité à l’inventaire ne permettrait qu’une console de lecture et son fonctionnement avec Dockhand doit être qualifié.

Pour une cible effectivement séparée, prévoir le conteneur indépendant, le volume neuf `ops01-dockhand-data`, l’image par digest ci-dessus et la publication `127.0.0.1:18770:3000`. Désactiver les politiques et planifications de mise à jour. Aucun socket de D8, aucun montage de projet ou de volume D8. Réserver 512 Mio, 1 CPU et 256 processus pour un premier démarrage de contrôle, puis mesurer l’usage avant extension.

URL locale **prévue** `http://127.0.0.1:18770`, actuellement indisponible. Tunnel prévu après installation qualifiée.

```sh
ssh -N -L 18770:127.0.0.1:18770 <alias-vps>
```

Lors de l’amorçage, garder le moteur déconnecté et ouvrir le tunnel uniquement pour l’opérateur. Dans Settings → Authentication, activer l’authentification et créer l’administrateur avec un secret distinct dans le gestionnaire de l’opérateur. Tester fermeture de session, refus anonyme HTTP et WebSocket, et portée exacte de la cible isolée avant d’y connecter un moteur. Vérifier l’écoute loopback avec `ss`, sans règle publique. Les mises à jour éventuelles restent une opération manuelle et distincte.
