# 参考驱动 PPT skill
本包适用于支持文件式 skill 的助手。将整个 reference-to-ppt 文件夹放入你所用客户端规定的 skills 目录，或直接让助手读取 SKILL.md。各客户端加载方式不同；本包尚未安装到任何客户端。
## 运行
Python 3.10+，安装 requirements.txt。预览还需要 LibreOffice 的 soffice 命令。WPS 需另行安装并做实际播放验收。
```bash
python -m pip install -r requirements.txt
python scripts/build_presentation.py --input examples/warm-cozy-classroom/deck.json --output demo.pptx --potx demo.potx
python scripts/inspect_presentation.py demo.pptx --output inspection.json
python scripts/render_preview.py demo.pptx --output previews
```
命令从本文件所在目录运行。修改 JSON 内容、palette、fonts 后重跑即可；复杂新风格需由助手扩展绘图与版式。--template template.pptx 保留输入模板母版/主题并重新生成内容页，不会自动匹配任意原始占位符。输入模板为 .potx 时先在编辑器另存 .pptx。
## 示例与边界
示例“让课堂表达更清楚”为演示内容，不是用户实际课程。9 个内容页，流程累计揭示增加 2 个物理页。文本、图形和柱形图可编辑；纸张纹理为原创 PNG。标题使用 Noto Serif CJK SC 作为可用替代，未实现真正中文手写字体。
已写入淡化切换、目录超链接与连续页揭示。未实现复杂对象级移动或 WPS 原生点击触发。高级动画需在目标编辑器补做并验收。目标 WPS 播放尚未验证；预览由 LibreOffice 生成。
## 使用提示
“使用 reference-to-ppt。参考这些图片，内容在附件中，面向初中生，讲 15 分钟。先给设计选择和页纲，我确认后再做代表页。”
“沿用已确认参数，直接完成全稿，输出可编辑 PPT、模板、预览和检查报告。”
本包保留设计与代表页确认流程；已获得直接制作授权时不重复询问。
