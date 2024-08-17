def main():
    load_operator_list('operators_in_recruitment.csv')

def load_tag_list(file_name: str) -> list[str]:
    with open(file_name, 'r') as file:
        content = file.read()
        all_tag: list[str] = content.split('\n')
        return all_tag

def load_operator_list(file_name: str) -> list[tuple]:
    import csv

    res = []

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            res.append((row['名前'],row['募集タグ']))

    print(*res,sep='\n')

    return res

def split_string_by_tags(s: str, all_tag: list[str]) -> list[str]:
    result = []
    while s:
        match = next(word for word in all_tag if s.startswith(word))
        result.append(match)
        s = s[len(match):]
    return result

if __name__ == '__main__':
    main()
