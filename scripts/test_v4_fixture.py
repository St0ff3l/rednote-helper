"""Verify three branches and URL pairing with local fixtures; never call Apps/Photos."""
import base64,copy,plistlib,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=plistlib.load(open(ROOT/'work/xhs-v4-unsigned.shortcut','rb'))
def out(u):return {'Value':{'Type':'ActionOutput','OutputUUID':u,'OutputName':'结果'},'WFSerializationType':'WFTextTokenAttachment'}
def action(k,u=None,**q):q['UUID']=u or str(uuid.uuid4()).upper();return {'WFWorkflowActionIdentifier':'is.workflow.actions.'+k,'WFWorkflowActionParameters':q}
def literal(s,u=None):return action('gettext',u,WFTextActionText=s)
import json
for mode,label in [(1,'live'),(2,'image'),(3,'video')]:
 a=copy.deepcopy(p['WFWorkflowActions']);start=next(i for i,x in enumerate(a) if x['WFWorkflowActionIdentifier']=='is.workflow.actions.detect.dictionary' and x['WFWorkflowActionParameters'].get('WFInput',{}).get('Value',{}).get('VariableName')=='解析响应');a=a[start:]
 payload={'code':0,'body':{'urls':'https://example.test/one\nhttps://example.test/two','lives':json.dumps({'pic':'https://example.test/cover-1','video':'https://example.test/video-1'})+'\n'+json.dumps({'pic':'https://example.test/cover-2','video':'https://example.test/video-2'})}}
 result=[]
 for name,value in [('保存类型',str(mode)),('解析响应',json.dumps(payload)),('服务配置',json.dumps({'Rename':'视频.mp4'}))]:
  l=action('number',WFNumberActionNumber=value) if name=='保存类型' else literal(value);result.append(l)
  if name=='服务配置':l=action('detect.dictionary',WFInput=out(l['WFWorkflowActionParameters']['UUID']));result.append(l)
  result.append(action('setvariable',WFInput=out(l['WFWorkflowActionParameters']['UUID']),WFVariableName=name))
 for i,x in enumerate(a):
  k=x['WFWorkflowActionIdentifier'];q=x['WFWorkflowActionParameters'];u=q['UUID']
  if k=='is.workflow.actions.downloadurl':
   following=a[i+1]['WFWorkflowActionIdentifier']
   data=(ROOT/'work'/('image-0.bin' if mode!=3 else 'live-sample.mp4')).read_bytes()
   l=literal(base64.b64encode(data).decode());result.append(l)
   x=action('base64encode',u,WFInput=out(l['WFWorkflowActionParameters']['UUID']),WFEncodeMode='Decode')
  elif k=='is.workflow.actions.choosefromlist':x=action('getitemfromlist',u,WFInput=q['WFInput'],WFItemSpecifier='Last Item')
  elif k=='is.workflow.actions.previewdocument':x=action('getvariable',u,WFVariable=q['WFInput'])
  elif k.endswith('LiveExtension'):
   result.append(action('gettext',WFTextActionText=q['imageURL']));result.append(action('gettext',WFTextActionText=q['videoURL']))
   x=action('number',u,WFNumberActionNumber='0')
  elif k.endswith('ResourceExtractionExtension'):x=action('gettext',u,WFTextActionText=q['mediaURL'])
  elif k=='is.workflow.actions.savetocameraroll':x=action('getitemtype',u,WFInput=q['WFInput'])
  result.append(x)
 t=copy.deepcopy(p);t['WFWorkflowActions']=result;t['WFWorkflowHasShortcutInputVariables']=False;t['WFWorkflowTypes']=[]
 plistlib.dump(t,open(ROOT/'work'/('test-v4-'+label+'.shortcut'),'wb'))
print('Fixtures: service reply + local files; save calls captured, not executed')

if __name__ == '__main__':
 import subprocess
 for label in ('live','image','video'):
  run=subprocess.run(['swift','work/run-native.swift',f'work/test-v4-{label}.shortcut'],cwd=ROOT,capture_output=True,text=True)
  log=run.stdout+run.stderr
  (ROOT/'work'/f'v4-{label}.log').write_text(log)
  assert run.returncode == 0 and 'DONE OK false' in log, (label,log[-1500:])
  if label=='live':
   assert ': https://example.test/cover-2' in log and ': https://example.test/video-2' in log
   assert ': Media' not in log
  elif label=='image':
   assert ': https://example.test/two' in log and ': Media' not in log
  else:
   assert ': Media' in log and ': https://example.test/cover-2' not in log
  print(label, 'fixture passed; App and Photos save calls replaced')
