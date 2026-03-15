import { listInfluencers } from "./queries";

export default async function KeyMetricsPage() {
  const influencers = await listInfluencers();

  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <h1 className="text-2xl font-bold text-foreground">
        Les chiffres ... work in progress ...
      </h1>
      <h2 className="text-xl font-semibold text-foreground mt-8 mb-4">
        Influenceurs (A des fins de test on récupére ici la liste des
        influenceurs. )
      </h2>
      <table className="w-full text-sm text-left border-collapse">
        <thead>
          <tr className="border-b border-border">
            <th className="py-2 pr-4 font-semibold text-muted-foreground">
              ID
            </th>
            <th className="py-2 pr-4 font-semibold text-muted-foreground">
              Nom
            </th>
            <th className="py-2 font-semibold text-muted-foreground">
              Nb comptes
            </th>
          </tr>
        </thead>
        <tbody>
          {influencers.map((influencer) => (
            <tr key={influencer.id} className="border-b border-border">
              <td className="py-2 pr-4 text-muted-foreground">
                {influencer.id}
              </td>
              <td className="py-2 pr-4 text-foreground">
                {influencer.fields?.Name ?? "—"}
              </td>
              <td className="py-2 text-foreground">
                {influencer.fields?.Accounts ?? "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
