"""募集タグの組合せから星４以上のオペレーターが確定する組合せを探すモジュール"""

from collections import defaultdict
from typing import NamedTuple
import logging
import csv


class Operator(NamedTuple):
    """オペレーターを表すオブジェクト"""
    name: str
    tags: tuple[str, ...]
    rarity: int


def main() -> None:
    """メイン関数"""
    file_name = 'operators_in_recruitment_with_rarity.csv'
    operator_list: list[Operator] = load_operator_list(file_name)
    tag_to_operators: dict[str, set[Operator]] = invert_operator_list(operator_list)

    tag_list = ['牽制', '火力', '狙撃タイプ', '防御', '範囲攻撃']
    res = find_rare_operator_tag_combinations(tag_list, tag_to_operators)
    print(*res.items(), sep='\n')


def obtain_result_message(tag_list: list[str]) -> str:
    """結果を求めて、Discordに返信するメッセージを生成する"""
    file_name = 'operators_in_recruitment_with_rarity.csv'
    operator_list: list[Operator] = load_operator_list(file_name)
    tag_to_operators: dict[str, set[Operator]] = invert_operator_list(operator_list)
    rare_op_tag_combinations = find_rare_operator_tag_combinations(tag_list, tag_to_operators)

    if not rare_op_tag_combinations:
        return '星4以上が確定する組合せは見つかりませんでした…'

    result_mes = ''

    for tag_comb, operator_list in rare_op_tag_combinations.items():
        tag_comb_str = ', '.join(tag_comb)
        ope_list_str = ', '.join(map(lambda op: op.name, operator_list))
        result_mes += f'タグの組合せ: {tag_comb_str}\n出現するオペレーター: {ope_list_str}\n'

    return result_mes


def get_tag_list(texts: str) -> list[str]:
    """画像から抽出されたテキストからタグの文字列だけを抜き出したリストを作成"""
    all_tag = load_tag_list('all_tag.txt')

    tag_list = []

    for tag in all_tag:
        if tag in texts:
            tag_list.append(tag)

    if len(tag_list) < 5:
        logging.warning('タグの個数が少ないです: %s', len(tag_list))
    if len(tag_list) > 5:
        logging.warning('タグの個数が多すぎます: %s', len(tag_list))

    return tag_list


def find_rare_operator_tag_combinations(
        tag_list: list[str],
        tag_to_operators: dict[str, set[Operator]]
) -> dict[tuple[str, ...], list[Operator]]:
    """
    募集タグの組合せから星４以上のオペレーターが確定する組合せを探す

    Args:
        tag_list (list[str]): 募集タグのリスト（５つを想定）
        tag_to_operators (dict[str, set[Operator]]): {募集タグ: そのタグを持つオペレーターの集合}

    Returns:
        list[dict[tuple[str, ...], list[Operator]]]:
            募集タグの組合せ→その組合せで出るオペレーターのリスト、のリスト
    """
    if len(tag_list) < 5:
        logging.warning('募集タグの個数が少ないです: %s個', len(tag_list))
    tag_list.sort()

    res = dict()

    for comb in range(1 << len(tag_list)):
        tags_in_comb: list[str] = []
        set_op: set[Operator] | None = None
        for i, tag in enumerate(tag_list):
            if comb & (1 << i) > 0:
                set_op = tag_to_operators[tag] if set_op is None else \
                    set_op & tag_to_operators[tag]
                tags_in_comb.append(tag)
        if set_op and all(map(lambda op: op.rarity > 3, set_op)):
            ops = sorted(list(set_op))
            if '上級エリート' not in tags_in_comb:
                ops = list(filter(lambda op: op.rarity < 6, ops))
            if ops:
                res[tuple(tags_in_comb)] = ops

    return res


def load_tag_list(file_name: str) -> list[str]:
    """全てのタグが書かれたファイルから全てのタグのリストを作成"""
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        all_tag: list[str] = content.split('\n')
        all_tag = list(filter(lambda x: x, all_tag))  # 空文字列を取り除く
        return all_tag


def load_operator_list(file_name: str) -> list[Operator]:
    """公開求人で手に入るオペレーターのCSVからオペレーターのリストを作成"""
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
    """オペレーターが持つ募集タグのリストから、ある募集タグを持つオペレーターの逆対応を作る"""
    tag_to_operators: dict[str, set[Operator]] = defaultdict(set)
    for op in operator_list:
        for tag in op.tags:
            tag_to_operators[tag].add(op)
    return tag_to_operators


def split_string_by_tags(s: str, all_tag: list[str]) -> list[str]:
    """
    空白無しで結合された複数の募集タグの文字列から、募集タグを分割したリストを作成

    Args:
        s: タグ同士が結合された文字列

    Returns:
        募集タグ１つずつに分解されたリスト

    Examples:
        >>> split_string_by_tags('近距離火力支援', all_tag)
        ['支援', '火力', '近距離']
    """
    result: list[str] = []
    original_s = s
    while s:
        tag_match: str | None = None
        index_match: int = -1
        for tag in all_tag:
            if tag and s.find(tag) > -1:
                tag_match = tag
                index_match = s.find(tag)
                break
        if tag_match is None:
            break
        result.append(tag_match)
        s = s[:index_match] + s[index_match + len(tag_match):]
    if s:
        logging.warning('想定外の募集タグ文字列です: %s', original_s)
    result.sort()
    return result


if __name__ == '__main__':
    main()
