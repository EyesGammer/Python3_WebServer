# POSTs method functions
def postExample(datas, page):
    print(f"POST {datas}")
    return page
# GETs method functions
def getExample(datas, page):
    print(f"GET {datas}")
    return page
# Other functions ( for settings.py or for this file usage )
def plus():
    return "Ceci est un test"
post_files = {
        #"index.html": postExample
        }
get_files = {
        #"index.html": getExample
        }
