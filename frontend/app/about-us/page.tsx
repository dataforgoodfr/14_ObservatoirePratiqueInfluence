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
                {"Qui "}
                <Highlight bgClassName="bg-highlight-marker-hero">
                  {"sommes "}
                </Highlight>
                {" nous ?"}
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
                  {"Suivre notre compte Instagram"}
                </Link>
              </div>
            </div>

            <ImagePlaceholder />
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
                  {"En savoir plus"}
                </Link>
              </div>
            </div>

            <ImagePlaceholder />
          </div>
        </Container>
      </section>
    </main>
  );
}
