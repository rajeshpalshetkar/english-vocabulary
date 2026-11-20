#!/usr/bin/env python3
import argparse, json, os, re, sys
from common import load_article, validation_errors, article_to_html
from blogger_client import service, blog_id

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("article")
    args=parser.parse_args()
    article=load_article(args.article)
    errors=validation_errors(article)
    if errors:
        print("VALIDATION FAILED:\n- "+"\n- ".join(errors),file=sys.stderr)
        sys.exit(1)

    mode=os.getenv("PUBLISH_MODE","draft").strip().lower()
    if mode not in {"draft","live"}:
        raise SystemExit("PUBLISH_MODE must be either draft or live.")

    api=service()
    title=article["title"]
    slug=article["slug"]
    kind=article["kind"]

    # Duplicate guard: Blogger API has no slug uniqueness guarantee.
    if kind=="post":
        existing=api.posts().list(blogId=blog_id(),fetchBodies=False,maxResults=500).execute().get("items",[])
        for item in existing:
            if item.get("title","").strip().casefold()==title.strip().casefold():
                raise SystemExit(f"Duplicate title already exists in Blogger (post ID {item.get('id')}). Refusing to create another.")
        body={"kind":"blogger#post","title":title,"content":article_to_html(article),"labels":article.get("labels",[])}
        result=api.posts().insert(blogId=blog_id(),body=body,isDraft=(mode=="draft")).execute()
        if mode=="live":
            result=api.posts().publish(blogId=blog_id(),postId=result["id"]).execute()
    else:
        existing=api.pages().list(blogId=blog_id()).execute().get("items",[])
        for item in existing:
            if item.get("title","").strip().casefold()==title.strip().casefold():
                raise SystemExit(f"Duplicate page title already exists (page ID {item.get('id')}). Refusing to create another.")
        body={"kind":"blogger#page","title":title,"content":article_to_html(article)}
        result=api.pages().insert(blogId=blog_id(),body=body,isDraft=(mode=="draft")).execute()
        if mode=="live":
            result=api.pages().publish(blogId=blog_id(),pageId=result["id"]).execute()

    print(json.dumps({"status":"PUBLISHED" if mode=="live" else "DRAFT_CREATED","kind":kind,
        "id":result.get("id"),"title":result.get("title"),"url":result.get("url"),
        "labels":article.get("labels",[]),"mode":mode},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
