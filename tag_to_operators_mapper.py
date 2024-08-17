def main():
    file_name = 'operators_in_recruitment_with_rarity.csv'
    operator_list = load_operator_list(file_name)

def load_tag_list(file_name: str) -> list[str]:
    with open(file_name, 'r') as file:
        content = file.read()
        all_tag: list[str] = content.split('\n')
        return all_tag

def load_operator_list(file_name: str) -> list[tuple[str, list[str], int]]:
    import csv

    res = []
    all_tag = load_tag_list('all_tag.txt')

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags = split_string_by_tags(row['募集タグ'], all_tag)
            res.append((row['名前'],tags,int(row['レアリティ'])))

    return res

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
