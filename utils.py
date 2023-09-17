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
