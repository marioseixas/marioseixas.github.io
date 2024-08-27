import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
    """Generates all partial tags for a given tag."""
    parts = tag.split(">")
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append(">".join(parts[j : j + i]))
    return partial_tags


def process_tags(posts_dir, output_file):
    """
    Processes tags from markdown files, handling nested tags, highlighting exact matches,
    preventing duplicates using file paths, and generating a Mermaid graph.
    """

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
            {"title": title, "url": url, "date": post_date, "tags": tags}
        )

    # Second pass: Generate tag data based on frequency threshold
    tag_data = defaultdict(
        lambda: {"parents": set(), "children": set(), "related": set(), "posts": []}
    )
    combined_tags = set()  # Keep track of combined tags

    for post in all_posts:
        for tag in post["tags"]:
            tag_parts = tag.split(">")
            full_tag_path = tag

            # Detect combined tags and store relationships
            if len(tag_parts) > 1:
                combined_tags.add(tag)
                for i in range(len(tag_parts) - 1):
                    tag_data[tag]["parents"].add(tag_parts[i])
                    tag_data[tag_parts[i]]["children"].add(tag)

            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= THRESHOLD:
                    post_entry = {
                        "title": post["title"],
                        "url": post["url"],
                        "highlighted": partial_tag == tag,
                        "date": post["date"],
                    }
                    tag_data[partial_tag]["posts"].append(post_entry)

            # Establish parent-child relationships
            for i in range(1, len(tag_parts)):
                parent_tag = ">".join(tag_parts[:i])
                child_tag = ">".join(tag_parts[: i + 1])
                if (
                    tag_frequency[parent_tag] >= THRESHOLD
                    and tag_frequency[child_tag] >= THRESHOLD
                ):
                    tag_data[child_tag]["parents"].add(parent_tag)
                    tag_data[parent_tag]["children"].add(child_tag)

            # Track non-hierarchical (related) relationships between tags
            for other_tag in post["tags"]:
                if (
                    other_tag != tag
                    and tag_frequency[other_tag] >= THRESHOLD
                    and tag_frequency[full_tag_path] >= THRESHOLD
                    and other_tag not in tag_data[full_tag_path]['parents'] # Ensure no hierarchical relation
                    and other_tag not in tag_data[full_tag_path]['children'] # Ensure no hierarchical relation
                ):
                    tag_data[full_tag_path]["related"].add(other_tag)
                    tag_data[other_tag]["related"].add(full_tag_path)

    # Remove tags with no posts
    tag_data = {tag: data for tag, data in tag_data.items() if data["posts"]}

    # Clean up relationships
    for tag, data in tag_data.items():
        data["parents"] = {parent for parent in data["parents"] if parent in tag_data}
        data["children"] = {child for child in data["children"] if child in tag_data}
        data["related"] = {related for related in data["related"] if related in tag_data}

    # Sort posts within each tag by date (most recent first)
    for tag, data in tag_data.items():
        data["posts"] = sorted(
            data["posts"], key=lambda x: x.get("date", datetime.min), reverse=True
        )

    # Sort tags alphabetically before writing to YAML
    sorted_tag_data = sorted(tag_data.items())

    # Write the processed tags to a YAML file
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            [{"tag": tag, "posts": data["posts"]} for tag, data in sorted_tag_data],
            f,
            allow_unicode=True,
        )

    logging.info(f"Processed tags have been written to {output_file}")

    return tag_data, combined_tags


def generate_mermaid_graph(tag_data, combined_tags):
    """Generates Mermaid graph code for the tag structure."""
    graph = "graph TD\n"
    added_edges = set()  # Keep track of added edges to avoid duplicates

    # Add main nodes with styling
    main_nodes = ["software", "cloud", "mobile", "script", "google-apps-script"]
    for node in main_nodes:
        graph += f'{node.replace("-", "_")}((("{node}")))\n' # Using triple parentheses for main nodes

    # Add combined tags with styling
    for tag in combined_tags:
        safe_tag_name = tag.replace(">", "_").replace("#", "")
        graph += f'{safe_tag_name}[["{tag}"]]\n' # Using double square brackets for combined nodes

    # Add hierarchical relationships
    for tag_name, data in tag_data.items():
        safe_tag_name = tag_name.replace(">", "_").replace("#", "")
        for child in data["children"]:
            safe_child_name = child.replace(">", "_").replace("#", "")
            edge = (safe_tag_name, safe_child_name)
            if edge not in added_edges:
                graph += f"{safe_tag_name} --> {safe_child_name}\n"
                added_edges.add(edge)

    # Add non-hierarchical relationships (related tags) with dotted lines and labels
    for tag_name, data in tag_data.items():
        safe_tag_name = tag_name.replace(">", "_").replace("#", "")
        for related in data["related"]:
            safe_related_name = related.replace(">", "_").replace("#", "")
            edge1 = (safe_tag_name, safe_related_name)
            edge2 = (safe_related_name, safe_tag_name)
            if edge1 not in added_edges and edge2 not in added_edges:
                graph += f'{safe_tag_name} -.->|related| {safe_related_name}\n' # Added label "related"
                added_edges.add(edge1)
                added_edges.add(edge2)


    # Add cross-linking between combined tags (dashed lines)
    for tag in combined_tags:
        tag_parts = tag.split(">")
        for i in range(len(tag_parts) - 1):
            for j in range(i + 1, len(tag_parts)):
                source = ">".join(tag_parts[: i + 1]).replace(">", "_").replace("#", "")
                target = ">".join(tag_parts[: j + 1]).replace(">", "_").replace("#", "")
                edge = (source, target)
                if edge not in added_edges:
                    graph += f"{source} -...- {target}\n"  # Using dashed lines for cross-linking
                    added_edges.add(edge)

    # Add styling definitions
    graph += "\nclassDef mainNode fill:#f9f,stroke:#333,stroke-width:4px;\n"
    graph += "classDef combinedNode fill:#ccf,stroke:#33f,stroke-width:2px;\n"
    graph += f'class {", ".join(main_nodes).replace("-", "_")} mainNode;\n'  # Apply mainNode style
    graph += f'class {", ".join(combined_tags).replace(">", "_").replace("#", "")} combinedNode;\n'  # Apply combinedNode style

    return graph

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
