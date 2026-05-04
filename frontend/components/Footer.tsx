import Image from "next/image";
import Link from "next/link";

export function Footer() {
  return (
    <footer className="w-full border-t border-border bg-background">
      <div className="flex flex-col items-center gap-4 px-3 py-6 md:flex-row md:justify-between md:gap-6 md:px-5">
        <Image
          src="/logo-pti-italic.svg"
          alt="Paye ton influence"
          width={100}
          height={100}
          className="h-12 object-contain"
        />
        <nav className="flex items-center gap-6">
          <Link
            href="#"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-bold text-foreground transition-colors duration-300 hover:text-brand-accent"
          >
            Paye ton influence
          </Link>
          <Link
            href="#"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-bold text-foreground transition-colors duration-300 hover:text-brand-accent"
          >
            Data for Good
          </Link>
        </nav>
      </div>
    </footer>
  );
}
