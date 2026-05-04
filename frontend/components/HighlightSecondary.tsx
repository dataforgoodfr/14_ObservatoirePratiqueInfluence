import { cn } from "@/lib/utils";

export function HighlightSecondary({
  children,
  bgClassName,
  textClassName,
  className,
}: Readonly<{
  children: React.ReactNode;
  bgClassName?: string;
  textClassName?: string;
  className?: string;
}>) {
  return (
    <mark
      className={cn(
        "inline-block box-decoration-clone rounded-sm px-1 leading-tight",
        bgClassName ?? "bg-highlight-marker-hero",
        textClassName ?? "text-base",
        className,
      )}
    >
      {children}
    </mark>
  );
}
