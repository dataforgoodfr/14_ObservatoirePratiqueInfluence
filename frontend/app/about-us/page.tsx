import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/Container";
import { Highlight } from "@/components/Highlight";
import { buttonVariants } from "@/components/ui/button-variants";
import { cn } from "@/lib/utils";

// TO BE REMOVED
export function ImagePlaceholder() {
  return (
    <div className="w-full lg:w-1/2 aspect-video rounded-2xl bg-muted flex items-center justify-center">
      <svg
        className="h-16 w-16 text-muted-foreground/40"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
      >
        <rect x="3" y="3" width="18" height="18" rx="2" strokeWidth="1.5" />
        <circle cx="8.5" cy="8.5" r="1.5" strokeWidth="1.5" />
        <path strokeWidth="1.5" d="M21 15l-5-5L5 21" />
      </svg>
    </div>
  );
}

export default function AboutUsPage() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="py-16 background-secondary">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-[clamp(2.8rem,5vw,4.2rem)] text-center font-black text-muted leading-[1.1] mb-6">
                {"Qui sommes "}
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {"nous ?"}
                </Highlight>
              </h1>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Paye ton influence" className="py-15">
        <Container>
          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-center">
            <div className="flex flex-col gap-6 w-full lg:w-1/2">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {"Paye ton influence"}
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Paye ton influence est une association lanceuse d'alerte sur l'impact socio-environnemental du secteur de l'influence. À travers de la veille et du plaidoyer auprès des acteurs du secteur et des pouvoirs publics, nous œuvrons à responsabiliser l'influence sur les questions éthiques et écologiques, tout en travallons sur une meilleure régulation du secteur."
                  }
                </p>
              </div>
              <div className="flex flex-wrap gap-3 mt-2">
                <Link
                  href="#"
                  className={cn(
                    buttonVariants({ variant: "highlight", size: "pill" }),
                  )}
                >
                  {"Suivre notre compte Instagram"}
                </Link>
              </div>
            </div>

            <div className="relative w-full lg:w-1/2 aspect-video rounded-2xl overflow-hidden">
              <Image
                src="/aboutUs-pti.png"
                alt=""
                fill
                sizes="(min-width: 1024px) 50vw, 100vw"
                className="object-cover"
              />
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Data for Good" className="py-15 bg-muted">
        <Container>
          <div className="flex flex-col lg:flex-row-reverse gap-10 lg:gap-16 items-center">
            <div className="flex flex-col gap-6 w-full lg:w-1/2">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {"Data for Good"}
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Data For Good est une communauté de plus de 8000 bénévoles de la tech qui mettent leur temps et leurs compétences au service de l’intérêt général."
                  }
                </p>
                <p>
                  {
                    "Nous aidons des associations de terrain qui luttent pour défendre la démocratie, la justice sociale et l'environnement, à développer les outils numériques dont elles ont besoin, tout en développant un plaidoyer techno-critique sur l’usage responsable des technologies, de l'IA et de ses infrastructures."
                  }
                </p>
              </div>
              <div className="flex flex-wrap gap-3 mt-2">
                <Link
                  href="#"
                  className={cn(
                    buttonVariants({ variant: "highlight", size: "pill" }),
                  )}
                >
                  {"En savoir plus"}
                </Link>
              </div>
            </div>

            <div className="relative w-full lg:w-1/2 aspect-video rounded-2xl overflow-hidden">
              <Image
                src="/aboutUs-d4g.jpeg"
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
        aria-label="À propos de l’observatoire de l’influence responsable"
        className="py-15"
      >
        <Container>
          <div className="flex flex-col gap-6 w-full">
            <h2 className="text-center text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"À propos de l’observatoire de l’influence responsable"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                {
                  "Fast fashion. Malbouffe. Industries polluantes ou jalonnées de scandales. On les voit partout sur les réseaux sociaux et notamment dans les collaborations des influenceurs."
                }
              </p>
              <p>
                {
                  "Ces secteurs qui peuvent vous vendre des produits nocifs pour votre santé ou pour l'environnement, vous ciblent quotidiennement. Et en face, les créateurs de contenus se renseignent trop peu sur les impacts de ces produits et industries."
                }
              </p>
              <p>
                {
                  "Mais concrètement, quels secteurs dominent les partenariats des plus gros créateurs ? Quelles marques reviennent le plus dans les collabs ? Et in fine, quel impact sur nos habitudes de consommation, sur nos imaginaires ?"
                }
              </p>
              <p>
                {
                  "Pour répondre à ces questions, Paye ton influence a travaillé avec Data For Good pour créer l'Observatoire des pratiques de l'influence. Un outil pour analyser concrètement ce qui se passe sur les réseaux sociaux et ce que nous vendent les créateurs."
                }
              </p>
              <p>
                {
                  "La plateforme s'appuie sur un panel de plus de 1 000 créateurs parmi les plus suivis sur TikTok, Instagram et YouTube, dont l'audience est majoritairement âgée de 15 à 35 ans et localisée en France à au moins 20 %. Les données ont été extraites sur l'année 2025 (du 1er janvier au 31 décembre)."
                }
              </p>
              <p>
                {
                  "Elle permet de visualiser, à grande échelle, les collaborations commerciales sur TikTok, Instagram et YouTube sur la période 2024-2025."
                }
              </p>
              <ul className="list-disc pl-6 flex flex-col gap-2">
                <li>
                  {
                    "Vous pouvez voir les marques les plus présentes, par secteur"
                  }
                </li>
                <li>{"Identifier si certaines marques sont dominantes"}</li>
                <li>
                  {
                    "Visualiser le nombre moyen de collaborations par créateur et par réseau social pour l'année 2025"
                  }
                </li>
              </ul>
              <p>
                {
                  "L'observatoire permet aussi de zoomer sur les secteurs les plus polluants :"
                }
              </p>
              <ul className="list-disc pl-6 flex flex-col gap-2">
                <li>{"Fast fashion, énergies fossiles"}</li>
                <li>{"Combien de collaborations représentent-ils ?"}</li>
                <li>{"Quelle part occupent-ils dans le total ?"}</li>
                <li>{"Combien de personnes sont exposées à ces contenus"}</li>
              </ul>
              <p>
                {"Vous pouvez aussi contribuer en envoyant via notre page "}
                <Link href="/report-collaboration" className="underline">
                  {"Signaler une collaboration"}
                </Link>
                {
                  ", les collaborations des créateurs de contenu qui vous semblent peu compatibles avec les enjeux sociaux et environnementaux."
                }
              </p>
            </div>
          </div>
        </Container>
      </section>
    </main>
  );
}
