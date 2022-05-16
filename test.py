import re
with open(r'F:\社工库数据\geckosupervpn_signinuser.cql', 'r', encoding='utf-8') as file:
    for f in file:
        try:
            values = re.findall(r'VALUES \((.*?)\);', f)[0]
        except IndexError:
            continue
        value_list = [i.replace("'", '') for i in values.split(', ')]
        print(value_list)



