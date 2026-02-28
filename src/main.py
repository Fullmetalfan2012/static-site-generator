import os
from website_handler import *

    

def main():
    source_path = os.path.join(os.path.dirname(__file__), "..", "static")
    destination_path = os.path.join(os.path.dirname(__file__), "..", "public")
    template_path = os.path.join(os.path.dirname(__file__), "..", "template.html")
    content_path = os.path.join(os.path.dirname(__file__), "..", "content")
    source_path = os.path.abspath(source_path)
    destination_path = os.path.abspath(destination_path)
    template_path = os.path.abspath(template_path)
    content_path = os.path.abspath(content_path)
    copy_directory_recursive(source_path, destination_path)
    generate_pages_recursive(content_path, template_path, destination_path)
    



if __name__ == "__main__":    main()