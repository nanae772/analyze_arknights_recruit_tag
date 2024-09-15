'''
tag_to_operators_mapper.py の単体テストモジュール
'''

from tag_to_operators_mapper import split_string_by_tags, load_tag_list
from tag_to_operators_mapper import invert_operator_list, Operator

all_tag = load_tag_list('google_cloud/all_tag.txt')


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


class TestInvertOperatorList:
    '''
    invert_operator_listの単体テストクラス
    '''

    def test_positive(self) -> None:
        '''
        正常系のテストケース
        '''
        operator_list = [
            Operator('ポプカル', ('前衛タイプ', '近距離', '範囲攻撃', '生存'), 3),
            Operator('ラヴァ', ('術師タイプ', '遠距離', '範囲攻撃'), 3),
            Operator('ムース', ('前衛タイプ', '近距離', '火力'), 4),
            Operator('メテオ', ('狙撃タイプ', '遠距離', '火力', '弱化'), 4)
        ]

        expected_result = {
            '前衛タイプ': {
                Operator('ポプカル', ('前衛タイプ', '近距離', '範囲攻撃', '生存'), 3),
                Operator('ムース', ('前衛タイプ', '近距離', '火力'), 4)
            },
            '術師タイプ': {
                Operator('ラヴァ', ('術師タイプ', '遠距離', '範囲攻撃'), 3)
            },
            '狙撃タイプ': {
                Operator('メテオ', ('狙撃タイプ', '遠距離', '火力', '弱化'), 4)
            },
            '近距離': {
                Operator('ポプカル', ('前衛タイプ', '近距離', '範囲攻撃', '生存'), 3),
                Operator('ムース', ('前衛タイプ', '近距離', '火力'), 4)
            },
            '遠距離': {
                Operator('ラヴァ', ('術師タイプ', '遠距離', '範囲攻撃'), 3),
                Operator('メテオ', ('狙撃タイプ', '遠距離', '火力', '弱化'), 4)
            },
            '範囲攻撃': {
                Operator('ポプカル', ('前衛タイプ', '近距離', '範囲攻撃', '生存'), 3),
                Operator('ラヴァ', ('術師タイプ', '遠距離', '範囲攻撃'), 3),
            },
            '火力': {
                Operator('ムース', ('前衛タイプ', '近距離', '火力'), 4),
                Operator('メテオ', ('狙撃タイプ', '遠距離', '火力', '弱化'), 4)
            },
            '弱化': {
                Operator('メテオ', ('狙撃タイプ', '遠距離', '火力', '弱化'), 4)
            },
            '生存': {
                Operator('ポプカル', ('前衛タイプ', '近距離', '範囲攻撃', '生存'), 3)
            }
        }

        assert invert_operator_list(operator_list) == expected_result
