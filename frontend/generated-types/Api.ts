/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** Attachment */
export interface Attachment {
  mimetype?: string;
  size?: number;
  title?: string;
  url?: string;
  icon?: string;
}

/** Scrapp - Post (PROD) Response */
export interface ScrappPostPRODResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    "Post Id"?: string;
    Account?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    "Display Name"?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    Brand?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Social Network (from Account)"?: string;
  };
}

/** Scrapp - Post (PROD) Request */
export interface ScrappPostPRODRequest {
  /** Record fields data to be created/updated */
  fields: {
    "Post Id"?: string;
    Account?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    Brand?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
  };
}

/** Scrapp - Post (PROD) Update Request */
export interface ScrappPostPRODUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    "Post Id"?: string;
    Account?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    Brand?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
  };
}

/** Scrapp - Post (PROD) Id Request */
export interface ScrappPostPRODIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Scrapp - Influencer (PROD) Response */
export interface ScrappInfluencerPRODResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Name?: string;
    Accounts?: number;
    "Nb Accounts"?: number;
  };
}

/** Scrapp - Influencer (PROD) Request */
export interface ScrappInfluencerPRODRequest {
  /** Record fields data to be created/updated */
  fields: {
    Name?: string;
  };
}

/** Scrapp - Influencer (PROD) Update Request */
export interface ScrappInfluencerPRODUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Name?: string;
  };
}

/** Scrapp - Influencer (PROD) Id Request */
export interface ScrappInfluencerPRODIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Scrapp - Brand (PROD) Response */
export interface ScrappBrandPRODResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Name?: string;
    "Sponsored Posts"?: number;
    Category?: string;
  };
}

/** Scrapp - Brand (PROD) Request */
export interface ScrappBrandPRODRequest {
  /** Record fields data to be created/updated */
  fields: {
    Name?: string;
    Category?: string;
  };
}

/** Scrapp - Brand (PROD) Update Request */
export interface ScrappBrandPRODUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Name?: string;
    Category?: string;
  };
}

/** Scrapp - Brand (PROD) Id Request */
export interface ScrappBrandPRODIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Scrapp - Account (PROD) Response */
export interface ScrappAccountPRODResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    "Social Network"?: string;
    Influencer?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Account Id"?: string;
    "Display Name"?: string;
    Posts?: number;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    "View Count (Extracted)"?: number;
    Handle?: string;
    "Post Count (Extracted)"?: number;
    "Comment Count (Extracted)"?: number;
    account_extraction_date?: string;
  };
}

/** Scrapp - Account (PROD) Request */
export interface ScrappAccountPRODRequest {
  /** Record fields data to be created/updated */
  fields: {
    "Social Network"?: string;
    Influencer?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    account_extraction_date?: string;
  };
}

/** Scrapp - Account (PROD) Update Request */
export interface ScrappAccountPRODUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    "Social Network"?: string;
    Influencer?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    account_extraction_date?: string;
  };
}

/** Scrapp - Account (PROD) Id Request */
export interface ScrappAccountPRODIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** UserReport - Dash Admin Response */
export interface UserReportDashAdminResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Influenceur?: string;
    "Lien du post"?: string;
    "Marque(s)"?: string;
    "Plateforme(s)"?: string;
    Commentaires?: string;
  };
}

/** UserReport - Dash Admin Request */
export interface UserReportDashAdminRequest {
  /** Record fields data to be created/updated */
  fields: {
    Influenceur?: string;
    "Lien du post"?: string;
    "Marque(s)"?: string;
    "Plateforme(s)"?: string;
    Commentaires?: string;
  };
}

/** UserReport - Dash Admin Update Request */
export interface UserReportDashAdminUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Influenceur?: string;
    "Lien du post"?: string;
    "Marque(s)"?: string;
    "Plateforme(s)"?: string;
    Commentaires?: string;
  };
}

/** UserReport - Dash Admin Id Request */
export interface UserReportDashAdminIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Labellisation - Post Response */
export interface LabellisationPostResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    "Post Id"?: string;
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Account copy - Lien Technique"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Brand - Ajout Manuel"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Account Name"?: string;
    "Social Network"?: string;
  };
}

/** Labellisation - Post Request */
export interface LabellisationPostRequest {
  /** Record fields data to be created/updated */
  fields: {
    "Post Id"?: string;
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Account copy - Lien Technique"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Brand - Ajout Manuel"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Labellisation - Post Update Request */
export interface LabellisationPostUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    "Post Id"?: string;
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Account copy - Lien Technique"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Brand - Ajout Manuel"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Labellisation - Post Id Request */
export interface LabellisationPostIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Labellisation  - Account Response */
export interface LabellisationAccountResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    "Social Network"?: string;
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    "Influencer copy"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Posts copy"?: number;
  };
}

/** Labellisation  - Account Request */
export interface LabellisationAccountRequest {
  /** Record fields data to be created/updated */
  fields: {
    "Social Network"?: string;
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    "Influencer copy"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Labellisation  - Account Update Request */
export interface LabellisationAccountUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    "Social Network"?: string;
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    "Influencer copy"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Labellisation  - Account Id Request */
export interface LabellisationAccountIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Labellisation - Influencer Response */
export interface LabellisationInfluencerResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Name?: string;
    Accounts?: number;
  };
}

/** Labellisation - Influencer Request */
export interface LabellisationInfluencerRequest {
  /** Record fields data to be created/updated */
  fields: {
    Name?: string;
  };
}

/** Labellisation - Influencer Update Request */
export interface LabellisationInfluencerUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Name?: string;
  };
}

/** Labellisation - Influencer Id Request */
export interface LabellisationInfluencerIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Labelisation - Brand Response */
export interface LabelisationBrandResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Name?: string;
    Category?: string;
    "Sponsored Posts"?: number;
  };
}

/** Labelisation - Brand Request */
export interface LabelisationBrandRequest {
  /** Record fields data to be created/updated */
  fields: {
    Name?: string;
    Category?: string;
  };
}

/** Labelisation - Brand Update Request */
export interface LabelisationBrandUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Name?: string;
    Category?: string;
  };
}

/** Labelisation - Brand Id Request */
export interface LabelisationBrandIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Dash Admin - Post Response */
export interface DashAdminPostResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    "Post Id"?: string;
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Account - Lien Technique"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Brand - Ajout Manuel"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Dash Admin - Post Request */
export interface DashAdminPostRequest {
  /** Record fields data to be created/updated */
  fields: {
    "Post Id"?: string;
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Account - Lien Technique"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Brand - Ajout Manuel"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Dash Admin - Post Update Request */
export interface DashAdminPostUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    "Post Id"?: string;
    /** @format uri */
    "Post Url"?: string;
    "Published At"?: string;
    Title?: string;
    Description?: string;
    "Comment Count"?: number;
    "Save Count"?: number;
    "View Count"?: number;
    "Repost Count"?: number;
    "Share Count"?: number;
    Categories?: string;
    Tags?: string;
    "Post Type"?: string;
    "SN Brand"?: string;
    "SN Has Paid Placement"?: boolean;
    "Account - Lien Technique"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
    "Brand - Ajout Manuel"?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Dash Admin - Post Id Request */
export interface DashAdminPostIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Data Admin- Account Response */
export interface DataAdminAccountResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    "Social Network"?: string;
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    Posts?: number;
    Influencer?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Data Admin- Account Request */
export interface DataAdminAccountRequest {
  /** Record fields data to be created/updated */
  fields: {
    "Social Network"?: string;
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    Influencer?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Data Admin- Account Update Request */
export interface DataAdminAccountUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    "Social Network"?: string;
    "Account Id"?: string;
    "Enable Data Extraction"?: boolean;
    Description?: string;
    "Follower Count"?: number;
    "Following Count"?: number;
    "Post Count"?: number;
    "View Count"?: number;
    "Like Count"?: number;
    Categories?: string;
    Handle?: string;
    Influencer?: {
      /** Record identifier for linking */
      id: string | number;
    }[];
  };
}

/** Data Admin- Account Id Request */
export interface DataAdminAccountIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Data Admin- Influencer Response */
export interface DataAdminInfluencerResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Name?: string;
    Accounts?: number;
  };
}

/** Data Admin- Influencer Request */
export interface DataAdminInfluencerRequest {
  /** Record fields data to be created/updated */
  fields: {
    Name?: string;
  };
}

/** Data Admin- Influencer Update Request */
export interface DataAdminInfluencerUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Name?: string;
  };
}

/** Data Admin- Influencer Id Request */
export interface DataAdminInfluencerIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

/** Data Admin - Brand Response */
export interface DataAdminBrandResponse {
  /** Record identifier (primary key value) */
  id: string | number;
  /** Record fields data (excluding primary key) */
  fields?: {
    Name?: string;
    Category?: string;
    "Sponsored Posts"?: number;
  };
}

/** Data Admin - Brand Request */
export interface DataAdminBrandRequest {
  /** Record fields data to be created/updated */
  fields: {
    Name?: string;
    Category?: string;
  };
}

/** Data Admin - Brand Update Request */
export interface DataAdminBrandUpdateRequest {
  /** Record identifier (primary key value) for the record to be updated */
  id: string | number;
  /** Record fields data to be updated */
  fields: {
    Name?: string;
    Category?: string;
  };
}

/** Data Admin - Brand Id Request */
export interface DataAdminBrandIdRequest {
  /** Record identifier (primary key value) for the record to be deleted */
  id: string | number;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown>
  extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  JsonApi = "application/vnd.api+json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "https://noco.services.dataforgood.fr";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) =>
    fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter(
      (key) => "undefined" !== typeof query[key],
    );
    return keys
      .map((key) =>
        Array.isArray(query[key])
          ? this.addArrayQueryParam(query, key)
          : this.addQueryParam(query, key),
      )
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.JsonApi]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.Text]: (input: any) =>
      input !== null && typeof input !== "string"
        ? JSON.stringify(input)
        : input,
    [ContentType.FormData]: (input: any) => {
      if (input instanceof FormData) {
        return input;
      }

      return Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData());
    },
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(
    params1: RequestParams,
    params2?: RequestParams,
  ): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (
    cancelToken: CancelToken,
  ): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(
      `${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`,
      {
        ...requestParams,
        headers: {
          ...(requestParams.headers || {}),
          ...(type && type !== ContentType.FormData
            ? { "Content-Type": type }
            : {}),
        },
        signal:
          (cancelToken
            ? this.createAbortSignal(cancelToken)
            : requestParams.signal) || null,
        body:
          typeof body === "undefined" || body === null
            ? null
            : payloadFormatter(body),
      },
    ).then(async (response) => {
      const r = response as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const responseToParse = responseFormat ? response.clone() : response;
      const data = !responseFormat
        ? r
        : await responseToParse[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title NocoDB v3
 * @version 3.0
 * @baseUrl https://noco.services.dataforgood.fr
 *
 * NocoDB API Documentation
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  api = {
    /**
     * @description List all rows from **Scrapp - Post (PROD)** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Scrapp - Post (PROD)
     * @name ScrappPostProdDbTableRowList
     * @summary Scrapp - Post (PROD) list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/records
     * @secure
     */
    scrappPostProdDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwth1z408z2f68nx - Youtube posts
         * * vwe38gvc7m21khnm - Default view
         * * vwi5hm3q41rk8akg - Instagram posts
         * * vw4wnwb4xddpiqpj - TikTok posts
         * * vw5f4pi7o3fkpksc - Brand Tagging
         * * vwc6b65j418y3oel - Stats
         * * vw760vgg5z0ied0f - Shorts
         */
        viewId?:
          | "vwth1z408z2f68nx"
          | "vwe38gvc7m21khnm"
          | "vwi5hm3q41rk8akg"
          | "vw4wnwb4xddpiqpj"
          | "vw5f4pi7o3fkpksc"
          | "vwc6b65j418y3oel"
          | "vw760vgg5z0ied0f";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappPostPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Scrapp - Post (PROD)
     * @name ScrappPostProdRead
     * @summary Scrapp - Post (PROD) read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/records/{recordId}
     * @secure
     */
    scrappPostProdRead: (recordId: string, params: RequestParams = {}) =>
      this.request<ScrappPostPRODResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Scrapp - Post (PROD)
     * @name ScrappPostProdCount
     * @summary Scrapp - Post (PROD) count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/count
     * @secure
     */
    scrappPostProdCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Scrapp - Post (PROD)
     * @name ScrappPostProdNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/links/{linkFieldId}/{recordId}
     * @secure
     */
    scrappPostProdNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappPostPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mvztjishbiehoo6/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Scrapp - Influencer (PROD)** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Scrapp - Influencer (PROD)
     * @name ScrappInfluencerProdDbTableRowList
     * @summary Scrapp - Influencer (PROD) list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/records
     * @secure
     */
    scrappInfluencerProdDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwmkkbjbd9bdcvhv - Default view
         */
        viewId?: "vwmkkbjbd9bdcvhv";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappInfluencerPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Scrapp - Influencer (PROD)
     * @name ScrappInfluencerProdRead
     * @summary Scrapp - Influencer (PROD) read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/records/{recordId}
     * @secure
     */
    scrappInfluencerProdRead: (recordId: string, params: RequestParams = {}) =>
      this.request<ScrappInfluencerPRODResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Scrapp - Influencer (PROD)
     * @name ScrappInfluencerProdCount
     * @summary Scrapp - Influencer (PROD) count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/count
     * @secure
     */
    scrappInfluencerProdCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Scrapp - Influencer (PROD)
     * @name ScrappInfluencerProdNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/links/{linkFieldId}/{recordId}
     * @secure
     */
    scrappInfluencerProdNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappInfluencerPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m8xy3xbcghv7sd0/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Scrapp - Brand (PROD)** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Scrapp - Brand (PROD)
     * @name ScrappBrandProdDbTableRowList
     * @summary Scrapp - Brand (PROD) list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/records
     * @secure
     */
    scrappBrandProdDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwhumrpl0edwn8ga - Default view
         */
        viewId?: "vwhumrpl0edwn8ga";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappBrandPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Scrapp - Brand (PROD)
     * @name ScrappBrandProdRead
     * @summary Scrapp - Brand (PROD) read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/records/{recordId}
     * @secure
     */
    scrappBrandProdRead: (recordId: string, params: RequestParams = {}) =>
      this.request<ScrappBrandPRODResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Scrapp - Brand (PROD)
     * @name ScrappBrandProdCount
     * @summary Scrapp - Brand (PROD) count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/count
     * @secure
     */
    scrappBrandProdCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Scrapp - Brand (PROD)
     * @name ScrappBrandProdNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/links/{linkFieldId}/{recordId}
     * @secure
     */
    scrappBrandProdNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappBrandPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/me9ocmu6nkvu9rf/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Scrapp - Account (PROD)** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Scrapp - Account (PROD)
     * @name ScrappAccountProdDbTableRowList
     * @summary Scrapp - Account (PROD) list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/records
     * @secure
     */
    scrappAccountProdDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vww70jh08497zgvb - Default view
         * * vwo6e6b2uv2hlb8r - Accounts - Youtube
         * * vwqmgyn5kgcwaggt - Accounts - Tiktok
         * * vwbtj1frl4wh4jj3 - Accounts - Instagram
         * * vwnq89k6qwe91ezc - Stats
         */
        viewId?:
          | "vww70jh08497zgvb"
          | "vwo6e6b2uv2hlb8r"
          | "vwqmgyn5kgcwaggt"
          | "vwbtj1frl4wh4jj3"
          | "vwnq89k6qwe91ezc";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappAccountPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Scrapp - Account (PROD)
     * @name ScrappAccountProdRead
     * @summary Scrapp - Account (PROD) read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/records/{recordId}
     * @secure
     */
    scrappAccountProdRead: (recordId: string, params: RequestParams = {}) =>
      this.request<ScrappAccountPRODResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Scrapp - Account (PROD)
     * @name ScrappAccountProdCount
     * @summary Scrapp - Account (PROD) count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/count
     * @secure
     */
    scrappAccountProdCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Scrapp - Account (PROD)
     * @name ScrappAccountProdNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/links/{linkFieldId}/{recordId}
     * @secure
     */
    scrappAccountProdNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: ScrappAccountPRODResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mqkpvq79dfvut7i/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **UserReport - Dash Admin** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags UserReport - Dash Admin
     * @name UserreportDashAdminDbTableRowList
     * @summary UserReport - Dash Admin list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mpnz6mrvelyx7fo/records
     * @secure
     */
    userreportDashAdminDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwh2cmco361n96ww - Default view
         */
        viewId?: "vwh2cmco361n96ww";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: UserReportDashAdminResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mpnz6mrvelyx7fo/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags UserReport - Dash Admin
     * @name UserreportDashAdminRead
     * @summary UserReport - Dash Admin read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mpnz6mrvelyx7fo/records/{recordId}
     * @secure
     */
    userreportDashAdminRead: (recordId: string, params: RequestParams = {}) =>
      this.request<UserReportDashAdminResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mpnz6mrvelyx7fo/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags UserReport - Dash Admin
     * @name UserreportDashAdminCount
     * @summary UserReport - Dash Admin count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mpnz6mrvelyx7fo/count
     * @secure
     */
    userreportDashAdminCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mpnz6mrvelyx7fo/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Labellisation - Post** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Labellisation - Post
     * @name LabellisationPostDbTableRowList
     * @summary Labellisation - Post list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/records
     * @secure
     */
    labellisationPostDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwymhn1772ic7cma - Default view
         * * vw7c6tc6p3ts68sy - Posts - Instagram
         * * vwgpe1cntei2nkhy - Posts - Youtube
         * * vw4irogu5ljw05qq - Posts - Tiktok
         */
        viewId?:
          | "vwymhn1772ic7cma"
          | "vw7c6tc6p3ts68sy"
          | "vwgpe1cntei2nkhy"
          | "vw4irogu5ljw05qq";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabellisationPostResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Labellisation - Post
     * @name LabellisationPostRead
     * @summary Labellisation - Post read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/records/{recordId}
     * @secure
     */
    labellisationPostRead: (recordId: string, params: RequestParams = {}) =>
      this.request<LabellisationPostResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Labellisation - Post
     * @name LabellisationPostCount
     * @summary Labellisation - Post count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/count
     * @secure
     */
    labellisationPostCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Labellisation - Post
     * @name LabellisationPostNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/links/{linkFieldId}/{recordId}
     * @secure
     */
    labellisationPostNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabellisationPostResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m60gwj0y6wn3azo/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Labellisation  - Account** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Labellisation  - Account
     * @name LabellisationAccountDbTableRowList
     * @summary Labellisation  - Account list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/records
     * @secure
     */
    labellisationAccountDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwkbn8s8x318a8yg - Default view
         * * vw842ls07kza1d3s - Accounts - Instagram
         * * vwvqhfisww7hbjrk - Accounts - Youtube
         * * vw0n0wmw1fkl9q6b - Accounts - Tiktok
         */
        viewId?:
          | "vwkbn8s8x318a8yg"
          | "vw842ls07kza1d3s"
          | "vwvqhfisww7hbjrk"
          | "vw0n0wmw1fkl9q6b";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabellisationAccountResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Labellisation  - Account
     * @name LabellisationAccountRead
     * @summary Labellisation  - Account read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/records/{recordId}
     * @secure
     */
    labellisationAccountRead: (recordId: string, params: RequestParams = {}) =>
      this.request<LabellisationAccountResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Labellisation  - Account
     * @name LabellisationAccountCount
     * @summary Labellisation  - Account count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/count
     * @secure
     */
    labellisationAccountCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Labellisation  - Account
     * @name LabellisationAccountNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/links/{linkFieldId}/{recordId}
     * @secure
     */
    labellisationAccountNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabellisationAccountResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mrdiwk0l9q63fwq/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Labellisation - Influencer** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Labellisation - Influencer
     * @name LabellisationInfluencerDbTableRowList
     * @summary Labellisation - Influencer list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/records
     * @secure
     */
    labellisationInfluencerDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vw6p5w7vz5q38apx - Default view
         */
        viewId?: "vw6p5w7vz5q38apx";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabellisationInfluencerResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Labellisation - Influencer
     * @name LabellisationInfluencerRead
     * @summary Labellisation - Influencer read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/records/{recordId}
     * @secure
     */
    labellisationInfluencerRead: (
      recordId: string,
      params: RequestParams = {},
    ) =>
      this.request<LabellisationInfluencerResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Labellisation - Influencer
     * @name LabellisationInfluencerCount
     * @summary Labellisation - Influencer count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/count
     * @secure
     */
    labellisationInfluencerCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Labellisation - Influencer
     * @name LabellisationInfluencerNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/links/{linkFieldId}/{recordId}
     * @secure
     */
    labellisationInfluencerNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabellisationInfluencerResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m765ngurv9ejyef/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Labelisation - Brand** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Labelisation - Brand
     * @name LabelisationBrandDbTableRowList
     * @summary Labelisation - Brand list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/records
     * @secure
     */
    labelisationBrandDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwqmnvv8o4w5maoj - Default view
         */
        viewId?: "vwqmnvv8o4w5maoj";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabelisationBrandResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Labelisation - Brand
     * @name LabelisationBrandRead
     * @summary Labelisation - Brand read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/records/{recordId}
     * @secure
     */
    labelisationBrandRead: (recordId: string, params: RequestParams = {}) =>
      this.request<LabelisationBrandResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Labelisation - Brand
     * @name LabelisationBrandCount
     * @summary Labelisation - Brand count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/count
     * @secure
     */
    labelisationBrandCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Labelisation - Brand
     * @name LabelisationBrandNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/links/{linkFieldId}/{recordId}
     * @secure
     */
    labelisationBrandNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: LabelisationBrandResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mfowyc1u8edm4o2/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Dash Admin - Post** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Dash Admin - Post
     * @name DashAdminPostDbTableRowList
     * @summary Dash Admin - Post list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/records
     * @secure
     */
    dashAdminPostDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vww3y8izqf6iqghu - Default view
         * * vwhkcnks4o2vtlsi - Posts - Instagram
         * * vwkvx3caoc1xhjs1 - Posts - Youtube
         * * vw7wuicmgtdycrdx - Posts - Tiktok
         */
        viewId?:
          | "vww3y8izqf6iqghu"
          | "vwhkcnks4o2vtlsi"
          | "vwkvx3caoc1xhjs1"
          | "vw7wuicmgtdycrdx";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DashAdminPostResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Dash Admin - Post
     * @name DashAdminPostRead
     * @summary Dash Admin - Post read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/records/{recordId}
     * @secure
     */
    dashAdminPostRead: (recordId: string, params: RequestParams = {}) =>
      this.request<DashAdminPostResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Dash Admin - Post
     * @name DashAdminPostCount
     * @summary Dash Admin - Post count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/count
     * @secure
     */
    dashAdminPostCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Dash Admin - Post
     * @name DashAdminPostNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/links/{linkFieldId}/{recordId}
     * @secure
     */
    dashAdminPostNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DashAdminPostResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/moi68mbg71wxc7h/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Data Admin- Account** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Data Admin- Account
     * @name DataAdminAccountDbTableRowList
     * @summary Data Admin- Account list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/records
     * @secure
     */
    dataAdminAccountDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwbzj7wr515se4qz - Default view
         * * vwcr8vqnvyb8wcgo - Accounts - Instagram
         * * vw5cum0nsdhokz6b - Accounts - Youtube
         * * vwmv8ghdiaj8l902 - Accounts - Tiktok
         */
        viewId?:
          | "vwbzj7wr515se4qz"
          | "vwcr8vqnvyb8wcgo"
          | "vw5cum0nsdhokz6b"
          | "vwmv8ghdiaj8l902";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DataAdminAccountResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Data Admin- Account
     * @name DataAdminAccountRead
     * @summary Data Admin- Account read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/records/{recordId}
     * @secure
     */
    dataAdminAccountRead: (recordId: string, params: RequestParams = {}) =>
      this.request<DataAdminAccountResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Data Admin- Account
     * @name DataAdminAccountCount
     * @summary Data Admin- Account count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/count
     * @secure
     */
    dataAdminAccountCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Data Admin- Account
     * @name DataAdminAccountNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/links/{linkFieldId}/{recordId}
     * @secure
     */
    dataAdminAccountNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DataAdminAccountResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mr1kg4i8t4h8icc/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Data Admin- Influencer** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Data Admin- Influencer
     * @name DataAdminInfluencerDbTableRowList
     * @summary Data Admin- Influencer list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/records
     * @secure
     */
    dataAdminInfluencerDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwxb525oolht67k7 - Default view
         */
        viewId?: "vwxb525oolht67k7";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DataAdminInfluencerResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Data Admin- Influencer
     * @name DataAdminInfluencerRead
     * @summary Data Admin- Influencer read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/records/{recordId}
     * @secure
     */
    dataAdminInfluencerRead: (recordId: string, params: RequestParams = {}) =>
      this.request<DataAdminInfluencerResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Data Admin- Influencer
     * @name DataAdminInfluencerCount
     * @summary Data Admin- Influencer count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/count
     * @secure
     */
    dataAdminInfluencerCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Data Admin- Influencer
     * @name DataAdminInfluencerNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/links/{linkFieldId}/{recordId}
     * @secure
     */
    dataAdminInfluencerNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DataAdminInfluencerResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/mio77xdjf4tkff8/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description List all rows from **Data Admin - Brand** table. Fields to be included in the response can be refined through query parameters. Additionally, filtering, sorting, and pagination can be applied to the results.
     *
     * @tags Data Admin - Brand
     * @name DataAdminBrandDbTableRowList
     * @summary Data Admin - Brand list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/records
     * @secure
     */
    dataAdminBrandDbTableRowList: (
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Controls pagination of nested (linked) records in the API response by specifying the page number. By default, the first page is returned; increment the page number to retrieve subsequent pages.
         *
         * Example: nestedPage=`2` will return the second page of nested data records in the dataset.
         * @min 1
         */
        nestedPage?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
        /**
         * Fetches records that are visible within a specific view. If the view has sorting enabled, the API returns records in the same order as displayed in the view. Specifying a **sort** query parameter overrides the view’s sorting configuration. Similarly, a **where** query parameter applies additional filtering on top of the view’s filters. By default, all fields—including those disabled in the view—are included in the response. Use the **fields** query parameter to include or exclude specific fields and customize the output.
         *
         * **Views:**
         * * vwacj2515o3gl45k - Default view
         */
        viewId?: "vwacj2515o3gl45k";
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DataAdminBrandResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        any
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/records`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Read a row data by using the **primary key** column value.
     *
     * @tags Data Admin - Brand
     * @name DataAdminBrandRead
     * @summary Data Admin - Brand read
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/records/{recordId}
     * @secure
     */
    dataAdminBrandRead: (recordId: string, params: RequestParams = {}) =>
      this.request<DataAdminBrandResponse, any>({
        path: `/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/records/${recordId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Get rows count of a table by applying optional filters.
     *
     * @tags Data Admin - Brand
     * @name DataAdminBrandCount
     * @summary Data Admin - Brand count
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/count
     * @secure
     */
    dataAdminBrandCount: (
      query?: {
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count?: number;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/count`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This API endpoint allows you to retrieve list of linked records for a specific `Link field` and `Record ID`. The response is an array of objects containing Primary Key and its corresponding display value.
     *
     * @tags Data Admin - Brand
     * @name DataAdminBrandNestedList
     * @summary Link Records list
     * @request GET:/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/links/{linkFieldId}/{recordId}
     * @secure
     */
    dataAdminBrandNestedList: (
      linkFieldId: string,
      recordId: string,
      query?: {
        /**
         * Specify fields to include in the API response.
         *
         * Example: fields=`field1` will include only field1 in the response.
         */
        fields?: string[];
        /**
         * Allows you to specify the fields by which you want to sort the records in your API response. Each sort object must have a 'field' property specifying the field name and a 'direction' property with value 'asc' or 'desc'. If **viewId** query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.
         *
         * Example: sort=`{"direction":"asc", "field":"field1"}` will sort records in ascending order based on field1.
         */
        sort?: string[];
        /**
         * Enables defining conditions to filter records in the API response. Multiple conditions can be combined using the logical operators 'and' or 'or'. Each condition consists of three components: a field name, a comparison operator, and a value.
         *
         * Example: where=`(field1,eq,value1)~and(field2,eq,value2)` will filter records where field1 equals value1 AND field2 equals value2.
         *
         * If **viewId** parameter is also included, these filters are applied on top of the view’s predefined filter configuration.
         *
         * **NOTE**: Maintain the specified format; do not include spaces between components of a condition. For further information on this please see [the documentation](https://nocodb.com/docs/product-docs/developer-resources/rest-apis#v3-where-query-parameter)
         */
        where?: string;
        /**
         * Controls pagination of the API response by specifying the page number to retrieve. By default, the first page is returned. Increment the page number to retrieve subsequent pages.
         *
         * Example: page=`2` will return the second page of data records in the dataset.
         * @min 1
         */
        page?: number;
        /**
         * Sets a limit on the number of records returned in the API response. By default, all available records are returned, but this parameter allows you to control the quantity.
         *
         * Example: pageSize=`100` will limit the response to 100 records per page.
         * @min 1
         */
        pageSize?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          records: DataAdminBrandResponse[];
          /** Pagination token for next page */
          next?: string | null;
          /** Pagination token for previous page */
          prev?: string | null;
          /** Nested pagination token for next page */
          nestedNext?: string | null;
          /** Nested pagination token for previous page */
          nestedPrev?: string | null;
        },
        {
          /** @example "BadRequest [Error]: <ERROR MESSAGE>" */
          msg: string;
        }
      >({
        path: `/api/v3/data/pcvkn4m1kpeytae/m676z15lsdev0cz/links/${linkFieldId}/${recordId}`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),
  };
}
