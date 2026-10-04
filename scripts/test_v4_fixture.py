"""Verify three branches and URL pairing with local fixtures; never call Apps/Photos."""
import base64,copy,plistlib,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=plistlib.load(open(ROOT/'work/xhs-v4-unsigned.shortcut','rb'))
def out(u):return {'Value':{'Type':'ActionOutput','OutputUUID':u,'OutputName':'结果'},'WFSerializationType':'WFTextTokenAttachment'}
def action(k,u=None,**q):q['UUID']=u or str(uuid.uuid4()).upper();return {'WFWorkflowActionIdentifier':'is.workflow.actions.'+k,'WFWorkflowActionParameters':q}
def literal(s,u=None):return action('gettext',u,WFTextActionText=s)
import json
for mode,label in [(1,'live'),(2,'image'),(3,'video'),(2,'service-error')]:
 a=copy.deepcopy(p['WFWorkflowActions']);start=next(i for i,x in enumerate(a) if x['WFWorkflowActionIdentifier']=='is.workflow.actions.detect.dictionary' and x['WFWorkflowActionParameters'].get('WFInput',{}).get('Value',{}).get('VariableName')=='解析响应');a=a[start:]
 payload={'code':0,'body':{'urls':'https://example.test/one\nhttps://example.test/two','lives':json.dumps({'pic':'https://example.test/cover-1','video':'https://example.test/video-1'})+'\n'+json.dumps({'pic':'https://example.test/cover-2','video':'https://example.test/video-2'})}}
 if label=='service-error':payload.update(code=1,msg='fixture service unavailable')
 result=[]
 for name,value in [('保存类型',str(mode)),('解析响应',json.dumps(payload)),('服务配置',json.dumps({'Rename':'视频.mp4'}))]:
  l=action('number',WFNumberActionNumber=value) if name=='保存类型' else literal(value);result.append(l)
  if name=='服务配置':l=action('detect.dictionary',WFInput=out(l['WFWorkflowActionParameters']['UUID']));result.append(l)
  result.append(action('setvariable',WFInput=out(l['WFWorkflowActionParameters']['UUID']),WFVariableName=name))
 for i,x in enumerate(a):
  k=x['WFWorkflowActionIdentifier'];q=x['WFWorkflowActionParameters'];u=q['UUID']
  if k=='is.workflow.actions.downloadurl':
   result.append(action('gettext',WFTextActionText=q['WFURL']))
   nextq=a[i+1]['WFWorkflowActionParameters']
   is_live_video=mode==1 and nextq.get('Input',{}).get('Value',{}).get('OutputUUID')==u
   data=(ROOT/'work'/('live-sample.mp4' if mode==3 or is_live_video else 'image-0.bin')).read_bytes()
   l=literal(base64.b64encode(data).decode());result.append(l)
   x=action('base64encode',u,WFInput=out(l['WFWorkflowActionParameters']['UUID']),WFEncodeMode='Decode')
  elif k=='is.workflow.actions.choosefromlist':x=action('getitemfromlist',u,WFInput=q['WFInput'],WFItemSpecifier='Last Item')
  elif k=='is.workflow.actions.previewdocument':x=action('getvariable',u,WFVariable=q['WFInput'])
  elif k.endswith('SaveLivePhotoFromFilesIntent'):
   result.append(literal('CAPTURE_LIVE_FILES'))
   result.append(action('getitemname',WFInput=q['imageFile']))
   result.append(action('getitemtype',WFInput=q['videoFile']))
   x=action('nothing',u)
  elif k.endswith('LiveExtension'):
   result.append(action('gettext',WFTextActionText=q['imageURL']));result.append(action('gettext',WFTextActionText=q['videoURL']))
   x=action('number',u,WFNumberActionNumber='0')
  elif k.endswith('ResourceExtractionExtension'):x=action('gettext',u,WFTextActionText=q['mediaURL'])
  elif k=='is.workflow.actions.savetocameraroll':
   result.append(literal('CAPTURE_PHOTOS_SAVE'))
   x=action('getitemtype',u,WFInput=q['WFInput'])
  elif k=='is.workflow.actions.alert':x=action('gettext',u,WFTextActionText=q['WFAlertActionMessage'])
  elif k=='is.workflow.actions.notification':
   result.append(literal('CAPTURE_SUCCESS_NOTIFICATION'))
   x=action('gettext',u,WFTextActionText=q['WFNotificationActionBody'])
  result.append(x)
 t=copy.deepcopy(p);t['WFWorkflowActions']=result;t['WFWorkflowHasShortcutInputVariables']=False;t['WFWorkflowTypes']=[]
 plistlib.dump(t,open(ROOT/'work'/('test-v4-'+label+'.shortcut'),'wb'))
print('Fixtures: service reply + local files; save calls captured, not executed')

if __name__ == '__main__':
 import subprocess
 for label in ('live','image','video','service-error'):
  run=subprocess.run(['swift','work/run-native.swift',f'work/test-v4-{label}.shortcut'],cwd=ROOT,capture_output=True,text=True)
  log=run.stdout+run.stderr
  (ROOT/'work'/f'v4-{label}.log').write_text(log)
  assert run.returncode == 0 and 'DONE OK false' in log, (label,log[-1500:])
  if label=='service-error':
   assert 'fixture service unavailable' in log and 'CAPTURE_SUCCESS_NOTIFICATION' not in log and 'CAPTURE_PHOTOS_SAVE' not in log
   print('service-error fixture passed; no save or success notification')
   continue
  assert log.count(': CAPTURE_SUCCESS_NOTIFICATION') == 1, log[-2000:]
  marker = 'CAPTURE_LIVE_FILES' if label=='live' else 'CAPTURE_PHOTOS_SAVE'
  assert log.index(marker) < log.index('CAPTURE_SUCCESS_NOTIFICATION')
  assert r'\U5df2\U4fdd\U5b58 1' in log, log[-2000:]
  if label=='live':
   assert ': https://example.test/cover-2' in log and ': https://example.test/video-2' in log
   assert 'CAPTURE_LIVE_FILES' in log and ': 2\"' in log and ': Media' in log
  elif label=='image':
   assert ': https://example.test/two' in log and ': Image' in log and ': Media' not in log
  else:
   assert ': Media' in log and ': https://example.test/cover-2' not in log
  print(label, 'fixture passed; App and Photos save calls replaced')
