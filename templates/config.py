c = get_config()

c.Exporter.template_file = 'template.tpl'
c.Exporter.template_path = ["src", "/".join(__file__.split("/")[:-1])]