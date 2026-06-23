import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/Container";
import { Highlight } from "@/components/Highlight";
import { buttonVariants } from "@/components/ui/button-variants";
import { cn } from "@/lib/utils";

export default function AboutUsPage() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="py-16 background-secondary">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-hero text-center font-black text-muted leading-[1.1] mb-6">
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
              {"À propos de la méthodologie de l’Observatoire"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                {
                  "L’observatoire s’appuie sur un panel de 1 147 créateurs identifiés par Paye Ton Influence, sélectionnés selon trois critères : figurer parmi les 400 comptes les plus suivis sur TikTok, Instagram et YouTube ; avoir une audience majoritairement âgée de 15 à 35 ans ; être suivi en France à hauteur d’au moins 20 %. Les données ont été extraites sur l’année 2025 (1er janvier – 31 décembre)."
                }
              </p>

              <h3 className="mt-4 text-foreground font-bold leading-tight text-xl md:text-2xl">
                {"Étape 1 — Scraping des réseaux sociaux"}
              </h3>
              <p>{"Les formats retenus pour le scraping sont :"}</p>
              <div className="flex flex-col gap-2">
                <p>
                  <strong>{"Pour YouTube :"}</strong>
                </p>
                <ul className="list-disc pl-6 flex flex-col gap-2">
                  <li>{"les vidéos classiques"}</li>
                  <li>{"les Shorts sur YouTube"}</li>
                </ul>
              </div>
              <div className="flex flex-col gap-2">
                <p>
                  <strong>{"Sur TikTok :"}</strong>
                </p>
                <ul className="list-disc pl-6 flex flex-col gap-2">
                  <li>{"les vidéos et posts"}</li>
                </ul>
              </div>
              <div className="flex flex-col gap-2">
                <p>
                  <strong>{"Sur Instagram :"}</strong>
                </p>
                <ul className="list-disc pl-6 flex flex-col gap-2">
                  <li>
                    {"les posts à l’exclusion des Reels et des Stories."}
                  </li>
                </ul>
              </div>
              <ul className="list-disc pl-6 flex flex-col gap-2">
                <li>
                  {"1 147 comptes scrapés pour 185 425 posts récupérés."}
                </li>
                <li>{"YouTube : 337 comptes, ~31 000 posts."}</li>
                <li>{"Instagram : 219 comptes, ~24 000 posts."}</li>
                <li>{"TikTok : 591 comptes, ~129 000 posts."}</li>
              </ul>

              <h3 className="mt-4 text-foreground font-bold leading-tight text-xl md:text-2xl">
                {"Étape 2 — Labellisation « collaboration commerciale »"}
              </h3>
              <p>
                {
                  "Trois scripts de détection par expression régulière (regex), un par réseau social, analysent la description de chaque post pour déterminer s’il s’agit d’une collaboration commerciale et, le cas échéant, identifier la marque associée. Les résultats ne sont ni exhaustifs ni vérifiés manuellement : ils proviennent uniquement de l’application de ces scripts sur les 185 425 posts scrapés."
                }
              </p>
              <ul className="list-disc pl-6 flex flex-col gap-2">
                <li>
                  {
                    "7 518 posts en collaboration identifiés, pour 1 309 marques et 702 comptes différents."
                  }
                </li>
                <li>{"YouTube : 1 033 posts en collab pour 183 marques."}</li>
                <li>
                  {"Instagram : 1 449 posts en collab pour 537 marques."}
                </li>
                <li>{"TikTok : 5 036 posts en collab pour 945 marques."}</li>
              </ul>

              <h3 className="mt-4 text-foreground font-bold leading-tight text-xl md:text-2xl">
                {"Étape 3 — Ventilation des marques"}
              </h3>
              <p>
                {
                  "Chaque marque identifiée est rattachée à une catégorie, et certaines sont en plus signalées par Paye Ton Influence comme « à impact négatif ». Ces marques appartiennent à des industries dont les impacts sociétaux et environnementaux sont documentés, avérés, et comptent parmi les plus significatifs selon la grille de lecture de Paye Ton Influence, disponible en annexe de ce document."
                }
              </p>
              <p>
                {
                  "Ce classement est subjectif et assumé comme un choix éditorial de l’association : si un grand nombre d’annonceurs ne sont pas catégorisés « à impact négatif », ce n’est pas qu’ils en seraient exempts, mais parce qu’ils relèvent d’un « business as usual » difficile à documenter avec des sources fiables. Seules les entreprises dont les impacts sociétaux, environnementaux ou sanitaires sont avérés et documentés ont été classées « à impact négatif »."
                }
              </p>
              <p>
                <strong>
                  <em>{"Limite méthodologique"}</em>
                </strong>
                <em>
                  {
                    " : ces résultats reposent sur un script de labellisation automatisé (regex) et non sur une relecture humaine poste par poste. La qualification de marque « à impact négatif » est un choix éditorial de Paye Ton Influence. Les volumes absolus doivent donc être lus comme des ordres de grandeur ; les écarts relatifs entre marques et entre réseaux sont, en revanche, robustes et se confirment sur les trois plateformes."
                  }
                </em>
              </p>
            </div>
          </div>
        </Container>
      </section>
    </main>
  );
}
