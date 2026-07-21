# 联网搜索策略（WebSearch + 自动回退）

> 本文件定义 `travel-social-content` Skill 在联网模式下的搜索词模板、调用顺序、失败回退机制。
> 适用领域：通用旅游社媒 / 多平台

---

## 🎯 核心原则

1. **优先尝试联网** — 默认 `web=auto`
2. **失败自动回退** — 任何联网失败立即回退到 LLM 知识 + 速查档案
3. **不打扰用户** — 回退静默执行
4. **缓存复用** — 同一目的地查询结果可缓存 24 小时

---

## 🔍 搜索词模板

### 1. 基础信息

```
{目的地} 简介 {当前年}
{目的地} 门票 开放时间
{目的地} 最佳季节
{目的地} 游玩时长 推荐路线
```

### 2. 交通 / 住宿

```
{城市} 高铁 飞机 交通指南
{城市} 必住酒店 住宿区域
{景点} 怎么去 自驾 公交
```

### 3. 爆款规律

```
{目的地} 小红书 爆款笔记
{目的地} 小红书 攻略
{景点} 小红书 种草
{目的地} 必打卡 网红
```

### 4. 季节 / 天气

```
{城市} {当前月} 天气 穿衣
{城市} 最佳旅游时间
```

### 5. 限制 / 风险

```
{景点} 限流 预约
{景点} 安全提示
{景点} 注意事项 避坑
```

---

## 🛠️ 调用顺序

```python
def search_destination(destination, web_mode="auto"):
    if web_mode == "false":
        return llm_knowledge(destination)
    
    if web_mode == "auto":
        if destination in destinations_cache:
            base = destinations_cache[destination]
        else:
            base = llm_knowledge(destination)
        
        try:
            return websearch_enhance(destination, base)
        except (TimeoutError, NetworkError, PermissionError, EmptyResult):
            return base
    
    if web_mode == "true":
        return websearch_enhance(destination, {})
```

### 推荐 5 步调用

```
Step 1: WebSearch "{目的地} 简介 2026"
Step 2: WebSearch "{目的地} 门票 开放时间"
Step 3: WebSearch "{目的地} 小红书 爆款"
Step 4: WebSearch "{城市} 必吃/必玩"（可选）
Step 5: WebFetch "携程/小红书 URL"（可选）
```

---

## 🚨 失败检测与回退

### 触发回退的 4 种情况

| 情况 | 检测方式 | 回退目标 |
|---|---|---|
| Agent 无 WebSearch | 检查工具注册表 | 离线模式 |
| WebSearch 超时 | timeout > 10s | 离线模式 |
| WebSearch 403 | HTTP 403 | 离线模式 |
| WebSearch 空结果 | result.length == 0 | 离线模式（标注） |

---

## 🎛️ 用户控制接口

```
/travel-social-content 目的地=稻城亚丁 web=auto
/travel-social-content 目的地=稻城亚丁 web=true
/travel-social-content 目的地=稻城亚丁 web=false
```

---

## 📈 缓存策略

- ✅ 缓存：景点基础信息、门票（变化慢）
- ⚠️ 不缓存：热搜话题、实时天气（变化快）
- ❌ 不缓存：用户具体需求（个性化）

---

## ⚡ 性能优化

1. 批量查询：一次 WebSearch 同时问多个问题
2. 并行调用：多个 WebSearch 并行
3. 结果裁剪：取前 200 字符足够
4. 超时控制：单个查询 ≤10s，整体 Step 2 ≤30s

---

*版本：v1.0 | 维护：travel-social-content*
