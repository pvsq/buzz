from buzz import (
    copy_dir_recursively,
    generate_pages_recursive
)

def main():
    copy_dir_recursively("./static/", "./public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")

main()
