# 课题组英文主页

Yongwen Zhang (张永文) Research Group 的英文主页使用免费的 GitHub Pages 托管。网站地址为 [zhangyongwen77.github.io](https://zhangyongwen77.github.io/)。

## 查看页面

直接用浏览器打开 `index.html`，或打开 `publications.html` 查看按年份排列的论文目录。网页没有外部字体、脚本或图片依赖，可离线查看。

## 更新内容

主页资料在 `content/site.json`，论文引文在 `content/publications.json`。组名为 Yongwen Zhang (张永文) Research Group，副标题为 Complex Systems Science。News 是导航中的固定栏目，位于 People 和 Publications 之间。

People 先展示负责人张永文的报告现场照和简介。Group Members 依次展示三位教师和在读研究生，Alumni 列出已毕业学生。

- `name`：课题组英文名称；`short_name`：简写。
- `affiliation`：学校、院系。
- `headline`、`introduction`：组名下方的副标题与首页简介。`scholar_url` 用于负责人简介中的 Google Scholar 链接。
- `research`：研究方向列表，每项包含 `title` 和 `description`，可在 `figure` 中填写配图、图注和来源。
- `people`：成员列表，按数组顺序展示。每项包含 `name`（英文姓名）、`name_native`（中文姓名记录）、`role`、`bio` 和 `image`（本地照片路径）。需要展示学校主页链接时填写 `profile_url`。照片不可用时显示姓名首字母。
- `image_crop`：可选照片取景范围。张永文的报告现场照采用方形取景，保留双手、遥控器和麦克风。
- `students` 中的学生按录入顺序显示。`role` 记录培养阶段，`start_year` 记录入学年，`bio` 记录研究方向。`alumni` 中的 `cohorts` 记录各阶段的入学年。
- 首页 Publications 栏按年份倒序直接展示全部论文。每篇论文只需在 `content/publications.json` 中录入一次，字段为 `title`、`authors`（按署名顺序）、`journal`、`year`、`volume`、`locator`（页码或文章号）和 `doi`。仅在线发表时可将卷、页留空。`corresponding_authors` 记录通讯作者姓名，与 `authors` 的拼写一致。`correspondence_source` 保存核验链接或作者确认记录。网页自动为每位通讯作者加上星号。
- `news` 保存组内活动、来访或研究动态，按日期倒序显示。每条填写 `date`（YYYY-MM-DD）、英文标题 `title` 和简述 `text`。可选的 `url` 将标题链接到论文或活动网页。可用 `figure` 添加新闻配图、替代文本、来源和原尺寸图片链接。
- `opportunities`：招生、招聘和合作信息。
- `email` 为联系邮箱，`address` 可按顺序填写多个单位地址。重点实验室的英文名采用[昆明理工大学理学院的署名格式](https://lxy.kust.edu.cn/info/1151/2522.htm)。

更新资料后运行 `python3 scripts/build.py`，重新生成首页与论文目录。也可以把资料交给 Codex 来更新。日常发布的是生成后的 `index.html`、`publications.html` 和 `assets`，不需要让访问者运行 Python。

正式发布使用 `"preview": false`。如需仅在本地审阅草稿，可临时改为 `true` 并生成预览，定稿后恢复 `false` 再生成发布文件。

首页影像采用旅行者 1 号 1990 年 2 月 14 日拍摄的《暗淡蓝点》，图片署名 NASA/JPL-Caltech。网页使用 2020 年再处理版本，等比例缩小并保存到本地。[NASA/JPL 影像说明](https://www.jpl.nasa.gov/images/pia23645-pale-blue-dot-revisited/)

联系区的课题组合影拍摄于 2026 年 5 月 29 日滇池徒步时，图注使用活动日期。

## 将更新发布到 GitHub Pages

1. 修改本地 `content` 中的资料或 `assets` 中的图片。
2. 在项目目录中运行 `python3 scripts/build.py`，随后用浏览器打开 `index.html` 预览。
3. 在 GitHub Desktop 的 **Changes** 中核对资料、图片和生成的网页，填写改动说明，点击 **Commit to main**。
4. 点击 **Push origin**，等待 GitHub Pages 发布后打开 [课题组主页](https://zhangyongwen77.github.io/) 核对更新。

仓库名称为 `zhangyongwen77.github.io`。发布来源设置在 **Settings → Pages** 中，使用 **Deploy from a branch → main → /(root)**。发布记录可在仓库的 **Actions** 中查看。[GitHub Pages 发布文档](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
