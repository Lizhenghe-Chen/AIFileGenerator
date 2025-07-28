from mailmerge import MailMerge
#相对路径
template = "WordGenProject\\template.docx"
document = MailMerge(template)

print("模板字段：", document.get_merge_fields())

document.merge(
    name='david',
    birthday='1990-01-01',
    intro='''我是一名Python工程师，热爱开源。''',
    weight='70公斤'
)

document.write('output.docx')