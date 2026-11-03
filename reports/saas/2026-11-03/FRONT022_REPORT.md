> Copie documentaire expurgée pour GitHub. Les adresses publiques, domaines d’exploitation, identité client et chemins propres à l’hôte sont remplacés par des alias. Les SHA, dépendances, diagnostics et limites sont conservés. Le rapport décrit l’état observé lors de sa mission ; voir WORKSPACE02_REPORT.md pour la sauvegarde ultérieure. Les fichiers originaux locaux restent intacts.

# FRONT-02.2 — Sculpture AXENOR statique

Intégration prête pour validation visuelle opérateur. Aucune fusion ni publication active.

## Source et périmètre

Branche de travail : `feature/front022-static-glass-saucer`, créée depuis la branche asset au commit `9b5d66bf03aa9a0efdfc914c0547ac6a55772e0f`, descendante de FRONT-02.1 `433f69a040ca08a4f305212c83016fdb43ba64a9` (PR #11). PR empilée sur `fix/front021-organic-motion`. La branche asset reste intacte.

Le PNG fourni sur GitHub à `resources/images/axenor-glass-saucer.png` est déplacé vers `resources/images/front022/axenor-glass-saucer.png`, sans modification des octets. Blob Git : `3a4f48c136f20c9295427bd76a761af1dd2da398`. PNG RGBA 8 bits, 1774 × 887, 1 457 310 octets. Aucune régénération, retouche, conversion ou reconstruction de la sculpture.

Les modifications portent sur CommercialHome.vue, le nouveau GlassSaucerPrompt.vue, le déplacement de l’asset, les fichiers de prévisualisation et les preuves/documentation FRONT-02.2. Les autres sections et les composants FRONT-01, D8, Gateway, Stripe et métier restent inchangés. Les anciennes prévisualisations sur 4173/4174/4175 sont préservées.

## Intégration et saisie

L’image et le formulaire partagent un conteneur relatif au ratio 2:1. L’image utilise object-fit: contain, avec ses dimensions natives déclarées, sans filtre, transformation, halo ajouté ni animation. Les paramètres machine=a et machine=b sont ignorés par la nouvelle page. OrganicMachine et ses anciens assets ne sont plus importés par cette page ; ils restent disponibles pour les références antérieures.

Le titre, le champ et le bouton sont de vrais éléments Vue/HTML. Le composant expose le focus aux suggestions existantes et utilise defineModel pour conserver leur comportement. Un libellé accessible est masqué visuellement ; le placeholder disparaît à la saisie. La sélection, le remplacement du texte, le curseur, Tab/Entrée, le focus visible et le bouton fonctionnent. Les questions vides ou composées d’espaces produisent une erreur annoncée par role=alert et aria-invalid. Limite de 500 caractères.

L’envoi conserve le comportement commercial de FRONT-02 : confirmation explicite qu’aucune requête IA n’a été envoyée et invitation à accéder à l’espace. Aucun appel métier ni consommation de crédits n’a été ajouté.

## Prévisualisation privée

Conteneur `front022-preview`, accès uniquement sur la boucle locale du serveur : http://127.0.0.1:4176/ . Aucune route proxy publique ni modification des services actifs. CSP connect-src 'none' conservée.

Depuis le poste opérateur, utiliser le même accès SSH que pour FRONT-02.1 avec un nouveau transfert :

```sh
ssh -N -L 4176:127.0.0.1:4176 <SSH_USER>@<VPS_ADDRESS>
```

Ouvrir ensuite http://localhost:4176/ . Une archive autonome FRONT022_PRIVATE_PREVIEW.zip permet aussi une validation locale : extraire, lancer `node server.mjs`, ouvrir http://127.0.0.1:4176/ (Node 18+ ; aucune installation de dépendances).

## Validation

Build Vite du portail et build de la prévisualisation réussis. Navigateurs headless Linux : Chromium 156.0.8078.73 et Firefox 157.0. Les huit scénarios finaux passent :

| Format | Dimensions | Chromium | Firefox |
| --- | --- | --- | --- |
| Desktop | 1440 × 1000 | PASS | PASS |
| Mobile | 390 × 844 | PASS | PASS |
| Petit mobile | 320 × 740 | PASS | PASS |
| Tablette | 768 × 1024 | PASS | PASS |

Vérifications : aucune erreur JS ; aucune barre de débordement horizontal ; proportions 2:1 ; bords latéraux dans la fenêtre ; formulaire dans la largeur de l’image ; zéro animation dans la sculpture ; géométrie identique avant/après attente en saisie ; variantes A/B inactives ; erreur sur espaces ; sélection/remplacement ; focus par clavier ; soumission ; suggestions ; zéro violation axe automatique dans la section sculpture. Les résultats bruts sont dans docs/front022/TEST_RESULTS.json et FRONT022_TEST_RESULTS.json.

Les huit profils décodent le même alpha : 715 436 pixels totalement transparents, 857 984 partiellement transparents, 118 opaques ; quatre coins transparents. Les contrôles sur fonds clair et sombre et les captures de page ne montrent pas de bordure noire rectangulaire ni de frange noire perceptible à la taille d’affichage. Les pixels sombres partiellement transparents du fichier original restent inchangés ; ces mesures ne garantissent pas l’absence de défaut à tous les niveaux de zoom. Voir FRONT022_ALPHA_BACKGROUNDS.png.

Captures : FRONT022_chromium_desktop.png, FRONT022_chromium_mobile.png, équivalents Firefox, gros plans *_sculpture.png et captures de saisie *_typing.png. Vidéos réelles de la séquence de saisie : FRONT022_chromium_typing.webm et FRONT022_firefox_typing.webm.

## Compromis et limites

Sur mobile, le champ occupe 76 % de la largeur de l’image contre 60 % sur desktop, et le titre remonte légèrement pour conserver un bouton de 44 × 44 px et une police de saisie de 16 px. Le champ couvre davantage les reflets inférieurs du corps central. Les extrémités de la sculpture restent visibles ; l’asset est intégralement préservé. Les textes longs défilent horizontalement dans le champ natif. La mention d’aperçu et les erreurs sont sous l’image pour ne pas masquer la sculpture.

Le PNG original de 1,46 Mo est conservé afin de privilégier la fidélité. Aucune mesure de fluidité d’animation n’est pertinente ici ; aucune nouvelle animation n’est livrée. Les tests sont headless Linux et ne certifient pas le rendu sur le Firefox/Edge du poste opérateur, son clavier virtuel mobile ou son écran. Une validation visuelle finale sur ces appareils reste nécessaire et ne peut être remplacée par les tests automatiques.

## Historique FRONT-02.2 : blocage initial de publication

La branche GitHub `feature/front022-static-glass-saucer` a été créée depuis `9b5d66bf03aa9a0efdfc914c0547ac6a55772e0f`. Aucun fichier FRONT-02.2 ni commit n’y a ensuite été enregistré ; aucune PR n’a été créée.

Le contrôle automatique a rejeté la création du blob contenant CommercialHome.vue : il considère que l’export du code interne vers `Pascal440/trinity-saas-portal` exige une autorisation utilisateur explicite nommant ce dépôt. La provenance a ensuite été démontrée : le hash de l’original local correspond exactement à celui du fichier de cette même branche GitHub (`e328e4fab366a576f9c7a1b448620184e00fc1bc`), et le diff est limité à la mission. Une nouvelle tentative a été refusée pour le même motif. Aucun contournement n’a été effectué.

Les modifications, tests et livrables locaux sont terminés. FRONT022_SOURCE_CHANGES.zip et FRONT022_CHANGES.patch rendent le changement examinable avant autorisation. L’autorisation encore demandée concerne uniquement l’enregistrement des fichiers de cette mission dans le dépôt `Pascal440/trinity-saas-portal`, sur `feature/front022-static-glass-saucer`, puis la création d’une PR en brouillon vers `fix/front021-organic-motion`. Elle n’autorise aucune fusion ni aucun déploiement.

## Mise à jour WORKSPACE-02 — 3 novembre 2026

L’utilisateur a explicitement autorisé la sauvegarde dans Pascal440/trinity-saas-portal. Les modifications sont reprises dans un clone séparé depuis 9b5d66bf03aa9a0efdfc914c0547ac6a55772e0f, sur feature/front022-static-glass-saucer, pour une PR en brouillon vers fix/front021-organic-motion (433f69a040ca08a4f305212c83016fdb43ba64a9). Cette base est ancêtre de la branche et conserve les dépendances FRONT et D8. Le blocage décrit plus haut concerne la mission précédente.

Tests réellement rejoués : build Vite de prévisualisation et build Vite Laravel réussis, git diff --check, comparaison des hashes et contrôle de non-duplication du PNG. Les dépendances locales existantes ont été copiées dans le clone isolé, sans installation et sans modifier les copies utilisées par Docker. Le PNG source conserve le blob 3a4f48c136f20c9295427bd76a761af1dd2da398.

PHPUnit a été tenté avec environnement nettoyé et SQLite mémoire ; il ne peut démarrer faute des extensions dom, mbstring et xmlwriter sur l’hôte. Aucun test PHP n’a donc été exécuté avec succès pendant WORKSPACE-02. Aucun navigateur n’est disponible sur l’hôte pour rejouer les huit scénarios : docs/front022/TEST_RESULTS.json conserve les résultats HISTORIQUES de FRONT-02.2. Aucun succès navigateur historique n’est présenté comme un nouveau test.

Les fichiers sont destinés au commit de cette PR ; aucune publication de service, migration, fusion ou modification des conteneurs actifs. Validation visuelle opérateur toujours requise. La saisie reste une démonstration sans appel IA. Les preuves lourdes restent locales ; les résultats JSON et scripts de test sont sauvegardés dans le dépôt. Le SHA final de sauvegarde est référencé par le rapport WORKSPACE-02 centralisé dans trinity-docs.

## État GitHub confirmé par WORKSPACE-02

Code sauvegardé dans Pascal440/trinity-saas-portal au commit 517f9dc2cf191681cf7bdc0156b85ac6276b4609, branche feature/front022-static-glass-saucer. PR en brouillon : [#12](https://github.com/Pascal440/trinity-saas-portal/pull/12), base fix/front021-organic-motion. Aucune fusion ni déploiement.
