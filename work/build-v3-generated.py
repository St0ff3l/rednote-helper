import plistlib,uuid,copy
from pathlib import Path
A=[]
def uid():return str(uuid.uuid4()).upper()
def add(kind,**p):
 p.setdefault('UUID',uid());A.append({'WFWorkflowActionIdentifier':'is.workflow.actions.'+kind,'WFWorkflowActionParameters':p});return p['UUID']
def out(u,n='结果'):return {'Value':{'Type':'ActionOutput','OutputUUID':u,'OutputName':n},'WFSerializationType':'WFTextTokenAttachment'}
def named(n):return {'Value':{'Type':'Variable','VariableName':n},'WFSerializationType':'WFTextTokenAttachment'}
def txt(v,pre='',post=''):
 value=out(v)['Value'] if isinstance(v,str) else v['Value']
 return {'Value':{'string':pre+'\ufffc'+post,'attachmentsByRange':{'{%d, 1}'%len(pre):value}},'WFSerializationType':'WFTextTokenString'}
def cond(u,code,number=None,string=None):
 g=uid();p={'WFInput':{'Type':'Variable','Variable':out(u)},'WFCondition':code,'WFControlFlowMode':0,'GroupingIdentifier':g}
 if number is not None:p['WFNumberValue']=str(number)
 if string is not None:p['WFConditionalActionString']=string
 add('conditional',**p);return g
def end(g):return add('conditional',WFControlFlowMode=2,GroupingIdentifier=g)
def fail_empty(u,msg):
 c=add('count',Input=out(u),WFCountType='Items');g=cond(c,4,number=0)
 add('alert',WFAlertActionTitle='没有可用的媒体',WFAlertActionMessage=msg,WFAlertActionCancelButtonShown=False);add('exit');end(g)
def regex(u,p):return add('text.match',text=txt(u),WFMatchTextPattern=p,WFMatchTextCaseSensitive=True)
def key(u,k):return add('getvalueforkey',WFInput=out(u) if isinstance(u,str) else u,WFDictionaryKey=k,WFGetDictionaryValueType='Value')
def first(u):return add('getitemfromlist',WFInput=out(u),WFItemSpecifier='First Item')
def video_address(u):
 m=regex(u,r'"masterUrl"\s*:\s*"([^"\r\n]+)"');fail_empty(m,'网页未提供可下载的视频文件地址。')
 m=first(m);v=add('text.match.getgroup',matches=out(m),WFGroupIndex=1,WFGetGroupType='Group At Index')
 v=add('text.replace',WFInput=txt(v),WFReplaceTextFind='\\/',WFReplaceTextReplace='/',WFReplaceTextRegularExpression=False)
 v=add('text.replace',WFInput=txt(v),WFReplaceTextFind='http://',WFReplaceTextReplace='https://',WFReplaceTextRegularExpression=False)
 return v
add('comment',WFCommentActionText='V3：预览、多选后保存。静态图片下载原尺寸文件。新增保存为 Live Photo，需安装 Actions 4（iOS26+）；Actions 从视频帧生成封面并直接保存相册，不保留独立原图封面的分辨率。网页 Live 视频可能已经带水印，合成不会去除水印；不承诺动态源无水印。源视频不由本快捷指令转码。')
inputtxt={'Value':{'string':'\ufffc','attachmentsByRange':{'{0, 1}':{'Type':'ExtensionInput'}}},'WFSerializationType':'WFTextTokenString'}
u=add('detect.link',WFInput=inputtxt);fail_empty(u,'请在小红书复制笔记链接后运行，或从分享菜单运行。');u=first(u)
headers={'Value':{'WFDictionaryFieldValueItems':[{'WFItemType':0,'WFKey':{'Value':{'string':'User-Agent','attachmentsByRange':{}},'WFSerializationType':'WFTextTokenString'},'WFValue':{'Value':{'string':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1','attachmentsByRange':{}},'WFSerializationType':'WFTextTokenString'}}]},'WFSerializationType':'WFDictionaryFieldValue'}
h=add('downloadurl',WFURL=txt(u),WFHTTPHeaders=headers,WFHTTPMethod='GET');web_request=h
h=add('gethtmlfromrichtext',WFInput=out(h),WFMakeFullDocument=False)
s=regex(h,r'(?<=window\.__INITIAL_STATE__=)[\s\S]*?(?=</script>)');fail_empty(s,'没有读取到笔记数据，可能需要登录或分享链接失效。');s=first(s)
s=add('text.replace',WFInput=txt(s),WFReplaceTextFind=r'(?<=[\[:,])\s*undefined(?=\s*[,}\]])',WFReplaceTextReplace='null',WFReplaceTextRegularExpression=True)
d=add('detect.dictionary',WFInput=out(s));n=key(d,'noteData.data.noteData')
# Explicitly initialize an empty collection so appended links contain no blank element.
e=add('nothing');add('setvariable',WFInput=out(e),WFVariableName='下载地址');add('setvariable',WFInput=out(e),WFVariableName='实况视频地址')
t=key(n,'type');vm=regex(t,r'^video$');vc=add('count',Input=out(vm),WFCountType='Items');g=cond(vc,2,number=0)
video=key(n,'video.media.stream.h264');video=first(video);v=key(video,'masterUrl');add('appendvariable',WFInput=out(v),WFVariableName='下载地址')
add('conditional',WFControlFlowMode=1,GroupingIdentifier=g)
images=key(n,'imageList');fail_empty(images,'这个笔记没有返回静态图片数据。')
live=regex(images,r'"livePhoto"\s*:\s*true');lc=add('count',Input=out(live),WFCountType='Items');lg=cond(lc,2,number=0)
add('alert',WFAlertActionTitle='此笔记包含 Live 图',WFAlertActionMessage='可选择保存封面、动态视频、分别保存或合成为 Live Photo。合成需 Actions App，封面取自视频帧。网页动态视频可能已带小红书水印，合成不会去除。',WFAlertActionCancelButtonShown=True);end(lg)
# Download only previews before selecting full-resolution content.
rg=uid();add('repeat.each',WFInput=out(images),WFControlFlowMode=0,GroupingIdentifier=rg)
item=named('Repeat Item');preview=key(item,'url')
preview=add('text.replace',WFInput=txt(preview),WFReplaceTextFind='http://',WFReplaceTextReplace='https://',WFReplaceTextRegularExpression=False)
thumb=add('downloadurl',WFURL=txt(preview),WFHTTPMethod='GET')
thumb=add('setitemname',WFInput=out(thumb),WFName=txt(named('Repeat Index'),post='.jpg'),WFDontIncludeFileExtension=False)
thumbs=add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=rg,CustomOutputName='图片预览')
fail_empty(thumbs,'没有取得图片预览，请重新复制笔记链接。')
selected=add('choosefromlist',WFInput=out(thumbs),WFChooseFromListActionPrompt='选择要保存的图片或 Live 图（多选；此处为网页预览，保存时下载原图）',WFChooseFromListActionSelectMultiple=True,WFChooseFromListActionSelectAll=False)
fail_empty(selected,'没有选择内容，本次没有保存。')
# Live posts expose a choice of the still image, the motion clip, or both.
lg=cond(lc,2,number=0)
opts=add('list',WFItems=['1 图片/封面','2 Live 动态视频','3 图片和动态视频（分别保存）','4 合成为 Live Photo（需要 Actions）'])
mode=add('choosefromlist',WFInput=out(opts),WFChooseFromListActionPrompt='选择保存类型',WFChooseFromListActionSelectMultiple=False)
add('setvariable',WFInput=out(mode),WFVariableName='保存类型')
add('conditional',WFControlFlowMode=1,GroupingIdentifier=lg)
mode=add('gettext',WFTextActionText='1 图片/封面');add('setvariable',WFInput=out(mode),WFVariableName='保存类型');end(lg)
rg=uid();add('repeat.each',WFInput=out(selected),WFControlFlowMode=0,GroupingIdentifier=rg)
name=add('getitemname',WFInput=named('Repeat Item'));idx=regex(name,r'^\d+')
item=add('getitemfromlist',WFInput=out(images),WFItemSpecifier='Item At Index',WFItemIndex=txt(idx))
add('setvariable',WFInput=out(item),WFVariableName='所选媒体信息')
mode=add('getvariable',WFVariable=named('保存类型'));m=regex(mode,r'^[13]');c=add('count',Input=out(m),WFCountType='Items');cg=cond(c,2,number=0)
f=key(named('所选媒体信息'),'fileId');fail_empty(f,'某张图片没有原文件标识，已停止。')
a=add('gettext',WFTextActionText=txt(f,'https://ci.xiaohongshu.com/'));add('appendvariable',WFInput=out(a),WFVariableName='下载地址');end(cg)
mode=add('getvariable',WFVariable=named('保存类型'));m=regex(mode,r'^[23]');c=add('count',Input=out(m),WFCountType='Items');cg=cond(c,2,number=0)
itemtext=add('gettext',WFTextActionText=txt(named('所选媒体信息')));m=regex(itemtext,r'"livePhoto"\s*:\s*true');c=add('count',Input=out(m),WFCountType='Items');lg=cond(c,2,number=0)
v=video_address(itemtext);add('appendvariable',WFInput=out(v),WFVariableName='下载地址');end(lg);end(cg)
mode=add('getvariable',WFVariable=named('保存类型'));m=regex(mode,r'^4');c=add('count',Input=out(m),WFCountType='Items');cg=cond(c,2,number=0)
itemtext=add('gettext',WFTextActionText=txt(named('所选媒体信息')));m=regex(itemtext,r'"livePhoto"\s*:\s*true');c=add('count',Input=out(m),WFCountType='Items');lg=cond(c,2,number=0)
v=video_address(itemtext);add('appendvariable',WFInput=out(v),WFVariableName='实况视频地址');end(lg);end(cg)
add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=rg);end(g)
liveLinks=add('getvariable',WFVariable=named('实况视频地址'));c=add('count',Input=out(liveLinks),WFCountType='Items');liveg=cond(c,2,number=0)
rg=uid();add('repeat.each',WFInput=out(liveLinks),WFControlFlowMode=0,GroupingIdentifier=rg)
add('downloadurl',WFURL=txt(named('Repeat Item')),WFHTTPMethod='GET')
clips=add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=rg,CustomOutputName='实况动态视频')
fail_empty(clips,'没有取得实况视频，本次未保存。')
choice=add('choosefromlist',WFInput=out(clips),WFChooseFromListActionPrompt='选择要合成为实况照片的视频（多选）',WFChooseFromListActionSelectMultiple=True,WFChooseFromListActionSelectAll=False)
fail_empty(choice,'未选择任何实况视频，本次未保存。')
add('previewdocument',WFInput=out(choice))
add('alert',WFAlertActionTitle='保存为 Live Photo',WFAlertActionMessage='接下来由 Actions 直接保存到相册。封面取自视频第一帧；源视频已有的水印会保留。',WFAlertActionCancelButtonShown=True)
rg=uid();add('repeat.each',WFInput=out(choice),WFControlFlowMode=0,GroupingIdentifier=rg)
A.append({'WFWorkflowActionIdentifier':'com.sindresorhus.Actions.MakeLivePhotoFromVideoIntent','WFWorkflowActionParameters':{'AppIntentDescriptor':{'AppIntentIdentifier':'MakeLivePhotoFromVideoIntent','BundleIdentifier':'com.sindresorhus.Actions','TeamIdentifier':'YG56YK5RN5','Name':'Actions'},'video':named('Repeat Item'),'UUID':uid()}})
add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=rg)
add('conditional',WFControlFlowMode=1,GroupingIdentifier=liveg)
links=add('getvariable',WFVariable=named('下载地址'));fail_empty(links,'笔记没有提供可用的下载地址。');url_end=links
rg=uid();add('repeat.each',WFInput=out(links),WFControlFlowMode=0,GroupingIdentifier=rg)
dl=add('text.replace',WFInput=txt(named('Repeat Item')),WFReplaceTextFind='http://',WFReplaceTextReplace='https://',WFReplaceTextRegularExpression=False)
b=add('downloadurl',WFURL=txt(dl),WFHTTPMethod='GET');media_request=b
media=add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=rg,CustomOutputName='可选媒体')
fail_empty(media,'没有成功下载任何图片或视频，请重试。')
choice=add('choosefromlist',WFInput=out(media,'可选媒体'),WFChooseFromListActionPrompt='选择要保存的图片或视频（可多选；Live 图为图片+视频）',WFChooseFromListActionSelectMultiple=True,WFChooseFromListActionSelectAll=False)
fail_empty(choice,'未选择任何内容，本次没有保存。')
add('previewdocument',WFInput=out(choice))
add('savetocameraroll',WFInput=out(choice))
end(liveg)
# No unconditional success notification: Photos action errors must remain visible.
ref=plistlib.load(open('work/reference-decoded/Shortcut.wflow','rb'))
ref.update(WFWorkflowName='小红书选择保存 V3 实况',WFWorkflowActions=A,WFWorkflowTypes=['ActionExtension'],WFWorkflowInputContentItemClasses=['WFURLContentItem','WFStringContentItem','WFSafariWebPageContentItem'],WFWorkflowNoInputBehavior={'Name':'WFWorkflowNoInputBehaviorGetClipboard','Parameters':{}},WFWorkflowHasShortcutInputVariables=True)
plistlib.dump(ref,open('work/xhs-v3-unsigned.shortcut','wb'),fmt=plistlib.FMT_BINARY)
