# rednote-helper

项目中文名：**小红书助手**。当前快捷指令名为「小红书助手」，项目版本为 v1。

当前版本是 [小红书助手](outputs/小红书助手.shortcut)，说明见 [小红书助手 v1 说明](outputs/小红书助手%20v1%20说明.md)。快捷指令按 Live、图片、视频分流，支持预览和手动多选（默认不全选）。

## 使用声明

本项目仅供学习交流与个人技术研究。该声明本身不授予下载、保存或再分发任何第三方内容的权利。使用前请确认你有权处理相关内容，并遵守小红书及相关服务的用户协议、平台规则和适用法律；不得侵犯他人的知识产权、隐私或其他合法权益。使用者应自行判断并承担使用行为及其结果的责任。

- 静态图片与普通视频在快捷指令内解析笔记网页并从 CDN 下载，再调用系统相册动作保存；普通视频不依赖动图工厂。
- Live 图本地解析笔记页面，下载封面及配对视频，再交给动图工厂合成并保存为 Live Photo。每次进入 Live 分支都会显示“已安装，继续 / 未安装，去 App Store 下载”；下载分支打开官方页面并结束本次运行。iOS Shortcuts 没有可靠的已安装 App 检测，因此已安装用户也需每次点“继续”。
- 没有接入 Pro 作者或其他解析云服务；不要求解析授权码。

## 当前文件

| 路径 | 内容 |
| --- | --- |
| `outputs/` | V1 快捷指令和使用说明 |
| `scripts/build_v1.py` | V1 工作流生成器 |
| `scripts/test_v1_live_parser.py` | Live 配对及菜单静态检查 |
| `scripts/test_v1_image_parser.py` | 图片解析测试 |
| `scripts/test_v1_fixture.py` | 三类保存流程夹具测试 |

## 重新生成

```sh
python3 scripts/build_v1.py
shortcuts sign --mode anyone --input work/xhs-v1-unsigned.shortcut --output 'outputs/小红书助手.shortcut'
python3 scripts/test_v1_live_parser.py
python3 scripts/test_v1_image_parser.py
python3 scripts/test_v1_fixture.py
```

测试使用本地捕获的网页及媒体夹具，只覆盖本地解析与工作流结构，不模拟真实 iPhone 上的相册写入。
