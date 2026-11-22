"""R4: protect broad language searches and deliberate exact-tag searches."""

from pathlib import Path
import ast

import pandas as pd
from babel import Locale
from babel.core import UnknownLocaleError
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def screening_function():
    # Load only the function: importing app executes its Streamlit form and
    # contaminates the AppTest context in this same process.
    tree = ast.parse((ROOT / 'app.py').read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'screen_feeds', 'language_label'}]
    namespace = {'pd': pd, 'Locale': Locale, 'UnknownLocaleError': UnknownLocaleError,
                 'CATEGORY_COLUMNS': [f'category{i}' for i in range(1, 9)]}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(ROOT / 'app.py'), 'exec'), namespace)
    return namespace['screen_feeds']


def test_language_family_respects_tag_boundary_and_exact_selection():
    screen_feeds = screening_function()
    tags = ['es', 'es-mx', 'es-es', 'es_do', 'est', 'en', 'en-us', 'enough']
    feeds = pd.DataFrame({
        'title': tags,
        'language_normalized': tags,
        'latest_episode': pd.to_datetime(['2026-08-31'] * len(tags), utc=True),
        'episode_count': 20,
        'discovery_score': 1,
        'guid_normalized': tags,
        **{f'category{i}': 'music' if i == 1 else '' for i in range(1, 9)},
    })
    def titles(language):
        result, _, _ = screen_feeds(feeds, 'music', language, 90, 20, 'Any', 0)
        return set(result.title)

    assert titles('Spanish (all variants)') == {'es', 'es-mx', 'es-es', 'es_do'}
    assert titles('es') == {'es'}
    assert titles('es-mx') == {'es-mx'}
    assert titles('English (all variants)') == {'en', 'en-us'}


def test_spanish_family_and_exact_tags_in_real_app():
    at = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
    assert not at.exception
    language = next(w for w in at.selectbox if w.label == 'Language')
    assert 'Spanish (all variants)' in language.options
    assert 'Spanish (es)' in language.options
    assert 'Spanish (Mexico) (es-mx)' in language.options
    next(w for w in at.selectbox if w.label == 'Category').set_value('music')
    language.set_value('Spanish (all variants)')
    at.button[0].click().run(timeout=30)
    assert not at.exception
    assert set(at.dataframe[0].value['Title']) == {
        'Sonidos y Sonados', 'Tópica Radio', 'Women Riot Podcast',
    }
    for label, expected in [
        ('Spanish (es)', {'Sonidos y Sonados'}),
        ('Spanish (Mexico) (es-mx)', {'Tópica Radio'}),
        ('Spanish (Spain) (es-es)', {'Women Riot Podcast'}),
    ]:
        next(w for w in at.selectbox if w.label == 'Language').set_value(label)
        at.button[0].click().run(timeout=30)
        assert not at.exception
        assert set(at.dataframe[0].value['Title']) == expected
