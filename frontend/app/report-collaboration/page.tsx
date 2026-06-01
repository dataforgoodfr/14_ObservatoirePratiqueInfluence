import Image from "next/image";
import { Container } from "@/components/Container";
import { Highlight } from "@/components/Highlight";

const CONTACT_EMAIL = "test@test.fr";

export default function ReportCollaborationPage() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="py-16 background-secondary">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-hero text-center font-black text-muted leading-[1.1] mb-6">
                {"J'agis pour des pratiques"}
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {" d'influence "}
                </Highlight>
                {" plus "}
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {"éthiques"}
                </Highlight>
              </h1>
            </div>
          </div>
        </Container>
      </section>

      <section
        aria-label="Je signale une collaboration qui pose problème"
        className="py-15"
      >
        <Container>
          <div className="flex flex-col lg:flex-row-reverse gap-10 lg:gap-16 items-center">
            <div className="flex flex-col gap-6 w-full lg:w-1/2">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {"Je signale une collaboration qui pose problème"}
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Tu as vu passer sur les réseaux sociaux une collaboration entre un créateur de contenu et une organisation, mais quelque chose cloche : propos peu fiables, greenwashing suspect, ou mise en valeur d'une entité aux forts impacts environnementaux ?"
                  }
                </p>
                <p>
                  <a
                    href={`mailto:${CONTACT_EMAIL}`}
                    className="underline"
                    aria-label={`Envoyer un email à ${CONTACT_EMAIL} pour signaler une publication`}
                  >
                    {"Envoie-nous la publication"}
                  </a>
                  {"."}
                </p>
              </div>
            </div>

            <div className="relative w-full lg:w-1/2 aspect-video rounded-2xl overflow-hidden">
              <Image
                src="/reportCollab-part1.jpg"
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
        aria-label="Je suis créateur de contenu et je me pose des questions"
        className="py-15 bg-muted"
      >
        <Container>
          <div className="flex flex-col lg:flex-row-reverse gap-10 lg:gap-16 items-center">
            <div className="flex flex-col gap-6 w-full lg:w-1/2">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {"Je suis créateur de contenu et je me pose des questions ..."}
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Une organisation te contacte, l'offre est intéressante, mais tu n'arrives pas à savoir si l'entité est éthique. Son impact environnemental, ses pratiques, les clauses du contrat, sa réputation. Tu ne sais pas trop si c'est une bonne idée."
                  }
                </p>
                <p>
                  {"Tu peux nous envoyer un message "}
                  <a
                    href={`mailto:${CONTACT_EMAIL}`}
                    className="underline"
                    aria-label={`Envoyer un email à ${CONTACT_EMAIL}`}
                  >
                    {"ici"}
                  </a>
                  {" et on te répondra."}
                </p>
              </div>
            </div>

            <div className="relative w-full lg:w-1/2 aspect-video rounded-2xl overflow-hidden">
              <Image
                src="/reportCollab-part2.jpg"
                alt=""
                fill
                sizes="(min-width: 1024px) 50vw, 100vw"
                className="object-cover"
              />
            </div>
          </div>
        </Container>
      </section>
    </main>
  );
}
