"""Run the local Live parser against captured public-note pages; no photo writes."""
import base64
import copy
import json
import plistlib
import re
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHORTCUT = ROOT / "work/xhs-v4-unsigned.shortcut"
SAMPLES = [
    ("live-2qp-mobile.html", 10),
    ("live-7e2g-mobile.html", 9),
]


def output(uuid_value):
    return {
        "Value": {"Type": "ActionOutput", "OutputUUID": uuid_value, "OutputName": "结果"},
        "WFSerializationType": "WFTextTokenAttachment",
    }


def text_token(uuid_value, prefix="", suffix=""):
    offset = len(prefix.encode("utf-16-le")) // 2
    return {
        "Value": {
            "string": prefix + "\ufffc" + suffix,
            "attachmentsByRange": {f"{{{offset}, 1}}": output(uuid_value)["Value"]},
        },
        "WFSerializationType": "WFTextTokenString",
    }


def action(kind, **parameters):
    parameters["UUID"] = str(uuid.uuid4()).upper()
    return {"WFWorkflowActionIdentifier": "is.workflow.actions." + kind, "WFWorkflowActionParameters": parameters}


def note_pairs(html):
    match = re.search(r"window\.__INITIAL_STATE__\s*=\s*(.*?)</script>", html, re.S)
    assert match, "captured mobile HTML has no initial state"
    raw = re.sub(r"\bundefined\b", "null", match.group(1).strip().removesuffix(";"))
    state = json.loads(raw)
    note = state["noteData"]["data"]["noteData"]
    pairs = []
    for image in note["imageList"]:
        if image.get("livePhoto") is not True:
            continue
        cover = "https://ci.xiaohongshu.com/" + image["fileId"]
        video = image["stream"]["h264"][0]["masterUrl"].replace("http://", "https://", 1)
        pairs.append((cover, video))
    return pairs


document = plistlib.load(open(SHORTCUT, "rb"))
actions = document["WFWorkflowActions"]
download_index = next(
    i for i, item in enumerate(actions)
    if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.downloadurl"
    and "User-Agent" in str(item["WFWorkflowActionParameters"].get("WFHTTPHeaders"))
)
response_end = next(
    i for i in range(download_index + 1, len(actions))
    if actions[i]["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvariable"
    and actions[i]["WFWorkflowActionParameters"].get("WFVariableName") == "解析响应"
)

for sample_name, expected_count in SAMPLES:
    sample_path = ROOT / "work" / sample_name
    html = sample_path.read_text(errors="replace")
    expected_pairs = note_pairs(html)
    assert len(expected_pairs) == expected_count, (sample_name, len(expected_pairs))

    block = copy.deepcopy(actions[download_index:response_end + 1])
    download_uuid = block[0]["WFWorkflowActionParameters"]["UUID"]
    encoded = base64.b64encode(sample_path.read_bytes()).decode("ascii")
    block[0] = action("gettext", WFTextActionText=encoded)
    decode = action("base64encode", WFInput=output(block[0]["WFWorkflowActionParameters"]["UUID"]), WFEncodeMode="Decode")
    decode["WFWorkflowActionParameters"]["UUID"] = download_uuid
    block.insert(1, decode)

    pair_variable_index = next(
        i for i, item in enumerate(block)
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.getvariable"
        and item["WFWorkflowActionParameters"].get("WFVariable", {}).get("Value", {}).get("VariableName") == "本地Live配对JSON"
    )
    pair_variable_uuid = block[pair_variable_index]["WFWorkflowActionParameters"]["UUID"]
    exact_pair_pattern = r"(?:" + "|".join(
        re.escape(json.dumps({"pic": cover, "video": video}, ensure_ascii=False, separators=(",", ":")))
        for cover, video in expected_pairs
    ) + r")"
    match_pairs = action(
        "text.match",
        text=text_token(pair_variable_uuid),
        WFMatchTextPattern=exact_pair_pattern,
        WFMatchTextCaseSensitive=True,
    )
    count_pairs = action("count", Input=output(match_pairs["WFWorkflowActionParameters"]["UUID"]), WFCountType="Items")
    report = action("gettext", WFTextActionText=text_token(count_pairs["WFWorkflowActionParameters"]["UUID"], "V46_PAIR_MATCHES="))
    block[pair_variable_index + 1:pair_variable_index + 1] = [match_pairs, count_pairs, report]

    fixture = copy.deepcopy(document)
    fixture["WFWorkflowActions"] = block
    fixture["WFWorkflowTypes"] = []
    fixture["WFWorkflowHasShortcutInputVariables"] = False
    fixture_path = ROOT / "work" / f"test-v4-live-{expected_count}.shortcut"
    plistlib.dump(fixture, open(fixture_path, "wb"))

    run = subprocess.run(
        ["swift", "work/run-native.swift", str(fixture_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    log = run.stdout + run.stderr
    (ROOT / "work" / f"test-v4-live-{expected_count}.log").write_text(log)
    expected_report = f"V46_PAIR_MATCHES={expected_count}"
    assert run.returncode == 0 and "DONE OK false" in log, (sample_name, log[-2000:])
    assert expected_report in log, (sample_name, expected_report, log[-2500:])
    assert "ACTION is.workflow.actions.alert Error" not in log, (sample_name, log[-1500:])
    print(f"{sample_name}: all {expected_count} exact cover/video pairs matched")
