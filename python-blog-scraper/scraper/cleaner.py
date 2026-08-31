from datetime import datetime, timezone


REQUIRED_FIELDS = [
    "title",
    "author",
    "published_date",
    "url"
]


def clean_text(value):
    if not value:
        return None

    return " ".join(value.split())


def parse_date(value):
    if not value:
        return None

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def is_valid_post(post):
    for field in REQUIRED_FIELDS:
        if not post.get(field):
            return False

    return True


def remove_duplicates(posts):
    unique_posts = {}

    for post in posts:
        unique_posts[post["url"]] = post

    return list(unique_posts.values())

def get_scraped_at():
    return datetime.now(timezone.utc)
