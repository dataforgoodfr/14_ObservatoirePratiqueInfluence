import { Api } from "@/generated-types/Api";

const NOCODB_BASE_URL =
  process.env.NOCODB_BASE_URL ?? "https://noco.services.dataforgood.fr";

function createNocoApi() {
  const token = process.env["NOCODB_API_TOKEN"];
  if (!token) {
    throw new Error("NOCODB_API_TOKEN is not set");
  }

  return new Api({
    baseUrl: NOCODB_BASE_URL,
    securityWorker: () => ({
      headers: { "xc-token": token },
    }),
  });
}

export const nocoApi = createNocoApi().api;
