import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Threshold for generating permutations
THRESHOLD = 0  # Adjust this value as needed


def extract_frontmatter(file_content):
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ""
    content_lines = file_content.split("\n")
    if content_lines[0].strip() == "---":
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == "---":
                frontmatter = "\n".join(content_lines[1:i])
                break
    return frontmatter


def generate_partial_tags(tag):
    """
    Generates all partial tags for a given tag, including the tag itself.
    For example, "a>b>c" will generate ["a", "a>b", "a>b>c"].
    """
    parts = tag.split(">")
    partial_tags = []
    for i in range(1, len(parts) + 1):
        partial_tags.append(">".join(parts[:i]))
    return partial_tags


def process_tags(posts_dir, output_file):
    """Processes tags from markdown files and generates a tag relationship map."""

    tag_frequency = defaultdict(int)
    all_posts = []
    seen_posts = set()

    logging.info(f"Processing markdown files in directory: {posts_dir}")

    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(posts_dir, filename)
        if file_path in seen_posts:
            logging.warning(f"Skipping duplicate post: {filename}")
            continue
        seen_posts.add(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        frontmatter = extract_frontmatter(file_content)
        if not frontmatter:
            logging.warning(f"No frontmatter found in {filename}")
            continue

        try:
            post_data = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            logging.error(f"Error parsing frontmatter in {filename}: {e}")
            continue

        tags = post_data.get("tags", [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",")]
        elif not isinstance(tags, list):
            tags = [str(tags)]

        # Count tag frequencies including partial tags
        for tag in tags:
            for partial_tag in generate_partial_tags(tag):
                tag_frequency[partial_tag] += 1

        title = post_data.get("title", os.path.splitext(filename)[0])
        url = "/" + "-".join(filename.split("-")[3:]).replace(".md", "")

        try:
            post_date = datetime.strptime("-".join(filename.split("-")[:3]), "%Y-%m-%d")
        except ValueError:
            logging.warning(f"Unable to parse date from filename {filename}")
            post_date = datetime.min

        all_posts.append(
            {
                "title": title,
                "url": url,
                "date": post_date,
                "tags": tags,
            }
        )

    tag_data = defaultdict(lambda: {"children": set(), "related": set(), "posts": []})
    combined_tags = set()

    for post in all_posts:
        for tag in post["tags"]:
            tag_parts = tag.split(">")

            # Add combined tags and their relationships
            if len(tag_parts) > 1:
                combined_tags.add(tag)
                for i in range(len(tag_parts) - 1):
                    parent = ">".join(tag_parts[: i + 1])
                    child = ">".join(tag_parts[: i + 2])
                    tag_data[parent]["children"].add(child)

            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= THRESHOLD:
                    post_entry = {
                        "title": post["title"],
                        "url": post["url"],
                        "highlighted": partial_tag == tag,  # Highlight if it's the full tag
                        "date": post["date"],
                    }
                    tag_data[partial_tag]["posts"].append(post_entry)

            # Add relationships between combined tags and their parts
            for i in range(1, len(tag_parts)):
                for j in range(i + 1, len(tag_parts)):
                    tag1 = ">".join(tag_parts[:i])
                    tag2 = ">".join(tag_parts[:j])
                    if tag1 != tag2:
                        tag_data[tag1]["related"].add(tag2)
                        tag_data[tag2]["related"].add(tag1)

    # Remove tags with no posts
    tag_data = {tag: data for tag, data in tag_data.items() if data["posts"]}

    # Sort posts within each tag by date (most recent first)
    for tag, data in tag_data.items():
        data["posts"] = sorted(
            data["posts"], key=lambda x: x.get("date", datetime.min), reverse=True
        )

    # Write the processed tags to a YAML file
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            [{"tag": tag, "posts": data["posts"]} for tag, data in sorted(tag_data.items())],
            f,
            allow_unicode=True,
        )

    logging.info(f"Processed tags have been written to {output_file}")

    return tag_data, combined_tags


def generate_mermaid_graph(tag_data, combined_tags):
    """Generates Mermaid graph code for the tag structure."""
    graph = "graph TD\n"
    added_edges = set()  # Keep track of added edges to avoid duplicates

    def add_node(tag):
        safe_tag = tag.replace(">", "_").replace("#", "")
        graph.append(f'{safe_tag}("{tag}")')

    def add_edge(source, target, style):
        edge = (source, target, style)
        if edge not in added_edges:
            graph.append(f"{source} {style} {target}")
            added_edges.add(edge)

    # Add hierarchical edges first
    for tag, data in tag_data.items():
        safe_tag = tag.replace(">", "_").replace("#", "")
        add_node(tag)  # Add the node itself

        for child in data["children"]:
            safe_child = child.replace(">", "_").replace("#", "")
            add_edge(safe_tag, safe_child, "-->")

    # Add non-hierarchical (related) edges
    for tag, data in tag_data.items():
        safe_tag = tag.replace(">", "_").replace("#", "")
        for related in data["related"]:
            safe_related = related.replace(">", "_").replace("#", "")
            add_edge(safe_tag, safe_related, "---")

    # Add cross-links for combined tags with dashed lines
    for tag in combined_tags:
        tag_parts = tag.split(">")
        for i in range(len(tag_parts) - 1):
            for j in range(i + 1, len(tag_parts)):
                source = ">".join(tag_parts[: i + 1]).replace(">", "_").replace("#", "")
                target = ">".join(tag_parts[: j + 1]).replace(">", "_").replace("#", "")
                add_edge(source, target, "-...-")

    return "\n".join(graph)


if __name__ == "__main__":
    # Use environment variables to determine paths (adapt if necessary)
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml")

    tag_data, combined_tags = process_tags(posts_dir, output_file)
    mermaid_graph = generate_mermaid_graph(tag_data, combined_tags)

    # Write the Mermaid graph to a file
    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
