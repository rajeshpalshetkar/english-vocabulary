# English Fluency Guide — Blogger Content Engine

This repository turns ChatGPT-authored JSON lessons into Blogger content using GitHub Actions.

## Automatic publishing mode

When a reviewed article JSON is committed to `content/inbox/`, GitHub Actions:
1. validates schema, canonical labels, SEO fields, and minimum content length;
2. converts Markdown to safe HTML;
3. publishes to Blogger as **LIVE** when repository variable `PUBLISH_MODE=live`, or as a draft when `PUBLISH_MODE=draft`.

The repository should start with `PUBLISH_MODE=draft` for a test. After Blogger OAuth is configured and a test succeeds, change it to `live` to enable automatic live publishing after each committed article.

> Automation cannot verify educational correctness, rights to media, originality or AdSense compliance. Review every article before committing it. Do not submit bulk AI-generated thin or repetitive content.

## Connect Blogger

1. In Google Cloud Console enable **Blogger API v3**.
2. Create an OAuth client of type **Desktop app**.
3. Download the client file as `client_secret.json` in a trusted local copy.
4. Run:
   ```bash
   python -m pip install -r requirements.txt
   python scripts/oauth_setup.py
   ```
5. Add repository Actions secrets:
   - `BLOGGER_CLIENT_ID`
   - `BLOGGER_CLIENT_SECRET`
   - `BLOGGER_REFRESH_TOKEN`
   - `BLOGGER_BLOG_ID`
6. Set repository variable `PUBLISH_MODE` to `draft` for initial test; switch to `live` when ready.

Never commit OAuth secrets or refresh tokens.

## Workflow: prompt to Blogger

1. Give ChatGPT the prompt from `prompts/MASTER-CONTENT-PROMPT.md`.
2. Ask it for one complete JSON file following `content/templates/article-template.json`.
3. Save the JSON under `content/inbox/` with a unique filename.
4. Commit and push. The workflow publishes according to `PUBLISH_MODE`.

## Pages

Use `kind: "page"` for static Blogger pages. The same validation and publishing mode apply.

## Plan

`content/plan/content-plan.json` contains 16 canonical labels, 155 core posts, 30 challenge lessons and 52 weekly practice lessons (237 planned items).

## Required review

The JSON must have `author_reviewed: true` only after a human has checked accuracy, usefulness, grammar, originality and media rights. The validator cannot perform this review for you.
