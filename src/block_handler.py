from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")
	filtered_blocks = []
	for block in blocks:
		stripped_block = block.strip()
		if stripped_block != "":
			filtered_blocks.append(stripped_block)
	return filtered_blocks

def block_to_block_type(block):
    if block.startswith("#"):
        heading_level = 0
        while heading_level < len(block) and block[heading_level] == "#":
            heading_level += 1

        if (
            heading_level >= 1
            and heading_level <= 6
            and heading_level < len(block)
            and block[heading_level] == " "
        ):
            return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH