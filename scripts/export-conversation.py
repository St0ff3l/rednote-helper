"""Snapshot this project's original Codex conversation. Does not alter Codex state."""
import argparse
import json
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('session', type=Path, help='Exact JSONL file for the conversation to archive')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
archive = root / 'archive'
archive.mkdir(exist_ok=True)
shutil.copy2(args.session, archive / 'conversation.jsonl')
messages = []
for line in args.session.read_text().splitlines():
    record = json.loads(line)
    payload = record.get('payload', {})
    if record.get('type') != 'response_item' or payload.get('type') != 'message':
        continue
    role = payload.get('role')
    if role not in ('user', 'assistant'):
        continue
    parts = []
    for content in payload.get('content', []):
        if content.get('type') in ('input_text', 'output_text'):
            parts.append(content.get('text', ''))
        elif content.get('type') in ('input_image', 'image'):
            parts.append('[图片附件；原截图见 screenshots/，嵌入数据见 conversation.jsonl]')
    if parts:
        label = '用户' if role == 'user' else '助手'
        messages.append(f"## {label} · {record.get('timestamp', '')}\n\n" + '\n\n'.join(parts))
heading = '# 当前对话存档\n\n此文件是导出时的快照，后续消息不自动同步。原始 JSONL 包含工具调用、结果与压缩记录。\n\n'
(archive / 'conversation.md').write_text(heading + '\n\n'.join(messages))
print(f'Exported {len(messages)} messages')
