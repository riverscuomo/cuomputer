from bot.scripts.wiki_to_markdown import wiki_to_markdown


def test_internal_wiki_link_only_label():
    assert wiki_to_markdown('[[Ecce Homo]]', False) == '[Ecce Homo](https://www.weezerpedia.com/wiki/Ecce%20Homo)'

def test_internal_wiki_link_with_label_and_path():
    assert wiki_to_markdown('[[Blue Album|the Blue Album]]', False) == '[the Blue Album](https://www.weezerpedia.com/wiki/Blue%20Album)'


def test_remove_numeric_footnote_markers():
    text = "Weezer formed in 1992.[1] They released the Blue Album." 
    assert wiki_to_markdown(text, False) == "Weezer formed in 1992. They released the Blue Album."


def test_remove_nested_template():
    input_text = 'Info {{cite web|url={{URL|https://example.com}}|title=Example}} end'
    assert wiki_to_markdown(input_text, False) == 'Info  end'
