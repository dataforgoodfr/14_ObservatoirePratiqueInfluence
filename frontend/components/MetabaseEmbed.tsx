"use client";

import { cn } from "@/lib/utils";

interface MetabaseEmbedProps {
  embedUrl: string;
  title?: string;
  className?: string;
}

/**
 * Iframe responsive pour l'embedding statique Metabase.
 */
export function MetabaseEmbed({
  embedUrl,
  title = "Dashboard Metabase",
  className,
}: MetabaseEmbedProps) {
  return (
    <iframe
      src={embedUrl}
      title={title}
      className={cn("w-full rounded-lg border border-border", className)}
      style={{ height: "80vh" }}
    />
  );
}
