import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/Container";

export function Footer() {
  return (
    <footer className="w-full border-t border-border bg-background">
      <Container>
        <div className="py-8 md:py-10">
          <div className="flex flex-col items-start gap-8 md:flex-row md:items-start md:justify-between md:gap-6">
            <p className="text-sm text-muted-foreground">Un projet de :</p>

            <div className="flex flex-row gap-8 sm:flex-row sm:gap-10 md:gap-16">
              <div className="flex flex-col gap-3">
                <div className="flex items-center gap-3">
                  <Image
                    src="/logo-pti-italic.svg"
                    alt="Paye ton influence"
                    width={160}
                    height={56}
                    className="h-14 w-auto object-contain"
                  />
                  <span className="text-base font-semibold text-foreground">
                    Paye ton influence
                  </span>
                </div>
                <div className="flex flex-col gap-1.5">
                  <Link
                    href="https://www.instagram.com/payetoninfluence/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-foreground transition-colors duration-300 hover:text-brand-accent"
                  >
                    Instagram
                  </Link>
                  <Link
                    href="https://www.linkedin.com/company/paye-ton-influence/posts/?feedView=all"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-foreground transition-colors duration-300 hover:text-brand-accent"
                  >
                    LinkedIn
                  </Link>
                </div>
              </div>

              <div className="flex flex-col gap-3">
                <div className="flex items-center gap-3">
                  <Image
                    src="/dataforgood_logo.jpeg"
                    alt="Data for Good"
                    width={160}
                    height={56}
                    className="h-14 w-auto object-contain"
                  />
                  <span className="text-base font-semibold text-foreground">
                    Data for Good
                  </span>
                </div>
                <div className="flex flex-col gap-1.5">
                  <Link
                    href="https://dataforgood.fr"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-foreground transition-colors duration-300 hover:text-brand-accent"
                  >
                    Site internet
                  </Link>
                  <Link
                    href="https://www.instagram.com/dataforgoodfr/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-foreground transition-colors duration-300 hover:text-brand-accent"
                  >
                    Instagram
                  </Link>
                  <Link
                    href="https://www.linkedin.com/company/dataforgood/posts/?feedView=all"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-foreground transition-colors duration-300 hover:text-brand-accent"
                  >
                    LinkedIn
                  </Link>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8 flex justify-end border-t border-border pt-4">
            <Link
              href="#"
              className="text-xs text-muted-foreground transition-colors duration-300 hover:text-foreground"
            >
              Mentions légales
            </Link>
          </div>
        </div>
      </Container>
    </footer>
  );
}
