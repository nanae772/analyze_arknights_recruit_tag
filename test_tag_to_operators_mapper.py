'''
tag_to_operators_mapper.py の単体テストモジュール
'''

from tag_to_operators_mapper import split_string_by_tags, load_tag_list

all_tag = load_tag_list('all_tag.txt')


class TestSplitStringByTags:
    def test_positive_case(self) -> None:
        s = '近距離火力牽制'
        expected_result = sorted(['近距離', '火力', '牽制'])
        assert split_string_by_tags(s, all_tag) == expected_result

    def test_empty_case(self) -> None:
        s = ''
        expected_result: list[str] = []
        assert split_string_by_tags(s, all_tag) == expected_result
