import { getMetabaseEmbedUrl } from "@/lib/metabase";

/**
 * Récupère l'URL d'embedding pour le dashboard de test.
 */
export async function getDashboardEmbedUrl(
  dashboardId: number,
): Promise<string> {
  const params: Record<string, string> = {};
  return getMetabaseEmbedUrl(dashboardId, params);
}
