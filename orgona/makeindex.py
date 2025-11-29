from pathlib import Path

# usage: python makeindex.py > index.html

TEMPLATE_FILE = "index.html.template"

def render_title(word: str) -> str:
    parts = word.replace(".pdf", "").split("-")
    return " ".join(
    	(part[0].upper() + part[1:] for part in parts)
    )

ROOT_INDEX = {}

for path in Path(".").rglob("*.pdf"):
    str_path = str(path)
    # print(str_path)
    path_parts = str_path.split("/")
    title_parts = [render_title(path_part) for path_part in path_parts]
    title = title_parts[-1]
    target_index = ROOT_INDEX
    for folder in title_parts[0:-1]:
    	target_index = target_index.setdefault(folder, {})
    target_index[title] = str_path


def produce_html(name, item, level=0):
    indent = "".join([" "] * level * 4)
    if isinstance(item, str):
        print(f'{indent}<li><a href="./{item}">{name}</a></li>')
    elif isinstance(item, dict):
        header_class = f"h{level+1}"
        print(f"{indent}<p>")
        print(f"{indent}  <{header_class}>{name}</{header_class}>")
        print(f"{indent}  <ul>")
        for name, sub_item in item.items():
            produce_html(name, sub_item, level+1)
        print(f"{indent}  </ul>")
        print(f"{indent}</p>")
    else:
        assert False, "Unexpected type: {(type(item), item)}"



with open(TEMPLATE_FILE, "rt") as template:
    placeholder_status = None
    for line in template:
        if placeholder_status is None:
            if "<!-- CONTENT" in line:
                placeholder_status = "found"
            else:
                print(line)
        elif placeholder_status == "found":
            if "CONTENT -->" in line:
                placeholder_status = "complete"
                produce_html("Orgona művek", ROOT_INDEX, 1)
            else:
                pass  # ignore line
        else: # complete
            print(line)

            





