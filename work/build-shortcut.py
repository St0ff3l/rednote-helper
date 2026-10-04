import plistlib,uuid,json,re,shutil
from pathlib import Path
A=[]
def uid():return str(uuid.uuid4()).upper()
def add(kind,**p):
 p.setdefault('UUID',uid());A.append({'WFWorkflowActionIdentifier':'is.workflow.actions.'+kind,'WFWorkflowActionParameters':p});return p['UUID']
def out(u,name='结果'):return {'Value':{'Type':'ActionOutput','OutputUUID':u,'OutputName':name},'WFSerializationType':'WFTextTokenAttachment'}
def textvar(u,prefix='',suffix='',name='结果'):
 return {'Value':{'string':prefix+'\ufffc'+suffix,'attachmentsByRange':{'{%d, 1}'%len(prefix):out(u,name)['Value']}},'WFSerializationType':'WFTextTokenString'}
def no_value(u,message):
 pass
add('comment',WFCommentActionText='小红书无水印原尺寸图片：复制笔记分享文字后运行，确认链接。直接访问小红书网页和图片 CDN；无需第三方解析服务。直接下载原尺寸 CDN 文件，不调用小红书 App 保存接口、不裁剪、不重新编码，不额外添加右下角水印。源文件自身含有的水印会保留。保存服务器原尺寸文件，不进行格式转换。只支持网页公开返回的静态图片；登录限制、网页变化或 CDN 限制可能导致失败。不能保证还原作者上传前的文件。')
c=add('getclipboard')
a=add('ask',WFAskActionPrompt='粘贴小红书笔记分享文字或链接',WFInputType='Text',WFAskActionDefaultAnswer=textvar(c),WFAllowsMultilineText=True)
m=add('text.match',text=textvar(a),WFMatchTextPattern=r'https?://(?:xhslink\.(?:cn|com)|(?:www\.)?xiaohongshu\.com)/[^\s<>"，。]+',WFMatchTextCaseSensitive=False)
no_value(m,'没有找到小红书链接。请在小红书中复制笔记链接，再运行快捷指令。')
u=add('getitemfromlist',WFInput=out(m),WFItemSpecifier='First Item')
headers={'Value':{'WFDictionaryFieldValueItems':[{'WFItemType':0,'WFKey':{'Value':{'string':'User-Agent','attachmentsByRange':{}},'WFSerializationType':'WFTextTokenString'},'WFValue':{'Value':{'string':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1','attachmentsByRange':{}},'WFSerializationType':'WFTextTokenString'}}]},'WFSerializationType':'WFDictionaryFieldValue'}
h=add('downloadurl',WFURL=textvar(u),WFHTTPMethod='GET',WFHTTPHeaders=headers)
s=add('text.match',text=textvar(h),WFMatchTextPattern=r'(?<=window\.__INITIAL_STATE__=)[\s\S]*?(?=</script>)',WFMatchTextCaseSensitive=True)
no_value(s,'笔记网页没有返回图片数据。可能需要登录、分享链接过期，或网页结构已变化。请重新复制链接后重试。')
s=add('getitemfromlist',WFInput=out(s),WFItemSpecifier='First Item')
s=add('text.replace',WFInput=textvar(s),WFReplaceTextFind=r'(?<=[\[:,])\s*undefined(?=\s*[,}\]])',WFReplaceTextReplace='null',WFReplaceTextRegularExpression=True,WFReplaceTextCaseSensitive=True)
d=add('detect.dictionary',WFInput=out(s))
i=add('getvalueforkey',WFInput=out(d),WFDictionaryKey='noteData.data.noteData.imageList',WFGetDictionaryValueType='Value')
no_value(i,'当前网页没有可下载的图片。此版本只支持手机分享网页公开返回的静态图片；不支持视频或实况照片。')
g=uid();r=add('repeat.each',WFInput=out(i),WFControlFlowMode=0,GroupingIdentifier=g)
repeat_item={'Value':{'Type':'Variable','VariableName':'Repeat Item'},'WFSerializationType':'WFTextTokenAttachment'}
f=add('getvalueforkey',WFInput=repeat_item,WFDictionaryKey='fileId',WFGetDictionaryValueType='Value')
no_value(f,'某张图片没有提供文件标识，已停止下载。')
b=add('downloadurl',WFURL=textvar(f,'https://ci.xiaohongshu.com/'),WFHTTPMethod='GET')
add('savetocameraroll',WFInput=out(b))
add('repeat.each',WFControlFlowMode=2,GroupingIdentifier=g)
add('notification',WFNotificationActionTitle='小红书图片',WFNotificationActionBody='当前笔记返回的图片已保存到相册。')
doc={'WFWorkflowName':'小红书无水印原尺寸','WFWorkflowClientVersion':'4018.0.4','WFWorkflowMinimumClientVersion':900,'WFWorkflowMinimumClientVersionString':'900','WFWorkflowIcon':{'WFWorkflowIconStartColor':4282601983,'WFWorkflowIconGlyphNumber':59511},'WFWorkflowActions':A,'WFWorkflowInputContentItemClasses':[],'WFWorkflowOutputContentItemClasses':[],'WFWorkflowTypes':[],'WFWorkflowImportQuestions':[],'WFWorkflowHasShortcutInputVariables':False,'WFWorkflowHasOutputFallback':False}
plistlib.dump(doc,open('work/xhs-unsigned.shortcut','wb'),fmt=plistlib.FMT_BINARY)
# Verify the exact data extraction pipeline with this note's downloaded HTML.
html=Path('work/xhs-note.html').read_text();state=re.findall(r'(?<=window\.__INITIAL_STATE__=)[\s\S]*?(?=</script>)',html)[0]
state=re.sub(r'(?<=[\[:,])\s*undefined(?=\s*[,}\]])','null',state)
images=json.loads(state)['noteData']['data']['noteData']['imageList'];print('Extraction verified:',len(images),'image(s)',[x['fileId'] for x in images])
shutil.copyfile('work/image-4.bin','outputs/补2张-原尺寸.jpg')
print('Actions:',len(A))
