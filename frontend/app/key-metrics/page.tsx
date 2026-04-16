import { MetabaseEmbed } from "@/components/MetabaseEmbed";
import { getDashboardEmbedUrl } from "./queries";

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
