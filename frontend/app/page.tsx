import Link from "next/link";
import { Container } from "@/components/Container";

export default function Home() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="flex-1 py-15 bg-muted">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-[clamp(2.8rem,5vw,4.2rem)] text-center font-black text-muted leading-[1.1] mb-6">
                {"Observatoire des pratiques de "}
                <em className="font-italic text-highlight">{"l'influence"}</em>
              </h1>

              <p className="text-white text-center font-light mb-10">
                {
                  "Réveillons le monde de l'influence sur les questions climatiques et sociales en analysant les pratiques d'influence en France."
                }
              </p>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Pourquoi un observatoire" className="py-15">
        <Container>
          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-center">
            <div className="flex flex-col gap-6 w-full lg:w-1/2">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {"Pourquoi un observatoire de "}
                <em className="font-italic text-highlight">
                  {"l'influence ?"}
                </em>
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Les collaborations entre influenceurs et entreprises controversées ont connu une croissance sans précédent en 2024."
                  }
                </p>
                <p>
                  {"En seulement 11 mois, nous avons recensé "}
                  <strong>{"40 partenariats"}</strong>
                  {
                    " impliquant des entreprises aux pratiques douteuses, touchant plus de "
                  }
                  <strong>{"4,5 millions"}</strong>
                  {" de vues cumulées."}
                </p>
                <p>
                  {
                    "Cette tendance alarmante soulève des questions sur la responsabilité des créateurs de contenu et l'impact de ces promotions sur leurs audiences, souvent jeunes et influençables."
                  }
                </p>
              </div>
              <div className="flex flex-wrap gap-3 mt-2">
                <Link
                  href="/key-metrics"
                  className="rounded-full bg-primary px-6 py-3 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                >
                  Voir tous les chiffres
                </Link>
                <Link
                  href="/report-collaboration"
                  className="rounded-full border border-highlight px-6 py-3 text-sm font-medium text-highlight hover:bg-highlight/5"
                >
                  Signaler une collaboration
                </Link>
              </div>
            </div>

            {/* Placeholder image */}
            <div className="w-full lg:w-1/2 aspect-video rounded-2xl bg-muted flex items-center justify-center">
              <svg
                className="h-16 w-16 text-muted-foreground/40"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <rect
                  x="3"
                  y="3"
                  width="18"
                  height="18"
                  rx="2"
                  strokeWidth="1.5"
                />
                <circle cx="8.5" cy="8.5" r="1.5" strokeWidth="1.5" />
                <path strokeWidth="1.5" d="M21 15l-5-5L5 21" />
              </svg>
            </div>
          </div>
        </Container>
      </section>

      <section
        aria-label="Impact réel sur la consommation"
        className="py-16 background-secondary"
      >
        <Container>
          <div className="flex flex-col gap-10">
            <div className="flex flex-col gap-4 items-center text-center">
              <h2 className="text-white font-bold leading-tight text-3xl md:text-4xl">
                Un impact réel sur notre consommation
              </h2>
              <p className="text-white/80 text-base leading-relaxed max-w-2xl">
                {
                  "Chaque jour, des millions de personnes sont exposées à des contenus sponsorisés qui propagent des informations trompeuses, encouragent la surconsommation et banalisent des pratiques néfastes pour l'environnement et la société."
                }
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {["Léna Situations x Amazon", "collab2", "collab3"].map(
                (title) => (
                  <div key={title} className="flex flex-col gap-3">
                    <div className="aspect-video rounded-2xl bg-white/10 flex items-center justify-center">
                      <svg
                        className="h-12 w-12 text-white/30"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        aria-hidden="true"
                      >
                        <rect
                          x="3"
                          y="3"
                          width="18"
                          height="18"
                          rx="2"
                          strokeWidth="1.5"
                        />
                        <circle cx="8.5" cy="8.5" r="1.5" strokeWidth="1.5" />
                        <path strokeWidth="1.5" d="M21 15l-5-5L5 21" />
                      </svg>
                    </div>
                    <p className="font-bold text-white">{title}</p>
                  </div>
                ),
              )}
            </div>
          </div>
        </Container>
      </section>
      <section aria-label="Industries ultra-polluantes" className="py-16">
        <Container>
          <div className="flex flex-col gap-10 items-center text-center">
            <div className="flex flex-col gap-4 max-w-3xl">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {
                  "Des industries ultra-polluantes qui dépensent des milliers d'euros sur les réseaux"
                }
              </h2>
              {/* <p className="text-foreground/70 text-base leading-relaxed max-w-2xl">
                lorem ...
              </p> */}
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-16 gap-y-8 w-full max-w-2xl">
              {[
                "Fast Food",
                "Fast Fashion",
                "Fast Travel",
                "Fast Food",
                "Fast Fashion",
                "Fast Travel",
              ].map((label, i) => (
                <div key={i} className="flex items-center gap-3">
                  <svg
                    className="h-8 w-8 shrink-0 text-foreground"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden="true"
                  >
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                    <line x1="12" y1="22.08" x2="12" y2="12" />
                  </svg>
                  <span className="font-bold text-foreground">{label}</span>
                </div>
              ))}
            </div>

            <Link
              href="/key-metrics"
              className="rounded-full border border-highlight px-6 py-3 text-sm font-medium text-highlight hover:bg-highlight/5"
            >
              Voir tous les chiffres
            </Link>
          </div>
        </Container>
      </section>

      <section
        aria-label="Ne nous laissons pas influencer"
        className="py-16 background-secondary"
      >
        <Container>
          <div className="flex flex-col gap-8 items-center text-center">
            <div className="flex flex-col gap-4 max-w-2xl">
              <h2 className="text-white font-bold leading-tight text-3xl md:text-4xl">
                {"Ne nous laissons pas "}
                <em className="font-italic text-highlight">{"influencer "}</em>
                {"à n'importe quel prix."}
              </h2>
            </div>

            <Link
              href="/report-collaboration"
              className="rounded-full border border-white px-8 py-3 text-sm font-medium text-white hover:bg-white/10"
            >
              {"J'agis"}
            </Link>
          </div>
        </Container>
      </section>
    </main>
  );
}
