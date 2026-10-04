# xhs-media-helper

xhs 素材获取助手：用于 iOS 快捷指令的图片、视频和 Live 素材解析、预览、多选及相册保存实验。

## 当前状态

- 最新文件：`outputs/小红书选择保存-V3-实况.shortcut`。
- 静态图下载原尺寸文件；真实样例已验证原尺寸静态图没有平台附加水印。
- 支持预览、多选；V3 加入 Actions 的“Make Live Photo from Video”动作。当前 Actions 版本需要 iOS 26+。
- 真实笔记的本地解析与素材匹配测试通过；签名和导入通过。
- **尚未完成 iPhone 相册保存验证；Live 动态视频无水印目标尚未完成。**
- 已抽帧确认用户提供的 Live 笔记，其网页动态视频右下角含小红书水印。合成不会消除它。
- Actions 从视频帧生成封面，不能保留独立原尺寸封面。不得将该合成过程描述为原始 Live Photo 无损还原。
- 用户选择在 iPhone 测试，不授权在 Mac 运行下载的 Actions App。

## 文件

| 路径 | 内容 |
| --- | --- |
| `outputs/` | 各版签名快捷指令、样例图片和说明 |
| `work/build-v3.py` | V3 生成脚本，依赖 V2 及参考快捷指令 |
| `work/build-v3-generated.py` | 展开的 V3 生成脚本 |
| `work/run-native.swift` | macOS 原生快捷指令执行器测试工具 |
| `work/test-v3-real.py` | 从已捕获网页构建解析测试夹具 |
| `work/real-v3-live.log` | V3 Live 解析测试结果 |
| `work/actions-app/` | 作者官网链接下载的 Actions 4.0.1，仅用于静态元数据核对，未运行 |
| `archive/conversation.md` | 可读对话存档 |
| `archive/conversation.jsonl` | 原始对话记录，含工具调用与结果 |
| `archive/screenshots/` | 用户提供的原始流程截图 |
| `archive/migration-manifest.json` | 原文件校验清单 |

下载的 App、原始网页/媒体、生成的测试夹具、执行日志及完整 JSONL 对话仅在本地保留，由 `.gitignore` 排除。仓库保留源码、参考工作流、签名快捷指令、说明、可读对话及用户截图。解析测试依赖本地捕获的网页，不是新克隆仓库即可运行的联网测试。

此仓库为私密研究存档。网页响应和签名媒体地址可能过期，记录中可能包含个人对话信息。第三方 App、素材及代码的权利属于原作者；未授予整个存档统一开源许可证。

## 重新生成

在项目根目录执行（macOS）：

```sh
python3 work/build-v3.py
shortcuts sign --mode anyone --input work/xhs-v3-unsigned.shortcut --output outputs/小红书选择保存-V3-实况.shortcut
python3 work/test-v3-real.py
swift work/run-native.swift work/test-v3-real-live.shortcut
```

签名不代表手机保存验证完成。测试夹具替代了联网、用户选择和相册动作，只验证解析及对应媒体地址。
