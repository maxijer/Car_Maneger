import requests
from bs4 import BeautifulSoup as bs

response = requests.get("https://auto.ru/catalog/cars/audi/s5/21746753/21747079/specifications/")
htmlka = bs(response.content, 'html.parser')
haracteristika = list()
for niga in htmlka.select(".list-values__label"):
    haracteristika.append(str(niga).split('>')[1].split('<')[0])
for j in haracteristika:
    print(j)

r = requests.get("https://auto.ru/catalog/cars/")
html = bs(r.content, 'html.parser')
all_marks_ssilka = list()
horact = list()
for el in html.select('.search-form-v2-list__text-item'):
        marka = str(el).split()
        if 'href=' in marka[-2]:
            z = marka[-2]
            bad_ssilka = z.split("=")[1]
            norm_ssilka = bad_ssilka[1:-1]
            all_marks_ssilka.append(norm_ssilka)
        else:
            z = marka[-3]
            bad_ssilka = z.split("=")[1]
            norm_ssilka = bad_ssilka[1:-1]
            all_marks_ssilka.append(norm_ssilka)
        print(norm_ssilka)

d = dict()
for i in all_marks_ssilka:
    a = i.split('/')
    d[a[-2]] = list()
    rz = requests.get(i)
    html5 = bs(rz.content, 'html.parser')
    for el in html5.select('.brand-info__logo'):
        d[a[-2]].append(str(el).split(' ')[-1].split('/>')[-2].split("src=")[-1][1:-1])
        print(str(el).split(' ')[-1].split('/>')[-2].split("src=")[-1][1:-1])

for j in all_marks_ssilka:
    r2 = requests.get(j)
    html_2 = bs(r2.content, 'html.parser')
    slovar = list()
    for el in html_2.select('.search-form-v2-list__text-item'):
        marka = str(el).split()
        if 'href=' in marka[-2]:
            z = marka[-2]
            bad_ssilka = z.split("=")[1]
            norm_ssilka = bad_ssilka[1:-1]
            r3 = requests.get(norm_ssilka)
            html_3 = bs(r3.content, 'html.parser')
            for niga in html_3.select('.catalog-all-text-list__desc'):
                pochti = str(niga).split()
                for i in pochti:
                    if "href=" in i and not "used" in i:
                        har = i.split('=')[1][1:-1] + "specifications/"
                        if not har in horact:
                            horact.append(i.split('=')[1][1:-1] + "specifications/")
                            print(i.split('=')[1][1:-1] + "specifications/")
for i in horact:
    mark = i.split('/')[5]
    name = i.split('/')[6:-2]
    print(' '.join(name))
    response = requests.get(i)
    htmlka = bs(response.content, 'html.parser')
    count = 0
    d1 = {
        'mark': mark,
        'name': ' '.join(name)
    }
    for niga in htmlka.select(".list-values__value"):
        try:
            d1[haracteristika[count]] = str(niga).split('>')[1].split('<')[0]
        except IndexError:
            pass
        count += 1
    q = i.split('/')[:-2]
    new = '/'.join(q)
    print(new)
    response = requests.get(new)
    htmlka = bs(response.content, 'html.parser')
    count = 0
    for niga in htmlka.select(".photo-gallery__photo")[:1]:
        print(str(niga))
        try:
            d1['photo'] = str(niga).split()[3].split(')')[0].split('(')[1]
        except IndexError:
            pass
    try:
        d[mark].append(d1)
    except KeyError:
        pass
print(d)
for i in d.values():
    for j in i:
        print(j)
