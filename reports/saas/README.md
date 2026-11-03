# Rapports SaaS — Convention permanente

Chaque mission produit un rapport Markdown sous reports/saas/YYYY-MM-DD/, date Europe/Paris. Le rapport identifie l’objectif, les dépôts autorisés, branches et commits sources, le commit livré lorsqu’il existe et les liens PR. Un rapport ne prétend pas contenir son propre SHA : celui-ci est fourni par la PR, l’index ou le livrable de mission.

Le rapport distingue les tests réellement exécutés pendant la mission des résultats historiques et décrit la configuration de test, les échecs, les contrôles non exécutés, limites connues et risques résiduels. Il précise séparément : code seulement local, committé localement, poussé sur GitHub, PR en brouillon/ouverte/fusionnée et déploiement réellement effectué ou absent.

Les rapports importants sont enregistrés dans Pascal440/trinity-docs. Les preuves volumineuses peuvent rester dans les dépôts techniques : lien immuable vers un commit et chemin, résumé et portée de preuve dans le rapport. Les preuves qui restent seulement locales sont explicitement identifiées comme non accessibles sur GitHub.

Avant toute publication, sélectionner explicitement les fichiers et rechercher les secrets, tokens, mots de passe, clés privées, données personnelles clients et informations sensibles d’exploitation ; remplacer les éléments concernés par des alias stables ou retirer la section sensible tout en conservant le diagnostic utile. Aucun .env, dump SQL, archive non examinée ou rapport contenant des secrets ne doit être publié. Le scan automatique complète la relecture, sans garantir l’absence de toute donnée sensible.

Chaque publication GitHub reste limitée aux dépôts explicitement autorisés pour la mission. L’autorisation documentaire n’autorise ni publication de code dans un autre dépôt, ni fusion, ni déploiement. Utiliser une branche dédiée et une PR en brouillon selon les instructions de mission. Une exception d’initialisation de dépôt vide doit être explicitement autorisée et tracée.

Mettre à jour l’index des missions avec statut, dépôts, branches, SHA et références. Conserver les résultats historiques en les datant ; une mise à jour ultérieure doit être identifiable. Ne pas modifier rétroactivement les conclusions d’une mission pour masquer un blocage.

[Index des missions](INDEX.md)
