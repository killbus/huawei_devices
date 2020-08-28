#!/usr/bin/env python3.7
"""Huawei Devices Models Info scrapper"""

import re
import json
from requests import get
import yaml
from pathlib import Path

DEVICES = {}
HERE = Path(__file__).parent
DATA_DIR = HERE / 'data/'

def main():
    for brand in ['huawei', 'huawei_global_en', 'honor', 'honor_global_en']:
        dumper(brand)

def dumper(brand='huawei'):
    """
    scrapes Huawei devices md into yaml and json
    """
    DEVICES = {}
    data = get("https://raw.githubusercontent.com/KHwang9883/MobileModels/" +
               f"master/brands/{brand}.md").text
    data = [i for i in data.splitlines() if not str(i).startswith('#') and i]
    data = '\n'.join(data).replace('\n\n', '\n').replace('\n\n', '\n')
    devices = re.findall(r"\*(?:[\s\S]*?)\n\*|\*(?:[\s\S]*?)\Z", data, re.MULTILINE)
    for item in devices:
        info = {}
        details = item.split('*')
        details = [i for i in details if i]
        try:
            codename = details[0].split('(`')[1].split('`)')[0].strip()
        except IndexError:
            codename = ''
        try:
            details[0].index('(')
            name = details[0].split('(')[0].strip()
        except ValueError:
            name = details[0].split(':')[0].strip()
        models = details[1].replace('\n\n', '\n').strip().splitlines()
        info.update({"codename": codename})
        info.update({"name": name})
        # models_ = {}
        for i in models:
            for model in map(str.strip, i.split(':')[0].strip().split(',')):
                model = re.sub(r'HUAWEI ?', '', model, re.IGNORECASE)
                model_name = i.split(':')[1].strip()
                model_info = dict(info) # do a copy
                model_info.update({"model_name": model_name})
                
                DEVICES.update({model: model_info})

    # print(DEVICES)
    with open(f'{DATA_DIR / brand}.json', 'w') as output:
        json.dump(DEVICES, output, indent=1, ensure_ascii=False)
    with open(f'{DATA_DIR / brand}.yml', 'w') as output:
        yaml.dump(DEVICES, output, allow_unicode=True)


if __name__ == '__main__':
    main()
