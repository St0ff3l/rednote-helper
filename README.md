# xhs-media-helper

xhs 素材获取助手：用于 iOS 快捷指令的图片、视频和 Live 素材解析、预览、多选及相册保存实验。

## 当前状态

- 最新优化版：`outputs/xhs-media-helper-v4.1.shortcut`，说明见 `outputs/V4.1动图工厂版说明.md`；原 V4 保留用于回退。
- 用户选择沿用参考作者的实况捷径 App 和解析服务。初始菜单分为 Live、图片、视频，支持预览和多选。
- V4.1 将独立封面 PNG 与视频文件交给动图工厂保存，图片 PNG 与视频使用系统相册。Live 解析仍需要实况捷径的 payload；未接入新卖家的付费解析和设备绑定。
- 三路本地夹具验证通过，已签名；**尚未在 iPhone 验证实际保存，真实解析服务 POST 也未在此环境验证成功**。
- **动态源无水印与保存后的原尺寸封面仍需验证**；不裁剪或 AI 擦除，不把拆分保存等同于 Live Photo。
- 不在 Mac 运行下载的 Actions 或实况捷径 App。V3 和免费版实验不作为当前推荐版本。
- 参考作者服务有免费额度及付费限制，详见说明。

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
python3 scripts/build_v4.py
shortcuts sign --mode anyone --input work/xhs-v4-unsigned.shortcut --output outputs/xhs-media-helper-v4.1.shortcut
python3 scripts/test_v4_fixture.py
```

夹具依赖本地 `work/image-0.bin`、`work/live-sample.mp4` 及原生执行器。测试替换联网、用户选择、App 与相册调用，只验证流程和输入，不能证明手机保存成功。
