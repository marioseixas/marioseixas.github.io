import os
import yaml
from collections import defaultdict
from datetime import datetime

def extract_frontmatter(file_content):
    frontmatter = ""
    content_lines = file_content.split('\n')
    if content_lines[0].strip() == '---':
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == '---':
                frontmatter = '\n'.join(content_lines[1:i])
                break
    return frontmatter

def process_tags(posts_dir, output_file):
    tag_data = defaultdict(list)
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            frontmatter = extract_frontmatter(file_content)
            if not frontmatter:
                print(f"Warning: No frontmatter found in {filename}")
                continue
            
            try:
                post_data = yaml.safe_load(frontmatter)
            except yaml.YAMLError as e:
                print(f"Error parsing frontmatter in {filename}: {e}")
                continue
            
            tags = post_data.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',')]
            elif not isinstance(tags, list):
                tags = [str(tags)]
            
            title = post_data.get('title', os.path.splitext(filename)[0])
            
            # Extract the slug (remove date and file extension)
            url = '/' + '-'.join(filename.split('-')[3:]).replace('.md', '')
            
            # Extract post date for sorting
            try:
                post_date = datetime.strptime('-'.join(filename.split('-')[:3]), '%Y-%m-%d')
            except ValueError:
                print(f"Warning: Unable to parse date from filename {filename}")
                post_date = datetime.min
            
            for tag in tags:
                if isinstance(tag, str):
                    tag_parts = tag.split('>')
                else:
                    tag_parts = [str(tag)]
                
                for i in range(len(tag_parts)):
                    partial_tag = '>'.join(tag_parts[:i+1])
                    tag_data[partial_tag].append({
                        'title': title,
                        'url': url,
                        'date': post_date
                    })

    # Sort posts within each tag by date, most recent first
    for tag, posts in tag_data.items():
        tag_data[tag] = sorted(posts, key=lambda x: x['date'], reverse=True)
        # Remove date from final output
        for post in tag_data[tag]:
            del post['date']

    # Sort tags alphabetically
    sorted_tag_data = sorted(tag_data.items())

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump([{'tag': tag, 'posts': posts} for tag, posts in sorted_tag_data], f, allow_unicode=True)

if __name__ == '__main__':
    process_tags('_posts', '_data/processed_tags.yml')
