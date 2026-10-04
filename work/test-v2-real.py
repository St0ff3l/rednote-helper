import plistlib,uuid,copy,base64
p=plistlib.load(open('work/xhs-v2-unsigned.shortcut','rb'))
v=lambda u:{'Value':{'Type':'ActionOutput','OutputUUID':u,'OutputName':'结果'},'WFSerializationType':'WFTextTokenAttachment'}
for name,source in [('image','work/xhs-note.html'),('live','work/live-note.html'),('video','work/video-note.html')]:
 t=copy.deepcopy(p);a=t['WFWorkflowActions'];web=next(i for i,x in enumerate(a) if x['WFWorkflowActionIdentifier']=='is.workflow.actions.downloadurl');a=a[web:]
 orig=a[0]['WFWorkflowActionParameters']['UUID'];u=str(uuid.uuid4()).upper();a[0]={'WFWorkflowActionIdentifier':'is.workflow.actions.getrichtextfromhtml','WFWorkflowActionParameters':{'UUID':orig,'WFHTML':v(u)}}
 a.insert(0,{'WFWorkflowActionIdentifier':'is.workflow.actions.gettext','WFWorkflowActionParameters':{'UUID':u,'WFTextActionText':open(source).read()}})
 result=[]
 for x in a:
  par=x['WFWorkflowActionParameters'];kind=x['WFWorkflowActionIdentifier']
  if kind=='is.workflow.actions.downloadurl':
   u=str(uuid.uuid4()).upper();result.append({'WFWorkflowActionIdentifier':'is.workflow.actions.gettext','WFWorkflowActionParameters':{'UUID':u,'WFTextActionText':base64.b64encode(open('work/image-0.bin','rb').read()).decode()}})
   x={'WFWorkflowActionIdentifier':'is.workflow.actions.base64encode','WFWorkflowActionParameters':{'UUID':par['UUID'],'WFEncodeMode':'Decode','WFInput':v(u)}}
  elif kind=='is.workflow.actions.choosefromlist':
   if par['WFChooseFromListActionPrompt'].startswith('选择保存类型'):
    x={'WFWorkflowActionIdentifier':'is.workflow.actions.gettext','WFWorkflowActionParameters':{'UUID':par['UUID'],'WFTextActionText':'3 图片和动态视频（分别保存）'}}
   else:
    x={'WFWorkflowActionIdentifier':'is.workflow.actions.getitemfromlist','WFWorkflowActionParameters':{'UUID':par['UUID'],'WFInput':par['WFInput'],'WFItemSpecifier':'First Item'}}
  elif kind=='is.workflow.actions.alert' and par.get('WFAlertActionTitle')=='此笔记包含 Live 图':
   x={'WFWorkflowActionIdentifier':'is.workflow.actions.comment','WFWorkflowActionParameters':{'UUID':par['UUID'],'WFCommentActionText':'Live alert suppressed in automated parser test only.'}}
  result.append(x)
  if kind=='is.workflow.actions.getvariable' and par.get('WFVariable',{}).get('Value',{}).get('VariableName')=='下载地址':break
 t['WFWorkflowActions']=result;t['WFWorkflowHasShortcutInputVariables']=False;t['WFWorkflowTypes']=[]
 plistlib.dump(t,open('work/test-v2-real-'+name+'.shortcut','wb'))
