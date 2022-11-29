
import re
import sys
import time
from collections import Counter
import xml.etree.ElementTree as ET

num_spaces_in_tab = 2
input_file = sys.argv[1] if len(sys.argv) >= 2 else "my_day.xml"
output_file = sys.argv[2] if len(sys.argv) >= 3 else "my_day_1.yaml"
time_file = sys.argv[3] if len(sys.argv) >= 4 else "check_time.txt"


def get_data():
    # Считываем файл
    text = open(input_file, encoding="utf-8").read()

    return text.split("\n")

#row - исходная строка
#result - массив строк
#cur_spaces - текущий отступ
#spaces_tags - все отступы тегов в текущем блоке

def process_row(row: str, result: list, cur_spaces: int, spaces_tags: dict):
    row = row.strip()

    if not row or row.startswith("<?xml"):
        return result, cur_spaces, spaces_tags
    elif row.startswith("<") and not row.startswith("</"):
        cur_spaces += num_spaces_in_tab

        if cur_spaces not in spaces_tags:
            spaces_tags[cur_spaces] = []

        # end_tag_index - индекс конца тега
        # full_tag - тег без <>

        end_tag_index = row.index(">")
        full_tag = row[1:end_tag_index]
        self_closing = False

        if full_tag[-1] == "/":
            self_closing = True
            full_tag = full_tag[:-1]
        #full_tag_info - массив тега и атрибутов

        full_tag_info = full_tag.split()
        tag = full_tag_info.pop(0)

        if spaces_tags[cur_spaces].count(tag) == 1:
            for ind in range(len(result) - 1, -1, -1):
                previous_row = result[ind].strip()


                if previous_row.startswith(tag):
                    result.insert(ind, " " * cur_spaces + "-")
                    break

        if tag in spaces_tags[cur_spaces]:
            result.append(" " * cur_spaces + "-")

        result.append(" " * cur_spaces + tag + ":")
        spaces_tags[cur_spaces].append(tag)


        #key и value означают атрибут и его значение
        for param in full_tag_info:
            key, value = param.split("=")
            result.append("%s_%s: %s" % (
                " " * (cur_spaces + num_spaces_in_tab),
                key, value.replace('"', "")
            ))

        cur_spaces -= num_spaces_in_tab if self_closing else 0

        if end_tag_index != len(row) - 1:
            result, cur_spaces, spaces_tags = process_row(
                row[end_tag_index + 1:], result, cur_spaces, spaces_tags
            )
    elif row.startswith("</"):
        previous_row = result[-1].strip()

        if not row.startswith(previous_row.replace(":", "")):
            spaces_tags[cur_spaces + num_spaces_in_tab] = []
        else:
            result.pop()
        cur_spaces -= num_spaces_in_tab

        end_tag_index = row.index(">")
        if end_tag_index != len(row) - 1:
            result, cur_spaces, spaces_tags = process_row(
                row[end_tag_index + 1:], result, cur_spaces, spaces_tags
            )
    else:
        end_index = row.index("<") if "<" in row else len(row)
        result.append(
            " " * (cur_spaces + num_spaces_in_tab) +
            "- " + row[:end_index]
        )

        if end_index != len(row):
            result, cur_spaces, spaces_tags = process_row(
                row[end_index:], result, cur_spaces, spaces_tags
            )

    return result, cur_spaces, spaces_tags


def process(first_row):
    result = []
    cur_spaces = -2
    spaces_tags = {}
    row = first_row

    while row is not None:
        result, cur_spaces, spaces_tags = process_row(
            row, result, cur_spaces, spaces_tags
        )
        row = (yield)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    yield


def main():
    data = get_data()

    if len(data) > 0:
        main_process = process(data.pop(0))
        next(main_process)

        for row in data:
            main_process.send(row)

        main_process.send(None)


if __name__ == '__main__':
    start_time = time.time()

    for _ in range(10):
        main()


    with open(time_file, "a") as file:
        file.write(
            "---- Test One ----\n%s sec\n" % (
                time.time() - start_time
            )
        )