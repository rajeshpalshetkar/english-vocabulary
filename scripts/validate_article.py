#!/usr/bin/env python3
import argparse,json,sys
from common import load_article,validation_errors,word_count,article_to_html
p=argparse.ArgumentParser(); p.add_argument("article"); args=p.parse_args()
a=load_article(args.article); errors=validation_errors(a)
if errors:
 print("VALIDATION FAILED"); print("\\n".join("- "+x for x in errors)); sys.exit(1)
print(json.dumps({"ok":True,"title":a["title"],"kind":a["kind"],"labels":a["labels"],"words":word_count(a["body_markdown"]),"html_chars":len(article_to_html(a))},ensure_ascii=False,indent=2))
