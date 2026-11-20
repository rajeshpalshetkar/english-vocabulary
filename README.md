# English Fluency Guide — JSON-First Static Learning Portal

GitHub JSON is the content source of truth. GitHub Actions builds a fast static website with a separate HTML URL for every completed lesson. Blogger is not required to store 237 separate lesson posts.

## Content structure
- `content/data/content-catalog.json`: 16 topic labels, 155 core topics, 30 challenge days and 52 weekly practice topics.
- `content/lessons/`: one complete JSON file per finished lesson. Use `lesson-template.json` as a schema reference; do not edit it as a lesson.
- `content/data/portal-index.json`: catalogue navigation configuration.
- `prompts/MASTER-CONTENT-PROMPT.md`: prompt for creating each lesson JSON.
- `scripts/build_site.py`: renders lesson HTML, topic pages, challenge pages, sitemap and robots.txt.
- `.github/workflows/deploy-pages.yml`: builds and deploys the site to GitHub Pages.

## Add a lesson
1. Use the master prompt to create one complete JSON lesson.
2. Review the accuracy, examples, exercises, answers, originality and sources.
3. Save it as `content/lessons/<unique-slug>.json`. Do not overwrite `lesson-template.json`.
4. Commit and push to `main`. GitHub Actions automatically builds and deploys the site.
5. The lesson URL will be `https://vocab.prasiddhbharat.com/lessons/<unique-slug>/`.

## First-time GitHub Pages setup
1. Open repository Settings → Pages.
2. Set Build and deployment source to **GitHub Actions**.
3. Ensure the repository Actions are enabled.
4. Add DNS record at your DNS provider: CNAME `vocab` → `rajeshpalshetkar.github.io` (DNS Only while configuring).
5. After Pages deployment recognizes the custom domain and HTTPS certificate is provisioned, enable Enforce HTTPS.

The build writes a CNAME file for `vocab.prasiddhbharat.com`.

## SEO and quality
Each completed lesson gets a unique static HTML URL, title, meta description and canonical URL. The sitemap is generated on each build. Catalogue topics without full lesson JSON are shown as planned, not linked to missing lesson URLs. A topic appearing in the 237-item plan is not yet a published article until its full JSON lesson has been added.

The content validator/build process cannot guarantee accuracy, originality, search ranking or AdSense approval. Review every lesson before publishing.

## Blogger
Blogger can remain the main brand/blog or host a portal landing page, but the full lesson pages in this architecture are deployed from GitHub Pages. The optional Blogger catalogue loader is at `portal/blogger-catalogue-loader.html`.
