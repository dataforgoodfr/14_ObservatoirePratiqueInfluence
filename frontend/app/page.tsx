import { listInfluencers } from "@/app/queries";

/** Page temporaire d'exemple qui liste les influenceurs */
export default async function Home() {
  const influencers = await listInfluencers();

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col gap-8 py-16 px-8 bg-white dark:bg-black">
        <h1 className="text-2xl font-bold text-zinc-900 dark:text-white">
          Influenceurs
        </h1>
        <table className="w-full text-sm text-left border-collapse">
          <thead>
            <tr className="border-b border-zinc-200 dark:border-zinc-700">
              <th className="py-2 pr-4 font-semibold text-zinc-500 dark:text-zinc-400">
                ID
              </th>
              <th className="py-2 pr-4 font-semibold text-zinc-500 dark:text-zinc-400">
                Nom
              </th>
              <th className="py-2 font-semibold text-zinc-500 dark:text-zinc-400">
                Nb comptes
              </th>
            </tr>
          </thead>
          <tbody>
            {influencers.map((influencer) => (
              <tr
                key={influencer.id}
                className="border-b border-zinc-100 dark:border-zinc-800"
              >
                <td className="py-2 pr-4 text-zinc-400">{influencer.id}</td>
                <td className="py-2 pr-4 text-zinc-900 dark:text-white">
                  {influencer.fields?.Name ?? "—"}
                </td>
                <td className="py-2 text-zinc-900 dark:text-white">
                  {influencer.fields?.Accounts ?? "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
