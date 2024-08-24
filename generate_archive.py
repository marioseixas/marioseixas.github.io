import yaml
import os
from datetime import datetime, date
# Load the processed tags from the YAML file
with open('_data/processed_tags.yml', 'r') as file:
    processed_tags = yaml.safe_load(file)
# Function to format the date
def format_date(date_obj, format_str='%Y-%m-%d'):
    return date_obj.strftime(format_str)
# Function to convert a value to a datetime object
def to_datetime(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            raise ValueError(f"Date string '{value}' is not in the correct format: {e}")
    elif isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    elif isinstance(value, datetime):
        return value
    else:
        raise ValueError(f"Unexpected date type: {type(value)}")
# Directory containing the posts
posts_directory = '_posts/'
# List to hold the post data
all_posts = []
# Read the post files and extract metadata
for post_file in os.listdir(posts_directory):
    if post_file.endswith('.md'):  # Only process Markdown files
        with open(os.path.join(posts_directory, post_file), 'r') as file:
            post_content = file.read()
            # Assuming the post's front matter is YAML at the top of the file
            try:
                post_meta = yaml.safe_load(post_content.split('---')[1])
                
                # Convert date fields to datetime objects
                if 'date' in post_meta:
                    post_meta['date'] = to_datetime(post_meta['date'])
                if 'last_modified_at' in post_meta:
                    post_meta['last_modified_at'] = to_datetime(post_meta['last_modified_at'])
                
                all_posts.append(post_meta)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {post_file}: {e}")
                continue
# Sort posts by date, considering both 'last_modified_at' and 'date'
all_sorted_posts = sorted(all_posts, key=lambda x: x.get('last_modified_at', x['date']), reverse=True)
# Function to generate HTML for the archive
def generate_archive_html(posts, tags):
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
        <a class="internal-link" href="/">
          <img src="/assets/Sudden_Death_Rune.gif" alt="Sudden Death Rune" class="favicon">
        </a>
        <a href="https://ib.bsb.br/archive">
          <img src="/favicon.ico" alt="Archive Icon" class="favicon">
        </a>
        <a href="https://ib.bsb.br/tags">
          <img src="/assets/Label.gif" alt="Tags Icon" class="favicon">
        </a>
        <a href="https://ib.bsb.br/events">
          <img src="/assets/Paralyse_Rune.gif" alt="Events Icon" class="favicon">
        </a>
      </div>
    </nav>
  </header>
  <div class="wrapper">
    <main class="tags-page">
      <img src="/assets/archive.webp" alt="archive" class="favicon">
      <section>
    '''
    for post in posts:
        post_url = post.get('permalink', post.get('url'))
        post_date = format_date(post.get('date'))
        post_title = post.get('title')
        post_last_modified = post.get('last_modified_at')
        # Find the tags for the current post
        post_tags = []
        for entry in tags:
            for p in entry['posts']:
                if p['url'] == post_url:
                    post_tags.append(entry['tag'])
        tags_str = f"[{', '.join(post_tags)}]" if post_tags else ''
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
            html_output += f'↣ {formatted_last_modified}'
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
with open('archive.html', 'w') as output_file:
    output_file.write(archive_html)
print("Archive HTML generated successfully!")
