import os


def download_erp_file():
    if not os.path.exists("./situations_erp.jsonl"):
        import urllib.request

        urllib.request.urlretrieve(
            "https://furoriented.org/erp/situations_erp.jsonl", "situations_erp.jsonl"
        )
