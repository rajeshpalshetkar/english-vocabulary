#!/usr/bin/env python3
import argparse,json
from blogger_client import service,blog_id
p=argparse.ArgumentParser(); p.add_argument("--post-id",required=True); p.add_argument("--confirm",required=True); a=p.parse_args()
if a.confirm!="PUBLISH": raise SystemExit("Confirmation must be exactly PUBLISH")
api=service()
draft=api.posts().get(blogId=blog_id(),postId=a.post_id).execute()
if draft.get("status")!="DRAFT": raise SystemExit("Refusing: selected item is not a Blogger DRAFT")
out=api.posts().publish(blogId=blog_id(),postId=a.post_id).execute()
print(json.dumps({"status":"PUBLISHED","id":out.get("id"),"title":out.get("title"),"url":out.get("url")},ensure_ascii=False,indent=2))
