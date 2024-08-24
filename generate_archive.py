import yaml
import os
from datetime import datetime, date
# Load the processed tags from the YAML file
with open('_data/processed_tags.yml', 'r', encoding='utf-8') as file:
    processed_tags = yaml.safe_load(file)
def format_date(date_obj, format_str='%Y-%m-%d'):
    """Format a date object to a string."""
    return date_obj.strftime(format_str)
def to_datetime(value):
    """Convert various date formats to datetime object."""
    if isinstance(value, str):
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            # Handle potential alternative date formats
            date_formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S%z']
            for fmt in date_formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Unable to parse date string: {value}")
    elif isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    elif isinstance(value, datetime):
        return value
    else:
        raise ValueError(f"Unexpected date type: {type(value)}")
def process_post_file(file_path):
    """Process a single post file and return its metadata."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        try:
            # Extract YAML front matter
            _, front_matter, _ = content.split('---', 2)
            post_meta = yaml.safe_load(front_matter)
            
            # Convert date fields to datetime objects
            for date_field in ['date', 'last_modified_at']:
                if date_field in post_meta:
                    post_meta[date_field] = to_datetime(post_meta[date_field])
            
            return post_meta
        except (yaml.YAMLError, ValueError) as e:
            print(f"Error processing file {file_path}: {e}")
            return None
# Process all post files
posts_directory = '_posts/'
all_posts = []
for post_file in os.listdir(posts_directory):
    if post_file.endswith('.md'):
        post_meta = process_post_file(os.path.join(posts_directory, post_file))
        if post_meta:
            all_posts.append(post_meta)
# Sort posts by date (newest first), considering both date and last_modified_at
all_sorted_posts = sorted(all_posts, key=lambda x: x.get('last_modified_at', x['date']), reverse=True)
def generate_archive_html(posts, tags):
    """Generate the HTML for the archive page."""
    html_output = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>archive — infoBAG</title>
    <link rel="canonical" href="https://ib.bsb.br/archive.html">
    <link rel="alternate" type="application/rss+xml" title="infoBAG" href="/rss.xml">
    <meta property="og:site_name" content="infoBAG">
    <meta property="og:title" content="archive">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://ib.bsb.br/archive.html">
    <link href="/style.css" rel="stylesheet">
    <link href="/pagefind/pagefind-ui.css" rel="stylesheet">
    <script src="/pagefind/pagefind-ui.js"></script>
    <script type="module">
        import PagefindHighlight from '/pagefind/pagefind-highlight.js';
        new PagefindHighlight({ highlightParam: "highlight" });
    </script>
    <script src="/assets/js/search.js" defer></script>
</head>
<body>
    <a class="search-input-block" id="search"></a>
    <header>
        <nav aria-label="Main navigation">
            <div class="header-container">
                <a class="internal-link" href="/"><img src="/assets/Sudden_Death_Rune.gif" alt="Sudden Death Rune" class="favicon"></a>
                <a href="https://ib.bsb.br/archive"><img src="/favicon.ico" alt="Archive Icon" class="favicon"></a>
                <a href="https://ib.bsb.br/tags"><img src="/assets/Label.gif" alt="Tags Icon" class="favicon"></a>
                <a href="https://ib.bsb.br/events"><img src="/assets/Paralyse_Rune.gif" alt="Events Icon" class="favicon"></a>
            </div>
        </nav>
    </header>
    <div class="wrapper">
        <main class="tags-page">
            <img src="/assets/archive.webp" alt="archive" class="favicon">
            <section>
    '''
    
    for post in posts:
        post_url = post.get('permalink') or post.get('url', '#')
        post_date = format_date(post['date'])
        post_title = post.get('title', 'Untitled')
        post_last_modified = post.get('last_modified_at')
        post_tags = [entry['tag'] for entry in tags if any(p['url'] == post_url for p in entry['posts'])]
        tags_str = f"[{', '.join(post_tags)}]" if post_tags else ''
        html_output += f'''
            <article>
                <time datetime="{post_date}" class="post-date">
                    <img src="/assets/gold.ico" alt="gold icon">
                    {tags_str}
                    <h3>{post_date}'''
        
        if post_last_modified and post_last_modified != post['date']:
            formatted_last_modified = format_date(post_last_modified)
            html_output += f' ↣ {formatted_last_modified}'
        
        html_output += f'''
                    </h3>
                    <h2><a href="{post_url}">{post_title}</a></h2>
                </time>
            </article>
        '''
    
    html_output += '''
            </section>
        </main>
    </div>
</body>
</html>
    '''
    return html_output
# Generate the HTML for the archive
archive_html = generate_archive_html(all_sorted_posts, processed_tags)
# Output the generated HTML
with open('archive.html', 'w', encoding='utf-8') as output_file:
    output_file.write(archive_html)
print("Archive HTML generated successfully!")
