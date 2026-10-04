# rednote-helper

项目中文名：**小红书助手**。当前快捷指令名为「小红书助手」，项目版本为 v1。

当前版本是 [小红书助手](outputs/小红书助手.shortcut)，说明见 [小红书助手 v1 说明](outputs/小红书助手%20v1%20说明.md)。快捷指令按 Live、图片、视频分流，支持预览和手动多选（默认不全选）。

- 静态图片与普通视频在快捷指令内解析笔记网页并从 CDN 下载，再调用系统相册动作保存；普通视频不依赖动图工厂。
- Live 图本地解析笔记页面，下载封面及配对视频，再交给动图工厂合成并保存为 Live Photo。每次进入 Live 分支都会显示“已安装，继续 / 未安装，去 App Store 下载”；下载分支打开官方页面并结束本次运行。iOS Shortcuts 没有可靠的已安装 App 检测，因此已安装用户也需每次点“继续”。
- 没有接入 Pro 作者或其他解析云服务；不要求解析授权码。动态源是否带水印、封面是否保持原尺寸、以及 Live 是否成功写入 iPhone 相册仍需实机验证。

`references/` 保存两份仅供本项目内部对照的快捷指令：Pro v4.7，以及用户提供的独立参考快捷指令「小红书下载器」（分享卡片标题）。两者与本项目独立，名称和流程不作为本项目产品名或最终实现的来源。

## 当前文件

| 路径 | 内容 |
| --- | --- |
| `outputs/` | V1 快捷指令和使用说明 |
| `references/` | Pro 与流程参考原件，仅供对照 |
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

测试使用本地捕获的网页及媒体夹具。它们替换网络、第三方 App、用户选择和相册写入；测试结果不代表 iPhone 端到端保存成功。
