# ----------------------------------------------------------------------
# rainbow, a command line colorizer
# Copyright (C) 2011-2017 Julien Nicoulaud <julien.nicoulaud@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import re

from rainbow import ansi
from rainbow.filter import FILTERS_BY_NAME
from rainbow.transformer import IdentityTransformer
from rainbow.transformer import InsertAfterRegexTransformer
from rainbow.transformer import InsertBeforeAndAfterRegexTransformer
from rainbow.transformer import InsertBeforeRegexTransformer
from rainbow.transformer import ListTransformer
from rainbow.transformer import ReplaceRegexTransformer
from rainbow.transformer import ReplaceTransformer
from rainbow.transformer import TransformerBuilder


def test_identity():
    assert IdentityTransformer().transform("test") == "test"


def test_replace_not_matching():
    assert ReplaceTransformer('a', 'b').transform("test") == "test"


def test_replace_matching():
    assert ReplaceTransformer('test', 'b').transform("test") == "b"


def test_replace_multiples_matches():
    assert ReplaceTransformer('test', 'b').transform("testtesttest") == "bbb"


def test_replace_regex_not_matching():
    assert ReplaceRegexTransformer(re.compile('a'), 'b').transform("test") == "test"


def test_replace_regex_matching():
    assert ReplaceRegexTransformer(re.compile('test'), 'b').transform("test") == "b"


def test_replace_regex_multiples_matches():
    assert ReplaceRegexTransformer(re.compile('test'), 'b').transform("testtesttest") == "bbb"


def test_before_whole_line_matches():
    assert InsertBeforeRegexTransformer(re.compile("test"), "BEFORE").transform("test") == "BEFOREtest"


def test_after_whole_line_matches():
    assert InsertAfterRegexTransformer(re.compile("test"), "AFTER").transform("test") == "testAFTER"


def test_before_and_after_whole_line_matches():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("test"), "BEFORE", "AFTER").transform(
        "test") == "BEFOREtestAFTER"


def test_before_partial_line_matches():
    assert InsertBeforeRegexTransformer(re.compile("test"), "BEFORE").transform("aaatestaaa") == "aaaBEFOREtestaaa"


def test_after_partial_line_matches():
    assert InsertAfterRegexTransformer(re.compile("test"), "AFTER").transform("aaatestaaa") == "aaatestAFTERaaa"


def test_before_and_after_partial_line_matches():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("test"), "BEFORE", "AFTER").transform(
        "aaatestaaa") == "aaaBEFOREtestAFTERaaa"


def test_before_several_matches():
    assert InsertBeforeRegexTransformer(re.compile("test"), "BEFORE").transform(
        "AAAtestBBBtestCCC") == "AAABEFOREtestBBBBEFOREtestCCC"


def test_after_several_matches():
    assert InsertAfterRegexTransformer(re.compile("test"), "AFTER").transform(
        "AAAtestBBBtestCCC") == "AAAtestAFTERBBBtestAFTERCCC"


def test_before_and_after_several_matches():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("test"), "BEFORE", "AFTER").transform(
        "AAAtestBBBtestCCC") == "AAABEFOREtestAFTERBBBBEFOREtestAFTERCCC"


def test_before_only_match_whole_line():
    assert InsertBeforeRegexTransformer(re.compile("^test$"), "BEFORE").transform(
        "testA") == "testA"


def test_after_only_match_whole_line():
    assert InsertAfterRegexTransformer(re.compile("^test$"), "AFTER").transform(
        "testA") == "testA"


def test_before_and_after_only_match_whole_line():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("^test$"), "BEFORE", "AFTER").transform(
        "testA") == "testA"


def test_list_transformer():
    assert ListTransformer([
        InsertBeforeRegexTransformer(re.compile("test"), "BEFORE"),
        InsertAfterRegexTransformer(re.compile("test"), "AFTER")
    ]).transform("test") == "BEFOREtestAFTER"


def test_transformer_builder():
    builder = TransformerBuilder()
    builder.add_mapping("test1", FILTERS_BY_NAME['foreground-red'])
    builder.add_mapping("test2", FILTERS_BY_NAME['background-green-before'])
    builder.add_mapping("test3", FILTERS_BY_NAME['foreground-yellow-after'])
    transformer = builder.build()
    assert isinstance(transformer, ListTransformer)
    assert isinstance(transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert transformer.transformers[0].regex.pattern == 'test1'
    assert transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert isinstance(transformer.transformers[1], InsertBeforeRegexTransformer)
    assert transformer.transformers[1].regex.pattern == 'test2'
    assert transformer.transformers[1].before == ansi.ANSI_BACKGROUND_GREEN
    assert isinstance(transformer.transformers[2], InsertAfterRegexTransformer)
    assert transformer.transformers[2].regex.pattern == 'test3'
    assert transformer.transformers[2].after == ansi.ANSI_FOREGROUND_YELLOW


def test_transformer_identity_str():
    assert IdentityTransformer().__str__() == 'identity'


def test_transformer_replace_str():
    assert ReplaceTransformer("test", "REPLACEMENT").__str__() == 'replace "test" with "REPLACEMENT"'


def test_transformer_replace_regex_str():
    assert ReplaceRegexTransformer(re.compile("test"), "REPLACEMENT").__str__() == 'replace "test" with "REPLACEMENT"'


def test_transformer_before_str():
    assert InsertBeforeRegexTransformer(re.compile("test"), "BEFORE").__str__() == 'insert "BEFORE" before "test"'


def test_transformer_after_str():
    assert InsertAfterRegexTransformer(re.compile("test"), "AFTER").__str__() == 'insert "AFTER" after "test"'


def test_transformer_before_and_after_str():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("test"), "BEFORE",
                                                "AFTER").__str__() == 'insert "BEFORE" before and "AFTER" after "test"'


def test_transformer_list_str():
    assert ListTransformer([
        InsertBeforeRegexTransformer(re.compile("test"), "BEFORE"),
        InsertAfterRegexTransformer(re.compile("test"), "AFTER")
    ]).__str__() == 'insert "BEFORE" before "test"\ninsert "AFTER" after "test"'


def test_transformer_identity_eq():
    assert IdentityTransformer() == IdentityTransformer()


def test_transformer_replace_eq():
    assert ReplaceTransformer("test", "REPLACEMENT") == ReplaceTransformer("test", "REPLACEMENT")


def test_transformer_replace_regex_eq():
    assert ReplaceRegexTransformer(re.compile("test"), "REPLACEMENT") == ReplaceRegexTransformer(re.compile("test"),
                                                                                                 "REPLACEMENT")


def test_transformer_before_eq():
    assert InsertBeforeRegexTransformer(re.compile("test"), "BEFORE") == InsertBeforeRegexTransformer(
        re.compile("test"), "BEFORE")


def test_transformer_after_eq():
    assert InsertAfterRegexTransformer(re.compile("test"), "AFTER") == InsertAfterRegexTransformer(re.compile("test"),
                                                                                                   "AFTER")


def test_transformer_before_and_after_eq():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("test"), "BEFORE",
                                                "AFTER") == InsertBeforeAndAfterRegexTransformer(re.compile("test"),
                                                                                                 "BEFORE", "AFTER")


def test_transformer_list_eq():
    assert ListTransformer([
        InsertBeforeRegexTransformer(re.compile("test"), "BEFORE"),
        InsertAfterRegexTransformer(re.compile("test"), "AFTER")
    ]) == ListTransformer([
        InsertBeforeRegexTransformer(re.compile("test"), "BEFORE"),
        InsertAfterRegexTransformer(re.compile("test"), "AFTER")
    ])


def test_transformer_replace_not_eq():
    assert ReplaceTransformer("test", "REPLACEMENT") != ReplaceTransformer("test", "REPLACEMENT2")


def test_transformer_replace_regex_not_eq():
    assert ReplaceRegexTransformer(re.compile("test"), "REPLACEMENT") != ReplaceRegexTransformer(re.compile("test"),
                                                                                                 "REPLACEMENT2")


def test_transformer_before_not_eq():
    assert InsertBeforeRegexTransformer(re.compile("test"), "BEFORE") != InsertBeforeRegexTransformer(
        re.compile("test"), "BEFORE2")


def test_transformer_after_not_eq():
    assert InsertAfterRegexTransformer(re.compile("test"), "AFTER") != InsertAfterRegexTransformer(re.compile("test"),
                                                                                                   "AFTER2")


def test_transformer_before_and_after_not_eq():
    assert InsertBeforeAndAfterRegexTransformer(re.compile("test"), "BEFORE",
                                                "AFTER") != InsertBeforeAndAfterRegexTransformer(re.compile("test"),
                                                                                                 "BEFORE", "AFTER2")


def test_transformer_list_not_eq():
    assert ListTransformer([
        InsertBeforeRegexTransformer(re.compile("test"), "BEFORE"),
        InsertAfterRegexTransformer(re.compile("test"), "AFTER")
    ]) != ListTransformer([
        InsertBeforeRegexTransformer(re.compile("test"), "BEFORE"),
        InsertAfterRegexTransformer(re.compile("test"), "AFTER2")
    ])
