import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/Container";
import { Highlight } from "@/components/Highlight";
import { buttonVariants } from "@/components/ui/button-variants";
import { cn } from "@/lib/utils";

export default function Home() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="flex-1 py-15 bg-muted">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-hero text-center font-black text-muted leading-[1.1] mb-6">
                {"Observatoire des pratiques de "}
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {"l'influence"}
                </Highlight>
              </h1>

              <p className="text-white text-center font-light mb-10">
                {
                  "Réveillons le monde de l'influence sur les questions environnementales et sociales en analysant les pratiques d'influence en France"
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
                <em className="font-italic">{"l'influence ?"}</em>
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Les collaborations entre influenceurs et entreprises progressent, + 13,1% de croissance des investissements en marketing d'influence en 2025."
                  }
                </p>
                <p>
                  {
                    "Avec elle, les partenariats avec des entreprises controversées aux impacts sociétaux et environnementaux importants."
                  }
                </p>
                <p>
                  {
                    "Cette tendance alarmante soulève des questions sur la responsabilité des créateurs de contenu et l'impact de ces promotions sur leurs audiences, souvent jeunes et influençables."
                  }
                </p>
                <p>
                  {
                    "Mais concrètement, quels secteurs dominent les partenariats des plus gros créateurs ? Quelles marques reviennent le plus dans les collabs ? Et in fine, quel impact sur nos habitudes de consommation, sur nos imaginaires ?"
                  }
                </p>
                <p>
                  {
                    "C’est ce à quoi tente de répondre l’Observatoire des pratiques de l’influence."
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
                  className={cn(
                    buttonVariants({ variant: "highlight", size: "pill" }),
                  )}
                >
                  Signaler une collaboration
                </Link>
              </div>
            </div>

            <div className="relative w-full lg:w-1/2 aspect-video rounded-2xl overflow-hidden">
              <Image
                src="/homePage.jpg"
                alt=""
                fill
                sizes="(min-width: 1024px) 50vw, 100vw"
                className="object-cover"
              />
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
                  "Chaque jour, des millions de personnes sont exposées à des contenus sponsorisés qui propagent des informations trompeuses, encouragent la"
                }
                {" surconsommation "}
                {
                  "et banalisent des pratiques néfastes pour l'environnement et la société."
                }
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                {
                  metric: "61%",
                  text: "des Français estiment que les influenceurs ont un impact direct sur leurs goûts et leurs modes de consommation.",
                  sourceIndex: 1,
                },
                {
                  metric: "85%",
                  text: "des personnes exposées à un partenariat entre une marque et un influenceur ont envisagé un achat.",
                },
                {
                  metric: "84%",
                  text: "des 15-25 ans suivent des influenceurs.",
                  sourceIndex: 2,
                },
              ].map((infosToBeDisplayed, index) => (
                <div key={index} className="flex flex-col gap-6">
                  <p className="text-center text-white font-black text-6xl md:text-7xl leading-none">
                    <Highlight bgClassName="bg-highlight-marker-hero">
                      {infosToBeDisplayed.metric}
                    </Highlight>
                  </p>
                  <p className="text-base text-center text-white font-bold leading-relaxed">
                    {infosToBeDisplayed.text}
                    {infosToBeDisplayed.sourceIndex !== undefined && (
                      <sup
                        aria-describedby={`source-${infosToBeDisplayed.sourceIndex}`}
                        className="ml-0.5 text-white/70 font-normal"
                      >
                        {infosToBeDisplayed.sourceIndex}
                      </sup>
                    )}
                  </p>
                </div>
              ))}
            </div>

            <aside
              aria-label="Sources des chiffres cités"
              className="border-t border-white/20 pt-6 text-white/60 text-xs leading-relaxed"
            >
              <ol className="flex flex-col gap-1 list-none">
                {[
                  "Observatoire Cetelem et Harris Interactive (2023)",
                  "Statista 2025",
                ].map((source, i) => (
                  <li key={i} id={`source-${i + 1}`}>
                    <sup className="mr-1">{i + 1}</sup>
                    {source}
                  </li>
                ))}
              </ol>
            </aside>
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
              className={cn(
                buttonVariants({ variant: "highlight", size: "pill" }),
              )}
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
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {"influencer "}
                </Highlight>
                {" à n'importe quel prix."}
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
