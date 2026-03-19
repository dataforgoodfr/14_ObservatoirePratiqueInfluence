export function Container({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <div className="mx-auto max-w-7xl px-3 md:px-5">{children}</div>;
}
