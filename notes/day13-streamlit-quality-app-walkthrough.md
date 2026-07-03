# Day 13：Streamlit 数据质量平台页面

## 目标

Day 13 的目标是把命令行数据质量 pipeline 包装成一个可交互页面，让项目从“脚本工具”升级为“AI 数据质量分析平台”的第一版。

当前页面支持：

- 使用内置 BridgeData-style JSONL 样例。
- 上传 JSON / JSONL episode 文件。
- 选择 dataset profile。
- 点击按钮运行质量检查、分布统计、图表生成和 Markdown 报告生成。
- 在页面中查看 quality summary、distribution summary、图表、report 和运行日志。

## 第一步：安装依赖

执行：

```powershell
pip install -r requirements.txt
```

如果已经安装过 Streamlit，可以跳过。

## 第二步：启动页面

执行：

```powershell
streamlit run app.py
```

启动后浏览器会打开本地页面。

## 第三步：运行样例

页面左侧保持默认配置：

```text
Use sample BridgeData-style JSONL: checked
Profile path: configs/bridge_v2_profile.json
```

点击：

```text
Run Quality Pipeline
```

## 第四步：观察结果

页面会展示：

- Episodes
- Steps
- Issue Count
- Language Tasks
- Quality Summary JSON
- Action / State Distribution JSON
- Action / State 分布图
- 自动生成的 Markdown report
- pipeline 运行日志

## 面试表达

> Day 13 我把原来的命令行 pipeline 包装成 Streamlit 页面。这样使用者不需要手动输入长命令，可以直接上传机器人 episode 数据、选择 profile、点击运行，并在页面里查看质量检查结果、分布图和自动报告。这一步让项目从脚本能力升级成了一个可交互的数据质量分析工具。

## 今天完成标准

- 能启动 `streamlit run app.py`。
- 能使用默认样例运行 pipeline。
- 能解释页面里的 4 个指标：Episodes、Steps、Issue Count、Language Tasks。
- 能打开 Plots 和 Report 页面。
- 能说明 Streamlit 页面调用的是已有 pipeline，而不是重写了一套逻辑。
