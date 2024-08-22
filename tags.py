import os
import yaml
from collections import defaultdict

def process_tags(posts_dir, output_file):
    tag_data = defaultdict(list)
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            with open(os.path.join(posts_dir, filename), 'r') as f:
                frontmatter = ''
                for line in f:
                    if line.strip() == '---':
                        if frontmatter:
                            break
                        frontmatter = '---\n'
                    else:
                        frontmatter += line
                
                post_data = yaml.safe_load(frontmatter)
                tags = post_data.get('tags', [])
                
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(',')]
                elif not isinstance(tags, list):
                    tags = [str(tags)]
                
                title = post_data.get('title', filename.replace('.md', ''))
                url = '/' + filename.replace('.md', '')
                
                for tag in tags:
                    if isinstance(tag, str):
                        tag_parts = tag.split('>')
                    else:
                        tag_parts = [str(tag)]
                    
                    for i in range(len(tag_parts)):
                        partial_tag = '>'.join(tag_parts[:i+1])
                        tag_data[partial_tag].append({'title': title, 'url': url})

    with open(output_file, 'w') as f:
        yaml.dump([{'tag': tag, 'posts': posts} for tag, posts in tag_data.items()], f)

if __name__ == '__main__':
    process_tags('_posts', '_data/processed_tags.yml')
