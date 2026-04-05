"""
x-tweetcraft MCP Server

Minimal MCP server that wraps X (Twitter) API v2 via tweepy.
Exposes only the functions x-tweetcraft skills need:
- post_tweet        : Post a tweet (Free plan OK)
- get_my_tweets     : Fetch authenticated user's recent tweets (Free plan limited)
- get_tweet_metrics : Fetch metrics for a specific tweet (Basic plan recommended)
- search_trending   : Search recent tweets (Basic plan required)

Security note:
  This server reads credentials from ~/.x-tweetcraft.env (outside the repo).
  It only calls X API v2 endpoints — nothing else.
  The entire source is <150 lines and fully auditable by the user.

Docs reference:
  - tweepy: https://docs.tweepy.org/en/stable/client.html
  - X API v2: https://developer.x.com/en/docs/x-api

Status:
  ⚠️ Not yet tested against live X API by the plugin author.
  Use at your own risk. If something breaks, pair with Claude Code
  to debug/customize — the code is designed to be readable and fixable.
"""

import os
import sys
from pathlib import Path

try:
    import tweepy
    from dotenv import load_dotenv
    from fastmcp import FastMCP
except ImportError as e:
    print(
        f"Missing dependency: {e}\n"
        "Install with: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


# Load credentials from ~/.x-tweetcraft.env (user's home, NOT in repo)
env_path = Path.home() / ".x-tweetcraft.env"
if not env_path.exists():
    print(
        f"Credentials file not found: {env_path}\n"
        "Run x-connect-api skill to set up credentials first.",
        file=sys.stderr,
    )
    sys.exit(1)

load_dotenv(env_path)

# Initialize tweepy client with all 5 credential sets.
# Bearer token alone covers reads; consumer+access tokens enable posting.
# Reference: https://docs.tweepy.org/en/stable/client.html
_client = tweepy.Client(
    bearer_token=os.getenv("X_BEARER_TOKEN"),
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    wait_on_rate_limit=True,  # Sleeps on rate limit instead of raising
)


mcp = FastMCP(name="x-tweetcraft")


@mcp.tool
def post_tweet(text: str) -> dict:
    """Post a tweet to the authenticated user's X account.

    Args:
        text: Tweet body (max 280 chars, Japanese counts as 2 each)

    Returns:
        dict with 'id' (tweet ID) and 'text' (posted text)

    API ref: POST /2/tweets
    https://developer.x.com/en/docs/x-api/tweets/manage-tweets/api-reference/post-tweets
    tweepy ref: client.create_tweet(text=...)
    Plan: Free (1,500 posts/month) or above.
    """
    response = _client.create_tweet(text=text, user_auth=True)
    return {"id": response.data["id"], "text": text}


@mcp.tool
def get_my_tweets(count: int = 30) -> list[dict]:
    """Fetch the authenticated user's recent original tweets.

    Args:
        count: Number of tweets to fetch (max 100 per request)

    Returns:
        List of dicts with 'id', 'text', 'created_at', 'metrics'

    API ref: GET /2/users/:id/tweets
    https://developer.x.com/en/docs/x-api/tweets/timelines/api-reference/get-users-id-tweets
    tweepy ref: client.get_users_tweets(id=..., max_results=...)
    Plan: Free allows ~100 reads/month (very limited). Basic recommended.
    """
    # Get own user ID first
    me = _client.get_me(user_auth=True)
    user_id = me.data.id

    # Fetch tweets with public_metrics (likes, retweets, etc.)
    response = _client.get_users_tweets(
        id=user_id,
        max_results=min(count, 100),
        tweet_fields=["created_at", "public_metrics"],
        exclude=["retweets", "replies"],  # Original posts only
        user_auth=True,
    )

    if not response.data:
        return []

    return [
        {
            "id": t.id,
            "text": t.text,
            "created_at": str(t.created_at),
            "metrics": t.public_metrics,
        }
        for t in response.data
    ]


@mcp.tool
def get_tweet_metrics(tweet_id: str) -> dict:
    """Fetch engagement metrics for a specific tweet.

    Args:
        tweet_id: Tweet ID (as string)

    Returns:
        dict with metrics (retweet_count, reply_count, like_count,
        quote_count, bookmark_count, impression_count)

    API ref: GET /2/tweets/:id
    https://developer.x.com/en/docs/x-api/tweets/lookup/api-reference/get-tweets-id
    tweepy ref: client.get_tweet(id=..., tweet_fields=["public_metrics"])
    Plan: Free gets basic metrics. Impressions require Basic+.
    """
    response = _client.get_tweet(
        id=tweet_id,
        tweet_fields=["public_metrics"],
        user_auth=True,
    )
    if not response.data:
        return {}
    return response.data.public_metrics


@mcp.tool
def search_trending(query: str, count: int = 20) -> list[dict]:
    """Search recent tweets matching the query (last 7 days).

    Args:
        query: Search query (X search operator syntax)
        count: Max number of results (10-100)

    Returns:
        List of dicts with 'id', 'text', 'author_id', 'created_at', 'metrics'

    API ref: GET /2/tweets/search/recent
    https://developer.x.com/en/docs/x-api/tweets/search/api-reference/get-tweets-search-recent
    tweepy ref: client.search_recent_tweets(query=..., max_results=...)
    Plan: **Basic plan ($200/month) required**. Not available on Free.
    """
    response = _client.search_recent_tweets(
        query=query,
        max_results=min(max(count, 10), 100),
        tweet_fields=["created_at", "public_metrics", "author_id"],
    )

    if not response.data:
        return []

    return [
        {
            "id": t.id,
            "text": t.text,
            "author_id": t.author_id,
            "created_at": str(t.created_at),
            "metrics": t.public_metrics,
        }
        for t in response.data
    ]


if __name__ == "__main__":
    # Start the MCP server over stdio (standard for Claude Code plugins)
    mcp.run()
