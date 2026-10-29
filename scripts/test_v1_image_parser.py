"""Test V1 image parser against locally captured HTML; no network or photo writes."""
import base64
import copy
import plistlib
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
doc = plistlib.load(open(ROOT / 'work/xhs-v1-unsigned.shortcut', 'rb'))
actions = doc['WFWorkflowActions']
image_menu = next(i for i, a in enumerate(actions) if a['WFWorkflowActionIdentifier'] == 'is.workflow.actions.choosefrommenu' and a['WFWorkflowActionParameters'].get('WFMenuItemTitle') == '🖼️ 图片')
start = next(i for i in range(image_menu + 1, len(actions)) if actions[i]['WFWorkflowActionIdentifier'].endswith('.downloadurl') and 'User-Agent' in str(actions[i]['WFWorkflowActionParameters']))
stop = next(i for i in range(start, len(actions)) if actions[i]['WFWorkflowActionIdentifier'].endswith('.setvariable') and actions[i]['WFWorkflowActionParameters'].get('WFVariableName') == '解析响应')
items = copy.deepcopy(actions[start:stop+1])
def out(u):
    return {'Value': {'Type':'ActionOutput','OutputUUID':u,'OutputName':'结果'},'WFSerializationType':'WFTextTokenAttachment'}
def action(kind, u=None, **params):
    params['UUID'] = u or str(uuid.uuid4()).upper()
    return {'WFWorkflowActionIdentifier':'is.workflow.actions.'+kind,'WFWorkflowActionParameters':params}
u = items[0]['WFWorkflowActionParameters']['UUID']
t = str(uuid.uuid4()).upper()
items[0] = action('base64encode', u, WFInput=out(t), WFEncodeMode='Decode')
items.insert(0, action('gettext', t, WFTextActionText=base64.b64encode((ROOT/'work/wallpaper-mobile.html').read_bytes()).decode()))
last = items[-1]['WFWorkflowActionParameters']['UUID']
# Convert the constructed service-shaped JSON back into URLs and count them.
d = action('detect.dictionary', WFInput=out(last)); items.append(d)
v = action('getvalueforkey', WFInput=out(d['WFWorkflowActionParameters']['UUID']), WFDictionaryKey='body.urls', WFGetDictionaryValueType='Value'); items.append(v)
s = action('text.split', text=out(v['WFWorkflowActionParameters']['UUID']), WFTextSeparator='New Lines'); items.append(s)
items.append(action('count', Input=out(s['WFWorkflowActionParameters']['UUID']), WFCountType='Items'))
fixture = copy.deepcopy(doc)
fixture['WFWorkflowActions'] = items
fixture['WFWorkflowTypes'] = []
fixture['WFWorkflowHasShortcutInputVariables'] = False
path = ROOT/'work/test-v1-wallpaper-parser.shortcut'
plistlib.dump(fixture, open(path, 'wb'))
run = subprocess.run(['swift','work/run-native.swift',str(path)], cwd=ROOT, capture_output=True, text=True)
log = run.stdout + run.stderr
(ROOT/'work/wallpaper-parser.log').write_text(log)
assert run.returncode == 0 and 'DONE OK false' in log, log[-1000:]
assert 'https://ci.xiaohongshu.com/1040g2sg323jrojj8nuk05pd1b6l8gnpj4293vm0?imageView2/format/jpg' in log
assert log.rstrip().endswith('DONE OK false') and ': 2"' in log[-1000:]
print('Real wallpaper HTML parser passed: two original image URLs; no network/App/Photos calls')
