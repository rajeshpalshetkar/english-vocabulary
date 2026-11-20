# Blogger Portal Pages backed by GitHub JSON

JSON source:
- `content/data/content-catalog.json`: 16 labels, core lesson titles, challenge days and weekly practice titles.
- `content/data/portal-index.json`: route and track map.

## Recommended Blogger implementation

Keep Blogger pages as stable, indexable landing pages:
- `/p/learning-library.html`
- `/p/30-day-challenge.html`
- `/p/365-day-practice.html`
- topic landing pages (Grammar, Vocabulary, Speaking Practice, etc.).

The JavaScript loader fetches GitHub Raw JSON, builds accessible cards, and links each lesson to a stable slug route. Do not publish 237 thin Blogger pages simply to host title-only JSON.

Important SEO limitation: a JavaScript-only viewer which fetches lesson data after page load may not provide the same indexing reliability as server-rendered HTML. For each lesson expected to rank in Google, use a separately rendered Blogger post/page or a static HTML page with a unique canonical URL, title, meta description and full lesson body. The JSON remains the editorial source of truth; GitHub Actions can build/publish SEO HTML from it.

## Blogger page loader

Use `portal/blogger-catalogue-loader.html` as the common loader snippet. Set its `data-view` value to `library`, `challenge30`, `practice365`, or a canonical label slug such as `Grammar`.
