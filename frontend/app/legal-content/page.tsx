import { Container } from "@/components/Container";

const CONTACT_EMAIL = "payetoninfluence@gmail.com";

function ContactEmailLink() {
  return (
    <a
      href={`mailto:${CONTACT_EMAIL}`}
      className="underline transition-colors duration-300 hover:text-brand-accent"
    >
      {CONTACT_EMAIL}
    </a>
  );
}

export default function LegalContentPage() {
  return (
    <main className="min-h-screen font-sans bg-background">
      <section aria-label="Hero" className="py-16 background-secondary">
        <Container>
          <div className="background-secondary rounded-3xl">
            <div className="relative block items-center px-12 pt-32 pb-16 overflow-hidden">
              <h1 className="text-hero text-center font-black text-muted leading-[1.1] mb-6">
                {"Mentions légales"}
              </h1>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Éditeur du site" className="py-15">
        <Container>
          <div className="flex flex-col gap-6 max-w-3xl">
            <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"Éditeur du site"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                <strong>{"Observatoire des pratiques d’influence"}</strong>
                <br />
                {"Paye ton influence et Data for good"}
                <br />
                {"SIRET de Paye ton influence : 92454239200015"}
              </p>
              <p>
                <strong>{"Contact"}</strong>
                {" : "}
                <ContactEmailLink />
              </p>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Hébergement" className="py-15 bg-muted">
        <Container>
          <div className="flex flex-col gap-6 max-w-3xl">
            <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"Hébergement"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                {"Le site est hébergé par : OVH SAS"}
                <br />
                {"Siège social : 2 rue Kellermann, 59100 Roubaix, France"}
                <br />
                {"RCS Lille Métropole 424 761 419 00045"}
                <br />
                {"Téléphone : 1007"}
              </p>
              <p>{"Métabase pour les données."}</p>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Propriété intellectuelle" className="py-15">
        <Container>
          <div className="flex flex-col gap-6 max-w-3xl">
            <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"Propriété intellectuelle"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                {
                  "L’ensemble du contenu de ce site (textes, images, vidéos, graphismes, logo, icônes) est la propriété exclusive de l’Observatoire des pratiques d’influence ou de ses partenaires, sauf mention contraire. Toute reproduction, représentation, modification ou adaptation, totale ou partielle, est interdite sans autorisation écrite préalable."
                }
              </p>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Données personnelles" className="py-15 bg-muted">
        <Container>
          <div className="flex flex-col gap-6 max-w-3xl">
            <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"Données personnelles"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                {
                  "Conformément au Règlement Général sur la Protection des Données (RGPD) et à la loi Informatique et Libertés, vous disposez d’un droit d’accès, de rectification, de suppression et de portabilité de vos données personnelles."
                }
              </p>
              <p>
                {
                  "Pour exercer ces droits ou pour toute question relative à vos données personnelles, vous pouvez nous contacter à l’adresse : "
                }
                <ContactEmailLink />
                {"."}
              </p>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Cookies" className="py-15">
        <Container>
          <div className="flex flex-col gap-6 max-w-3xl">
            <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"Cookies"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                {
                  "Ce site utilise des cookies techniques nécessaires à son bon fonctionnement. Dans le but de voir l’audience du site, nous collectons de manière anonyme les visites du site."
                }
              </p>
            </div>
          </div>
        </Container>
      </section>

      <section aria-label="Crédits" className="py-15 bg-muted">
        <Container>
          <div className="flex flex-col gap-6 max-w-3xl">
            <h2 className="text-foreground font-bold leading-tight text-3xl md:text-4xl">
              {"Crédits"}
            </h2>
            <div className="flex flex-col gap-4 text-foreground text-base leading-relaxed">
              <p>
                <strong>{"Conception et développement"}</strong>
                {" : Data For Good / Paye Ton Influence"}
              </p>
            </div>
          </div>
        </Container>
      </section>
    </main>
  );
}
