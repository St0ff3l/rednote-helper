"""Build the three-way workflow adapted from the user-supplied reference.
Reference: https://www.icloud.com/shortcuts/48c45bf28b50473f82c818d5977d1a14
Requires macOS signing separately; the Live branch needs JustLive for parsing and GIF Factory for saving.
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
    add('alert', WFAlertActionTitle='⚠️ 未完成保存', WFAlertActionMessage=message, WFAlertActionCancelButtonShown=False); add('exit')
def require(value, message):
    c = count(value); g = cond(out(c), 4, 0); error(message); end(g)
def success(value, unit):
    n = count(value)
    add('notification', WFNotificationActionTitle='🎉 保存成功', WFNotificationActionBody=text('✅ 已保存 ', out(n), unit, '到相册'), WFNotificationActionSound=True)
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

add('comment', WFCommentActionText='V4.4：参考用户提供的“空什么格 / 小红书下载器”指令。先分流 Live / 图片 / 视频，再解析、选择和保存。Live/视频沿用 qsy.jiejing.fun / a.jiejing.fun 服务；静态图片本地读取笔记原图标识，从原图端点下载。Live 保存参考小红书助手pro v4.7 的动图工厂文件动作，传入独立封面和视频文件。Live 解析仍需实况捷径。V4.3 用户已反馈可保存；本版增加保存完成通知和分支错误提示，新增提示尚待 iPhone 测试，不承诺所有动态源无水印。')
links=add('detect.link',WFInput=text({'Value':{'Type':'ExtensionInput'},'WFSerializationType':'WFTextTokenAttachment'}))
require(out(links),'🔗 没有找到分享链接\n请复制完整的小红书笔记分享文字，或从分享表单运行。')
u=first(out(links)); add('setvariable',WFInput=out(u),WFVariableName='笔记链接')
mg=uid();add('choosefrommenu',WFMenuPrompt='📥 选择要获取的内容',WFMenuItems=['📸 Live 实况图','🖼️ 图片','🎬 视频'],WFControlFlowMode=0,GroupingIdentifier=mg)
for mode,title in [(1,'📸 Live 实况图'),(2,'🖼️ 图片'),(3,'🎬 视频')]:
    add('choosefrommenu',WFMenuItemTitle=title,WFControlFlowMode=1,GroupingIdentifier=mg)
    n=add('number',WFNumberActionNumber=str(mode));add('setvariable',WFInput=out(n),WFVariableName='保存类型')
    if mode!=2:
        add('comment',WFCommentActionText='以下 Live/视频解析调用第三方 qsy.jiejing.fun / a.jiejing.fun 服务。下方文本留空使用该服务免费额度；只有已有该服务授权码时才填写。此项属于第三方服务，与本指令的本地图片解析无关。')
        u=add('gettext',WFTextActionText='');add('setvariable',WFInput=out(u),WFVariableName='第三方服务授权码')
        c=add('downloadurl',WFURL='https://qsy.jiejing.fun/xhs.json',WFHTTPMethod='GET')
        c=add('detect.dictionary',WFInput=out(c));add('setvariable',WFInput=out(c),WFVariableName='服务配置')
    if mode==1:
        add('alert',WFAlertActionTitle='📸 Live 实况图',WFAlertActionMessage='解析需要“实况捷径”，保存需要“动图工厂”。此分支下载独立封面与对应视频文件，再配对存入相册。',WFAlertActionCancelButtonShown=True)
        cred=app('EncryptExtension');require(out(cred),'📸 实况捷径未返回解析凭据\n请确认已安装实况捷径，并完成它所需的首次设置。')
        endpoint=key(var('服务配置'),'livexhs');require(out(endpoint),'🌐 Live 解析服务配置缺失\n未取得解析接口，请稍后重试。')
        resp=add('downloadurl',WFURL=text(out(endpoint)),WFHTTPMethod='POST',WFHTTPBodyType='JSON',WFJSONValues=dictionary_fields({'kl':var('第三方服务授权码'),'url':var('笔记链接'),'payload':out(cred)}))
    elif mode==2:
        # Read this note's image list locally; do not save a styled preview URL.
        page=add('downloadurl',WFURL=text(var('笔记链接')),WFHTTPMethod='GET',WFHTTPHeaders=dictionary_fields({'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'}))
        page=add('gethtmlfromrichtext',WFInput=out(page),WFMakeFullDocument=False)
        state=add('text.match',text=text(out(page)),WFMatchTextPattern=r'(?s)window\.__INITIAL_STATE__\s*=\s*(.*?)</script>',WFMatchTextCaseSensitive=True)
        require(out(state),'🖼️ 图片解析失败：没有取得笔记数据\n链接可能失效、需要登录，或网页结构已变化。请从笔记重新复制完整分享链接后重试。');state=first(out(state))
        state=add('text.match.getgroup',matches=out(state),WFGroupIndex=1,WFGetGroupType='Group At Index')
        state=add('text.replace',WFInput=text(out(state)),WFReplaceTextFind=r'\bundefined\b',WFReplaceTextReplace='null',WFReplaceTextRegularExpression=True)
        state=add('text.replace',WFInput=text(out(state)),WFReplaceTextFind=r';\s*$',WFReplaceTextReplace='',WFReplaceTextRegularExpression=True)
        state=add('detect.dictionary',WFInput=out(state))
        images=key(out(state),'noteData.data.noteData.imageList');require(out(images),'🖼️ 图片解析失败：原图列表为空\n请确认这是一条图片笔记；视频笔记请在初始菜单选择“视频”。也可能是网页结构发生变化。')
        g=loop(out(images));fid=key(var('Repeat Item'),'fileId');require(out(fid),'🖼️ 图片解析失败：某张图片缺少原图标识\n当前笔记数据不完整，无法取得原图。请重新复制链接后重试。')
        fid=add('text.match',text=text(out(fid)),WFMatchTextPattern=r'^[A-Za-z0-9_/-]+$',WFMatchTextCaseSensitive=True);require(out(fid),'🖼️ 图片解析失败：原图标识格式异常\n小红书返回了无法识别的数据，已停止下载。请换一条笔记重试。')
        add('gettext',WFTextActionText=text('https://ci.xiaohongshu.com/',out(fid)))
        urls=loop_end(g)
        urls=add('text.combine',text=out(urls),WFTextSeparator='New Lines')
        urls=add('text.replace',WFInput=text(out(urls)),WFReplaceTextFind='\n',WFReplaceTextReplace=r'\n',WFReplaceTextRegularExpression=False)
        resp=add('gettext',WFTextActionText=text('{"code":0,"body":{"urls":"',out(urls),'"}}'))
    else:
        headers={}
        if mode==3:
            # Honor the reference service's high-quality video availability flag.
            available=key(var('服务配置'),'hdvideo'); gate=cond(out(available),5,0)
            error('🎬 视频解析暂不可用\n第三方服务当前未开放高清视频解析。请稍后重试，或使用参考作者指令的普通视频选项。');end(gate)
            # Matches the reference's 1080P/4K branch, including its service-provided Cookie.
            ckurl=key(var('服务配置'),'xhsck');ck=add('downloadurl',WFURL=text(out(ckurl)),WFHTTPMethod='GET')
            headers={'WFHTTPHeaders':dictionary_fields({'Cookie':out(ck)})}
        page=add('downloadurl',WFURL=text(var('笔记链接')),WFHTTPMethod='GET',**headers)
        page=add('gethtmlfromrichtext',WFInput=out(page),WFMakeFullDocument=False)
        endpoint=key(var('服务配置'),'xhshd' if mode==2 else 'hdvideoxhs')
        target=text(out(endpoint),'?url=',var('笔记链接'),'&v=13&kl=',var('第三方服务授权码'))
        resp=add('downloadurl',WFURL=target,WFHTTPMethod='POST',WFHTTPBodyType='File',WFRequestVariable=out(page),**headers)
    add('setvariable',WFInput=out(resp),WFVariableName='解析响应')
add('choosefrommenu',WFControlFlowMode=2,GroupingIdentifier=mg)
d=add('detect.dictionary',WFInput=var('解析响应'));add('setvariable',WFInput=out(d),WFVariableName='解析结果')
code=key(var('解析结果'),'code');require(out(code),'🌐 解析响应不完整：缺少结果状态\n第三方服务可能暂时异常。请稍后重试；本次未执行保存。')
code=add('number',WFNumberActionNumber=out(code));g=cond(out(code),5,0)
msg=key(var('解析结果'),'msg');error(text('🌐 第三方解析失败\n服务返回：',out(msg)));end(g)
mode=add('getvariable',WFVariable=var('保存类型'));liveg=cond(out(mode),4,1)
# The reference returns one JSON pair per line in body.lives.
pairs=key(var('解析结果'),'body.lives');require(out(pairs),'📸 Live 解析失败：没有封面与视频配对\n请确认笔记包含实况图；静态图请改选“图片”。第三方服务也可能暂未返回动态素材。')
pairs=split(out(pairs));add('setvariable',WFInput=out(pairs),WFVariableName='实况配对列表')
g=loop(out(pairs));pair=add('detect.dictionary',WFInput=var('Repeat Item'));pic=key(out(pair),'pic');require(out(pic),'📸 Live 封面缺失\n第三方返回的某个项目没有封面地址，无法预览及配对。请稍后重新解析。')
pic=url_https(out(pic));p=add('downloadurl',WFURL=text(out(pic)),WFHTTPMethod='GET')
p=add('image.convert',WFInput=out(p),WFImageFormat='PNG',WFImagePreserveMetadata=True)
p=add('setitemname',WFInput=out(p),WFName=text(var('Repeat Index'),'.png'),WFDontIncludeFileExtension=False)
thumbs=loop_end(g);require(out(thumbs),'📸 Live 封面下载为空\n无法生成选择列表。请检查网络后重试。')
selected=choose(out(thumbs),'📸 选择 Live，确认后保存（可多选）');require(out(selected),'☑️ 未选择 Live 实况图\n请至少勾选一项后确认。本次未保存。')
g=loop(out(selected));add('setvariable',WFInput=var('Repeat Item'),WFVariableName='Live封面文件');name=add('getitemname',WFInput=var('Repeat Item'))
idx=add('text.match',text=text(out(name)),WFMatchTextPattern=r'^\d+',WFMatchTextCaseSensitive=True)
pair=add('getitemfromlist',WFInput=var('实况配对列表'),WFItemSpecifier='Item At Index',WFItemIndex=text(out(idx)))
pair=add('detect.dictionary',WFInput=out(pair));pic=key(out(pair),'pic');video=key(out(pair),'video')
require(out(pic),'📸 Live 配对失败：所选项目缺少封面\n无法生成完整实况照片，请重新解析该笔记。');require(out(video),'📸 Live 配对失败：所选项目缺少动态视频\n只有封面无法保存为实况照片，请重新解析或改选“图片”。')
# Download the paired video; GIF Factory accepts files, not URL strings.
video=url_https(out(video));video=add('downloadurl',WFURL=text(out(video)),WFHTTPMethod='GET')
require(out(video),'📸 Live 视频下载为空\n请检查网络后重试。此项尚未交给动图工厂保存；此前已完成的项目可能已经保存。')
video=add('setitemname',WFInput=out(video),WFName='xhs-live-video.mp4',WFDontIncludeFileExtension=False)
add('setvariable',WFInput=out(video),WFVariableName='Live视频文件')
A.append({'WFWorkflowActionIdentifier':'com.liudh.giffactory.SaveLivePhotoFromFilesIntent','WFWorkflowActionParameters':{'UUID':uid(),'AppIntentDescriptor':{'TeamIdentifier':'Q36V269ZQ9','BundleIdentifier':'com.liudh.giffactory','Name':'动图工厂','AppIntentIdentifier':'SaveLivePhotoFromFilesIntent'},'imageFile':var('Live封面文件'),'videoFile':var('Live视频文件')}})
# The intent saves directly; its return is not a JustLive numeric quota status.
add('nothing')
loop_end(g)
success(out(selected),' 张实况照片')
add('conditional',WFControlFlowMode=1,GroupingIdentifier=liveg)
urls=key(var('解析结果'),'body.urls');require(out(urls),'📥 下载地址列表为空\n请检查初始菜单是否选对笔记类型；第三方视频服务也可能未返回素材。请重新解析。');urls=split(out(urls));add('setvariable',WFInput=out(urls),WFVariableName='媒体地址列表')
mode=add('getvariable',WFVariable=var('保存类型'));imageg=cond(out(mode),4,2)
# Decode the actual image and save PNG files, following the new reference.
g=loop(out(urls));address=url_https(var('Repeat Item'));media=add('downloadurl',WFURL=text(out(address)),WFHTTPMethod='GET')
media=add('image.convert',WFInput=out(media),WFImageFormat='PNG',WFImagePreserveMetadata=True)
media=add('setitemname',WFInput=out(media),WFName=text(var('Repeat Index'),'.png'),WFDontIncludeFileExtension=False)
previews=loop_end(g);require(out(previews),'🖼️ 图片下载为空\n无法生成选择列表。请检查网络后重试。')
selected=choose(out(previews),'🖼️ 选择图片，确认后存相册（可多选）');require(out(selected),'☑️ 未选择图片\n请至少勾选一张后确认。本次未保存。');add('savetocameraroll',WFInput=out(selected));success(out(selected),' 张图片')
add('conditional',WFControlFlowMode=1,GroupingIdentifier=imageg)
g=loop(out(urls));address=url_https(var('Repeat Item'));media=add('downloadurl',WFURL=text(out(address)),WFHTTPMethod='GET')
# Exact file naming strategy from the reference before Photos import.
rename=key(var('服务配置'),'Rename')
add('setitemname',WFInput=out(media),WFName=text(out(rename)),WFDontIncludeFileExtension=False)
media=loop_end(g);require(out(media),'🎬 视频下载为空\n请检查网络或稍后重新解析。尚未执行相册保存。')
selected=choose(out(media),'🎬 选择视频，确认后存相册（可多选）');require(out(selected),'☑️ 未选择视频\n请至少勾选一个视频后确认。本次未保存。')
add('savetocameraroll',WFInput=out(selected));success(out(selected),' 个视频')
end(imageg)
end(liveg)
root={'WFWorkflowMinimumClientVersion':1113,'WFWorkflowMinimumClientVersionString':'1113','WFWorkflowClientVersion':'5037.0.19','WFWorkflowIcon':{'WFWorkflowIconStartColor':4282601983,'WFWorkflowIconGlyphNumber':59726},'WFWorkflowActions':A,'WFWorkflowTypes':['ActionExtension'],'WFWorkflowInputContentItemClasses':['WFURLContentItem','WFStringContentItem','WFSafariWebPageContentItem'],'WFWorkflowNoInputBehavior':{'Name':'WFWorkflowNoInputBehaviorGetClipboard','Parameters':{}},'WFWorkflowHasShortcutInputVariables':True,'WFWorkflowImportQuestions':[]}
(ROOT/'work').mkdir(exist_ok=True)
plistlib.dump(root,open(ROOT/'work/xhs-v4-unsigned.shortcut','wb'),fmt=plistlib.FMT_BINARY)
print('Generated',len(A),'actions')
