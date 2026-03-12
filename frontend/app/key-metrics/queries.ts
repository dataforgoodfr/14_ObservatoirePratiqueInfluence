import { nocoApi } from "@/lib/nocodb";
import { ScrappInfluencerPRODResponse } from "@/generated-types/Api";

export async function listInfluencers(): Promise<
  ScrappInfluencerPRODResponse[]
> {
  const { data } = await nocoApi.scrappInfluencerProdDbTableRowList({
    pageSize: 10,
  });
  return data.records;
}
