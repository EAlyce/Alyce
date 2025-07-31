---
name: "Release Checklist"
about: "Checklist for new releases"
title: "Release vX.Y.Z"
labels: ["release"]
---

## 发布清单

### 代码检查
- [ ] 所有测试通过
- [ ] 代码风格符合规范
- [ ] 文档已更新
- [ ] 版本号已更新

### 发布准备
- [ ] 创建发布分支 `release/vX.Y.Z`
- [ ] 更新 CHANGELOG.md
- [ ] 更新版本号
- [ ] 提交并推送更改

### 发布
- [ ] 创建 Git 标签 `vX.Y.Z`
- [ ] 推送到 GitHub
- [ ] 等待 CI/CD 完成
- [ ] 验证 PyPI 发布
- [ ] 创建 GitHub Release

### 发布后
- [ ] 合并回 main 分支
- [ ] 删除发布分支
- [ ] 发送发布公告
