import { MetabaseEmbed } from "@/components/MetabaseEmbed";
import { getDashboardEmbedUrl } from "./queries";
import { Container } from "@/components/Container";
import { Highlight } from "@/components/Highlight";

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
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="py-16 background-secondary">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-hero text-center font-black text-muted leading-[1.1] mb-6">
                {"Les "}
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {" chiffres "}
                </Highlight>
                {"derrière les posts"}
              </h1>
            </div>
          </div>
        </Container>
      </section>
      <MetabaseEmbed
        embedUrl={embedUrl}
        title="Quelques chiffres"
        className="h-[var(--metabase-embed-height-hack-avoiding-double-scroll)]"
      />
    </main>
  );
}
