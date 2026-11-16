# 云环境设置

将此仓库连接到有访问权限的 GitHub 账号后，在 Codex 云环境的 **Setup script** 中填写：

```bash
bash ./install.sh
```

脚本要求环境中有 Node.js 18+、npm、Python 3.10+ 和 `unzip`。它会解压 `ppt-skills.zip`，把三个 Skill 安装到 `${CODEX_HOME:-~/.codex}/skills`，然后根据 `package-lock.json` 安装 Playwright、Chromium 和 Sharp，根据 `requirements.txt` 在仓库的 `.venv` 中安装 Python 图片与演示文稿校验工具，最后运行浏览器启动与 HTML 模板校验。无需设置启动脚本。

`gravity-ppt-skill` 与 `pixel-ppt-skill` 的模板、脚本均在压缩包内。云环境需要能下载 Chromium；如果浏览器无法启动，还需由云环境提供相应的 Linux 系统库。

`presentations` 是 Codex 内置 Skill 的快照。它使用 `@oai/artifact-tool` 和 Codex 演示文稿运行环境。这个核心包不在公开 npm 仓库中，不能由本仓库预装或替代。脚本会报告是否检测到目标账号提供的运行时。若没有该能力，HTML 两个 Skill 仍可使用，但按此 Skill 制作 `.pptx` 需在具备该运行时的环境执行。

仓库提交的是依赖清单和安装脚本；二进制工具会在目标云环境建立时安装，以匹配其操作系统。

如果目标账号无法在云环境中选择此仓库，请先在该账号的 Codex GitHub 连接中授权访问仓库，或将仓库 fork / 导入到该账号。安装脚本不能授予仓库访问权限。
