This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

Ce repo contient le front du projet OPI.

Paradigme choisis :

- Utilisation de l'App router
- Colocation pour lister les query utilisé par chaque page
- Fichier css global + tailwind

## Architecture globale

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
│ ├── metabase.ts # Génération d'URLs d'embed Metabase (JWT signé)
│ └── utils.ts # Utilitaires partagés (dont `cn` pour la fusion de classes Tailwind)
│
├── components/ # Composants React réutilisables
│ ├── ui/ # Composants shadcn/ui (générés via CLI, ne pas modifier manuellement)
│ └── data/ # Composants écrits manuellement, hors shadcn
│
├── public/ # Assets statiques servis à la racine (accessibles via `/nom-du-fichier`)
│
├── .env.example # Variables d'environnement d'exemple à copier sur son .env local (URL + secret Metabase)
├── components.json # Configuration shadcn/ui (style, aliases, thème…)
├── next.config.ts # Configuration Next.js
├── tsconfig.json # Configuration TypeScript
└── package.json # Dépendances et scripts npm

## Pour bien commencer en tant que developeur

1: Récupérer `METABASE_URL` et `METABASE_SECRET_KEY` auprès de l'admin Metabase OPI.
2: Copier `.env.example` et le renommer en `.env.local`. Renseigner les valeurs.

3: Lancer le serveur de développement :

```bash
npm run dev
```

4: Lire attentivement la suite pour être en accord avec les "guidelines" du projet.

---

## Composants UI — shadcn/ui

Le projet utilise [shadcn/ui](https://ui.shadcn.com/) comme bibliothèque de composants. Contrairement à une librairie npm classique, **les composants sont copiés directement dans `components/ui/`** — ils font partie du dépôt et peuvent être modifiés librement.

### Ajouter un composant

```bash
npx shadcn@latest add <composant>
# exemples :
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add table
```

Le composant est créé dans `components/ui/` et s'importe via :

```ts
import { Button } from "@/components/ui/button";
```

### Utilitaire `cn`

`lib/utils.ts` expose `cn`, une fonction de fusion de classes Tailwind (`clsx` + `tailwind-merge`). À utiliser dans tous les composants :

```ts
import { cn } from "@/lib/utils"

<div className={cn("base-class", condition && "extra-class")} />
```

---

## Charte graphique

L'identité visuelle est centralisée dans **`app/globals.css`** — c'est l'unique source de vérité pour les couleurs, le rayon de bordure, etc.

### Fonctionnement

Le système repose sur trois blocs interdépendants :

- **`:root`** — valeurs du thème clair (tokens sémantiques en CSS custom properties)
- **`.dark`** — valeurs du thème sombre (mêmes noms, valeurs différentes)
- **`@theme inline`** — expose les variables CSS comme tokens Tailwind (ex: `bg-primary`, `text-foreground`)

Les couleurs sont exprimées en **OKLCH**, qui garantit une perception linéaire de la luminosité.

### Règles à respecter

- **Ne jamais hardcoder une couleur** dans un composant (pas de `bg-blue-500`). Toujours utiliser un token sémantique (`bg-primary`, `text-muted-foreground`…).
- Pour modifier la charte : changer les valeurs dans `:root` et `.dark`. Les composants se mettent à jour automatiquement.
- Si un nouveau token est ajouté, il doit être déclaré dans les **trois blocs** (`:root`, `.dark`, `@theme inline`).
- Tous les tokens sont conservés même s'ils ne sont pas tous utilisés immédiatement, pour éviter des régressions lors de l'ajout de composants shadcn.
