'''
募集タグの組合せから星４以上のオペレーターが確定する組合せを探すモジュール
'''

from collections import defaultdict
from typing import NamedTuple
import logging
import csv


class Operator(NamedTuple):
    '''
    オペレーターを表すオブジェクト
    '''
    name: str
    tags: tuple[str, ...]
    rarity: int


def main():
    '''
    メイン関数
    '''
    file_name = 'operators_in_recruitment_with_rarity.csv'
    operator_list: list[Operator] = load_operator_list(file_name)
    tag_to_operators: dict[str, set[Operator]] = invert_operator_list(operator_list)

    tag_list = ['牽制', '火力', '狙撃タイプ', '防御', '範囲攻撃']
    res: list[dict[tuple[str, ...], list[Operator]]] = find_rare_operator_tag_combinations(tag_list, tag_to_operators)
    print(*res, sep='\n')


def find_rare_operator_tag_combinations(
        tag_list: list[str],
        tag_to_operators: dict[str, set[Operator]]
) -> list[dict[tuple[str, ...], list[Operator]]]:
    '''
    募集タグの組合せから星４以上のオペレーターが確定する組合せを探す

    Args:
        tag_list (list[str]): 募集タグのリスト（５つを想定）
        tag_to_operators (dict[str, set[Operator]]): {募集タグ: そのタグを持つオペレーターの集合}

    Returns:
        list[dict[tuple[str, ...], list[Operator]]]:
            募集タグの組合せ→その組合せで出るオペレーターのリスト、のリスト
    '''
    if len(tag_list) < 5:
        logging.warning(f'募集タグの個数が少ないです: {len(tag_list)}個')
    tag_list.sort()

    res = []

    for comb in range(1 << len(tag_list)):
        tags_in_comb: list[str] = []
        set_op: set[Operator] | None = None
        for i in range(len(tag_list)):
            if comb & (1 << i) > 0:
                set_op = tag_to_operators[tag_list[i]] if set_op is None else (set_op & tag_to_operators[tag_list[i]])
                tags_in_comb.append(tag_list[i])
        if set_op and all(map(lambda op: op.rarity > 3, set_op)):
            ops = sorted(list(set_op))
            if '上級エリート' not in tags_in_comb:
                ops = list(filter(lambda op: op.rarity < 6, ops))
            if ops:
                res.append({tuple(tags_in_comb): ops})

    return res


def load_tag_list(file_name: str) -> list[str]:
    '''
    全てのタグが書かれたファイルから全てのタグのリストを作成
    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        all_tag: list[str] = content.split('\n')
        return all_tag


def load_operator_list(file_name: str) -> list[Operator]:
    '''
    公開求人で手に入るオペレーターのCSVからオペレーターのリストを作成
    '''
    res = []
    all_tag = load_tag_list('all_tag.txt')

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags = split_string_by_tags(row['募集タグ'], all_tag)
            tags.append(f'{row['職業']}タイプ')
            if row['レアリティ'] == '6':
                tags.append('上級エリート')
            elif row['レアリティ'] == '5':
                tags.append('エリート')
            else:
                pass
            res.append(Operator(row['名前'], tuple(tags), int(row['レアリティ'])))

    return res


def invert_operator_list(operator_list: list[Operator]) -> dict[str, set[Operator]]:
    '''
    オペレーターが持つ募集タグのリストから、ある募集タグを持つオペレーターの逆対応を作る
    '''
    tag_to_operators: dict[str, set[Operator]] = defaultdict(set)
    for op in operator_list:
        for tag in op.tags:
            tag_to_operators[tag].add(op)
    return tag_to_operators


def split_string_by_tags(s: str, all_tag: list[str]) -> list[str]:
    '''
    空白無しで結合された複数の募集タグの文字列から、募集タグを分割したリストを作成
    '''
    result = []
    while s:
        match = next(word for word in all_tag if s.startswith(word))
        result.append(match)
        s = s[len(match):]
    result.sort()
    return result


if __name__ == '__main__':
    main()
