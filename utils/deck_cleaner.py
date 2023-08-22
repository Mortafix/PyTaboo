from os import mkdir, path, walk

from yaml import safe_dump, safe_load

base_folder = "assets/deck"

if not path.exists(path.join(base_folder, "cleaned")):
    mkdir(path.join(base_folder, "cleaned"))

files = [file for file in list(walk(base_folder))[0][2] if file.endswith(".yaml")]
for file in files:
    with open(path.join(base_folder, file)) as f:
        content = f.read()
        total_words = len(content.split("\n"))
        print(f"> Reading '{file}': {total_words} words")
        words = {str(word): taboo for word, taboo in safe_load(content).items()}
        words_capitalize = {
            word[0].upper() + word[1:]: taboo for word, taboo in words.items()
        }
    with open(path.join(base_folder, "cleaned", file), "w+") as new_file:
        safe_dump(words_capitalize, new_file)
        print(f"> Cleaned '{file}': {len(words_capitalize)} words")
    taboo_n = dict()
    for taboo in words_capitalize.values():
        taboo_n[len(taboo)] = taboo_n.get(len(taboo), 0) + 1
    print(f"  # stats {taboo_n}")
    print("-" * 10)
