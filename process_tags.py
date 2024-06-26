import os
import yaml
import glob
from collections import defaultdict

def get_posts():
    posts = []
    for filename in glob.glob('_posts/*.md'):
        with open(filename, 'r') as file:
            content = file.read()
            front_matter, _ = content.split('---', 2)[1:]
            post = yaml.safe_load(front_matter)
            post['filename'] = filename
            posts.append(post)
    return posts

def generate_tag_pages(posts):
    tags = defaultdict(list)
    for post in posts:
        for tag in post.get('tags', []):
            tags[tag].append(post)

    if not os.path.exists('tags'):
        os.makedirs('tags')

    for tag, posts in tags.items():
        with open(f'tags/{tag}.html', 'w') as file:
            file.write(f'---\nlayout: tag\ntag: {tag}\n---\n')
            for post in posts:
                file.write(f'- [{post["title"]}]({post["slug"]})\n')

def main():
    posts = get_posts()
    generate_tag_pages(posts)

if __name__ == '__main__':
    main()
