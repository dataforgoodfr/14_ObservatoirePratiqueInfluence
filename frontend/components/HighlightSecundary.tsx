import { cn } from "@/lib/utils";

export function HighlightSecundary({
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
        "inline-block box-decoration-clone rounded-sm px-1",
        bgClassName ?? "bg-highlight-secondary",
        textClassName ?? "text-highlight-tertiary",
        className,
      )}
    >
      {children}
    </mark>
  );
}
