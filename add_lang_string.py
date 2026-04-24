#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Add "Language:" string to translations

hi_trans = {
    "Language:": "भाषा:",
}

mr_trans = {
    "Language:": "भाषा:",
}

# Update Hindi
with open('translations/hi/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
    hi_content = f.read()

for eng, hin in hi_trans.items():
    if f'msgid "{eng}"' not in hi_content:
        hi_content = hi_content.rstrip() + f'\n\nmsgid "{eng}"\nmsgstr "{hin}"\n'

with open('translations/hi/LC_MESSAGES/messages.po', 'w', encoding='utf-8') as f:
    f.write(hi_content)

# Update Marathi
with open('translations/mr/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
    mr_content = f.read()

for eng, mar in mr_trans.items():
    if f'msgid "{eng}"' not in mr_content:
        mr_content = mr_content.rstrip() + f'\n\nmsgid "{eng}"\nmsgstr "{mar}"\n'

with open('translations/mr/LC_MESSAGES/messages.po', 'w', encoding='utf-8') as f:
    f.write(mr_content)

print("Added 'Language:' translation")
