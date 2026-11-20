#!/usr/bin/env python3
import argparse,json,sys
from common import load_article,validation_errors,article_to_html
from blogger_client import service,blog_id
p=argparse.ArgumentParser(); p.add_argument("article"); args=p.parse_args()
a=load_article(args.article); errors=validation_errors(a)
if errors: print("\\n".join(errors),file=sys.stderr); sys.exit(1)
api=service()
if a["kind"]=="page":
 result=api.pages().insert(blogId=blog_id(),body={"kind":"blogger#page","title":a["title"],"content":article_to_html(a)},isDraft=True).execute()
else:
 body={"kind":"blogger#post","title":a["title"],"content":article_to_html(a),"labels":a.get("labels",[])}
 result=api.posts().insert(blogId=blog_id(),body=body,isDraft=True).execute()
print(json.dumps({"status":"DRAFT_CREATED","id":result.get("id"),"title":result.get("title"),"url":result.get("url"),"kind":a["kind"]},ensure_ascii=False,indent=2))
