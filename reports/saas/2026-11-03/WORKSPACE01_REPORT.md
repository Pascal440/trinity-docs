> Copie documentaire expurgée pour GitHub. Les adresses publiques, domaines d’exploitation, identité client et chemins propres à l’hôte sont remplacés par des alias. Les SHA, dépendances, diagnostics et limites sont conservés. Le rapport décrit l’état observé lors de sa mission ; voir WORKSPACE02_REPORT.md pour la sauvegarde ultérieure. Les fichiers originaux locaux restent intacts.

# WORKSPACE-01 — Audit de continuité
Destinataire : Maya, direction stratégique et produit  
Observation : 3 novembre 2026, vers 11 h 42 (Europe/Paris).  
Statut : reconnaissance terminée ; arbitrage requis avant modification.

## 1. Diagnostic et périmètre
Cet environnement est déjà le VPS de préproduction correspondant à l'adresse <VPS_ADDRESS>, et non un poste de développement vierge : interface réseau, Docker, chemins <PREPRODUCTION_ROOT> et manifeste public concordent. L'appartenance contractuelle à IONOS n'a pas été vérifiée dans une console fournisseur.

La reprise est techniquement possible sans recréer les services. Elle doit cependant être préparée dans un espace de sources distinct des chemins utilisés par les conteneurs. Un développement directement dans les répertoires FRONT montés dans Docker changerait immédiatement les prévisualisations.

Toutes les vérifications sont en lecture seule. Seule écriture intentionnelle : ce rapport demandé, hors dépôts et hors infrastructure active. Aucun commit, push, merge, fetch Git local, installation, changement d'accès, exécution applicative, migration, redémarrage ou déploiement. Aucun contenu .env, token ou secret consulté. Le statut gh a affiché uniquement un jeton masqué. Les commandes ont nécessité une exécution hors bac à sable après l'erreur bwrap « Operation not permitted » ; sudo non interactif a servi exclusivement aux observations Docker/système.

Distinction de preuve : les services, ports, hashes et états PR ci-dessous ont été observés pendant cet audit. Les tests fonctionnels, paiements, restaurations et métriques antérieurs proviennent des descriptions PR et rapports existants ; ils n'ont pas été rejoués.

## 2. Connexions SSH et GitHub
- Linux : uid/gid utilisateur de développement, groupes sudo/users ; répertoire courant /.
- Git 2.53.0 ; gh 2.46.0 disponible ; authentification CLI HTTPS active Pascal440, appel GitHub de lecture réussi.
- Connecteur GitHub : identité Pascal440, liste des dépôts et PR accessible. Les permissions remontées sont administrateur/lecture/écriture : accès utilisé uniquement en lecture, ce n'est pas un credential techniquement limité à la lecture.
- SSH : client présent, ssh.service actif, écoute TCP 22 IPv4/IPv6. Plusieurs connexions entrantes établies observées, dont une session avec transfert local 50648. Une connexion TCP établie ne prouve pas à elle seule une authentification réussie.
- <USER_HOME>/.ssh contient authorized_keys ; aucun fichier de clé privée ni config dans ce répertoire. SSH_AUTH_SOCK défini ; identité de l'agent et capacité d'authentification sortante non qualifiées. Aucun nouvel essai SSH, aucune modification known_hosts.
- Aucun besoin de nouvelle connexion VPS pour cet inventaire, puisque l'exécution se déroule sur l'hôte de préproduction.

Dépôts retournés par la liste accessible (14, non assimilés à tous les dépôts possibles du compte) : Pascal440/la_gazette_monaco, TrinityIA, trinity-gateway, memory-trinity, trinity-orchestrator, trinity-core-sdk, trinity-docker, trinity-docs, trinity-client, callmetrinity-site, UniversalAIDataEngine, digital-tissue, trinity-saas-infra, trinity-saas-portal. Les trois dépôts principaux existent et sont privés.

## 3. Sources locales et branches
Recherche parcourue : /home, /opt, /srv, /mnt, /tmp et /var/www lorsqu'accessibles ; dépendances/cache exclus. Aucun inventaire exhaustif des répertoires privés hors droits courants n'est revendiqué.

### Clone projet détecté
<WORKSPACE_LAUNCH>/work/launch023d11
- Branche active : fix/launch023d11-preproduction.
- HEAD : 0232c06e8c13bfcd5a1a780a122eea6c3ca42b03, 1 novembre 2026, « Local work copy of upstream source 35b6a14 ».
- Ce HEAD est une copie locale historique et ne correspond pas à la tête GitHub actuelle 96e119091200799eab74e735e966d43b072169c2.
- 18 fichiers suivis modifiés : .dockerignore, .gitignore, README.md, compose.clients.yaml, compose.production.yaml, compose.provisioner.yaml, compose.yaml, gateway/Dockerfile, gateway/entrypoint.sh, provisioner/Dockerfile, provisioner/src/Engine.php, provisioner/tests/topology.py, provisioner/worker.php, scripts/prepare-provisioner.py, scripts/prepare.py, scripts/source.sh, scripts/verify.py, tests/test_topology.py.
- 17 entrées non suivies au niveau du statut : LAUNCH023D11_COMPOSE_REPORT.md, LAUNCH023D11_PRIVILEGED_AUDIT.md, compose.clients.production.yaml, compose.preproduction.yaml, deployment/, docs/launch023d11/, evidence/, gateway/financial-config.php, portal/, provisioner/tests/routes023d11.php, scripts/check-deployment-manifest.py, scripts/check-public-routes.py, scripts/portal-source.sh, scripts/preproduction.sh, scripts/routing.py, scripts/validate-preproduction.py, tests/test_preproduction.py.
- Ne pas réinitialiser ou réutiliser ce clone comme base propre.

Autre clone détecté : <USER_HOME>/.codex/.tmp/plugins, branche master, HEAD 0722921d5542fc593105c27bd52630babd8b8c2a ; aucun changement suivi observé. Dépôt technique de plugins, hors projet.

### Copies de travail sans .git
- <PREPRODUCTION_ROOT>/infra : infrastructure active, archives et surcharges successives, runtime et secrets ; ce n'est pas un clone.
- <PREPRODUCTION_ROOT>/sources : gateway, gateway-d7, portal, portal-d6, portal-d7, portal-d8, sdk.
- <WORKSPACE_LAUNCH>/work/front01/portal
- même racine /work/front02/portal et /work/front021/portal.
- <WORKSPACE_FRONT022>/work/front022/portal.
Les quatre copies FRONT sont les sources montées dans les prévisualisations. Sans .git, elles n'ont ni branche active ni statut Git fiable ; leur provenance doit être établie par référence et comparaison de fichiers.

### Main GitHub observés
| Dépôt | SHA main | Situation |
| --- | --- | --- |
| Gateway | d3fd05f8b135b909d0bf15025508f87f313579a2 | Merge phase 2, 28 octobre |
| Portal | 12d44144b90a2f4fd146afe143658e1e6b5f4b3e | Initialisation, 30 octobre |
| Infra | 1318befa2d0b0f3e7408b39800397dddefb8ceb0 | Initialisation, 29 octobre |

Main ne représente donc pas le dernier état fonctionnel.

## 4. Continuité GitHub : PR et dépendances
Les recherches ont retourné 9 PR Gateway, 11 Portal et 15 Infra ; les limites demandées (40 par dépôt) ne sont pas atteintes. Toutes les PR Portal et Infra retournées sont ouvertes. Gateway #1–#5 sont fusionnées, #6–#9 ouvertes. Total : 30 ouvertes, dont 16 brouillons.

Les bases des PR constituent les dépendances techniques observées, pas un ordre de fusion approuvé.


### trinity-gateway
| PR | Chantier | État | Base ← tête | Commit tête |
| --- | --- | --- | --- | --- |
| [#9](https://github.com/Pascal440/trinity-gateway/pull/9) | LAUNCH 02.3-D7 — Interdire les sessions web de l’acteur financier technique | ouverte, brouillon | feature/launch022-finance ← fix/launch023d7-noninteractive-financial-actor | f79ff7f4ca938e0610a6e753b4b107dd4edc7437 |
| [#8](https://github.com/Pascal440/trinity-gateway/pull/8) | LAUNCH 02.2 : qualification HTTP et SQL du Gateway financier | ouverte, hors brouillon | feature/launch021-finance ← feature/launch022-finance | cca6ed29510888a26c00c7c88e5a4c5a958291cf |
| [#7](https://github.com/Pascal440/trinity-gateway/pull/7) | LAUNCH 02.1 : crédits mensuels internes, autorisations et clôture idempotente | ouverte, hors brouillon | feature/saas-automated-release ← feature/launch021-finance | 9c870067334974610b3b96d95f777e0425a8c5b5 |
| [#6](https://github.com/Pascal440/trinity-gateway/pull/6) | SaaS Phase 3 : build privé reproductible et archive IONOS autonome | ouverte, hors brouillon | main ← feature/saas-automated-release | 3875577636df5c5291e0461f691dcab4b8bd2017 |
| [#5](https://github.com/Pascal440/trinity-gateway/pull/5) | SaaS Phase 2 : portefeuille prépayé et exploitation financière | fusionnée | main ← feature/saas-credit-wallet | ef4537dcac5108688e7034447d6db735edd93da2 |
| [#4](https://github.com/Pascal440/trinity-gateway/pull/4) | Préparer la confidentialité et la comptabilisation SaaS — phase 1 | fusionnée | main ← feature/saas-accounting-foundation | 0e07ac10d5dd57f204d3817a6b4f191ea44e2ba0 |
| [#3](https://github.com/Pascal440/trinity-gateway/pull/3) | Fix admin login redirect | fusionnée | main ← codex/fix-admin-login-redirect | f1e2f438ccb1007d2d40e5fe0e75ef3dc7722ab1 |
| [#2](https://github.com/Pascal440/trinity-gateway/pull/2) | Prepare IONOS gateway integration | fusionnée | main ← codex/ionos-sync-gips | 0be090af0d398777a935eba97538a66d3ea2140e |
| [#1](https://github.com/Pascal440/trinity-gateway/pull/1) | Add redesigned Gateway client portal | fusionnée | main ← gateway-gips | e01f29f1b8090a0e65353aafe9c54eacc14a7598 |

Branches retournées : `codex/fix-admin-login-redirect`, `codex/ionos-sync-gips`, `feature/launch021-finance`, `feature/launch022-finance`, `feature/provider-routing`, `feature/saas-accounting-foundation`, `feature/saas-automated-release`, `feature/saas-credit-wallet`, `fix/launch023d7-noninteractive-financial-actor`, `gateway-gips`, `main`.

### trinity-saas-portal
| PR | Chantier | État | Base ← tête | Commit tête |
| --- | --- | --- | --- | --- |
| [#11](https://github.com/Pascal440/trinity-saas-portal/pull/11) | FRONT-02.1 — Reflets organiques, comparaison A/B et fallback statique | ouverte, brouillon | feature/front02-immersive-axenor ← fix/front021-organic-motion | 433f69a040ca08a4f305212c83016fdb43ba64a9 |
| [#10](https://github.com/Pascal440/trinity-saas-portal/pull/10) | FRONT-02 — Accueil AXENOR immersif et prévisualisation isolée | ouverte, brouillon | feature/front01-premium-home ← feature/front02-immersive-axenor | 8c01fdd424eddb04b6d56fa00845cfb04ec66b3e |
| [#9](https://github.com/Pascal440/trinity-saas-portal/pull/9) | FRONT-01 — Accueil premium Trinity et prototype isolé | ouverte, brouillon | fix/launch023d8-owner-activation ← feature/front01-premium-home | 362eb7c76ef24a2b62632d0f6c4b802abc5a5e64 |
| [#8](https://github.com/Pascal440/trinity-saas-portal/pull/8) | LAUNCH 02.3-D8 — Débloquer l’activation du propriétaire administrateur | ouverte, brouillon | fix/launch023d7-recette-onboarding ← fix/launch023d8-owner-activation | b9c84b5de9671c1be73f8e8cb3198bea3cfec855 |
| [#7](https://github.com/Pascal440/trinity-saas-portal/pull/7) | LAUNCH 02.3-D7 — Inscription de recette et vérification email réelle | ouverte, brouillon | fix/launch023d6-stripe-endive ← fix/launch023d7-recette-onboarding | 12ef3933e13b3fef72d28b6436cf0398d117ee41 |
| [#6](https://github.com/Pascal440/trinity-saas-portal/pull/6) | LAUNCH 02.3-D6 — Migrer les contrats Stripe Basil vers Endive | ouverte, brouillon | feature/launch022-stripe ← fix/launch023d6-stripe-endive | 824ad1796fced672a2e49823dae35d963667ca25 |
| [#5](https://github.com/Pascal440/trinity-saas-portal/pull/5) | LAUNCH 02.2 : Checkout Stripe test et événements financiers vérifiés | ouverte, hors brouillon | feature/launch021-finance ← feature/launch022-stripe | ad88d19942504604f5544eef3b57eab113e53247 |
| [#4](https://github.com/Pascal440/trinity-saas-portal/pull/4) | LAUNCH 02.1 : abonnement indépendant du PSP et reprise commerciale confirmée | ouverte, hors brouillon | feature/saas-phase612 ← feature/launch021-finance | e8060f5414c6eb9f78ef1f52792274b96dcba6d2 |
| [#3](https://github.com/Pascal440/trinity-saas-portal/pull/3) | Phase 6.1.2 : onboarding propriétaire avec le provisionneur v2 signé | ouverte, hors brouillon | feature/saas-phase611 ← feature/saas-phase612 | 569a9eedf513c55773447f79adb0f11b49899a43 |
| [#2](https://github.com/Pascal440/trinity-saas-portal/pull/2) | Phase 6.1.1 : approbation commerciale, onboarding suivi et blocage WebUI documenté | ouverte, hors brouillon | feature/saas-phase61 ← feature/saas-phase611 | 18abeae7b12f2b38956b8dfb5ffcc1d1a6363259 |
| [#1](https://github.com/Pascal440/trinity-saas-portal/pull/1) | Phase 6.1 : portail SaaS client et console administration | ouverte, hors brouillon | main ← feature/saas-phase61 | 5464ed03fc73719fe64cba0fcce7525e5fa6ed20 |

Branches retournées : `assets/front022-axenor-sculpture`, `docs/launch023b-stripe-cli`, `docs/launch023c-quick-tunnel`, `feature/front01-premium-home`, `feature/front02-immersive-axenor`, `feature/front022-static-glass-saucer`, `feature/launch021-finance`, `feature/launch022-stripe`, `feature/saas-phase61`, `feature/saas-phase611`, `feature/saas-phase612`, `fix/front021-organic-motion`, `fix/launch023d6-stripe-endive`, `fix/launch023d7-recette-onboarding`, `fix/launch023d8-owner-activation`, `main`.

### trinity-saas-infra
| PR | Chantier | État | Base ← tête | Commit tête |
| --- | --- | --- | --- | --- |
| [#15](https://github.com/Pascal440/trinity-saas-infra/pull/15) | LAUNCH 02.3-D8 — Premier espace IA <TENANT_NAME> et consommation réelle qualifiés | ouverte, brouillon | ops/launch023d7-sandbox-checkout ← ops/launch023d8-first-ai-client | 5bd6fee98a468191613766e0093bdcda8de59099 |
| [#14](https://github.com/Pascal440/trinity-saas-infra/pull/14) | LAUNCH 02.3-D7 — Checkout sandbox et crédit unique qualifiés | ouverte, brouillon | ops/launch023d6-stripe-endive ← ops/launch023d7-sandbox-checkout | 52e22ad35a3d8dfe5cc51c24495bbd5595339e41 |
| [#13](https://github.com/Pascal440/trinity-saas-infra/pull/13) | LAUNCH 02.3-D6 — Endive déployé et premier webhook Stripe signé accepté | ouverte, brouillon | ops/launch023d5-public-https ← ops/launch023d6-stripe-endive | 621fd4234ec1f7455503b9ca5c0b3c428ff52263 |
| [#12](https://github.com/Pascal440/trinity-saas-infra/pull/12) | LAUNCH 02.3-D5 — HTTPS réel, récupération Restic et filtrage réseau | ouverte, brouillon | fix/launch023d4-portal-<TENANT_NAME> ← ops/launch023d5-public-https | 35e2820c39e1eda613fa4c7bacabf0f3b92210fc |
| [#11](https://github.com/Pascal440/trinity-saas-infra/pull/11) | LAUNCH 02.3-D4 — Préparer <PORTAL_HOST> et vérifier le DNS | ouverte, brouillon | ops/launch023d3-backup-https ← fix/launch023d4-portal-<TENANT_NAME> | 7ec289d9eab65ac6c3a98eb9ec062032e0cacc39 |
| [#10](https://github.com/Pascal440/trinity-saas-infra/pull/10) | LAUNCH 02.3-D3 : Restic S3 restauré, sauvegardes planifiées et HTTPS préparé | ouverte, brouillon | fix/launch023d2-private-boot ← ops/launch023d3-backup-https | 9af6e8838078c78427fb37ebf554f07e70a13aef |
| [#9](https://github.com/Pascal440/trinity-saas-infra/pull/9) | LAUNCH 02.3-D2 : premier démarrage privé, images immuables et restauration vérifiée | ouverte, brouillon | fix/launch023d11-preproduction ← fix/launch023d2-private-boot | bbc199bb64f59caa7f240cb2bda8de9198a3c4ff |
| [#8](https://github.com/Pascal440/trinity-saas-infra/pull/8) | LAUNCH 02.3-D1.1 : HTTPS dynamique, portail/scheduler et audit privilégié | ouverte, brouillon | feature/launch022-qualification ← fix/launch023d11-preproduction | 96e119091200799eab74e735e966d43b072169c2 |
| [#7](https://github.com/Pascal440/trinity-saas-infra/pull/7) | docs(LAUNCH 02.3-D1): audit statique et plan de préparation VPS — non qualifié | ouverte, brouillon | feature/launch022-qualification ← docs/launch023d1-vps-preparation | 8840b2ab036ba29e4767285e78b0f67bfa6a4f5e |
| [#6](https://github.com/Pascal440/trinity-saas-infra/pull/6) | LAUNCH 02.2 : rapport, preuves intégrées et procédure sandbox | ouverte, hors brouillon | feature/launch021-lifecycle ← feature/launch022-qualification | 35b6a14bf750f1f9ee3e04bfe5c772d7d9fc56db |
| [#5](https://github.com/Pascal440/trinity-saas-infra/pull/5) | LAUNCH 02.1 : suspension réversible et révocation terminale v2 | ouverte, hors brouillon | feature/saas-phase52 ← feature/launch021-lifecycle | 9cb0060e05620418aaa7a96690f81be219859dfd |
| [#4](https://github.com/Pascal440/trinity-saas-infra/pull/4) | Phase 5.2 : activation propriétaire WebUI sécurisée et préparation Gateway | ouverte, hors brouillon | feature/saas-phase51 ← feature/saas-phase52 | 19300d3802ca16dd08f4cf983f9010f12738ecae |
| [#3](https://github.com/Pascal440/trinity-saas-infra/pull/3) | Phase 5.1 : suspension complète, résilience Gateway et contrat portail | ouverte, hors brouillon | feature/saas-phase5 ← feature/saas-phase51 | ade14bd7f6e9e6f5888bb93976480535aea34336 |
| [#2](https://github.com/Pascal440/trinity-saas-infra/pull/2) | Phase 5 : provisionnement asynchrone et cycle de vie SaaS | ouverte, hors brouillon | feature/saas-phase4 ← feature/saas-phase5 | 9b840cdaa14d0b22e7a00095c6d4444aed3c7fbb |
| [#1](https://github.com/Pascal440/trinity-saas-infra/pull/1) | Phase 4 : infrastructure Docker SaaS multi-instances | ouverte, hors brouillon | main ← feature/saas-phase4 | 44fed2a7e00d55c39f353b1fdcf66b88822b3bc8 |

Branches retournées : `docs/launch01-recovery`, `docs/launch02-contract-audit`, `docs/launch023d1-real-audit`, `docs/launch023d1-vps-preparation`, `feature/launch021-lifecycle`, `feature/launch022-qualification`, `feature/saas-phase4`, `feature/saas-phase5`, `feature/saas-phase51`, `feature/saas-phase52`, `fix/launch023d2-private-boot`, `fix/launch023d4-portal-<TENANT_NAME>`, `fix/launch023d11-preproduction`, `main`, `ops/launch023d3-backup-https`, `ops/launch023d5-public-https`, `ops/launch023d6-stripe-endive`, `ops/launch023d7-sandbox-checkout`, `ops/launch023d8-first-ai-client`.

### Lecture des chantiers
- Phases SaaS 4–5.2 et 6.1–6.1.2 : implémentations documentées et validations historiques, encore dans les chaînes de PR ouvertes ; l'activation positive du propriétaire est documentée à partir de 6.1.2. Ne pas interpréter les blocages anciens de 6.1.1 comme l'état final.
- LAUNCH 01 : branche docs/launch01-recovery présente. Son rapport précis et sa tête n'ont pas été lus ; niveau de clôture non établi.
- LAUNCH 02.1 : ensemble coordonné Infra #5, Gateway #7, Portal #4 ; description Portal : application infrastructure puis Gateway puis portail.
- LAUNCH 02.2 : Infra #6, Gateway #8, Portal #5. Leurs réserves historiques sur l'absence de paiement réel sont complétées par les qualifications ultérieures D6/D7.
- LAUNCH 02.3-D1/D1.1 : préparation et candidat non déployable historique ; ne pas sélectionner ce manifeste au lieu de D8.
- D2–D8 : PR infra #9–#15 empilées. D6 reçoit le webhook signé Endive ; D7 documente un paiement Stripe TEST de 49 EUR et un crédit d'usage unique de 1 EUR ; D8 documente activation, première inférence et restauration isolée D7. Ce sont des preuves historiques déclarées, pas des transactions exécutées pendant WORKSPACE-01.
- D8 : Infra #15 dépend de #14 ; Portal #8 de #7 ; Gateway #9 de #8. Les trois restent en brouillon.
- FRONT-01 #9 dépend de Portal D8 #8 ; FRONT-02 #10 dépend de #9 ; FRONT-02.1 #11 dépend de #10. Tous en brouillon et en attente de validation visuelle.
- Statuts CI, reviews, discussions et mergeabilité effective n'ont pas été requalifiés. « Hors brouillon » ne vaut pas approbation de Maya ou aptitude au déploiement.

### État exact de FRONT-02.2
Le rapport local FRONT022_REPORT.md décrit une intégration terminée localement et prête pour revue visuelle, avec champ Vue/HTML, validation de saisie et sculpture PNG statique. La soumission reste une démonstration commerciale : aucune requête IA ou consommation de crédit ajoutée.

GitHub : assets/front022-axenor-sculpture et feature/front022-static-glass-saucer pointent toutes deux sur 9b5d66bf03aa9a0efdfc914c0547ac6a55772e0f. Derniers commits :
- 9b5d66b — Add files via upload — 3 novembre, 06 h 54 Paris.
- 7664716 — préparation du transfert asset et des exigences de saisie — 06 h 46 Paris.
- 433f69a — FRONT-02.1 — 06 h 17 Paris.

La branche FRONT-02.2 ne contient ni GlassSaucerPrompt.vue ni le rapport final ni les fichiers docs de tests locaux ; aucune PR FRONT-02.2 dans les résultats. L'implémentation n'est donc pas sauvegardée dans GitHub.

Hashes Git des fichiers locaux observés :
- CommercialHome.vue : e67a98ab995cdabd0bc87f0c788cbb5be8c72774.
- GlassSaucerPrompt.vue : f29547b007c0b213340c57d2353fb65983ef4e54.
- resources/images/front022/axenor-glass-saucer.png : 3a4f48c136f20c9295427bd76a761af1dd2da398, conforme au blob asset annoncé.

Prévisualisation front022-preview active et healthy sur 127.0.0.1:4176. Le rapport local annonce builds réussis, huit scénarios Chromium/Firefox et contrôles alpha/accessibilité ; non rejoués ici. Il mentionne FRONT022_SOURCE_CHANGES.zip et FRONT022_CHANGES.patch, dont l'intégrité n'a pas été vérifiée ici.

Le même rapport relate deux refus du contrôle automatique de publication de CommercialHome.vue, faute d'autorisation explicite nommant le dépôt. Il s'agit d'un blocage antérieur rapporté, pas d'une tentative réalisée pendant WORKSPACE-01. Cette mission interdit de toute façon commit/push et ne le lève pas. Validation visuelle opérateur et enregistrement GitHub restent à faire après arbitrage.

AXENOR demeure une marque de prototype ; aucune validation commerciale n'en est déduite.

## 5. Préproduction : correspondance avec GitHub
Manifeste local <PREPRODUCTION_ROOT>/infra/deployment/launch023d8.json :
- Portal source b9c84b5de9671c1be73f8e8cb3198bea3cfec855 = PR Portal #8.
- Gateway source f79ff7f4ca938e0610a6e753b4b107dd4edc7437 = PR Gateway #9.
- Infrastructure source 52e22ad35a3d8dfe5cc51c24495bbd5595339e41 = base D7 de la PR Infra #15 ; la tête de cette PR est 5bd6fee98a468191613766e0093bdcda8de59099.
- SDK annoncé : 7930327bdd3ce3ab9ba5367930b39098bcb35a5f.

Les IDs d'images des conteneurs observés correspondent aux références du manifeste D8 :
| Composant | ID image observé |
| --- | --- |
| Portal + scheduler | sha256:50173a5cf60b06f87ac392b8187b1bd4d47387feb89c05301a488e99754aa4f5 |
| Gateway | sha256:71d466513a1b85539313d47f6928da0159dbb52a964a1895f68becacf7453852 |
| Provisioner API/worker | sha256:2e5be0ec0d8a2fc170fca7068ad4d354dc0429ce8859ead9e0e8228a5623e061 |
| Traefik | sha256:fd5932c796f7e2db9fd6bff485ef693d53797f0ee8ad03dc68aa424ea6f21958 |
| MySQL | sha256:0426ec38c7a10aa45ba383887df7878f74ee70e2fd589c7b69207f3577901903 |
| Open WebUI | sha256:aa1344cd76b57c571d778cf3436d3901cb3a2d64182bf69a7cb0777a18c9469a |

Cette correspondance confirme les images sélectionnées, pas l'identité intégrale des fichiers de l'hôte avec GitHub. <PREPRODUCTION_ROOT>/infra est sans .git, avec surcharges runtime : aucun « arbre propre » revendiqué. Le manifeste conserve notamment un commentaire historique infrastructure_reference_role faisant référence à D6/D7 ; sa source infrastructure D7 n'est pas la tête D8. Traçabilité à clarifier avant un prochain déploiement.

FRONT-01 à FRONT-02.2 sont des prévisualisations séparées ; aucune de leurs images n'est l'image Portal D8 observée. Le manifeste public désigne <PORTAL_HOST> en HTTPS. Aucun contrôle externe TLS, DNS, pare-feu IONOS, ni lecture SQL ou état financier actuel réalisé.

Le manifeste D8 annonce une recette limitée à 10 appels, expiration le 3 novembre 2026 à 16 h 48 min 20 s Paris. Il ne constitue aucune autorisation d'appel dans cette mission. Flags financiers/Stripe désactivés déclarés dans le manifeste ; configuration effective non relue pour éviter les secrets.

## 6. Docker, ports et tâches observés
13 conteneurs présents : 12 healthy ; registre en cours d'exécution, sans état de santé annoncé. Aucun conteneur arrêté retourné.

| Service / conteneur | Image | Publication hôte |
| --- | --- | --- |
| front01-preview | node:24.19.0-bookworm-slim | 127.0.0.1:4173 → 4173 |
| front02-preview | même image | 127.0.0.1:4174 → 4173 |
| front021-preview | même image | 127.0.0.1:4175 → 4173 |
| front022-preview | même image | 127.0.0.1:4176 → 4173 |
| trinity-saas-portal-1 | registre local/trinity-portal | aucune ; 80 interne |
| trinity-saas-portal-scheduler-1 | même image Portal | aucune ; 80 interne |
| trinity-saas-gateway-1 | registre local/trinity-gateway | aucune ; 80 interne |
| trinity-saas-provisioner-api-1 | registre local/trinity-provisioner | 127.0.0.1:8091 → 80 |
| trinity-saas-provisioner-worker-1 | même image provisioner | aucune ; 80 interne |
| trinity-saas-proxy-1 | traefik:v3.6.1 | 0.0.0.0:80 et :443 |
| trinity-saas-mysql-1 | mysql:8.4.7 | aucune ; 3306/33060 internes |
| <TENANT_INSTANCE> | Open WebUI v0.6.34-slim | aucune ; 8080 interne |
| ai-saas-image-registry | registry:3 | 127.0.0.1:5000 → 5000 |

Autres écoutes : SSH 22 IPv4/IPv6 ; DNS 127.0.0.53/54:53 TCP/UDP ; NTP local 323 UDP ; DHCP 68 UDP ; Tailscale 41641 UDP et ports TCP d'interface VPN 63327/38488 ; transfert SSH local 50648. Attribution Docker/SSH vérifiée par ss privilégié. Aucun scan externe.

Contexte Docker default, socket unix:///var/run/docker.sock. L'utilisateur de développement n'a pas accès direct au socket ; sudo -n permet la lecture. Services docker/containerd, SSH, Tailscale et services système actifs.

Volumes persistants observés : trinity-saas_mysql_data, trinity-saas_gateway_storage, trinity-saas_portal_storage, trinity-saas_certificates et <TENANT_INSTANCE>-data.
Réseaux : quatre réseaux FRONT distincts ; trinity-saas_database, family_edge, gateway_edge, portal_edge, provisioner_admin, solo_edge ; réseaux bootstrap/edge de l'instance WebUI ; bridge/host/none.

Les labels Compose centraux pointent vers <PREPRODUCTION_ROOT>/infra et une composition de compose.yaml, compose.provisioner.yaml, compose.preproduction.yaml, compose.production.yaml, compose.https-qualification.yaml et, selon service, compose.mail.yaml. MySQL conserve les labels historiques du profil privé. Ne pas déduire la commande correcte de reprise d'un seul label ancien.

Le worker provisioner monte le socket Docker ; les previews montent leurs fichiers serveur et public directement depuis les copies FRONT. Les services centraux utilisent volumes et chemins runtime persistants.

Timers ai-saas-backup et ai-saas-backup-monitor présents ; dernière activation affichée respectivement le 3 novembre à 03 h 19 et 11 h 03 Paris. Cette observation ne prouve pas la réussite des sauvegardes : journaux et snapshots non contrôlés. Aucun timer lancé ou modifié.

## 7. Risques de conflit
1. Préproduction et previews partagent cet hôte : reprise de Compose, noms/ports réutilisés ou action globale Docker pourrait toucher des services existants.
2. Le clone D1.1 est sale et ancien ; les copies FRONT n'ont pas de suivi Git local. Reset, extraction ou reconstruction au même endroit pourrait perdre des travaux.
3. FRONT-02.2 est essentiellement local : sa branche distante donne une impression trompeuse de sauvegarde complète.
4. Une modification d'un répertoire public FRONT monté peut altérer une preview en cours d'utilisation sans nouveau déploiement.
5. La chaîne de PR est longue et inter-dépôts ; partir de main perdrait les fonctionnalités et correctifs D8.
6. Les manifestes historiques restent présents, avec états contradictoires selon date. Le candidat D1.1 ne décrit pas les images actives D8.
7. Le provisioner dispose du socket Docker ; aucun test de création client ne doit être lancé contre lui pendant une reprise non isolée.
8. Des connexions SSH et tâches planifiées sont en cours ; la concurrence humaine et système doit être prise en compte.
9. Les données MySQL, conversations et certificats sont persistants ; leur sauvegarde n'a pas été requalifiée pendant cet audit.

## 8. Prérequis manquants et limites
- Arbitrage Maya : chantier à reprendre, base exacte et critère d'acceptation ; aucune seconde mission engagée.
- Pour FRONT-02.2 : validation visuelle sur poste opérateur ; sauvegarde GitHub des changements et PR en brouillon seulement dans une mission autorisant ces écritures.
- Choix d'un espace de développement distinct et stratégie de conservation des changements locaux avant checkout ou synchronisation.
- PHP, Python et SSH disponibles ; Composer, Node et npm absents du PATH hôte. Les previews disposent de Node dans leurs conteneurs existants. Versions/extensions PHP, dépendances et capacité complète de test non qualifiées ; aucune installation réalisée.
- Accès SSH sortant, autre environnement de développement, firewall fournisseur et mécanisme de secours opérateur non qualifiés.
- Revue des checks CI/reviews et comparaison exhaustive des sources de déploiement à GitHub encore nécessaires avant intégration ou déploiement.
- Aucun test navigateur, appel IA, paiement, restauration, lecture DB ou test de charge exécuté. La santé Docker n'est pas une certification commerciale.

## 9. Recommandation soumise à Maya
GO pour préparer une reprise de développement dans un espace distinct, sur les références de la chaîne active choisies explicitement, après décision de Maya. Aucun service existant n'a besoin d'être recréé pour cette préparation.

Priorité proposée : préserver et examiner les livrables FRONT-02.2 locaux, puis décider de leur enregistrement dans trinity-saas-portal avec PR vers fix/front021-organic-motion. La base distante actuelle seule ne contient pas l'intégration. Pour un chantier métier, repartir des références D8 coordonnées Portal #8 / Gateway #9 / Infra #15 plutôt que main.

Aucune fusion, publication, migration, installation, modification runtime ou déploiement autorisé par cette recommandation. Maya arbitre la suite ; l'opérateur conserve la validation des engagements financiers et opérations irréversibles.

Fin de WORKSPACE-01. Aucune seconde mission démarrée.

