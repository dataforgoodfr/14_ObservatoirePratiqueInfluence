import { cn } from "@/lib/utils";

export function Highlight({
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
        "inline-block box-decoration-clone rounded-sm px-1 -rotate-2",
        bgClassName ?? "bg-highlight-marker",
        textClassName ?? "text-highlight-marker-foreground",
        className,
      )}
    >
      {children}
    </mark>
  );
}
