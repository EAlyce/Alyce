# 贡献指南

欢迎为 Alyce 项目贡献代码！以下是参与贡献的步骤：

## 开发环境设置

1. Fork 仓库并克隆到本地
2. 创建并激活虚拟环境
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或
   # venv\Scripts\activate  # Windows
   ```
3. 安装开发依赖
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## 代码规范

- 使用 Black 格式化代码
- 使用 isort 排序导入
- 编写类型注解
- 为公共 API 添加文档字符串

## 提交信息

使用约定式提交：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

## 拉取请求流程

1. 从 `main` 分支创建特性分支
2. 提交清晰的提交信息
3. 确保所有测试通过
4. 更新相关文档
5. 发起 Pull Request

## 测试

运行测试：
```bash
pytest
```

## 报告问题

请使用 Issues 报告 bug 或提出建议。
