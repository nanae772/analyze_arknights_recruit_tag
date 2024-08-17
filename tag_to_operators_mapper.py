from collections import defaultdict, namedtuple
Operator = namedtuple('Operator', ['name', 'tags', 'rarity'])

def main():
    file_name = 'operators_in_recruitment_with_rarity.csv'
    operator_list = load_operator_list(file_name)
    tag_to_operators = invert_operator_list(operator_list)
    print(tag_to_operators)

def load_tag_list(file_name: str) -> list[str]:
    with open(file_name, 'r') as file:
        content = file.read()
        all_tag: list[str] = content.split('\n')
        return all_tag

def load_operator_list(file_name: str) -> list[Operator]:
    import csv

    res = []
    all_tag = load_tag_list('all_tag.txt')

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags = split_string_by_tags(row['募集タグ'], all_tag)
            if row['レアリティ'] == '6':
                tags.append('上級エリート')
            elif row['レアリティ'] == '5':
                tags.append('エリート')
            else:
                pass
            res.append(Operator(row['名前'],tags, row['レアリティ']))

    return res

def invert_operator_list(operator_list: list[Operator]) -> dict[str, set]:
    tag_to_operators: dict[str, set[str]] = defaultdict(set)
    for op in operator_list:
        for tag in op.tags:
            tag_to_operators[tag].add(op.name)
    return tag_to_operators


def split_string_by_tags(s: str, all_tag: list[str]) -> list[str]:
    result = []
    while s:
        match = next(word for word in all_tag if s.startswith(word))
        result.append(match)
        s = s[len(match):]
    result.sort()
    return result

if __name__ == '__main__':
    main()
