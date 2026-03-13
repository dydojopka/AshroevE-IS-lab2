import re
from collections import Counter

# русский алфавит (без Ё) + пробел
alphabet = " абвгдежзийклмнопрстуфхцчшщъыьэюя"
m = len(alphabet)

# частоты букв русского языка
freq = {
' ':0.146,'о':0.094,'е':0.071,'а':0.069,'и':0.064,'н':0.057,'т':0.054,
'с':0.046,'р':0.042,'л':0.039,'в':0.038,'к':0.029,'м':0.027,'п':0.026,
'д':0.024,'у':0.023,'я':0.017,'з':0.017,'ы':0.015,'г':0.014,'б':0.013,
'ь':0.013,'ч':0.012,'й':0.010,'х':0.008,'ж':0.007,'ш':0.006,'ц':0.005,
'ю':0.005,'щ':0.004,'ф':0.003,'э':0.002,'ъ':0.001
}

# индексы букв
index = {c:i for i,c in enumerate(alphabet)}


# дешифрование
def decrypt(text, key):

    res = ""
    j = 0

    for c in text:

        if c not in index:
            res += c
            continue

        k = key[j % len(key)]
        j += 1

        p = (index[c] - k) % m
        res += alphabet[p]

    return res


# критерий x^2
def chi_square(text):

    n = len(text)
    counter = Counter(text)

    score = 0

    for c in alphabet:

        observed = counter.get(c,0)
        expected = freq.get(c,0) * n

        if expected > 0:
            score += (observed - expected) ** 2 / expected

    return score


# поиск ключа
def find_key(text, block):

    key = []

    for i in range(block):

        column = text[i::block]

        best_shift = 0
        best_score = 1e18

        for shift in range(m):

            decrypted = ""

            for c in column:

                if c in index:
                    p = (index[c] - shift) % m
                    decrypted += alphabet[p]

            score = chi_square(decrypted)

            if score < best_score:
                best_score = score
                best_shift = shift

        key.append(best_shift)

    return key


# ручное редактирование ключа
def edit_key(text, key):

    while True:

        key_str = "".join(alphabet[k] for k in key)

        decrypted = decrypt(text, key)

        print("\nКлюч:", key_str)
        print("\nФрагмент расшифрованного текста:\n")
        print(decrypted[:400])

        new_key = input(
            "\nВведите новый ключ (Enter - оставить текущий): "
        ).strip().lower()

        if new_key == "":
            return key

        try:

            key = [index[c] for c in new_key]

        except:
            print("Ошибка: используйте только русские буквы.")


# обработка файла
def process_file(mode):

    with open("input.txt","r",encoding="utf-8") as f:
        data = f.read()

    parts = re.split(r"\d+\.", data)[1:]

    outputs = []

    for part in parts:

        block = int(re.search(r"блок\s*-\s*(\d+)", part).group(1))

        text = re.sub(r"блок\s*-\s*\d+","",part)
        text = text.lower()

        text = re.sub(r"[^а-я ]","",text)

        key = find_key(text, block)

        # режим ручного редактирования
        if mode == "2":
            key = edit_key(text, key)

        decrypted = decrypt(text, key)

        key_str = "".join(alphabet[k] for k in key)

        outputs.append(
            f"Блок {block}\nКлюч: {key_str}\n{decrypted}\n\n"
        )

    with open("output.txt","w",encoding="utf-8") as f:
        f.write("\n".join(outputs))

    print("\nРасшифровка завершена. Результат записан в output.txt")


# главное меню
def main():

    print("\nРасшифровка гаммированного текста (алгоритм Вернона)\n")

    mode = input(
        "1 - автоматический подбор ключей\n"
        "2 - подбор ключей с ручной корректировкой\n"
        "Выберите режим: "
    )

    process_file(mode)


main()