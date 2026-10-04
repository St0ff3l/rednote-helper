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


def variable(name):
    return {
        "Value": {"Type": "Variable", "VariableName": name},
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
selection_actions = [
    item["WFWorkflowActionParameters"]
    for item in actions
    if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.choosefromlist"
]
assert len(selection_actions) == 3, f"expected Live, image and video selectors; found {len(selection_actions)}"
assert all(item.get("WFChooseFromListActionSelectMultiple") is True for item in selection_actions)
assert all(item.get("WFChooseFromListActionSelectAll") is False for item in selection_actions), "selectors must start with nothing selected"

# Live uses GIF Factory; show an install/continue menu every time because iOS
# Shortcuts cannot reliably inspect the installed-app inventory.
setup_index = next(
    i for i, item in enumerate(actions)
    if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.choosefrommenu"
    and item["WFWorkflowActionParameters"].get("WFMenuPrompt") == "🧰 Live 保存需要动图工厂"
)
setup = actions[setup_index]["WFWorkflowActionParameters"]
setup_group = setup["GroupingIdentifier"]
assert setup["WFMenuItems"] == ["✅ 已安装，继续", "📲 未安装，去 App Store 下载"]
setup_end = next(
    i for i in range(setup_index + 1, len(actions))
    if actions[i]["WFWorkflowActionIdentifier"] == "is.workflow.actions.choosefrommenu"
    and actions[i]["WFWorkflowActionParameters"].get("WFControlFlowMode") == 2
    and actions[i]["WFWorkflowActionParameters"].get("GroupingIdentifier") == setup_group
)
setup_block = actions[setup_index:setup_end + 1]
continue_index = next(
    i for i, item in enumerate(setup_block)
    if item["WFWorkflowActionParameters"].get("WFMenuItemTitle") == "✅ 已安装，继续"
)
download_index = next(
    i for i, item in enumerate(setup_block)
    if item["WFWorkflowActionParameters"].get("WFMenuItemTitle") == "📲 未安装，去 App Store 下载"
)
open_app_store = next(
    (i, item) for i, item in enumerate(setup_block)
    if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.openurl"
)
app_store_url = open_app_store[1]["WFWorkflowActionParameters"]["WFURL"]["Value"]["string"]
assert app_store_url == "https://apps.apple.com/us/app/id6762482512?l=zh-Hans-CN"
assert continue_index < download_index < open_app_store[0] < len(setup_block) - 1
assert setup_block[open_app_store[0] + 1]["WFWorkflowActionIdentifier"] == "is.workflow.actions.exit", "App Store branch must end the current run"
assert "is.workflow.actions.nothing" in [item["WFWorkflowActionIdentifier"] for item in setup_block[continue_index + 1:download_index]], "continue branch must fall through without opening the App Store"

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

    response_var = action("getvariable", WFVariable=variable("解析响应"))
    response_dictionary = action("detect.dictionary", WFInput=output(response_var["WFWorkflowActionParameters"]["UUID"]))
    response_code = action(
        "getvalueforkey",
        WFInput=output(response_dictionary["WFWorkflowActionParameters"]["UUID"]),
        WFDictionaryKey="code",
        WFGetDictionaryValueType="Value",
    )
    match_code = action(
        "text.match",
        text=text_token(response_code["WFWorkflowActionParameters"]["UUID"]),
        WFMatchTextPattern=r"^0$",
        WFMatchTextCaseSensitive=True,
    )
    count_code = action("count", Input=output(match_code["WFWorkflowActionParameters"]["UUID"]), WFCountType="Items")
    report_code = action("gettext", WFTextActionText=text_token(count_code["WFWorkflowActionParameters"]["UUID"], "V46_CODE_MATCHES="))
    response_body = action(
        "getvalueforkey",
        WFInput=output(response_dictionary["WFWorkflowActionParameters"]["UUID"]),
        WFDictionaryKey="body",
        WFGetDictionaryValueType="Value",
    )
    response_lives = action(
        "getvalueforkey",
        WFInput=output(response_body["WFWorkflowActionParameters"]["UUID"]),
        WFDictionaryKey="lives",
        WFGetDictionaryValueType="Value",
    )
    split_lives = action("text.split", text=output(response_lives["WFWorkflowActionParameters"]["UUID"]), WFTextSeparator="New Lines")
    match_wrapped_pairs = action(
        "text.match",
        text=text_token(split_lives["WFWorkflowActionParameters"]["UUID"]),
        WFMatchTextPattern=exact_pair_pattern,
        WFMatchTextCaseSensitive=True,
    )
    count_wrapped_pairs = action("count", Input=output(match_wrapped_pairs["WFWorkflowActionParameters"]["UUID"]), WFCountType="Items")
    report_wrapped_pairs = action(
        "gettext",
        WFTextActionText=text_token(count_wrapped_pairs["WFWorkflowActionParameters"]["UUID"], "V46_WRAPPED_PAIR_MATCHES="),
    )
    block.extend([
        response_var,
        response_dictionary,
        response_code,
        match_code,
        count_code,
        report_code,
        response_body,
        response_lives,
        split_lives,
        match_wrapped_pairs,
        count_wrapped_pairs,
        report_wrapped_pairs,
    ])

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
    expected_code_report = "V46_CODE_MATCHES=1"
    expected_wrapped_report = f"V46_WRAPPED_PAIR_MATCHES={expected_count}"
    assert run.returncode == 0 and "DONE OK false" in log, (sample_name, log[-2000:])
    assert expected_report in log, (sample_name, expected_report, log[-2500:])
    assert expected_code_report in log, (sample_name, expected_code_report, log[-3500:])
    assert expected_wrapped_report in log, (sample_name, expected_wrapped_report, log[-3500:])
    assert "ACTION is.workflow.actions.alert Error" not in log, (sample_name, log[-1500:])
    print(f"{sample_name}: valid response code and all {expected_count} wrapped cover/video pairs matched")
