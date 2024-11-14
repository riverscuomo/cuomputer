from bot.scripts.wiki_to_markdown import wiki_to_markdown


def test_internal_wiki_link_only_label():
    assert wiki_to_markdown('[[Ecce Homo]]', False) == '[Ecce Homo](https://www.weezerpedia.com/wiki/Ecce%20Homo)'

def test_internal_wiki_link_with_label_and_path():
    assert wiki_to_markdown('[[Blue Album|the Blue Album]]', False) == '[the Blue Album](https://www.weezerpedia.com/wiki/Blue%20Album)'
