import os.path
import shutil

from block_md2text import markdown_to_html_node

def copy_dir_recursively(src: str, dst: str):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    if not os.path.exists(dst):
        os.mkdir(dst)

    if os.listdir(dst):
        shutil.rmtree(dst)
        os.mkdir(dst)

    src_files = os.listdir(src)
    for file in src_files:
        src_file_path = os.path.join(src, file)
        dst_file_path = os.path.join(dst, file)
        if os.path.isdir(src_file_path):
            copy_dir_recursively(src_file_path, dst_file_path)
        else:
            shutil.copy(src_file_path, dst)


def extract_title(markdown: str):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise ValueError("No h1 header found. At least one h1 header must be present.")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")

    markdown = ''
    with open(from_path, 'r') as f:
        markdown = f.read()
    if markdown[-1] == '\n':
        markdown = markdown[:-1]

    template_html = ''
    with open(template_path, 'r') as t:
        template_html = t.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    withtitle = template_html.replace("{{ Title }}", title)
    htmlpage = withtitle.replace("{{ Content }}", content)

    opdir = os.path.dirname(dest_path)
    if not os.path.exists(opdir):
        os.makedirs(opdir)

    output = open(dest_path, 'w')
    output.write(htmlpage)
    output.flush()
    output.close()


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
        return

    files = os.listdir(dir_path_content)
    for file in files:
        destfile = file
        if file.endswith(".md"):
            destfile = file.removesuffix(".md")
            destfile = destfile + ".html"
        new_dir_path = os.path.join(dir_path_content, file)
        new_dest_path = os.path.join(dest_dir_path, destfile)
        generate_pages_recursive(new_dir_path, template_path, new_dest_path)

