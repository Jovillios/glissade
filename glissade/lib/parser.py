import re


def parse_markdown_metadata(markdown: str) -> tuple[dict, str]:
    """Parse YAML front matter (between --- markers) and return (metadata, content)."""
    pattern = r"^---\s*(?P<metadata>.+?)\s*---\s*(?P<content>.*)$"
    match = re.search(pattern, markdown, re.DOTALL)

    if not match:
        return {}, markdown

    metadata_str = match.group("metadata")
    content = match.group("content").strip()

    metadata = {}
    for line in metadata_str.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()

            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            metadata[key.strip()] = value

    return metadata, content


def parse_markdown_comments(markdown: str) -> tuple[dict, str]:
    """Parse <!-- --> comments and extract global and area-specific content (supports nesting)."""
    result: dict = {"global": "", "areas": {}}

    begin_pattern = r"<!--\s*begin\s+([\w-]+)\s*-->"
    end_pattern = r"<!--\s*end\s+([\w-]+)\s*-->"

    tags: list[tuple] = []
    for match in re.finditer(begin_pattern, markdown):
        tags.append(("begin", match.group(1), match.start(), match.end()))
    for match in re.finditer(end_pattern, markdown):
        tags.append(("end", match.group(1), match.start(), match.end()))

    tags.sort(key=lambda x: x[2])

    stack: list[tuple] = []
    matched_regions: list[tuple[int, int]] = []

    for tag_type, name, start, end in tags:
        if tag_type == "begin":
            stack.append((name, start, end))
        elif tag_type == "end" and stack:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    begin_name, begin_start, begin_end = stack.pop(i)
                    content_start = begin_end
                    content_end = start
                    content = markdown[content_start:content_end].strip()

                    nested_result = parse_markdown_comments(content)
                    result["areas"][name] = nested_result

                    matched_regions.append((begin_start, end))
                    break

    global_content = markdown
    for start, end in sorted(matched_regions, reverse=True):
        end_tag_match = re.search(end_pattern, global_content[end:])
        if end_tag_match:
            actual_end = end + end_tag_match.end()
            global_content = global_content[:start] + global_content[actual_end:]

    result["global"] = global_content.strip()

    return result


def parse_slide_classes(slide_content: str) -> tuple[list[str], str]:
    """Extract CSS classes from <!-- classes --> tags and return (classes, cleaned_content)."""
    pattern = r"<!--\s*([\w][\w\s-]*)\s*-->"
    classes: list[str] = []
    for match in re.finditer(pattern, slide_content):
        classes.extend(match.group(1).strip().split())
    cleaned = re.sub(pattern, "", slide_content).strip()
    return classes, cleaned
