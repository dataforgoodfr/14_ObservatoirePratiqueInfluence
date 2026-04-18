import { SignJWT } from "jose";

const METABASE_URL = process.env.METABASE_URL;

function getSecretKey(): Uint8Array {
  const secret = process.env["METABASE_SECRET_KEY"];
  if (!secret) {
    throw new Error("METABASE_SECRET_KEY is not set");
  }
  return new TextEncoder().encode(secret);
}

/**
 * Génère une URL d'embedding statique Metabase pour un dashboard donné.
 */
export async function getMetabaseEmbedUrl(
  dashboardId: number,
  params: Record<string, string> = {},
): Promise<string> {
  const token = await new SignJWT({
    resource: { dashboard: dashboardId },
    params,
  })
    .setProtectedHeader({ alg: "HS256", typ: "JWT" })
    .setIssuedAt()
    .setExpirationTime("10m")
    .sign(getSecretKey());

  return `${METABASE_URL}/embed/dashboard/${token}#bordered=true&titled=true`;
}
