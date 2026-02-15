
import instaloader

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    compress_json=False,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
)

profile = instaloader.Profile.from_username(L.context, "carlamoreau_____")


description = profile.biography
follower_count = profile.followers
following_count = profile.followees
post_count = 0
view_count = 0
like_count = 0

print(f"- description:   {description}\n")
print(f"- follower_count:   {follower_count}\n")
print(f"- following_count:   {following_count}\n")

print(f"- biography_hashtags:   {profile.biography_hashtags}\n")
print(f"- biography_mentions:   {profile.biography_mentions}\n")
print(f"- business_category_name:   {profile.business_category_name}\n")
print(f"- external_url:   {profile.external_url}\n")
print(f"- is_business_account:   {profile.is_business_account}\n")
