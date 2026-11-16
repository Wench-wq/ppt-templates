# 云环境设置

将此仓库连接到有访问权限的 GitHub 账号后，在 Codex 云环境的 **Setup script** 中填写：

```bash
bash ./install.sh
```

脚本要求环境中有 Node.js 18+、Python 3 和 `unzip`。它会解压仓库里的 `ppt-skills.zip`，把三个 Skill 安装到 `${CODEX_HOME:-~/.codex}/skills`，并运行 Gravity 和 Pixel 模板的静态校验。无需设置启动脚本。

`gravity-ppt-skill` 与 `pixel-ppt-skill` 的模板、脚本均在压缩包内。浏览器逐页渲染检查需要云环境提供浏览器能力。

`presentations` 是 Codex 内置 Skill 的快照。它使用 `@oai/artifact-tool` 和 Codex 演示文稿运行环境；仓库中的文件无法单独提供这个运行时。若目标账号的云环境没有该能力，HTML 两个 Skill 仍可使用，但 `.pptx` 制作需在具备该运行时的环境执行。

如果目标账号无法在云环境中选择此仓库，请先在该账号的 Codex GitHub 连接中授权访问仓库，或将仓库 fork / 导入到该账号。安装脚本不能授予仓库访问权限。
