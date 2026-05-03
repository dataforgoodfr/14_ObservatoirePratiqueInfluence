import { Container } from "@/components/Container";
import { Highlight } from "@/components/Highlight";
import { ImagePlaceholder } from "../about-us/page";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button-variants";
import { cn } from "@/lib/utils";

export default function ReportCollaborationPage() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="py-16 background-secondary">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-[clamp(2.8rem,5vw,4.2rem)] text-center font-black text-muted leading-[1.1] mb-6">
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
        aria-label="Je suis créateur de contenu et je me pose des questions ..."
        className="py-15"
      >
        <Container>
          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-center">
            <ImagePlaceholder />

            <div className="flex flex-col gap-6 w-full lg:w-1/2">
              <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
                {"Je suis créateur de contenu et je me pose des questions ..."}
              </h2>
              <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
                <p>
                  {
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim"
                  }
                </p>
                <p>
                  {
                    "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate"
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
                  {"Nous contacter"}
                </Link>
              </div>
            </div>
          </div>
        </Container>
      </section>
    </main>
  );
}
