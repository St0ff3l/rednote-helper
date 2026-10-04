"""Build the three-way workflow adapted from the user-supplied reference.
Reference: https://www.icloud.com/shortcuts/48c45bf28b50473f82c818d5977d1a14
Builds local XHS mobile-page parsing and a Live Photo save branch that calls GIF Factory. Signing is separate.
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
def choose(value, prompt):
    return add(
        'choosefromlist',
        WFInput=value,
        WFChooseFromListActionPrompt=prompt,
        WFChooseFromListActionSelectMultiple=True,
        WFChooseFromListActionSelectAll=False,
    )
def url_https(value): return add('text.replace',WFInput=text(value),WFReplaceTextFind='http://',WFReplaceTextReplace='https://',WFReplaceTextRegularExpression=False)

add('comment', WFCommentActionText='V4.6：图片、Live 与普通视频均在快捷指令内读取小红书移动网页状态并提取 CDN 地址，不调用 Pro/qsy 解析云服务。Live 下载封面和配对视频文件，再交给动图工厂保存。动态资源是否可访问、封面尺寸及源视频水印仍需 iPhone 验证。')
links=add('detect.link',WFInput=text({'Value':{'Type':'ExtensionInput'},'WFSerializationType':'WFTextTokenAttachment'}))
require(out(links),'🔗 没有找到分享链接\n请复制完整的小红书笔记分享文字，或从分享表单运行。')
u=first(out(links)); add('setvariable',WFInput=out(u),WFVariableName='笔记链接')
mg=uid();add('choosefrommenu',WFMenuPrompt='📥 选择要获取的内容',WFMenuItems=['📸 Live 实况图','🖼️ 图片','🎬 视频'],WFControlFlowMode=0,GroupingIdentifier=mg)
for mode,title in [(1,'📸 Live 实况图'),(2,'🖼️ 图片'),(3,'🎬 视频')]:
    add('choosefrommenu',WFMenuItemTitle=title,WFControlFlowMode=1,GroupingIdentifier=mg)
    n=add('number',WFNumberActionNumber=str(mode));add('setvariable',WFInput=out(n),WFVariableName='保存类型')
    if mode==1:
        add('comment',WFCommentActionText='Live 数据在本地从笔记移动网页提取；原图和动态视频仍从小红书 CDN 下载。保存动作只使用动图工厂。')
        # Shortcuts on iOS cannot reliably query whether another app is installed.
        # Ask on each Live run, and stop after opening the official App Store page.
        live_setup=uid()
        add('choosefrommenu',WFMenuPrompt='🧰 Live 保存需要动图工厂',WFMenuItems=['✅ 已安装，继续','📲 未安装，去 App Store 下载'],WFControlFlowMode=0,GroupingIdentifier=live_setup)
        add('choosefrommenu',WFMenuItemTitle='✅ 已安装，继续',WFControlFlowMode=1,GroupingIdentifier=live_setup)
        add('nothing')
        add('choosefrommenu',WFMenuItemTitle='📲 未安装，去 App Store 下载',WFControlFlowMode=1,GroupingIdentifier=live_setup)
        add('openurl',WFURL=text('https://apps.apple.com/us/app/id6762482512?l=zh-Hans-CN'))
        add('exit')
        add('choosefrommenu',WFControlFlowMode=2,GroupingIdentifier=live_setup)
        headers=dictionary_fields({'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'})
        page=add('downloadurl',WFURL=text(var('笔记链接')),WFHTTPMethod='GET',WFHTTPHeaders=headers)
        page=add('gethtmlfromrichtext',WFInput=out(page),WFMakeFullDocument=False)
        state=add('text.match',text=text(out(page)),WFMatchTextPattern=r'(?s)window\.__INITIAL_STATE__\s*=\s*(.*?)</script>',WFMatchTextCaseSensitive=True)
        require(out(state),'📸 Live 解析失败：没有读取到笔记数据\n笔记可能需要登录，或分享链接已失效。请重新复制链接后重试。');state=first(out(state))
        state=add('text.match.getgroup',matches=out(state),WFGroupIndex=1,WFGetGroupType='Group At Index')
        state=add('text.replace',WFInput=text(out(state)),WFReplaceTextFind=r'\bundefined\b',WFReplaceTextReplace='null',WFReplaceTextRegularExpression=True)
        state=add('text.replace',WFInput=text(out(state)),WFReplaceTextFind=r';\s*$',WFReplaceTextReplace='',WFReplaceTextRegularExpression=True)
        state=add('detect.dictionary',WFInput=out(state));images=key(out(state),'noteData.data.noteData.imageList')
        require(out(images),'📸 Live 解析失败：笔记没有图片列表\n请确认分享的是包含实况图的笔记。')
        pairs=add('list',WFItems=[]);add('setvariable',WFInput=out(pairs),WFVariableName='本地Live配对JSON')
        g=loop(out(images));itemtext=add('gettext',WFTextActionText=text(var('Repeat Item')))
        liveflag=add('text.match',text=text(out(itemtext)),WFMatchTextPattern=r'"livePhoto"\s*:\s*true',WFMatchTextCaseSensitive=True)
        livecount=count(out(liveflag));liveg=cond(out(livecount),2,0)
        fid=key(var('Repeat Item'),'fileId');require(out(fid),'📸 Live 封面缺少原图标识，已停止。')
        cover=add('gettext',WFTextActionText=text('https://ci.xiaohongshu.com/',out(fid)))
        streams=key(var('Repeat Item'),'stream.h264');streams=first(out(streams));video=key(out(streams),'masterUrl')
        require(out(video),'📸 Live 项目没有动态视频地址，无法配对保存。')
        video=url_https(out(video))
        # Materialize the tokenized text as a real Text action output before
        # appending it. Append to Variable silently ignores an inline text-token
        # parameter here, leaving the Live pair collection empty.
        pair=add('gettext',WFTextActionText=text('{"pic":"',out(cover),'","video":"',out(video),'"}'))
        add('appendvariable',WFInput=out(pair),WFVariableName='本地Live配对JSON')
        add('conditional',WFControlFlowMode=2,GroupingIdentifier=liveg)
        loop_end(g)
        pairs=add('getvariable',WFVariable=var('本地Live配对JSON'));require(out(pairs),'📸 这条笔记没有找到可用的 Live 图。')
        pairs=add('text.combine',text=out(pairs),WFTextSeparator='New Lines')
        pairs=add('text.replace',WFInput=text(out(pairs)),WFReplaceTextFind='\n',WFReplaceTextReplace=r'\n',WFReplaceTextRegularExpression=False)
        # The pairs are JSON objects embedded in the response's JSON string.
        # Escape their quotes after preserving the line separators, or the
        # response dictionary cannot be parsed and its `code` key disappears.
        pairs=add('text.replace',WFInput=text(out(pairs)),WFReplaceTextFind='"',WFReplaceTextReplace=r'\"',WFReplaceTextRegularExpression=False)
        resp=add('gettext',WFTextActionText=text('{"code":0,"body":{"lives":"',out(pairs),'"}}'))
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
        headers=dictionary_fields({'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'})
        page=add('downloadurl',WFURL=text(var('笔记链接')),WFHTTPMethod='GET',WFHTTPHeaders=headers)
        page=add('gethtmlfromrichtext',WFInput=out(page),WFMakeFullDocument=False)
        state=add('text.match',text=text(out(page)),WFMatchTextPattern=r'(?s)window\.__INITIAL_STATE__\s*=\s*(.*?)</script>',WFMatchTextCaseSensitive=True)
        require(out(state),'🎬 视频解析失败：没有读取到笔记数据\n请重新复制完整的视频笔记链接。');state=first(out(state))
        state=add('text.match.getgroup',matches=out(state),WFGroupIndex=1,WFGetGroupType='Group At Index')
        state=add('text.replace',WFInput=text(out(state)),WFReplaceTextFind=r'\bundefined\b',WFReplaceTextReplace='null',WFReplaceTextRegularExpression=True)
        state=add('text.replace',WFInput=text(out(state)),WFReplaceTextFind=r';\s*$',WFReplaceTextReplace='',WFReplaceTextRegularExpression=True)
        state=add('detect.dictionary',WFInput=out(state));note=key(out(state),'noteData.data.noteData')
        video=key(out(note),'video.media.stream.h264');video=first(out(video));video=key(out(video),'masterUrl')
        require(out(video),'🎬 笔记没有可用的视频地址。请确认这是视频笔记。')
        video=url_https(out(video))
        resp=add('gettext',WFTextActionText=text('{"code":0,"body":{"urls":"',out(video),'"}}'))
    add('setvariable',WFInput=out(resp),WFVariableName='解析响应')
add('choosefrommenu',WFControlFlowMode=2,GroupingIdentifier=mg)
d=add('detect.dictionary',WFInput=var('解析响应'));add('setvariable',WFInput=out(d),WFVariableName='解析结果')
code=key(var('解析结果'),'code');require(out(code),'🧩 本地解析结果不完整\n请重新复制笔记分享链接后重试。')
code=add('number',WFNumberActionNumber=out(code));g=cond(out(code),5,0)
msg=key(var('解析结果'),'msg');error(text('🧩 本地解析没有完成\n返回信息：',out(msg)));end(g)
mode=add('getvariable',WFVariable=var('保存类型'));liveg=cond(out(mode),4,1)
# The reference returns one JSON pair per line in body.lives.
pairs=key(var('解析结果'),'body.lives');require(out(pairs),'📸 Live 解析失败：没有封面与视频配对\n请确认笔记包含实况图；静态图请改选“图片”。')
pairs=split(out(pairs));add('setvariable',WFInput=out(pairs),WFVariableName='实况配对列表')
g=loop(out(pairs));pair=add('detect.dictionary',WFInput=var('Repeat Item'));pic=key(out(pair),'pic');require(out(pic),'📸 Live 封面缺失\n笔记数据没有返回封面地址，无法预览及配对。请重试。')
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
urls=key(var('解析结果'),'body.urls');require(out(urls),'📥 下载地址列表为空\n请确认菜单类型与笔记内容匹配，并重新复制链接。');urls=split(out(urls));add('setvariable',WFInput=out(urls),WFVariableName='媒体地址列表')
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
rename=add('gettext',WFTextActionText='小红书视频.mp4')
add('setitemname',WFInput=out(media),WFName=text(out(rename)),WFDontIncludeFileExtension=False)
media=loop_end(g);require(out(media),'🎬 视频下载为空\n请检查网络或稍后重新解析。尚未执行相册保存。')
selected=choose(out(media),'🎬 选择视频，确认后存相册（可多选）');require(out(selected),'☑️ 未选择视频\n请至少勾选一个视频后确认。本次未保存。')
add('savetocameraroll',WFInput=out(selected));success(out(selected),' 个视频')
end(imageg)
end(liveg)
root={'WFWorkflowName':'小红书素材助手 V4.6','WFWorkflowMinimumClientVersion':1113,'WFWorkflowMinimumClientVersionString':'1113','WFWorkflowClientVersion':'5037.0.19','WFWorkflowIcon':{'WFWorkflowIconStartColor':4282601983,'WFWorkflowIconGlyphNumber':59726},'WFWorkflowActions':A,'WFWorkflowTypes':['ActionExtension'],'WFWorkflowInputContentItemClasses':['WFURLContentItem','WFStringContentItem','WFSafariWebPageContentItem'],'WFWorkflowNoInputBehavior':{'Name':'WFWorkflowNoInputBehaviorGetClipboard','Parameters':{}},'WFWorkflowHasShortcutInputVariables':True,'WFWorkflowImportQuestions':[]}
(ROOT/'work').mkdir(exist_ok=True)
plistlib.dump(root,open(ROOT/'work/xhs-v4-unsigned.shortcut','wb'),fmt=plistlib.FMT_BINARY)
print('Generated',len(A),'actions')
