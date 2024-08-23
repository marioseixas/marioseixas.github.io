import yaml
import os
from datetime import datetime

# Load the processed tags from the YAML file
with open('_data/processed_tags.yml', 'r') as file:
    processed_tags = yaml.safe_load(file)

# Function to format the date
def format_date(date_str, format_str='%Y-%m-%d'):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime(format_str)

# Directory containing the posts
posts_directory = '_posts/'

# List to hold the post data
all_posts = []

# Read the post files and extract metadata
for post_file in os.listdir(posts_directory):
    with open(os.path.join(posts_directory, post_file), 'r') as file:
        post_content = file.read()
        # Assuming the post's front matter is YAML at the top of the file
        post_meta = yaml.safe_load(post_content.split('---')[1])
        all_posts.append(post_meta)

# Sort posts by date (newest first)
all_sorted_posts = sorted(all_posts, key=lambda x: x['date'], reverse=True)

# Function to generate HTML for the archive
def generate_archive_html(posts, tags):
    html_output = ''
    for post in posts:
        post_url = post.get('url')
        post_date = format_date(post.get('date'))
        post_title = post.get('title')
        post_last_modified = post.get('last_modified_at')

        # Find the tags for the current post
        post_tags = []
        for entry in tags:
            if post_url in entry['posts']:
                post_tags.append(entry['tag'])

        # Format the tags
        if post_tags:
            tags_str = f"[{', '.join(post_tags)}]"
        else:
            tags_str = ''

        # Generate the HTML for the post
        html_output += f'''
        <article>
            <time datetime="{post_date}" class="post-date">
                <img src="/assets/gold.ico" alt="gold icon">
                {tags_str}
                <h3>{post_date}
        '''
        if post_last_modified and post_last_modified != post.get('date'):
            formatted_last_modified = format_date(post_last_modified)
            html_output += f'&rightarrowtail; {formatted_last_modified}'

        html_output += f'''
                </h3>
                <h2><a href="{post_url}">{post_title}</a></h2>
            </time>
        </article>
        '''
    return html_output

# Generate the HTML for the archive
archive_html = generate_archive_html(all_sorted_posts, processed_tags)

# Output the generated HTML (you can save this to a file or directly to the console)
with open('archive.html', 'w') as output_file:
    output_file.write(archive_html)

print("Archive HTML generated successfully!")
