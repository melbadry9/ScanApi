import tempfile
import validators


def check_domain(domains:list):
    domains_copy = set()
    # Check for vaild domains
    for av_dom in domains:
        av_dom = av_dom.lower().replace("*.","")
        if validators.domain(av_dom):
            domains_copy.add(av_dom)
    return list(domains_copy)

def temp_file(domains:list):
    tf = tempfile.NamedTemporaryFile("w+t", encoding="utf-8", delete=False)
    for item in domains:
        tf.writelines(item + "\n")
    tf.seek(0)
    return tf.name

