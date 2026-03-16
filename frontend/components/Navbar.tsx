"use client";

import Image from "next/image";
import Link from "next/link";
import { CircleHelp, Menu, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="w-full border-b border-border bg-background">
      <nav className="mx-auto flex h-16 max-w-7xl items-center">
        <Link
          href="/"
          className="flex shrink-0 items-center gap-3"
          onClick={menuOpen ? () => setMenuOpen(false) : undefined}
        >
          <Image
            src="/logo.png"
            alt="Paye ton influence"
            width={160}
            height={64}
            className="h-16 object-contain"
          />
        </Link>

        {/* Desktop nav */}
        <div className="ml-auto hidden items-center gap-3 md:flex">
          <Link
            href="/key-metrics"
            className="px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            Les chiffres
          </Link>
          <Link
            href="/about-us"
            className="flex items-center gap-1.5 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            <CircleHelp className="h-4 w-4" />
            Qui sommes nous
          </Link>
          <Link
            href="/report-collaboration"
            className="rounded-full bg-primary px-5 py-2 text-sm text-primary-foreground hover:bg-primary/90"
          >
            Signaler une collaboration
          </Link>
        </div>

        {/* Mobile nav */}
        <div className="ml-auto flex items-center gap-2 md:hidden">
          <Link
            href="/report-collaboration"
            className="rounded-full bg-primary px-4 py-1.5 text-sm text-primary-foreground hover:bg-primary/90"
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

      {/* Menu mobile déroulant
          Note: volontairement intégré dans Navbar plutôt qu'extrait en composant séparé.
          Si la complexité augmente (animations, sous-menus, auth...), envisager un composant MobileMenu. */}
      {menuOpen && (
        <div className="border-t border-border bg-background px-6 py-3 md:hidden">
          <div className="flex flex-col gap-1">
            <Link
              href="/key-metrics"
              className="rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
              onClick={() => setMenuOpen(false)}
            >
              Les chiffres
            </Link>
            <Link
              href="/about-us"
              className="flex items-center gap-1.5 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
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
