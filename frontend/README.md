This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

Ce repo contient le front du projet OPI.

Paradigme choisis :

- Utilisation de l'App router
- Colocation pour lister les query utilisé par chaque page
- Typing generé automatiquement via swagger-typescript-api ( https://www.npmjs.com/package/swagger-typescript-api)
- Fichier css global + tailwind

Voici l'architecture globale

frontend/
├── app/ # App Router — chaque dossier = une route
│ ├── layout.tsx # Layout racine (structure HTML, navbar…)
│ ├── globals.css # Styles globaux + directives Tailwind
│ ├── page.tsx # Page d'accueil
│ ├── queries.ts # Fonctions de fetching pour la page d'accueil
│ │
│ ├── pagePubliqueExemple/ # Route /pagePubliqueExemple
│ │ ├── page.tsx # Rendu de la page
│ │ ├── queries.ts # Fonctions de fetching colocalisées pour cette page
│
├── lib/ # Logique partagée et utilitaires
│ └── nocodb.ts # Client API NocoDB (config, auth, fetch générique)
│
├── components/ # Composants React réutilisables
│ ├── ui/ # Composants visuels génériques (boutons, cards…)
│ └── data/ # Composants liés à l'affichage de données NocoDB
│
├── generated-types/ # Types TypeScript
│ └── nocodb.ts # Types générés automatiquement depuis le swagger NocoDB
│
├── scripts/ # Scripts utilitaires hors runtime
│ └── generateTypes.sh # générer les types depuis le swagger exposé par nocodb
│
├── .env.local # Variables d'environnement (URL + token NocoDB)
├── next.config.ts # Configuration Next.js
├── tsconfig.json # Configuration TypeScript
└── package.json # Dépendances et scripts npm

En tant que développeur, pour commencer :

1: Avoir des accès NocoDB et générer un API token depuis l'admin.
2: Toujours sur NocoDB, récupérer l'id de la base utilisée par OPI.
3: Copier `.env.example` et le renommer en `.env.local`. Modifier les valeurs.

4: Générer les types TypeScript depuis le swagger NocoDB :

```bash
npm run generate::type
```

> À relancer manuellement après chaque modification du schéma NocoDB. Cette commande devra aussi être exécutée automatiquement lors du `npm run build` (CI/production).

5: Lancer le serveur de développement :

```bash
npm run dev
```
