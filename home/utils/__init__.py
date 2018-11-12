def markdown_from_file(path):
    import markdown
    from io import open

    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    html = markdown.markdown(data, extensions=['fenced_code', 'tables'])

    return html
