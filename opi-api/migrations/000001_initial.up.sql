CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS "v1";

CREATE TABLE "v1"."influencer" (
  "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "username" TEXT NOT NULL
);
ALTER TABLE "v1"."influencer" ADD CONSTRAINT "v1_influencer_username" UNIQUE ("username");

CREATE TABLE "v1"."account" (
  "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "created_at" timestamptz NOT NULL DEFAULT (now()),
  "influencer_uid" uuid NOT NULL REFERENCES "v1"."influencer" ("uid"),
  "social_network" TEXT NOT NULL,
  "handle" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "follower_count" INT,
  "following_count" INT,
  "post_count" INT,
  "view_count" INT,
  "like_count" INT,
  "categories" TEXT [],
  "account_extracted_at" timestamptz
);

CREATE TABLE "v1"."post" (
    "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
    "created_at" timestamptz NOT NULL DEFAULT (now()),
    "account_uid" uuid REFERENCES "v1"."account" ("uid"),
    "post_url" TEXT NOT NULL,
    "published_at" timestamptz,
    "post_extracted_at" timestamptz,
    "title" TEXT,
    "description" TEXT,
    "comment_count" INT,
    "save_count" INT,
    "view_count" INT,
    "repost_count" INT,
    "share_count" INT,
    "categories" TEXT [],
    "tags" TEXT [],
    "sn_has_paid_placement" BOOLEAN,
    "sn_brand" TEXT,
    "post_type" TEXT,
    "text_content" TEXT,
    "subtitles_content" TEXT,
    "subtitles_language_code" TEXT
);

CREATE TABLE "v1"."brand" (
    "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
    "created_at" timestamptz NOT NULL DEFAULT (now()),
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "aliases" TEXT [],
    "categories" TEXT []
);

CREATE TABLE "v1"."brandpost" (
    "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
    "brand_uid" uuid REFERENCES "v1"."brand" ("uid"),
    "post_uid" uuid REFERENCES "v1"."post" ("uid"),
    "is_infered" BOOLEAN NOT NULL
);

CREATE TABLE "v1"."comment" (
    "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
    "created_at" timestamptz NOT NULL DEFAULT (now()),
    "post_uid" uuid REFERENCES "v1"."post" ("uid"),
    "account_uid" uuid REFERENCES "v1"."account" ("uid"),
    "is_authored_by_account" BOOLEAN,
    "content" TEXT NOT NULL
);

CREATE TABLE "v1"."extraction_task" (
    "uid" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
    "created_at" timestamptz NOT NULL DEFAULT (now()),
    "type" TEXT NOT NULL,
    "config" JSON,
    "social_network" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "visible_at" timestamptz,
    "error" TEXT
);
