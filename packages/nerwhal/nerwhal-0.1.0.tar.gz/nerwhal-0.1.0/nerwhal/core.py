import importlib.util
import os
from collections import OrderedDict
from pathlib import Path
from typing import List

import nerwhal.backends
from nerwhal.combination_strategies import combine
from nerwhal.backends.stanza_ner_backend import StanzaNerBackend
from nerwhal.tokenizer import Tokenizer
from nerwhal.scorer import score_entities
from nerwhal.types import Config, NamedEntity
from nerwhal.entity_aligner import EntityAligner


class Analyzer:
    """The Analyzer class is NERwhal's core component, that runs named-entity recognition and caches the recognizers."""

    def __init__(self):
        self.config = None
        self.backends = OrderedDict()
        self.tokenizer = None
        self.recognizer_lookup = None

    def update_config(self, config):
        """Whenever one field of the config changed its value, the Analyzer's state is rebuilt from scratch.

        While reloading every recognizer and backend from scratch isn't the most efficient way, it is simple.
        """
        if config == self.config:
            return

        self.config = config

        self.tokenizer = Tokenizer(self.config.language)

        self.backends = {}

        if self.config.use_statistical_ner:
            self.backends["stanza"] = StanzaNerBackend(self.config.language)

        if self.config.load_integrated_recognizers:
            self._add_integrated_recognizers_to_config_recognizer_paths()

        self.recognizer_lookup = {}
        for recognizer_path in self.config.recognizer_paths:
            if not os.path.isfile(recognizer_path):
                raise ValueError(f"Configured recognizer {recognizer_path} is not a file")

            recognizer_cls = self._load_class(recognizer_path)
            self.recognizer_lookup[recognizer_cls.__name__] = recognizer_cls

            # import only the backend modules that are configured
            if recognizer_cls.BACKEND not in self.backends.keys():
                backend_cls = nerwhal.backends.load(recognizer_cls.BACKEND)

                if recognizer_cls.BACKEND == "entity-ruler":
                    backend_inst = backend_cls(self.config.language)
                else:
                    backend_inst = backend_cls()

                self.backends[recognizer_cls.BACKEND] = backend_inst

            self.backends[recognizer_cls.BACKEND].register_recognizer(recognizer_cls)

    def run_recognition(self, text):
        """Run recognition and return the recognized named-entities."""
        return self._run_backends(self.backends.values(), text)

    def _load_class(self, recognizer_path):
        """Load the class of a (custom) recognizer.

        This class may be located outside of NERwhal's package.
        """
        module_name = os.path.splitext(os.path.basename(recognizer_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, recognizer_path)
        module = importlib.util.module_from_spec(spec)
        class_name = "".join(word.title() for word in module_name.split("_"))
        spec.loader.exec_module(module)
        recognizer_cls = getattr(module, class_name)
        return recognizer_cls

    def _add_integrated_recognizers_to_config_recognizer_paths(self):
        """Traverse the directory of integrated recognizers and append them to the recognizer paths."""
        for root, _, files in os.walk(Path(__file__).parent / "integrated_recognizers"):
            for file in files:
                if file.endswith("_recognizer.py"):
                    example = os.path.join(root, file)
                    if all([example not in path for path in self.config.recognizer_paths]):
                        self.config.recognizer_paths.append(example)

    def _run_backends(self, backends, text):
        return [backend.run(text) for backend in backends]


analyzer = Analyzer()


def recognize(text: str, config: Config, combination_strategy=None, context_words=False, return_tokens=True) -> dict:
    """Find personally identifiable data in the given text and return it.

    :param text: the text that is searched for named entities
    :param config: pass a config object to configure the recognition methods
    :param combination_strategy: choose from None, `disjunctive_union`, `fusion`, and `smart-fusion`; see the docs of
        `combination_strategies.combine` for more details
    :param context_words: if True, use context words to boost the score of entities: this is the case, if one of a recognizer's
        context words appears in the entity's sentence. Setting `context_words` to True will also align each entity's
        start/end to the nearest token's start/end
    :param return_tokens: compute and return the tokenization; this will also align each entity's start/end to the nearest
        token's start/end
    """
    analyzer.update_config(config)
    recognition_results = analyzer.run_recognition(text)

    if len(recognition_results) == 0:
        ents = []
    else:
        ents = [ent for result in recognition_results for ent in result]

    result = {}
    tokens = []
    if return_tokens or context_words:
        # tokenize
        analyzer.tokenizer.tokenize(text)
        tokens = analyzer.tokenizer.get_tokens()
        # align entities with tokens
        entity_aligner = EntityAligner()
        entity_aligner.align_entities_with_tokens(ents, tokens)

    # combine entities after they have been aligned
    ents = combine(ents, strategy=combination_strategy)

    if return_tokens:
        result["tokens"] = tokens

    if context_words:
        for ent in ents:
            sentence_tokens = analyzer.tokenizer.get_sentence_for_token(
                ent.start_tok, exclude_tokens=list(range(ent.start_tok, ent.end_tok))
            )
            sentence_words = [token.text for token in sentence_tokens]
            context_words = analyzer.recognizer_lookup[ent.recognizer].CONTEXT_WORDS
            if any(word in sentence_words for word in context_words):
                ent.score = min(ent.score * analyzer.config.context_word_confidence_boost_factor, 1.0)

    result["ents"] = ents
    return result


def evaluate(ents: List[NamedEntity], gold: List[NamedEntity]) -> dict:
    """Compute the evaluation scores of computed named entities compared to the underlying true entities.

    Each entity has to have the fields `start_char`, `end_char` and `tag` populated. The remaining fields are ignored.
    """
    return score_entities(ents, gold)
