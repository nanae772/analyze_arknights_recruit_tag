'''
tag_to_operators_mapper.py の単体テストモジュール
'''

from tag_to_operators_mapper import split_string_by_tags, load_tag_list

all_tag = load_tag_list('all_tag.txt')


class TestSplitStringByTags:
    '''
    split_string_by_tagsの単体テスト群
    '''

    def test_positive_case(self) -> None:
        '''
        想定ケースで正しく動くことを確認
        '''
        s = '近距離火力牽制'
        expected_result = sorted(['近距離', '火力', '牽制'])
        assert split_string_by_tags(s, all_tag) == expected_result

        s = '先鋒タイプ近距離COST回復支援'
        expected_result = sorted(['先鋒タイプ', '近距離', 'COST回復', '支援'])
        assert split_string_by_tags(s, all_tag) == expected_result

        s = '前衛タイプ近距離火力支援'
        expected_result = sorted(['前衛タイプ', '近距離', '火力', '支援'])
        assert split_string_by_tags(s, all_tag) == expected_result

    def test_separate_slash_case(self) -> None:
        '''
        /区切りでも動くことを確認
        '''
        s = '近距離/火力/牽制'
        expected_result = sorted(['近距離', '火力', '牽制'])
        assert split_string_by_tags(s, all_tag) == expected_result

    def test_noise_case(self) -> None:
        '''
        文字列に様々なノイズが入っていても動くことを確認
        '''
        s = '近距離,火力　牽制b'
        expected_result = sorted(['近距離', '火力', '牽制'])
        assert split_string_by_tags(s, all_tag) == expected_result

    def test_empty_case(self) -> None:
        '''
        空文字列に空リストを返すことを確認
        '''
        s = ''
        expected_result: list[str] = []
        assert split_string_by_tags(s, all_tag) == expected_result
