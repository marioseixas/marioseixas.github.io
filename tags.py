import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Threshold for generating permutations
THRESHOLD = 0  # Adjust this value as needed


def extract_frontmatter(file_content: str) -> str:
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ""
    content_lines = file_content.split("\n")
    if content_lines[0].strip() == "---":
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == "---":
                frontmatter = "\n".join(content_lines[1:i])
                break
    return frontmatter


def generate_partial_tags(tag: str) -> List[str]:
    """Generates all partial tags for a given tag."""
    parts = tag.split(">")
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append(">".join(parts[j: j + i]))
    return partial_tags


def process_tags(posts_dir: str, output_file: str) -> tuple:
    """
    Processes tags from markdown files, handling nested tags, highlighting exact matches,
    preventing duplicates using file paths, and generating a Mermaid graph.
    """

    tag_frequency = defaultdict(int)
    all_posts = []
    seen_posts = set()
    tag_cooccurrences = defaultdict(lambda: defaultdict(int))

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

        # Count tag co-occurrences
        for i, tag1 in enumerate(tags):
            for tag2 in tags[i + 1 :]:
                tag_cooccurrences[tag1][tag2] += 1
                tag_cooccurrences[tag2][tag1] += 1

        title = post_data.get("title", os.path.splitext(filename)[0])
        url = "/" + "-".join(filename.split("-")[3:]).replace(".md", "")

        try:
            post_date = datetime.strptime("-".join(filename.split("-")[:3]), "%Y-%m-%d")
        except ValueError:
            logging.warning(f"Unable to parse date from filename {filename}")
            post_date = datetime.min

        all_posts.append({"title": title, "url": url, "date": post_date, "tags": tags})

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
                child_tag = ">".join(tag_parts[:i + 1])
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
                    and other_tag not in tag_data[full_tag_path]["parents"]
                    # Ensure no hierarchical relation
                    and other_tag not in tag_data[full_tag_path]["children"]
                    # Ensure no hierarchical relation
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

    return tag_data, combined_tags, tag_cooccurrences


def generate_mermaid_graph(
    tag_data: Union[List[Dict[str, Any]], Dict[str, Any]],
    tag_cooccurrences: Dict[str, Dict[str, int]],
    direction: str = "TD",
) -> str:
    """
    Generates Mermaid ER diagram code for the tag structure,
    including parent, child, SUPERset, and SUBset relationships.

    Args:
        tag_data (Union[List[Dict[str, Any]], Dict[str, Any]]):
            List of dictionaries or dictionary containing tag relationships.
        tag_cooccurrences (Dict[str, Dict[str, int]]):
            Dictionary of tag co-occurrences.
        direction (str): Graph direction (TD, LR, RL, BT). Defaults to "TD".

    Returns:
        str: Mermaid ER diagram code.
    """

    graph = [f"erDiagram"]
    added_nodes = set()
    added_edges = set()

    def add_node(tag: str) -> str:
        """
        Adds a node (entity) to the graph if it hasn't been added yet.

        Args:
            tag (str): The tag name to be added.

        Returns:
            str: The sanitized tag name used in the graph.
        """

        safe_tag = tag.replace(">", "_").replace(" ", "_")
        if safe_tag not in added_nodes:
            node_def = f"    {safe_tag} {{"
            graph.append(node_def)
            added_nodes.add(safe_tag)
        return safe_tag

    def add_edge(
        from_tag: str, to_tag: str, edge_type: str = "solid", label: str = ""
    ) -> None:
        """
        Adds an edge (relationship) between two nodes in the graph,
        including relationship attributes (parent, child, SUPERset, SUBset).

        Args:
            from_tag (str): The starting node of the edge.
            to_tag (str): The ending node of the edge.
            edge_type (str): The type of edge ('solid' or 'dashed').
                Defaults to 'solid'.
            label (str): The label for the edge. Defaults to ''.
        """

        safe_from = add_node(from_tag)
        safe_to = add_node(to_tag)
        edge = (safe_from, safe_to, edge_type)

        if edge not in added_edges:
            if edge_type == "solid":
                # Hierarchical relationship (parent-child)

                # Add parent attribute to the child entity
                if not any(
                    f'        parent "{to_tag}"' in line
                    for line in graph
                    if safe_from in line
                ):
                    graph.insert(
                        graph.index(f"    {safe_from} {{") + 1,
                        f'        parent "{to_tag}"',
                    )

                # Add child attribute to the parent entity (if not already present)
                if not any(
                    f'        child "{from_tag}"' in line
                    for line in graph
                    if safe_to in line
                ):
                    graph.insert(
                        graph.index(f"    {safe_to} {{") + 1,
                        f'        child "{from_tag}"',
                    )

            elif edge_type == "dashed":
                # Non-hierarchical relationship (related)
                cooccurrence_count = tag_cooccurrences[from_tag][to_tag]

                related_count_from = sum(
                    1
                    for line in graph
                    if line.startswith(f"        related_")
                    and f'"{to_tag}"' in line
                    and graph.index(line) < graph.index(f"    {safe_from} {{") + 10
                    and graph.index(f"    {safe_from} {{")
                    < graph.index(line)
                    < graph.index(f"    {safe_to} {{")
                )

                if not any(
                    f'        related_{related_count_from} "{to_tag}"' in line
                    for line in graph
                    if safe_from in line
                ):
                    graph.insert(
                        graph.index(f"    {safe_from} {{") + 1,
                        f'        related_{related_count_from} "{to_tag}"',
                    )

                related_count_to = sum(
                    1
                    for line in graph
                    if line.startswith(f"        related_")
                    and f'"{from_tag}"' in line
                    and graph.index(line) < graph.index(f"    {safe_to} {{") + 10
                    and graph.index(f"    {safe_to} {{")
                    < graph.index(line)
                    < graph.index(f"    {safe_from} {{")
                )

                if not any(
                    f'        related_{related_count_to} "{from_tag}"' in line
                    for line in graph
                    if safe_to in line
                ):
                    graph.insert(
                        graph.index(f"    {safe_to} {{") + 1,
                        f'        related_{related_count_to} "{from_tag}"',
                    )

            # Close the entity definitions for both entities if not already closed
            if not graph[graph.index(f"    {safe_from} {{") + 1].startswith("    }"):
                graph.insert(graph.index(f"    {safe_from} {{") + 2, "    }")
            if not graph[graph.index(f"    {safe_to} {{") + 1].startswith("    }"):
                graph.insert(graph.index(f"    {safe_to} {{") + 2, "    }")

            if edge_type == "solid":
                graph.append(f'    {safe_from} ||--|| {safe_to} : "parent of"')
            elif edge_type == "dashed":
                graph.append(
                    f'    {safe_from} ||..|| {safe_to} : "related ({cooccurrence_count})"'
                )

            added_edges.add(edge)

    def process_tag(tag_name: str, data: Dict[str, Any]) -> None:
        """
        Processes a single tag and its relationships, adding nodes and edges
        to the Mermaid graph.

        Args:
            tag_name (str): The name of the tag.
            data (Dict[str, Any]): The data associated with the tag,
                including children and related tags.
        """

        # Add main node (entity)
        add_node(tag_name)

        # Handle combined tags (entities representing tag combinations)
        if ">" in tag_name:
            parts = tag_name.split(">")
            for part in parts:
                add_edge(part, tag_name, "solid")

        # Add hierarchical relationships (parent-child)
        for child in data.get("children", []):
            add_edge(tag_name, child, "solid")

        # Add non-hierarchical relationships (related)
        related_tags = data.get("related", [])
        for related in related_tags:
            cooccurrence_count = tag_cooccurrences[tag_name].get(related, 0)
            if cooccurrence_count > 0:  # Only add related if co-occurrence > 0
                add_edge(
                    tag_name, related, "dashed", f"related ({cooccurrence_count})"
                )

    try:
        if isinstance(tag_data, list):
            for item in tag_data:
                if isinstance(item, dict) and "tag" in item:
                    process_tag(item["tag"], item)
                else:
                    logging.warning(f"Skipping invalid item in tag_data: {item}")
        elif isinstance(tag_data, dict):
            for tag_name, data in tag_data.items():
                process_tag(tag_name, data)
        else:
            logging.error(f"Unexpected tag_data type: {type(tag_data)}")
            return ""

    except Exception as e:
        logging.error(f"Error processing tag_data: {e}")
        return ""

    # Post-processing: Add SUPERset and SUBset relationships based on set theory
    for tag_name, data in tag_data.items():
        safe_tag_name = tag_name.replace(">", "_").replace(" ", "_")

        for child in data.get("children", []):
            safe_child = child.replace(">", "_").replace(" ", "_")
            # Add SUPERset to parent, SUBset to child (if not redundant with parent/child)
            if not any(
                f'        parent "{tag_name}"' in line for line in graph
                if safe_child in line
            ):
                if not any(
                    f'        SUPERset "{child}"' in line for line in graph
                    if safe_tag_name in line
                ):
                    graph.insert(
                        graph.index(f"    {safe_tag_name} {{") + 1,
                        f'        SUPERset "{child}"',
                    )
            if not any(
                f'        child "{tag_name}"' in line for line in graph
                if safe_tag_name in line
            ):
                if not any(
                    f'        SUBset "{tag_name}"' in line for line in graph
                    if safe_child in line
                ):
                    graph.insert(
                        graph.index(f"    {safe_child} {{") + 1,
                        f'        SUBset "{tag_name}"',
                    )

        for related in data.get("related", []):
            # Ensure related tags are also represented as entities
            add_node(related)

        # Ensure that the entity definition is closed if it's not already
        if not graph[graph.index(f"    {safe_tag_name} {{") + 1].startswith("    }"):
            graph.insert(graph.index(f"    {safe_tag_name} {{") + 2, "    }")

    return "\n".join(graph)


if __name__ == "__main__":
    # Use environment variables to determine paths (adapt if necessary)
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(
        os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml"
    )

    tag_data, combined_tags, tag_cooccurrences = process_tags(posts_dir, output_file)
    mermaid_graph = generate_mermaid_graph(tag_data, tag_cooccurrences)

    # Write the Mermaid graph to a file
    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
