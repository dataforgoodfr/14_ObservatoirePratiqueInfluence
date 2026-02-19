from instaloader import Post

import instaloader

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    compress_json=False,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
)

post_id = "DQpGQAeCJNz"

post = Post.from_shortcode(L.context, post_id)


print(f"- caption:   {post.caption}\n")
print(f"- pcaption:   {post.pcaption}\n")
print(f"- caption_hashtags:   {post.caption_hashtags}\n")
print(f"- caption_mentions:   {post.caption_mentions}\n")
print(f"- comments:   {post.comments}\n")
print(f"- date_local:   {post.date_local}\n")
print(f"- is_sponsored:   {post.is_sponsored}\n")
print(f"- sponsor_users:   {post.sponsor_users}\n")
print(
    f"- text_content:   {post.caption
                    + (
                        "Tagged users:" + " @".join(post.tagged_users)
                        if post.tagged_users
                        else ""
                    )}"
)
