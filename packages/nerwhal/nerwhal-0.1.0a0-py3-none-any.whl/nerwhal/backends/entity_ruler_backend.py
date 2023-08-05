from typing import Type

from spacy.pipeline import EntityRuler

from .base import Backend
from nerwhal.recognizer_bases import EntityRulerRecognizer
from nerwhal.types import NamedEntity
from nerwhal.nlp_utils import (
    configure_spacy_entity_extension_attributes,
    set_spacy_entity_extension_attributes,
    load_spacy_nlp,
)

configure_spacy_entity_extension_attributes()


class EntityRulerBackend(Backend):
    """This backend recognizes entities using the spaCy EntityRuler.

    See https://spacy.io/usage/rule-based-matching#entityruler for more information about the EntityRuler.
    """

    def __init__(self, language):
        self.nlp = load_spacy_nlp(language, disable_components=["tagger", "parser", "ner"])

    def register_recognizer(self, recognizer_cls: Type[EntityRulerRecognizer]):
        recognizer = recognizer_cls()

        recognizer_name = recognizer_cls.__name__
        ruler = EntityRuler(self.nlp)
        self.nlp.add_pipe(ruler, recognizer_name)
        rules = [{"label": recognizer.TAG, "pattern": pattern} for pattern in recognizer.patterns]
        ruler.add_patterns(rules)
        self.nlp.add_pipe(
            set_spacy_entity_extension_attributes(recognizer.SCORE, recognizer_name),
            name="label_" + recognizer_name,
            after=recognizer_name,
        )

    def run(self, text):
        doc = self.nlp(text)

        ents = []
        for ent in doc.ents:
            ents += [NamedEntity(ent.start_char, ent.end_char, ent.label_, ent.text, ent._.score, ent._.recognizer)]

        return ents
