
import sys
import time
from collections import Counter
import xml.etree.ElementTree as ET

num_spaces_in_tab = 2
input_file = sys.argv[1] if len(sys.argv) >= 2 else "my_day.xml"
output_file = sys.argv[2] if len(sys.argv) >= 3 else "my_day_2.yaml"
time_file = sys.argv[3] if len(sys.argv) >= 4 else "check_time.txt"

XML_NODE_CONTENT = "_xml_node_content"

#node - вершина
#result - массив строк
#num_spaces - текущий отступ
#node_attrs - атрибуты вершины
#content - содержимое текущей вершины
#children - дети вершины
def process(node, result: list, num_spaces=0):
    # Блоки как с содержимым, так и с вложенными блоками или атрибутами
    # Не имеют корректного сопоставления с yaml. Добавим блок "content" для этого случая
    node_attrs = node.attrib
    children = list(node)
    content = node.text.strip() if node.text else ''

    if node.tag.startswith("~"):
        result.append(" " * num_spaces + "-")
        node.tag = node.tag[1:]

    if content:
        if not node_attrs and not children:
            # Записываем как name: value, больше ничего вложенного
            result.append(
                "%s%s: %s" % (
                    " " * num_spaces, node.tag, content
                )
            )

            return result
        else:
            node_attrs[XML_NODE_CONTENT] = node.text

    result.append(" " * num_spaces + node.tag + ":")

    # Укажем различия атрибутов и вложенных блоков
    num_spaces += num_spaces_in_tab
    for key, value in node_attrs.items():
        result.append(
            "%s%s%s: %s" % (
                " " * num_spaces,
                "_" if key != XML_NODE_CONTENT else "",
                key, value
            )
        )
    child_tags = Counter([child.tag for child in children])

    for child in children:
        if child_tags[child.tag] > 1:
            child.tag = "~" + child.tag

        result = process(child, result, num_spaces)

    return result


if __name__ == '__main__':
    start_time = time.time()

    for _ in range(10):
        tree = ET.parse(input_file)
        result = process(tree.getroot(), [])
        #импорт xml файла

        with open(output_file, "w") as yaml_file:
            yaml_file.write("\n".join(result))

    with open(time_file, "a") as file:
        file.write(
            "---- Test Two ----\n%s sec\n" % (
                (time.time() - start_time) / 10
            )
        )
