"""Build the three-way workflow adapted from the user-supplied reference.
Reference: https://www.icloud.com/shortcuts/48c45bf28b50473f82c818d5977d1a14
Requires macOS signing separately; the Live branch needs Live Shortcuts on iPhone.
"""
import copy
import plistlib
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = []
def uid(): return str(uuid.uuid4()).upper()
def add(kind, **p):
    p.setdefault('UUID', uid())
    A.append({'WFWorkflowActionIdentifier': 'is.workflow.actions.' + kind, 'WFWorkflowActionParameters': p})
    return p['UUID']
def out(u, name='结果'): return {'Value': {'Type': 'ActionOutput', 'OutputUUID': u, 'OutputName': name}, 'WFSerializationType': 'WFTextTokenAttachment'}
def var(n): return {'Value': {'Type': 'Variable', 'VariableName': n}, 'WFSerializationType': 'WFTextTokenAttachment'}
def text(*parts):
    string = ''; attachments = {}
    for part in parts:
        if isinstance(part, str): string += part
        else:
            offset = len(string.encode('utf-16-le')) // 2
            attachments['{%d, 1}' % offset] = part['Value']
            string += '\ufffc'
    return {'Value': {'string': string, 'attachmentsByRange': attachments}, 'WFSerializationType': 'WFTextTokenString'}
def key(value, name): return add('getvalueforkey', WFInput=value, WFDictionaryKey=name, WFGetDictionaryValueType='Value')
def count(value): return add('count', Input=value, WFCountType='Items')
def cond(value, code, number):
    value = copy.deepcopy(value)
    value['Value']['Aggrandizements'] = [{'Type':'WFCoercionVariableAggrandizement','CoercionItemClass':'WFNumberContentItem'}]
    g = uid(); add('conditional', WFInput={'Type': 'Variable', 'Variable': value}, WFCondition=code, WFNumberValue=str(number), WFControlFlowMode=0, GroupingIdentifier=g); return g
def end(g): return add('conditional', WFControlFlowMode=2, GroupingIdentifier=g)
def error(message):
    add('alert', WFAlertActionTitle='未完成保存', WFAlertActionMessage=message, WFAlertActionCancelButtonShown=False); add('exit')
def require(value, message):
    c = count(value); g = cond(out(c), 4, 0); error(message); end(g)
def first(value): return add('getitemfromlist', WFInput=value, WFItemSpecifier='First Item')
def dictionary_fields(values):
    items = [{'WFKey':text(k), 'WFItemType':0, 'WFValue':text(v)} for k,v in values.items()]
    return {'Value': {'WFDictionaryFieldValueItems':items}, 'WFSerializationType':'WFDictionaryFieldValue'}
def app(intent, **params):
    u = uid(); params.update(UUID=u, AppIntentDescriptor={'TeamIdentifier':'857QPT2KGL','BundleIdentifier':'jiejing.fun.JustLive','Name':'实况捷径','AppIntentIdentifier':intent})
    A.append({'WFWorkflowActionIdentifier':'jiejing.fun.JustLive.'+intent,'WFWorkflowActionParameters':params}); return u
def loop(value):
    g=uid(); add('repeat.each',WFInput=value,WFControlFlowMode=0,GroupingIdentifier=g); return g
def loop_end(g): return add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=g)
def split(value): return add('text.split',text=value,WFTextSeparator='New Lines')
def choose(value, prompt): return add('choosefromlist',WFInput=value,WFChooseFromListActionPrompt=prompt,WFChooseFromListActionSelectMultiple=True,WFChooseFromListActionSelectAll=True)
def url_https(value): return add('text.replace',WFInput=text(value),WFReplaceTextFind='http://',WFReplaceTextReplace='https://',WFReplaceTextRegularExpression=False)

add('comment', WFCommentActionText='V4：参考用户提供的“空什么格 / 小红书下载器”指令。先分流 Live / 图片 / 视频，再解析、选择和保存。沿用其 qsy.jiejing.fun / a.jiejing.fun 服务与实况捷径动作，受作者服务及 App 额度限制。Live 传入独立封面和视频地址，不再使用 Actions。没有在 iPhone 验证保存，不承诺所有动态源无水印。')
u=add('gettext',WFTextActionText=''); add('setvariable',WFInput=out(u),WFVariableName='授权码')
add('comment',WFCommentActionText='上方文本留空使用参考服务的免费额度；已有作者授权码可填入。Live 需要安装“实况捷径”App，正常使用其免费额度/会员，不绕过限制。')
links=add('detect.link',WFInput=text({'Value':{'Type':'ExtensionInput'},'WFSerializationType':'WFTextTokenAttachment'}))
require(out(links),'请复制小红书笔记分享链接，或从分享表单运行。')
u=first(out(links)); add('setvariable',WFInput=out(u),WFVariableName='笔记链接')
c=add('downloadurl',WFURL='https://qsy.jiejing.fun/xhs.json',WFHTTPMethod='GET')
c=add('detect.dictionary',WFInput=out(c)); add('setvariable',WFInput=out(c),WFVariableName='服务配置')
mg=uid();add('choosefrommenu',WFMenuPrompt='先选择要获取的内容',WFMenuItems=['Live 实况图','图片','视频'],WFControlFlowMode=0,GroupingIdentifier=mg)
for mode,title in [(1,'Live 实况图'),(2,'图片'),(3,'视频')]:
    add('choosefrommenu',WFMenuItemTitle=title,WFControlFlowMode=1,GroupingIdentifier=mg)
    n=add('number',WFNumberActionNumber=str(mode));add('setvariable',WFInput=out(n),WFVariableName='保存类型')
    if mode==1:
        add('alert',WFAlertActionTitle='Live 实况图',WFAlertActionMessage='需要先安装并打开“实况捷径”App。此分支会把独立封面与动态视频配对并由 App 保存到相册。',WFAlertActionCancelButtonShown=True)
        cred=app('EncryptExtension')
        endpoint=key(var('服务配置'),'livexhs')
        resp=add('downloadurl',WFURL=text(out(endpoint)),WFHTTPMethod='POST',WFHTTPBodyType='JSON',WFJSONValues=dictionary_fields({'kl':var('授权码'),'url':var('笔记链接'),'payload':out(cred)}))
    else:
        headers={}
        if mode==3:
            # Honor the reference service's high-quality video availability flag.
            available=key(var('服务配置'),'hdvideo'); gate=cond(out(available),5,0)
            error('参考服务当前暂停高清视频解析，请稍后重试或使用原作者指令的普通视频选项。');end(gate)
            # Matches the reference's 1080P/4K branch, including its service-provided Cookie.
            ckurl=key(var('服务配置'),'xhsck');ck=add('downloadurl',WFURL=text(out(ckurl)),WFHTTPMethod='GET')
            headers={'WFHTTPHeaders':dictionary_fields({'Cookie':out(ck)})}
        page=add('downloadurl',WFURL=text(var('笔记链接')),WFHTTPMethod='GET',**headers)
        page=add('gethtmlfromrichtext',WFInput=out(page),WFMakeFullDocument=False)
        endpoint=key(var('服务配置'),'xhshd' if mode==2 else 'hdvideoxhs')
        target=text(out(endpoint),'?url=',var('笔记链接'),'&v=13&kl=',var('授权码'))
        resp=add('downloadurl',WFURL=target,WFHTTPMethod='POST',WFHTTPBodyType='File',WFRequestVariable=out(page),**headers)
    add('setvariable',WFInput=out(resp),WFVariableName='解析响应')
add('choosefrommenu',WFControlFlowMode=2,GroupingIdentifier=mg)
d=add('detect.dictionary',WFInput=var('解析响应'));add('setvariable',WFInput=out(d),WFVariableName='解析结果')
code=key(var('解析结果'),'code');require(out(code),'解析服务没有返回结果状态，请重试。')
code=add('number',WFNumberActionNumber=out(code));g=cond(out(code),5,0)
msg=key(var('解析结果'),'msg');error(text('解析服务未成功：',out(msg)));end(g)
mode=add('getvariable',WFVariable=var('保存类型'));liveg=cond(out(mode),4,1)
# The reference returns one JSON pair per line in body.lives.
pairs=key(var('解析结果'),'body.lives');require(out(pairs),'解析结果没有 Live 封面和视频配对，请改选图片。')
pairs=split(out(pairs));add('setvariable',WFInput=out(pairs),WFVariableName='实况配对列表')
g=loop(out(pairs));pair=add('detect.dictionary',WFInput=var('Repeat Item'));pic=key(out(pair),'pic');require(out(pic),'某个实况项目没有封面地址，已停止。')
pic=url_https(out(pic));p=add('downloadurl',WFURL=text(out(pic)),WFHTTPMethod='GET')
p=add('setitemname',WFInput=out(p),WFName=text(var('Repeat Index'),'.jpg'),WFDontIncludeFileExtension=False)
thumbs=loop_end(g);require(out(thumbs),'没有下载到实况封面。')
selected=choose(out(thumbs),'选择要保存的 Live 实况图（可多选）');require(out(selected),'没有选择实况图，本次未保存。')
add('previewdocument',WFInput=out(selected))
g=loop(out(selected));name=add('getitemname',WFInput=var('Repeat Item'))
idx=add('text.match',text=text(out(name)),WFMatchTextPattern=r'^\d+',WFMatchTextCaseSensitive=True)
pair=add('getitemfromlist',WFInput=var('实况配对列表'),WFItemSpecifier='Item At Index',WFItemIndex=text(out(idx)))
pair=add('detect.dictionary',WFInput=out(pair));pic=key(out(pair),'pic');video=key(out(pair),'video')
require(out(pic),'所选实况没有封面地址。');require(out(video),'所选实况没有动态视频地址。')
# Exact action and parameter names from the user's reference, with original cover preserved.
r=app('LiveExtension',imageURL=text(out(pic)),videoURL=text(out(video)),albumName='')
status=add('detect.number',WFInput=out(r));require(out(status),'实况捷径没有返回保存状态，请检查 App 与照片权限。')
status=first(out(status));limited=cond(out(status),4,1)
error('实况捷径返回保存受限；可能已达到 App 额度。已保存的项目保留，请在 App 中检查额度和照片权限。');end(limited)
loop_end(g)
add('conditional',WFControlFlowMode=1,GroupingIdentifier=liveg)
urls=key(var('解析结果'),'body.urls');require(out(urls),'解析结果没有图片或视频下载地址。');urls=split(out(urls));add('setvariable',WFInput=out(urls),WFVariableName='媒体地址列表')
mode=add('getvariable',WFVariable=var('保存类型'));imageg=cond(out(mode),4,2)
# Preview and select first, then use the reference's image extraction/save action.
g=loop(out(urls));address=url_https(var('Repeat Item'));media=add('downloadurl',WFURL=text(out(address)),WFHTTPMethod='GET')
media=add('setitemname',WFInput=out(media),WFName=text(var('Repeat Index'),'.jpg'),WFDontIncludeFileExtension=False)
previews=loop_end(g);require(out(previews),'没有下载到图片预览。')
selected=choose(out(previews),'选择要保存到相册的图片（可多选）');require(out(selected),'没有选择图片，本次未保存。');add('previewdocument',WFInput=out(selected))
g=loop(out(selected));name=add('getitemname',WFInput=var('Repeat Item'))
idx=add('text.match',text=text(out(name)),WFMatchTextPattern=r'^\d+',WFMatchTextCaseSensitive=True)
address=add('getitemfromlist',WFInput=var('媒体地址列表'),WFItemSpecifier='Item At Index',WFItemIndex=text(out(idx)))
app('ResourceExtractionExtension',mediaURL=text(out(address)))
# This action saves directly; do not feed its empty return value to Photos.
add('nothing');loop_end(g)
add('conditional',WFControlFlowMode=1,GroupingIdentifier=imageg)
g=loop(out(urls));address=url_https(var('Repeat Item'));media=add('downloadurl',WFURL=text(out(address)),WFHTTPMethod='GET')
# Exact file naming strategy from the reference before Photos import.
rename=key(var('服务配置'),'Rename')
add('setitemname',WFInput=out(media),WFName=text(out(rename)),WFDontIncludeFileExtension=False)
media=loop_end(g);require(out(media),'没有取得可保存的视频文件。')
selected=choose(out(media),'选择要保存到相册的视频（可多选）');require(out(selected),'没有选择视频，本次未保存。')
add('previewdocument',WFInput=out(selected))
add('savetocameraroll',WFInput=out(selected))
end(imageg)
end(liveg)
root={'WFWorkflowMinimumClientVersion':1113,'WFWorkflowMinimumClientVersionString':'1113','WFWorkflowClientVersion':'5037.0.19','WFWorkflowIcon':{'WFWorkflowIconStartColor':4282601983,'WFWorkflowIconGlyphNumber':59726},'WFWorkflowActions':A,'WFWorkflowTypes':['ActionExtension'],'WFWorkflowInputContentItemClasses':['WFURLContentItem','WFStringContentItem','WFSafariWebPageContentItem'],'WFWorkflowNoInputBehavior':{'Name':'WFWorkflowNoInputBehaviorGetClipboard','Parameters':{}},'WFWorkflowHasShortcutInputVariables':True,'WFWorkflowImportQuestions':[]}
(ROOT/'work').mkdir(exist_ok=True)
plistlib.dump(root,open(ROOT/'work/xhs-v4-unsigned.shortcut','wb'),fmt=plistlib.FMT_BINARY)
print('Generated',len(A),'actions')
