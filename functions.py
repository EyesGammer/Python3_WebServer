# POSTs method functions
def test(datas, page):
    print(f"POST {datas}")
    return page
# GETs method functions
def autre(datas, page):
    print(f"GET {datas}")
    return page
# Other functions ( for settings.py or for this file usage )
def plus():
    return "Ceci est un test"
post_files = {
        "index.html": test
        }
get_files = {
        "index.html": autre
        }
