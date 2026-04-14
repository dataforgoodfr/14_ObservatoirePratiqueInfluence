"use client";

import Image from "next/image";
import Link from "next/link";
import { CircleHelp, Menu, X } from "lucide-react";
import { useState } from "react";
import { Container } from "./Container";

export function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="w-full border-b border-border bg-background">
      <Container>
        <nav className="flex h-16 items-center">
          <Link
            href="/"
            className="flex shrink-0 items-center gap-3"
            onClick={menuOpen ? () => setMenuOpen(false) : undefined}
          >
            <Image
              src="/logo-pti-italic.svg"
              alt="Paye ton influence"
              width={100}
              height={100}
              className="h-16 object-contain"
            />
          </Link>
          <div className="flex flex-col leading-none">
            <span className="text-xs text-foreground uppercase italic">
              {"Paye ton "}
              <em className="font-black italic text-highlight">influence</em>
            </span>
          </div>

          {/* Desktop nav */}
          <div className="ml-auto hidden items-center gap-10 md:flex">
            <Link
              href="/key-metrics"
              className="relative text-base font-bold text-foreground"
            >
              Les chiffres
            </Link>
            <Link
              href="/about-us"
              className="relative flex items-center gap-1.5 text-base font-bold text-foreground"
            >
              Qui sommes-nous
            </Link>
            <Link
              href="/report-collaboration"
              className="rounded-full bg-highlight font--bold px-5 py-2 text-foreground text-base hover:bg-highlight/75"
            >
              Signaler une collaboration
            </Link>
          </div>

          {/* Mobile nav */}
          <div className="ml-auto flex items-center gap-2 md:hidden">
            <Link
              href="/report-collaboration"
              className="rounded-full bg-highlight px-4 py-1.5 text-sm font-bold text-foreground hover:bg-highlight/75"
            >
              Signaler
            </Link>
            <button
              onClick={() => setMenuOpen((o) => !o)}
              className="rounded-md p-2 text-muted-foreground hover:text-foreground"
              aria-label={menuOpen ? "Fermer le menu" : "Ouvrir le menu"}
            >
              {menuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </button>
          </div>
        </nav>
      </Container>

      {/* Menu mobile déroulant
          Note: volontairement intégré dans Navbar plutôt qu'extrait en composant séparé.
          Si la complexité augmente (animations, sous-menus, auth...), envisager un composant MobileMenu. */}
      {menuOpen && (
        <div className="border-t border-border bg-background px-6 py-3 md:hidden">
          <div className="flex flex-col gap-1">
            <Link
              href="/key-metrics"
              className="rounded-md px-3 py-2 text-sm font-bold text-foreground transition-colors duration-300 hover:text-brand-accent"
              onClick={() => setMenuOpen(false)}
            >
              Les chiffres
            </Link>
            <Link
              href="/about-us"
              className="flex items-center gap-1.5 rounded-md px-3 py-2 text-sm font-bold text-foreground transition-colors duration-300 hover:text-brand-accent"
              onClick={() => setMenuOpen(false)}
            >
              <CircleHelp className="h-4 w-4" />
              Qui sommes nous
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
