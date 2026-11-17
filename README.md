# PPT 模板与制作 Skill

本仓库保存用于制作演示文稿的 Codex Skill，以及可编辑 PPT 示例和复用模板。现有三个 Skill：下载并解压 [ppt-skills.zip](ppt-skills.zip) 后，可在 `skills/` 目录找到：

- `presentations`：创建、编辑和读取 PowerPoint / Google Slides 演示文稿。
- `gravity-ppt-skill`：制作北欧简约、紫色主题的 HTML 演示稿。
- `pixel-ppt-skill`：制作复古像素游戏风格的 HTML 演示稿。

每个目录均包含 `SKILL.md` 及其配套资源。`presentations` 是 Codex 内置 Skill 的快照，部分操作依赖 Codex 的演示文稿运行环境。

## 参考驱动的 PPT 制作 Skill

新增 [reference-to-ppt](skills/reference-to-ppt/README.md)：输入参考图或 PPT 模板和课程内容，先选择统一参数，再确认页纲与代表页，输出可编辑 PPT 和完整设计包。默认面向 WPS 课堂演讲，质量标准、素材说明与兼容边界均有记录。

- [Skill 入口](skills/reference-to-ppt/SKILL.md)
- [可编辑示例 PPT](skills/reference-to-ppt/examples/warm-cozy-classroom/editable.pptx)
- [可复用模板 POTX](skills/reference-to-ppt/examples/warm-cozy-classroom/reusable.potx)
- [页面预览](skills/reference-to-ppt/examples/warm-cozy-classroom/previews/contact-sheet.jpg)
- [检查报告](skills/reference-to-ppt/examples/warm-cozy-classroom/quality-report.md)

示例是参考图风格的简化原型。动态包含淡化、目录跳转与连续页揭示；WPS 实机播放未验证，复杂原生对象动画未实现。

### 工作区直接调用

在仓库目录中向助手说明：“使用 `skills/reference-to-ppt/SKILL.md`，根据我的参考和内容制作课堂 PPT。”

```bash
python3 -m pip install -r skills/reference-to-ppt/requirements.txt
python3 skills/reference-to-ppt/scripts/build_presentation.py \
  --input skills/reference-to-ppt/examples/warm-cozy-classroom/deck.json \
  --output output/classroom.pptx --potx output/classroom.potx
```

查看全部命令和依赖说明，请读 [Skill 使用说明](skills/reference-to-ppt/README.md)。现有 `install.sh` 仍负责原三套 Skill；本 Skill 可直接读取使用，或手动复制到客户端配置的 skills 目录。
