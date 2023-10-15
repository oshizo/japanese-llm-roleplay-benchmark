import os


def download_erp_file():
    if not os.path.exists("./situations_erp.jsonl"):
        import urllib.request

        urllib.request.urlretrieve(
            "https://furoriented.org/erp/situations_erp.jsonl", "situations_erp.jsonl"
        )


def download_erp_response(filename):
    if not os.path.exists(f"./responses_erp/{filename}"):
        import urllib.request

        urllib.request.urlretrieve(
            f"https://furoriented.org/erp/responses_erp/{filename}",
            f"./responses_erp/{filename}",
        )


def postprocess(text, character_name, n_sentences=1):
    # セリフと地の文を最大n_sentencesまで取得して返す

    text = f"{character_name}「" + text

    inside_quote = False
    current_sentence = ""
    sentences = []  # キャプチャしたセリフ、地の文を保存するリスト

    for char in text:
        # セリフの内部か外部かをトラッキング
        if char == "「":
            inside_quote = True
        elif char == "」":
            inside_quote = False
            current_sentence += char
            sentences.append(current_sentence)
            current_sentence = ""
            continue
        elif not inside_quote and char == "。":
            current_sentence += char
            sentences.append(current_sentence)
            current_sentence = ""
            continue

        current_sentence += char

    # 2文以上返す場合、文中で途切れている中途半端な生成は追加しない
    if n_sentences == 1:
        sentences.append(current_sentence)

    # センテンスから最初の2つを抽出し、結合
    return "".join(sentences[:n_sentences])
