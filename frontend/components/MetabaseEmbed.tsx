"use client";

import { cn } from "@/lib/utils";

interface MetabaseEmbedProps {
  dashboardPublicUrl: string;
  title?: string;
  className?: string;
}

/**
 * Iframe responsive pour l'embedding statique Metabase.
 */
export function MetabaseEmbed({
  dashboardPublicUrl,
  title = "Dashboard Metabase",
  className,
}: MetabaseEmbedProps) {
  return (
    <iframe
      src={dashboardPublicUrl}
      title={title}
      className={cn("w-full rounded-lg border border-border", className)}
    />
  );
}
