# DEMO-01A — Préparation de la démonstration

4 novembre 2026, heure de Paris.

**Kit hors ligne reproductible vérifié. La recette LLM attend un fournisseur, un budget et le raccordement autorisés.**

Le garde RUNTIME-01 avait programmé l’arrêt le 3 novembre à 18 h 59 min 13 s. Docker enregistre la fin de WebUI à 18 h 59 min 21 s et du Terminal à 18 h 59 min 22 s, tous deux avec code 0. Le marqueur du garde correspond à cet arrêt. Les deux conteneurs historiques sont restés arrêtés et leurs ports locaux fermés.

Le [kit](demo01a-kit/) conserve les réglages non secrets, les références des images épinglées, les scripts de recréation, les trois entrées originales Atelier Boréal et leurs empreintes. La [référence indépendante](demo01a-kit/independent-reference.json) reste celle de RUNTIME-01. Les secrets locaux sont générés à chaque lancement du nouveau labo et réservés à sa session. Aucun accès ou fichier de clés GIPS n’a été récupéré.

| Contrôle nouveau | Résultat |
| --- | --- |
| Recréation bornée | WebUI et Terminal créés à partir des images locales par digest, compte démo et grant dédié, catalogue vide, trois entrées copiées puis vérifiées par SHA256. Conteneurs temporaires retirés. |
| Excel vers PDF | Un classeur opérateur a reçu deux caches volontairement faux à 999 999. Calc a rendu 125 000 et 145 000. Le graphique avec deux séries et trois régions est visible sur la même page. SHA256 de l’entrée identique avant et après. |
| Isolation | Profil de départ en réseau none, sans port Docker publié. Le rendu Calc s’exécute lui aussi dans un conteneur jetable en réseau none. Catalogue modèle vide et profil de sortie désactivé. |

Avant la recréation, le VPS présentait environ 5 Gio de mémoire disponible, 179 Gio libres et quatre CPU. Les essais ont utilisé des objets DEMO-01A distincts, avec préconditions et plafonds de ressources. Pendant la comparaison finale, les 13 conteneurs existants ont conservé leurs images, heures de démarrage et compteurs de redémarrage. Les qualifications RUNTIME-01 des onglets, du bureau, de Chrome et des quatre formats restent des preuves historiques. Aucun essai agentique ou déploiement commercial. Aucun appel à un fournisseur, paiement ou activation Together AI.

L’aperçu Calc est un **PDF séparé**, à ouvrir dans WebUI à côté du XLSX original. L’export initial coupait le graphique entre deux pages. Le mode une page par feuille l’a réuni avec les données. Une feuille très large peut nécessiter un zoom et les fonctions Excel spécifiques doivent être contrôlées sur le livrable de recette. L’exemple publié est explicitement un fichier opérateur.

La [connexion modèle](DEMO01A_MODEL_CONNECTION.md) fixe le contrat du relais et les réglages WebUI. Le relais fournisseur reste une étape de mise en service future, conditionnée à l’autorisation et à ses contrôles d’isolation. Le [runbook](DEMO01A_RUNBOOK.md) couvre la session locale et le [scénario](DEMO01A_SCENARIO.md) décrit une seule recette complète, avec une modification dans le même chat.

Publication documentaire dans `Pascal440/trinity-docs`, branche `reports/demo01a-preparation` depuis `reports/runtime01-lab` au commit `a6b3df13fb8cedcfcfb3d2691e091e0ed4e645ff`. Références techniques reprises de RUNTIME-01 et détaillées dans le manifeste. Aucun commit dans Gateway, Portal ou Infra. Aucune suite lancée automatiquement.
