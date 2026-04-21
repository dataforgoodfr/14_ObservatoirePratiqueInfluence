import { MetabaseEmbed } from "@/components/MetabaseEmbed";
import { getDashboardEmbedUrl } from "./queries";

// Next.js App Router : désactive le cache pour cette page.
// Le JWT Metabase embarqué dans le HTML expire après 10 min,
// il faut donc en générer un nouveau à chaque requête.
// Voir https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic
// NE PAS SUPPRIMER
export const dynamic = "force-dynamic";

const TEST_DASHBOARD_ID = 5;

export default async function KeyMetricsPage() {
  const embedUrl = await getDashboardEmbedUrl(TEST_DASHBOARD_ID);

  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <h1 className="text-2xl font-bold text-foreground">Les chiffres</h1>
      <div className="mt-8">
        <MetabaseEmbed embedUrl={embedUrl} title="Quelques chiffres" />
      </div>
    </main>
  );
}
