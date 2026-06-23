# CLAUDE.md — OPI Frontend

## Projet

Frontend de l'Observatoire des Pratiques d'Influence (OPI), projet Data For Good. Application Next.js 16 (App Router) avec dashboards embarqués via Metabase.

## Stack technique

- **Framework** : Next.js 16.1.3 avec App Router
- **Langage** : TypeScript 5 (strict mode)
- **Styling** : Tailwind CSS v4 + OKLCH color tokens
- **Composants UI** : shadcn/ui (style `base-nova`, icônes `lucide-react`)
- **Data viz** : Metabase (dashboards embarqués via lien public)
- **Build** : output `standalone` (Docker)

## Commandes

```bash
npm run dev              # Serveur de dev
npm run build            # Build production
npm run lint             # ESLint
```

## Architecture

```
app/                     # App Router — chaque dossier = une route
  ├── layout.tsx         # Layout racine
  ├── globals.css        # Tokens de design + Tailwind
  ├── <route>/
  │   ├── page.tsx       # Page
  │   └── queries.ts     # Fetching colocalisé avec la page
components/
  ├── ui/                # Composants shadcn/ui (générés via CLI)
  └── ...                # Composants custom
lib/
  └── utils.ts           # Utilitaires (cn, etc.)
```

## Conventions à respecter

### Styling
- **Jamais de couleur hardcodée** (pas de `bg-blue-500`). Utiliser les tokens sémantiques (`bg-primary`, `text-muted-foreground`…).
- Les couleurs sont en **OKLCH** dans `app/globals.css`.
- Tout nouveau token doit être déclaré dans les **3 blocs** : `:root`, `.dark`, `@theme inline`.
- Utiliser `cn()` (de `@/lib/utils`) pour fusionner les classes Tailwind.

### Composants
- Les composants `components/ui/` sont gérés par shadcn/ui. Pour en ajouter : `npx shadcn@latest add <composant>`.
- Les composants custom vont dans `components/` (hors `ui/`).

### Data fetching
- Colocaliser les fonctions de fetch dans un fichier `queries.ts` au même niveau que la `page.tsx` de la route.

### Imports
- Utiliser l'alias `@/` pour tous les imports (ex: `@/components/ui/button`, `@/lib/utils`).

### Langue
- Le code (variables, fonctions, composants) est en **anglais**.
- Les commentaires et la documentation peuvent être en **français**.
