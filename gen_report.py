#!/usr/bin/env python3
"""Generate updated embodied AI VLA research report HTML - 2026.07.29 weekly update."""

import html

OUTPUT_FILE = "/Users/a1/Desktop/robot/paper/embodied_ai_report_2026.html"

# ========== CSS (kept from original) ==========
CSS = r'''
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', sans-serif; font-size: 13px; line-height: 1.6; color: #1a1a1a; background: #f7f7f5; }

/* ===== SIDEBAR ===== */
.sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: 200px; background: #fff; border-right: 0.5px solid rgba(0,0,0,0.1); z-index: 200; transition: width 0.25s ease, transform 0.25s ease; display: flex; flex-direction: column; }
.sidebar.collapsed { width: 48px; }
.sidebar-header { padding: 20px 14px 16px; border-bottom: 0.5px solid rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: space-between; }
.sidebar.collapsed .sidebar-header { padding: 20px 10px 16px; }
.sidebar-title { font-size: 13px; font-weight: 600; color: #1a1a1a; white-space: nowrap; overflow: hidden; transition: opacity 0.2s; }
.sidebar.collapsed .sidebar-title { opacity: 0; width: 0; }
.sidebar-toggle { width: 24px; height: 24px; border-radius: 6px; border: 0.5px solid rgba(0,0,0,0.12); background: #fafafa; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 14px; color: #666; flex-shrink: 0; transition: background 0.15s; }
.sidebar-toggle:hover { background: #f0f0f0; }
.sidebar-nav { flex: 1; padding: 12px 0; overflow-y: auto; }
.sidebar-nav a { display: flex; align-items: center; gap: 10px; padding: 10px 14px; color: #555; text-decoration: none; font-size: 13px; transition: all 0.15s; border-left: 2px solid transparent; }
.sidebar-nav a:hover { background: #f5f5f3; color: #1a1a1a; }
.sidebar-nav a.active { color: #1a1a1a; font-weight: 500; border-left-color: #1a1a1a; background: #f5f5f3; }
.sidebar.collapsed .sidebar-nav a { padding: 10px; justify-content: center; }
.sidebar.collapsed .sidebar-nav a span { display: none; }
.nav-icon { font-size: 15px; flex-shrink: 0; width: 20px; text-align: center; }

/* ===== MAIN CONTENT ===== */
.main { margin-left: 200px; transition: margin-left 0.25s ease; min-height: 100vh; }
.main.expanded { margin-left: 48px; }

/* ===== HEADER ===== */
.header { background: #fff; border-bottom: 0.5px solid rgba(0,0,0,0.1); padding: 24px 32px 20px; position: sticky; top: 0; z-index: 100; }
.header h1 { font-size: 18px; font-weight: 600; color: #1a1a1a; }
.header p { font-size: 12px; color: #888; margin-top: 4px; }
.meta-bar { display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap; align-items: center; }
.meta-badge { font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 400; }
.badge-cn { background: #fef3e2; color: #b25a00; border: 0.5px solid #f5c06a; }
.badge-intl { background: #e8f0fe; color: #1a56a0; border: 0.5px solid #93b8f5; }
.badge-lab { background: #e8f8f0; color: #156a3c; border: 0.5px solid #6dc99a; }
.badge-vla { background: #f0eeff; color: #5b35c9; border: 0.5px solid #b9a9f5; }

/* ===== CONTENT AREA ===== */
.content { padding: 24px 32px; max-width: 1200px; margin: 0 auto; }
.section-title { font-size: 16px; font-weight: 600; color: #1a1a1a; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.08); }
.section-block { margin-bottom: 40px; }

/* ===== SUMMARY (text-based) ===== */
.summary-section { background: #fff; border-radius: 12px; border: 0.5px solid rgba(0,0,0,0.08); padding: 24px 28px; margin-bottom: 20px; }
.summary-section h3 { font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 12px; }
.summary-section ul { list-style: none; padding: 0; }
.summary-section li { padding: 10px 0; border-bottom: 0.5px solid rgba(0,0,0,0.05); font-size: 12.5px; color: #444; line-height: 1.7; }
.summary-section li:last-child { border-bottom: none; }
.summary-section li strong { color: #1a1a1a; }
.summary-section li .trend-num { display: inline-block; width: 22px; height: 22px; line-height: 22px; text-align: center; border-radius: 6px; background: #f0eeff; color: #5b35c9; font-size: 11px; font-weight: 600; margin-right: 8px; }
.biz-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.biz-item { padding: 14px 16px; border-radius: 8px; border: 0.5px solid rgba(0,0,0,0.08); background: #fafafa; }
.biz-region { font-size: 13px; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; }
.biz-trend { font-size: 11px; color: #888; margin-bottom: 6px; }
.biz-players { font-size: 11px; color: #444; line-height: 1.5; }

/* ===== HOTSPOTS ===== */
.hotspot-controls { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 12px; }
.search-box { padding: 6px 12px; border-radius: 20px; border: 0.5px solid rgba(0,0,0,0.15); font-size: 12px; width: 200px; outline: none; }
.search-box:focus { border-color: rgba(0,0,0,0.35); }
.hs-filter-group { display: flex; gap: 4px; flex-wrap: wrap; }
.hs-filter { padding: 3px 8px; border-radius: 12px; border: 0.5px solid rgba(0,0,0,0.1); background: transparent; font-size: 10px; cursor: pointer; color: #666; transition: all 0.15s; }
.hs-filter.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
.hotspot-list { display: flex; flex-direction: column; gap: 6px; }
.hotspot-item { background: #fff; border-radius: 8px; border: 0.5px solid rgba(0,0,0,0.08); padding: 12px 16px; display: flex; align-items: flex-start; gap: 10px; transition: border-color 0.15s; }
.hotspot-item:hover { border-color: rgba(0,0,0,0.15); }
.hotspot-date { font-size: 11px; color: #aaa; white-space: nowrap; min-width: 82px; padding-top: 1px; }
.hotspot-tag { font-size: 10px; padding: 2px 7px; border-radius: 10px; white-space: nowrap; }
.ht-tag-pingce { background: #e8f0fe; color: #1a56a0; }
.ht-tag-rongzi { background: #fff0f0; color: #a31f1f; }
.ht-tag-zhibo { background: #fef3e2; color: #b25a00; }
.ht-tag-shujuji { background: #e8f8f0; color: #156a3c; }
.ht-tag-yingjian { background: #f0eeff; color: #5b35c9; }
.ht-tag-jishu { background: #e8f0fe; color: #1a56a0; }
.ht-tag-shengtai { background: #fef3e2; color: #b25a00; }
.ht-tag-jiating { background: #e8f8f0; color: #156a3c; }
.ht-tag-kaiyuan { background: #f0eeff; color: #5b35c9; }
.ht-tag-chanpin { background: #fff0f0; color: #a31f1f; }
.ht-tag-shijiemoxing { background: #e8f8f0; color: #156a3c; }
.ht-tag-xueshu { background: #f0eeff; color: #5b35c9; }
.ht-tag-fangzhen { background: #e8f0fe; color: #1a56a0; }
.ht-tag-fangwen { background: #fff8e1; color: #f57f17; }
.ht-tag-lunwen { background: #e8eaf6; color: #3f51b5; }

.hotspot-body { flex: 1; }
.hotspot-title { font-size: 12.5px; font-weight: 500; color: #1a1a1a; margin-bottom: 2px; }
.hotspot-desc { font-size: 11px; color: #666; line-height: 1.5; }
.hotspot-link { font-size: 10px; color: #1a56a0; text-decoration: none; }
.hotspot-link:hover { text-decoration: underline; }
.load-more-btn { display: block; width: 100%; padding: 10px; margin-top: 10px; border: 0.5px dashed rgba(0,0,0,0.15); border-radius: 8px; background: #fff; font-size: 12px; color: #666; cursor: pointer; transition: all 0.15s; }
.load-more-btn:hover { background: #f5f5f3; color: #1a1a1a; }

/* ===== TEAMS ===== */
.team-category-bar { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 16px; }
.cat-chip { padding: 6px 14px; border-radius: 20px; border: 0.5px solid rgba(0,0,0,0.12); background: transparent; font-size: 12px; cursor: pointer; color: #555; transition: all 0.15s; display: flex; align-items: center; gap: 4px; }
.cat-chip.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
.cat-count { font-size: 11px; }
.team-tag-filters { display: flex; gap: 6px; margin-bottom: 16px; flex-wrap: wrap; }
.team-tag-btn { padding: 5px 12px; border-radius: 16px; border: 0.5px solid rgba(0,0,0,0.12); background: transparent; font-size: 11px; cursor: pointer; color: #555; transition: all 0.15s; }
.team-tag-btn.active { border-color: #1a1a1a; background: #1a1a1a; color: #fff; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }
.card { background: #fff; border-radius: 12px; border: 0.5px solid rgba(0,0,0,0.08); padding: 20px; transition: border-color 0.15s; }
.card:hover { border-color: rgba(0,0,0,0.15); }
.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.avatar { width: 36px; height: 36px; line-height: 36px; text-align: center; border-radius: 10px; font-size: 14px; font-weight: 600; flex-shrink: 0; }
.av-cn { background: #fef3e2; color: #b25a00; }
.av-intl { background: #e8f0fe; color: #1a56a0; }
.av-lab { background: #e8f8f0; color: #156a3c; }
.card-title h3 { font-size: 14px; font-weight: 600; color: #1a1a1a; }
.subtitle { font-size: 11px; color: #888; margin-top: 2px; }
.card-tags { display: flex; gap: 4px; margin-top: 4px; }
.tag { font-size: 10px; padding: 2px 6px; border-radius: 8px; }
.tag-vla { background: #f0eeff; color: #5b35c9; }
.tag-wm { background: #e8f8f0; color: #156a3c; }
.tag-hw { background: #fef3e2; color: #b25a00; }
.tag-sim { background: #e8f0fe; color: #1a56a0; }
.tag-data { background: #fff0f0; color: #a31f1f; }
.tag-rongzi { background: #fff0f0; color: #a31f1f; }
.card-body { }
.work-item { padding: 8px 0; }
.work-title { font-size: 12.5px; font-weight: 500; color: #1a1a1a; display: flex; align-items: center; gap: 6px; }
.work-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.work-dot-vla { background: #5b35c9; }
.work-dot-wm { background: #156a3c; }
.work-dot-hw { background: #b25a00; }
.work-dot-sim { background: #1a56a0; }
.work-dot-data { background: #a31f1f; }
.work-dot-rongzi { background: #a31f1f; }
.work-desc { font-size: 11px; color: #666; line-height: 1.5; margin-top: 3px; }
.work-meta { font-size: 10px; color: #aaa; margin-top: 4px; display: flex; align-items: center; gap: 8px; }
.work-date { color: #999; }
.work-link { color: #1a56a0; text-decoration: none; font-size: 10px; }
.work-link:hover { text-decoration: underline; }
.extra-items { overflow: hidden; transition: max-height 0.3s ease; }
.extra-items.is-collapsed { max-height: 0; }
.extra-items.is-expanded { max-height: 500px; }
.expand-toggle { font-size: 11px; color: #666; cursor: pointer; border: none; background: none; padding: 6px 0; display: block; width: 100%; text-align: center; transition: color 0.15s; }
.expand-toggle:hover { color: #1a1a1a; }
.empty-state { text-align: center; padding: 40px 20px; color: #888; font-size: 14px; }
'''

# ========== HOTSPOT TAG MAPPING ==========
TAG_MAP = {
    '评测': 'ht-tag-pingce',
    '融资': 'ht-tag-rongzi',
    '直播': 'ht-tag-zhibo',
    '数据集': 'ht-tag-shujuji',
    '硬件': 'ht-tag-yingjian',
    '技术': 'ht-tag-jishu',
    '生态': 'ht-tag-shengtai',
    '家庭': 'ht-tag-jiating',
    '开源': 'ht-tag-kaiyuan',
    '产品': 'ht-tag-chanpin',
    '世界模型': 'ht-tag-shijiemoxing',
    '学术': 'ht-tag-xueshu',
    '仿真': 'ht-tag-fangzhen',
    '采访': 'ht-tag-fangwen',
    '论文': 'ht-tag-lunwen',
}

# ========== HOTSPOT DATA (newest first, only items from May 29 2026 onward) ==========
hotspots = [
    # 2026 July (week 4 updates)
    {"date": "2026.07.28", "tag": "技术", "title": "智在无界发布Being-H0.8：全球首个隐式触觉世界动作模型",
     "desc": "首次将触觉模态引入大规模模型预训练，视觉/触觉/动作/未来状态统一至同一隐空间，可完成挤牙膏、摘葡萄、写毛笔字等精细操作",
     "link": "https://new.qq.com/rain/a/20260728A02HQE00", "link_text": "腾讯新闻"},
    {"date": "2026.07.27", "tag": "学术", "title": "斯坦福/英伟达/UT Austin发布RoboTTT：机器人长程记忆突破8000时间步",
     "desc": "上下文长度比现有最优策略提升三个数量级（超4分钟连续历史），推理阶段不增加延迟，arXiv:2607.15275",
     "link": "https://new.qq.com/rain/a/20260727A0A9LA00", "link_text": "腾讯新闻"},
    {"date": "2026.07.27", "tag": "产品", "title": "自变量机器人WALL-B亮相APEC，家庭与养老场景落地",
     "desc": "在秘鲁APEC峰会展示WALL-B世界统一模型在家务整理、老人陪护等场景的长程自主能力，0755养老机器人进入实测",
     "link": "https://www.toutiao.com/article/7665885289646146100", "link_text": "今日头条"},
    {"date": "2026.07.24", "tag": "开源", "title": "灵初智能与北大联合开源EgoSteer双灵巧手通用操作大模型",
     "desc": "基于Qwen3-VL 2B，9600小时人类第一视角视频预训练，陌生语义新任务成功率62%，模型/代码/系统全开源",
     "link": "https://www.psibot.ai?p=2929", "link_text": "灵初智能官网"},
    {"date": "2026.07.23", "tag": "学术", "title": "清华团队提出Harness VLA：用Harness Layer释放冻结VLA能力",
     "desc": "System层框架让冻结VLA专注接触密集操作，Agentic Planner学习原语组织方式，LIBERO-Pro扰动评测成功率82.4%，arXiv:2607.08448",
     "link": "https://harnessvla.github.io/", "link_text": "项目主页"},
    {"date": "2026.07.23", "tag": "产品", "title": "至简动力i7 Pro完成首批百台交付，落成全球首个CNC智能化具身机器人产线",
     "desc": "从成立到百台交付不到一年，已进入国内头部谐波减速器制造企业产线，承担CNC机床上下料等真实作业",
     "link": "https://cinic.org.cn/zgzz/qy/1643389.html", "link_text": "中国网"},
    {"date": "2026.07.21", "tag": "产品", "title": "千寻智能Moz2机器人在WAIC 2026首发，Spirit v1.6演示长程任务",
     "desc": "双足人形机器人Moz2首次公开亮相，Spirit v1.6在真实场景中展示长程任务规划与跨本体泛化能力",
     "link": "https://www.sohu.com/a/1031461279_532789", "link_text": "搜狐科技"},
    {"date": "2026.07.21", "tag": "产品", "title": "灵初智能光模块产线方案落地长飞集团，实现亚毫米级插拔检测",
     "desc": "Psi-R2模型支撑800G/1.6T高速光模块检测与包装全流程自动化，已在头部工厂完成PoC验证",
     "link": "https://new.qq.com/rain/a/20260724A0B57T00", "link_text": "腾讯新闻"},
    {"date": "2026.07.20", "tag": "产品", "title": "西湖机器人西湖o1亮相WAIC，5个月完成三轮数亿元融资",
     "desc": "西湖大学首个AI机器人成果转化项目，全栈自研人形机器人西湖o1及GAE身外化身系统展示实时交互与运动控制",
     "link": "https://www.toutiao.com/article/7664497190856933942", "link_text": "钱江晚报"},
    {"date": "2026.07.20", "tag": "技术", "title": "极佳视界WAIC发布通用世界模型全系列产品线",
     "desc": "涵盖GigaBrain VLA、GigaWorld世界模型、拾光S1数据采集设备等，展示世界模型驱动的具身智能闭环",
     "link": "https://www.sohu.com/a/1045935697_121124731", "link_text": "搜狐科技"},
    {"date": "2026.07.18", "tag": "生态", "title": "WAIC 2026开幕：1100+企业参展，200+具身赛道企业汇聚",
     "desc": "展览面积首破10万平方米，300+全球首发产品，人形机器人、VLA大模型、世界模型成为核心议题",
     "link": "https://www.shanghai.gov.cn/nw9820/20260707/de3c6a83c5094876adb1bdf353120e64.html", "link_text": "上海市政府"},
    {"date": "2026.07.18", "tag": "产品", "title": "智元机器人WAIC发布远征A3 Ultra等新品，第1.5万台 milestone",
     "desc": "精灵G2交付龙旗科技3C产线，从1万台到1.5万台不足3月，刷新全球人形机器人量产纪录",
     "link": "https://finance.sina.com.cn/roll/2026-06-28/doc-inieykzn3656593.shtml", "link_text": "科创板日报"},
    {"date": "2026.07.17", "tag": "产品", "title": "1X NEO发布25-DoF灵巧手并开启Expert Mode消费者交付",
     "desc": "单手可完成叠衣服、拧瓶盖等精细家务，NEO Home Robot持续进入家庭场景",
     "link": "https://www.1x.tech/neo", "link_text": "1X官网"},
    {"date": "2026.07.16", "tag": "学术", "title": "UC Berkeley/NVIDIA/CMU/Bosch提出GaP图策略系统",
     "desc": "Graph-as-Policy将任务建模为图并在仿真中自我改进，再部署到真实机器人，面向变分自动化商业场景，arXiv:2607.05369",
     "link": "https://new.qq.com/rain/a/20260716A03T0F00", "link_text": "腾讯新闻"},
    {"date": "2026.07.15", "tag": "技术", "title": "逐际动力发布COSA 0.5：首个具身智能体操作系统，三层架构定义人形大脑",
     "desc": "System 0全身运动+System 1 VLA/WAM+System 2大语言/世界模型驱动，'堆模型堆不出大脑'，模型是技能不是脑，脑是操作系统",
     "link": "https://www.forbeschina.com/innovation/innovation/71885", "link_text": "福布斯中国"},
    {"date": "2026.07.14", "tag": "融资", "title": "逐际动力完成Pre-IPO轮融资近2亿美元，估值150亿元",
     "desc": "IDG资本、蓝思科技、GGG Group、华山资本等国际化投资机构入局，半年累计融资4亿美元，数千台海外订单",
     "link": "https://www.limxdynamics.com/news/BK000063", "link_text": "逐际动力官网"},
    {"date": "2026.07.14", "tag": "融资", "title": "PI(Physical Intelligence)正寻求10亿美元融资，估值目标超110亿美元",
     "desc": "Founders Fund、Lightspeed、Thrive Capital、Lux Capital、NVIDIA等参与洽谈，pi0.7组合泛化能力获验证",
     "link": "https://newclawtimes.com/articles/physical-intelligence-1-billion-funding-11-billion-valuation-ai-robotics", "link_text": "NewClawTimes"},
    {"date": "2026.07.11", "tag": "仿真", "title": "Genesis World发布v1.2.2：新增触觉传感器与高保真静摩擦模型",
     "desc": "面向灵巧操作训练的触觉噪声选项、非凸碰撞检测与elliptic friction cone，CPU仿真速度最高提升30%",
     "link": "https://www.laumy.tech/notes/posts/%E8%A1%8C%E4%B8%9A%E5%8A%A8%E6%80%81/%E7%AB%AF%E4%BE%A7-ai-%E4%B8%8E%E6%9C%BA%E5%99%A8%E4%BA%BA%E6%8A%80%E6%9C%AF%E9%9B%B7%E8%BE%BE2026-07-15", "link_text": "技术雷达"},
    {"date": "2026.07.10", "tag": "产品", "title": "特斯拉Optimus第三代方案评审通过，供应链采购指引已下发",
     "desc": "马斯克敲定Gen-3整机方案，要求9月周产1000台、年底周产2000-2500台(年化约10万台)，Fremont产线7月末启动试产",
     "link": "https://new.qq.com/rain/a/20260710A07RWK00", "link_text": "腾讯新闻"},
    {"date": "2026.07.09", "tag": "产品", "title": "影石Insta360组建机器人团队，进军消费级机器人领域",
     "desc": "代号Cameraman摄影机器人，核心团队近百人来自大疆/科沃斯/地平线，计划2027年下半年发布，面向家庭自主摄影",
     "link": "https://www.163.com/dy/article/L1G6BGRG05199NPP.html", "link_text": "21世纪经济报道"},
    {"date": "2026.07.09", "tag": "融资", "title": "墨奇智能(Morphi)完成超10亿元天使轮系列融资，估值70亿",
     "desc": "阿里、腾讯联合领投，创始团队来自华为车BU智驾AI部门，'智驾是具身的子集'，成立仅半年",
     "link": "https://new.qq.com/rain/a/20260709A063G200", "link_text": "腾讯新闻"},
    {"date": "2026.07.08", "tag": "生态", "title": "工信部：2026年中国人形机器人全年整机产量有望突破10万台",
     "desc": "WAIC 2026新闻发布会上工信部科技司副司长甘小斌表态，宇树已累计生产约11000台，智元完成第15000台",
     "link": "https://auto.ifeng.com/c/8uhgBke7bDp", "link_text": "凤凰网"},
    {"date": "2026.07.06", "tag": "融资", "title": "星动纪元完成10亿元新一轮融资，诚通基金领投",
     "desc": "2026年累计融资近50亿，清华系具身智能公司硬件自研率超95%，二季度启动千台级交付",
     "link": "https://www.163.com/dy/article/L15N8ODO05198NMR.html", "link_text": "网易科技"},
    {"date": "2026.07.05", "tag": "产品", "title": "Figure 03正式部署BMW Spartanburg工厂物流排序，续航翻倍效率提升5倍",
     "desc": "从Figure 02试点到Figure 03全面部署，2.3kWh电池续航3-4h，Helix 02三层架构，424件/小时分拣效率，3台机器人200h连续验证",
     "link": "https://k.sina.com.cn/article_5953189932_162d6782c06704kswe.html", "link_text": "新浪科技"},
    {"date": "2026.07.04", "tag": "融资", "title": "极佳视界完成B2轮10亿元融资，3个月累计融资35亿",
     "desc": "狮城资本、中比基金、建投投资等国家队与产业资本加持，国内首个世界模型独角兽",
     "link": "https://www.sohu.com/a/1045935697_121124731", "link_text": "搜狐科技"},
    {"date": "2026.07.03", "tag": "开源", "title": "Genesis AI正式开源Genesis World 1.0全栈仿真训练平台",
     "desc": "包含三大自主研发核心模块，可将复杂技能训练周期压缩80%、落地测试成本降低65%",
     "link": "https://cxgn.cn/17467.html", "link_text": "创新观察"},
    {"date": "2026.07.02", "tag": "融资", "title": "宇树科技科创板IPO注册获批，104天闪电过会",
     "desc": "3月20日受理、6月1日过会、7月2日注册获批，A股将迎来'具身智能第一股'，拟募资42.02亿",
     "link": "https://baijiahao.baidu.com/s?id=1869968747747361884", "link_text": "百度百家"},
    {"date": "2026.07.02", "tag": "技术", "title": "智源发布RoboBrain Orca世界模型：12.5万小时无标注视频训练",
     "desc": "让AI通过'看视频'自主学习物体运动规律和场景演变逻辑，SoulAgent个人智能体同步亮相",
     "link": "http://www.zqrb.cn/gscy/qiyexinxi/2026-07-02/A1782955137529.html", "link_text": "证券日报"},
    {"date": "2026.07.01", "tag": "学术", "title": "Google DeepMind发布Gemini Robotics On-Device与Apptronik Robot Park",
     "desc": "端侧机器人VLA能力再进一步，同时宣布在德州建设机器人公园以加速真实世界数据收集",
     "link": "https://deepmind.google/models/gemini-robotics/", "link_text": "DeepMind官网"},
    # 2026 June
    {"date": "2026.06.29", "tag": "融资", "title": "自变量机器人连续完成4轮融资，估值突破200亿",
     "desc": "2个多月完成B轮/B+/B++/C轮四轮融资并全部交割，投资方超30家，估值从百亿跃升至200亿",
     "link": "https://fund.eastmoney.com/a/202607073796678662.html", "link_text": "东方财富"},
    {"date": "2026.06.29", "tag": "融资", "title": "智平方完成近50亿元系列融资，估值超200亿",
     "desc": "深圳具身智能独角兽一年累计13轮融资，AlphaBrain+AlphaBot产品线推进量产交付",
     "link": "https://baijiahao.baidu.com/s?id=1869430282289626017", "link_text": "百度百家"},
    {"date": "2026.06.15", "tag": "技术", "title": "智平方发布全球首个类脑VLA架构NeuroVLA",
     "desc": "仿生'皮层-小脑-脊髓'三层分工协同，运动抖动降低75%，碰撞后20ms反射响应，AlphaBrain Platform同步开源",
     "link": "https://www.jiemian.com/article/14586417.html", "link_text": "界面新闻"},
    {"date": "2026.06.15", "tag": "技术", "title": "NVIDIA官方定义WAM范式：世界-动作模型与VLM-VLA并列两条主流路线",
     "desc": "NVIDIA技术博客将WAM定义为基于预训练视频/世界模型骨干网络的机器人基础模型新配方",
     "link": "https://developer.nvidia.cn/blog/r2d2-training-generalist-robots-with-nvidia-research-workflows-and-world-foundation-models", "link_text": "NVIDIA Developer"},
    {"date": "2026.06.11", "tag": "产品", "title": "1X NEO首批消费者交付：全球首款家用人形机器人进入家庭",
     "desc": "NEO Home Robot定价$5.5万，Redwood AI驱动，折叠衣物、整理房间等家务任务，持续学习进化",
     "link": "https://www.1x.tech/neo", "link_text": "1X官网"},
    {"date": "2026.06.03", "tag": "评测", "title": "千寻Spirit v1.6登顶RoboArena全球第一，力压英伟达Cosmos3和PI Pi0.5",
     "desc": "首个登顶具身智能权威评测的中国模型，真实世界数据训练击败仿真环境训练的硅谷巨头",
     "link": "https://www.sohu.com/a/1031461279_532789", "link_text": "搜狐科技"},
    {"date": "2026.06.01", "tag": "开源", "title": "NVIDIA发布GR00T N1.7开源VLA模型+人形机器人参考平台",
     "desc": "Apache 2.0开源，Cosmos-Reason2-2B backbone，DROID-F6基准提升61%，宇树H2 Plus参考设计同步发布",
     "link": "https://blogs.nvidia.cn/blog/nvidia-open-humanoid-robot-reference-design/", "link_text": "NVIDIA官方"},
]

# ========== TEAM DATA ==========
# Format: {"name", "avatar", "avatar_class", "type", "tags", "subtitle", "works": [{dot, title, desc, date, link}]}
# works: first item visible, rest in expandable section
# Only keep works from Jan 29 2026 onward (6 month cutoff)

teams = [
    # === 国内企业 ===
    {"name": "银河通用 (Galbot)", "avatar": "银", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla wm hw", "subtitle": "LDA-1B · Galbot S1量产 · 25亿元B轮",
     "works": [
         {"dot": "vla", "title": "LDA-1B开源，跨本体WAM登顶RSS 2026",
          "desc": "1.6B参数WAM（World-Action Model）框架，首次在隐空间统一世界模型与VLA，虚实共融数据利用与跨本体泛化。1小时跨本体自适应，性能提升48%。",
          "date": "2026.05.10", "link": "https://www.galbot.com", "link_text": "银河通用官网"},
         {"dot": "hw", "title": "Galbot S1投产量产，已进入宁德时代产线",
          "desc": "零遥操、全自主重载人形机器人，双臂最大负载50kg，在宁德时代电池生产线完成实际作业。",
          "date": "2026.03.01", "link": "https://www.galbot.com", "link_text": "银河通用官网"},
         {"dot": "rongzi", "title": "完成25亿元B轮融资，估值突破200亿",
          "desc": "宁德时代、比亚迪、小米产投等产业资本入局，创国内具身智能单轮最高纪录。",
          "date": "2026.02.28", "link": "https://www.36kr.com", "link_text": "36氪"},
     ]},

    {"name": "自变量机器人 (XVAR)", "avatar": "自", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla", "subtitle": "通用VLA大模型 · 4轮融资估值200亿 · WALL-B世界统一模型",
     "works": [
         {"dot": "vla", "title": "WALL-B亮相APEC，家庭与养老场景落地",
          "desc": "在秘鲁APEC峰会展示WALL-B世界统一模型在家务整理、老人陪护等场景的长程自主能力，0755养老机器人进入实测。",
          "date": "2026.07.27", "link": "https://www.toutiao.com/article/7665885289646146100", "link_text": "今日头条"},
         {"dot": "rongzi", "title": "连续完成B轮/B+/B++/C轮四轮融资，估值突破200亿",
          "desc": "2个多月密集融资并全部交割，投资方超30家(含字节、美团、阿里云、小米)，估值从百亿跃升至200亿。",
          "date": "2026.06.29", "link": "https://fund.eastmoney.com/a/202607073796678662.html", "link_text": "东方财富"},
         {"dot": "vla", "title": "发布WALL-B世界统一模型+WALL-OSS完全开源",
          "desc": "WALL-B于2026年4月发布为'世界统一模型'，WALL-OSS Apache 2.0开源，RoboChallenge评测全球开源模型第二。",
          "date": "2026.04.27", "link": "https://www.sina.com.cn", "link_text": "新浪财经"},
     ]},

    {"name": "千寻智能 (SpiritAI)", "avatar": "千", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "Spirit v1.6全球第一 · Moz2 WAIC首发 · 估值200亿+",
     "works": [
         {"dot": "hw", "title": "Moz2双足人形机器人在WAIC 2026首发",
          "desc": "Spirit v1.6长程任务能力在真实场景中演示，全身移动操作与跨本体泛化能力展示。",
          "date": "2026.07.21", "link": "https://www.sohu.com/a/1031461279_532789", "link_text": "搜狐科技"},
         {"dot": "vla", "title": "Spirit v1.6登顶RoboArena全球第一，力压英伟达Cosmos3和PI Pi0.5",
          "desc": "首个登顶具身智能权威评测的中国模型，真实世界数据训练击败仿真训练的硅谷巨头，综合得分92.7。",
          "date": "2026.06.03", "link": "https://www.sohu.com/a/1031461279_532789", "link_text": "搜狐科技"},
         {"dot": "rongzi", "title": "完成15亿元A+轮融资，3个月累计融资近50亿",
          "desc": "云锋基金、顺为资本、红杉中国、沙特阿美P7等一线基金入局，估值从百亿跃升至200亿以上。",
          "date": "2026.06.03", "link": "https://fund.eastmoney.com/a/202606033758465889.html", "link_text": "东方财富"},
     ]},

    {"name": "智元机器人 (AgiBot)", "avatar": "智", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "1.5万台量产 · 远征A3 Ultra · WAIC新品",
     "works": [
         {"dot": "hw", "title": "WAIC 2026发布远征A3 Ultra等新品，第1.5万台机器人下线",
          "desc": "精灵G2交付龙旗科技3C产线，不足3月从1万台到1.5万台，刷新全球人形机器人量产纪录。",
          "date": "2026.07.18", "link": "https://finance.sina.com.cn/roll/2026-06-28/doc-inieykzn3656593.shtml", "link_text": "科创板日报"},
         {"dot": "hw", "title": "灵犀X2跨过万台量产门槛",
          "desc": "2026年3月突破万台，全智能灵动机器人面向工业和服务场景。",
          "date": "2026.03.01", "link": "https://www.agibot.com", "link_text": "智元官网"},
     ]},

    {"name": "星海图 (Galaxea)", "avatar": "星", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla wm hw data", "subtitle": "G0.5开源 · Kengo人形 · EFM-1双系统 · 估值200亿",
     "works": [
         {"dot": "vla", "title": "G0.5 VLA基础模型开源发布，零样本泛化突破",
          "desc": "实现从任务后训练到零样本泛化的跨越，新物体直接操作、新场景自主适应、新指令组合理解执行。",
          "date": "2026.06.16", "link": "https://so.html5.qq.com/page/real/search_news?docid=70000021_8656a30ee3894052", "link_text": "查看详情"},
         {"dot": "hw", "title": "自研双足人形机器人Kengo（行客）首秀",
          "desc": "星海图全球开发者大会上完成首秀，配合G0.5和Fast-WAM实现全身控制。",
          "date": "2026.06.16", "link": "https://so.html5.qq.com/page/real/search_news?docid=70000021_8656a30ee3894052", "link_text": "查看详情"},
         {"dot": "wm", "title": "Fast-WAM世界模型与EFM-1双系统架构公布",
          "desc": "EFM-1(慢思考VLM+快执行VLA)'一脑多形'，Fast-WAM驱动机器人前瞻性规划，RSR空间智能引擎构建Real2Sim2Real数据飞轮。",
          "date": "2026.06.16", "link": "https://so.html5.qq.com/page/real/search_news?docid=70000021_8656a30ee3894052", "link_text": "查看详情"},
         {"dot": "rongzi", "title": "完成B+轮20亿元融资，估值突破200亿",
          "desc": "蚂蚁集团、美团、高瓴创投、IDG资本、蓝思科技等入局，累计融资近30-50亿。",
          "date": "2026.04.02", "link": "https://news.qq.com/rain/a/20260409A02XKY00", "link_text": "查看详情"},
     ]},

    {"name": "星动纪元 (RobotEra)", "avatar": "动", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "端到端VLA · 2026年融资近50亿 · 千台级交付 · 估值200亿",
     "works": [
         {"dot": "rongzi", "title": "完成10亿元新一轮融资，诚通基金领投",
          "desc": "2026年累计融资近50亿，清华系具身智能公司硬件自研率超95%，二季度启动千台级交付。",
          "date": "2026.07.06", "link": "https://www.163.com/dy/article/L15N8ODO05198NMR.html", "link_text": "网易科技"},
         {"dot": "vla", "title": "端到端VLA模型迭代：机器人效率达人类90%",
          "desc": "软硬件协同优化+数据飞轮运转，物流分拣等场景效率从70%提升至90%。",
          "date": "2026.02.13", "link": "https://news.qq.com/rain/a/20260213A0321J00", "link_text": "腾讯新闻"},
     ]},

    {"name": "智平方", "avatar": "平", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "NeuroVLA类脑 · AlphaBrain · '最像特斯拉' · 估值200亿",
     "works": [
         {"dot": "vla", "title": "发布全球首个类脑VLA架构NeuroVLA",
          "desc": "仿生'皮层-小脑-脊髓'三层分工协同，运动抖动降低75%，碰撞后20ms反射响应，AlphaBrain Platform同步开源。",
          "date": "2026.06.15", "link": "https://www.jiemian.com/article/14586417.html", "link_text": "界面新闻"},
         {"dot": "rongzi", "title": "完成近50亿元系列融资，估值超200亿",
          "desc": "深圳具身智能独角兽一年累计13轮融资，GOVLA全域VLA大模型+AlphaBot机器人推进量产交付，多家特斯拉生态链企业战略重仓。",
          "date": "2026.06.29", "link": "https://baijiahao.baidu.com/s?id=1869430282289626017", "link_text": "百度百家"},
         {"dot": "vla", "title": "AlphaBrain VLA大模型四代演进路线发布",
          "desc": "从端到端VLA到增强型VLA再到类脑VLA三阶段演进论，世界模型是VLA体系中的核心组件而非竞争路线。",
          "date": "2026.06.08", "link": "https://www.sohu.com/a/1033666912_114822", "link_text": "搜狐科技"},
     ]},

    {"name": "极佳视界", "avatar": "佳", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla wm", "subtitle": "GigaBrain VLA · 世界模型独角兽 · WAIC全系列 · 3个月融资35亿",
     "works": [
         {"dot": "wm", "title": "WAIC 2026发布通用世界模型全系列产品线",
          "desc": "涵盖GigaBrain VLA、GigaWorld世界模型、拾光S1数据采集设备等，展示世界模型驱动的具身智能闭环。",
          "date": "2026.07.20", "link": "https://www.sohu.com/a/1045935697_121124731", "link_text": "搜狐科技"},
         {"dot": "rongzi", "title": "完成B2轮10亿元融资，3个月累计融资35亿",
          "desc": "狮城资本、中比基金、建投投资等国家队与产业资本加持，国内首个世界模型独角兽。",
          "date": "2026.07.04", "link": "https://www.sohu.com/a/1045935697_121124731", "link_text": "搜狐科技"},
         {"dot": "wm", "title": "GigaBrain-0.5M*自我进化VLA大模型拿下世界第一",
          "desc": "世界模型预测未来状态驱动机器人决策，叠衣、冲咖啡等真实任务接近100%成功率。",
          "date": "2026.02.14", "link": "https://hub.baai.ac.cn/view/52604", "link_text": "智源Hub"},
     ]},

    {"name": "宇树科技 (Unitree)", "avatar": "宇", "avatar_class": "av-cn", "type": "cn",
     "tags": "hw vla", "subtitle": "科创板IPO获批 · G1/H1人形 · 累计11000台 · 具身智能第一股",
     "works": [
         {"dot": "rongzi", "title": "科创板IPO注册获批，104天闪电过会",
          "desc": "3月20日受理、6月1日过会、7月2日注册获批，A股将迎来'具身智能第一股'，拟募资42.02亿。截至6月初累计生产约11000台双足人形机器人。",
          "date": "2026.07.02", "link": "https://baijiahao.baidu.com/s?id=1869968747747361884", "link_text": "百度百家"},
         {"dot": "hw", "title": "G1人形机器人持续迭代，CES 2026海外首秀",
          "desc": "全尺寸通用人形机器人，在CES 2026上完整展示产品线，运动控制与操作能力全面升级。",
          "date": "2026.01.10", "link": "https://www.unitree.com", "link_text": "宇树官网"},
     ]},

    {"name": "逐际动力 (LimX Dynamics)", "avatar": "逐", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla wm hw sim", "subtitle": "COSA 0.5 · FluxVLA Engine · Luna · Pre-IPO估值150亿",
     "works": [
         {"dot": "vla", "title": "发布COSA 0.5具身智能体操作系统：三层架构定义人形大脑",
          "desc": "System 0全身运动+System 1 VLA/WAM+System 2大语言/世界模型驱动，'堆模型堆不出大脑'，模型是技能不是脑，脑是操作系统。全球最早提出的人形大脑系统架构。",
          "date": "2026.07.15", "link": "https://www.forbeschina.com/innovation/innovation/71885", "link_text": "福布斯中国"},
         {"dot": "rongzi", "title": "完成Pre-IPO轮融资近2亿美元，估值150亿元，半年累计融资4亿美元",
          "desc": "IDG资本、蓝思科技、GGG Group、华山资本等国际化投资机构入局，数千台海外订单，超半来自海外。",
          "date": "2026.07.14", "link": "https://www.limxdynamics.com/news/BK000063", "link_text": "逐际动力官网"},
         {"dot": "hw", "title": "发布全尺寸交互人形机器人LimX Luna，不到一个月已向海内外交付",
          "desc": "定义新一代交互型全尺寸人形机器人，为消费者重塑沉浸式交互体验。",
          "date": "2026.05.25", "link": "https://www.limxdynamics.com", "link_text": "逐际动力官网"},
         {"dot": "vla", "title": "开源FluxVLA Engine：面向具身智能的标准化VLA工程底座",
          "desc": "企业级开源平台，向全球开发者提供模型训练、迭代、部署的工程基础设施，推动从'训练好一个模型'到'让所有人都能够训练模型'。",
          "date": "2026.04.30", "link": "https://www.limxdynamics.com", "link_text": "逐际动力官网"},
     ]},

    {"name": "智在无界 (BeingBeyond)", "avatar": "界", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla wm", "subtitle": "Being-H/M系列 · 隐式世界动作模型 · 100+城商业落地",
     "works": [
         {"dot": "wm", "title": "发布Being-H0.8：全球首个隐式触觉世界动作模型",
          "desc": "首次将触觉模态引入大规模模型预训练，视觉/触觉/动作/未来状态统一至隐空间，可完成挤牙膏、摘葡萄、写毛笔字等精细操作。",
          "date": "2026.07.28", "link": "https://new.qq.com/rain/a/20260728A02HQE00", "link_text": "腾讯新闻"},
         {"dot": "wm", "title": "发布Being-M0.7：隐式世界动作模型打通全身移动灵巧操作",
          "desc": "全球首个将隐式世界动作模型能力从桌面灵巧操作扩展到全身移动操作，展示鱼缸捞鱼、镜像取物、移动放置抓取等能力。",
          "date": "2026.06.15", "link": "https://so.html5.qq.com/page/real/search_news?docid=70000021_4056a56ff7b38852", "link_text": "查看详情"},
         {"dot": "vla", "title": "WAIC联合速腾聚创等生态伙伴展示模型+本体深度融合",
          "desc": "桌面级灵巧手机械臂D1、无本体数采设备U1及Adam-U一体化数据采集与训练平台亮相。",
          "date": "2026.07.21", "link": "https://auto.cctv.com/2026/07/21/ARTInKLDQAOFzfWob4sfIOEC260721.shtml", "link_text": "央视网"},
     ]},

    {"name": "灵初智能", "avatar": "灵", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla data", "subtitle": "EgoSteer开源 · Psi-R2/Psi-W0 · 光模块产线落地",
     "works": [
         {"dot": "vla", "title": "与北大联合开源EgoSteer双灵巧手通用操作大模型",
          "desc": "基于Qwen3-VL 2B，9600小时人类第一视角视频预训练，陌生语义新任务成功率62%，模型/代码/系统全开源。",
          "date": "2026.07.24", "link": "https://www.psibot.ai?p=2929", "link_text": "灵初智能官网"},
         {"dot": "vla", "title": "光模块产线方案落地长飞集团，实现亚毫米级插拔检测",
          "desc": "Psi-R2模型支撑800G/1.6T高速光模块检测与包装全流程自动化，已在头部工厂完成PoC验证。",
          "date": "2026.07.21", "link": "https://new.qq.com/rain/a/20260724A0B57T00", "link_text": "腾讯新闻"},
         {"dot": "vla", "title": "发布Psi-R2/Psi-W0双模型架构，登顶MolmoSpaces全球榜单",
          "desc": "Psi-R2为全球首个基于10万小时人类多模态操作数据预训练的灵巧操作模型，Psi-W0世界模型负责物理规律判断与数据转换。",
          "date": "2026.04.15", "link": "https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260721145739a6de4ad4", "link_text": "腾讯自选股"},
     ]},

    {"name": "至简动力", "avatar": "至", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "i7 Pro百台交付 · LaST基座模型 · CNC智能化产线",
     "works": [
         {"dot": "hw", "title": "i7 Pro完成首批百台交付，落成全球首个CNC智能化具身机器人产线",
          "desc": "从成立到百台交付不到一年，已进入国内头部谐波减速器制造企业产线，承担CNC机床上下料等真实作业。",
          "date": "2026.07.06", "link": "https://cinic.org.cn/zgzz/qy/1643389.html", "link_text": "中国网"},
         {"dot": "vla", "title": "LaST-R1在LIBERO基准达到99.9%成功率",
          "desc": "融合世界模型与VLA的LaST0基座模型，隐空间时空思维链研究入选ICML 2026 Spotlight。",
          "date": "2026.06.20", "link": "https://robotscope.net/pulse/2026-07-10/simplexity-delivery/", "link_text": "RobotScope"},
     ]},

    {"name": "开普勒机器人", "avatar": "开", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "VTLA力触觉融合 · K2量产",
     "works": [
         {"dot": "hw", "title": "K2人形机器人开启量产交付",
          "desc": "全尺寸通用人形机器人，针对工业装配场景优化，已在多家汽车主机厂完成试点验证。",
          "date": "2026.03.01", "link": "https://www.gotokepler.com", "link_text": "开普勒官网"},
     ]},

    {"name": "腾讯 Robotics X", "avatar": "腾", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "HY-Embodied · 五轮小五",
     "works": [
         {"dot": "vla", "title": "HY-Embodied-0.5开源发布",
          "desc": "基于混元大模型构建的具身VLA模型，支持多模态指令理解与机器人动作生成，模型权重与推理代码已开源。",
          "date": "2026.02.01", "link": "https://tairos.tencent.com", "link_text": "腾讯AI Lab"},
     ]},

    {"name": "小米 (Mimo Labs)", "avatar": "米", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "MiMo-Embodied · CyberOne",
     "works": [
         {"dot": "vla", "title": "MiMo-Embodied VLA模型开源",
          "desc": "跨自动驾驶与具身智能的统一基础模型，实现多模态感知与动作生成的端到端融合。",
          "date": "2026.01.10", "link": "https://github.com/MiMo-AI", "link_text": "小米GitHub"},
     ]},

    {"name": "小鹏汽车 (IRON)", "avatar": "鹏", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "IRON人形机器人 · 工厂试点",
     "works": [
         {"dot": "hw", "title": "IRON人形机器人第二代发布",
          "desc": "专为汽车工厂场景设计，融合小鹏自动驾驶感知算法与机器人操作能力，已在广州黄埔工厂试点。",
          "date": "2026.03.01", "link": "https://www.xiaopeng.com", "link_text": "小鹏汽车官网"},
     ]},

    {"name": "无界动力", "avatar": "无", "avatar_class": "av-cn", "type": "cn",
     "tags": "vla hw", "subtitle": "3亿首轮融资 · 通用具身机器人",
     "works": [
         {"dot": "rongzi", "title": "完成3亿元首轮融资，红杉中国、高瓴创投领投",
          "desc": "通用具身智能机器人公司，地平线、华业天成等跟投。",
          "date": "2026.02.10", "link": "https://www.bjnews.com.cn/detail/1762825032169141.html", "link_text": "新京报"},
     ]},

    # === 国外企业 ===
    {"name": "Figure AI", "avatar": "F", "avatar_class": "av-intl", "type": "intl",
     "tags": "vla hw", "subtitle": "Figure 03 · BMW工厂 · Helix 02 · 5倍效率提升",
     "works": [
         {"dot": "hw", "title": "Figure 03正式部署BMW Spartanburg工厂物流排序",
          "desc": "续航翻倍(3-4h)、Helix 02三层架构(System0/1/2)、424件/小时分拣效率(5倍提升)、3台机器人200h连续验证、零件放置准确率99%+。",
          "date": "2026.07.05", "link": "https://k.sina.com.cn/article_5953189932_162d6782c06704kswe.html", "link_text": "新浪科技"},
         {"dot": "hw", "title": "Figure 03三台机器人物流分拣100小时直播",
          "desc": "Bob、Frank、Gary连续作业100小时+，累计处理超13万个包裹，零人工干预。",
          "date": "2026.05.14", "link": "https://www.figure.ai", "link_text": "Figure AI官网"},
         {"dot": "vla", "title": "Helix 02统一神经系统：System0/1/2三层端到端架构",
          "desc": "新增System0高频关节力矩控制层，单轮4分钟61个连贯动作全程无人工干预。",
          "date": "2026.05.01", "link": "https://www.figure.ai", "link_text": "Figure AI官网"},
     ]},

    {"name": "Physical Intelligence", "avatar": "pi", "avatar_class": "av-intl", "type": "intl",
     "tags": "vla wm", "subtitle": "pi0.7 · 涌现能力 · RL Token · MEM · 寻求$11B估值融资",
     "works": [
         {"dot": "rongzi", "title": "正寻求10亿美元融资，估值目标超110亿美元",
          "desc": "Founders Fund、Lightspeed、Thrive Capital、Lux Capital、NVIDIA等参与洽谈，4个月内估值从$5.6B翻倍至$11B，pi0.7组合泛化能力获验证。",
          "date": "2026.07.14", "link": "https://newclawtimes.com/articles/physical-intelligence-1-billion-funding-11-billion-valuation-ai-robotics", "link_text": "NewClawTimes"},
         {"dot": "vla", "title": "pi0.7发布：具有涌现能力的可引导模型",
          "desc": "首次展现组合泛化能力，能将不同任务中学到的技能重新组合解决新问题。在多项评测中超越pi0.5和RT-2。",
          "date": "2026.04.17", "link": "https://www.pi.website/blog/pi07", "link_text": "pi website"},
         {"dot": "vla", "title": "RL Token (RLT)：在线强化学习的精准操作",
          "desc": "专门改进细粒度操作的精密任务，仅需几分钟到几小时真实世界经验即可完成学习。",
          "date": "2026.03.19", "link": "https://www.pi.website/research/rlt", "link_text": "PI Research"},
         {"dot": "wm", "title": "MEM：VLAs with Long and Short-Term Memory",
          "desc": "结合密集短期视觉token与压缩长期语言摘要，使VLA模型能够解决需要长达15分钟记忆跨度的任务。",
          "date": "2026.03.03", "link": "https://www.pi.website/research/memory", "link_text": "pi website"},
     ]},

    {"name": "Nvidia (Isaac Lab)", "avatar": "N", "avatar_class": "av-intl", "type": "intl",
     "tags": "sim vla wm", "subtitle": "Cosmos 3 · GR00T N1.7 · WAM范式 · Isaac Lab-Arena",
     "works": [
         {"dot": "vla", "title": "GR00T N1.7开源VLA模型+人形机器人参考平台(Apache 2.0)",
          "desc": "Cosmos-Reason2-2B backbone，DROID-F6基准提升61%，宇树H2 Plus参考设计，1X/Skild AI/Stanford等已采用。",
          "date": "2026.06.01", "link": "https://blogs.nvidia.cn/blog/nvidia-open-humanoid-robot-reference-design/", "link_text": "NVIDIA官方"},
         {"dot": "wm", "title": "Cosmos 3发布：全球首个开源物理AI基础模型",
          "desc": "GTC台北发布，Mixture-of-Transformers架构，打通视觉、语言、动作、物理模拟全模态。",
          "date": "2026.05.31", "link": "https://nvidianews.nvidia.com/news/nvidia-expands-open-model-families-to-power-the-next-wave-of-agentic-physical-and-healthcare-ai", "link_text": "NVIDIA News"},
         {"dot": "wm", "title": "官方定义WAM范式：世界-动作模型与VLM-VLA并列两条主流路线",
          "desc": "NVIDIA技术博客将WAM定义为基于预训练视频/世界模型骨干网络的机器人基础模型新配方，与VLM-based VLA并列为两条主流路线。",
          "date": "2026.06.15", "link": "https://developer.nvidia.cn/blog/r2d2-training-generalist-robots-with-nvidia-research-workflows-and-world-foundation-models", "link_text": "NVIDIA Developer"},
     ]},

    {"name": "Tesla (Optimus)", "avatar": "T", "avatar_class": "av-intl", "type": "intl",
     "tags": "hw vla", "subtitle": "Optimus Gen-3评审通过 · 供应链采购指引 · 年化10万台目标",
     "works": [
         {"dot": "hw", "title": "Optimus Gen-3方案评审通过，供应链采购指引已下发",
          "desc": "马斯克敲定第三代整机方案，要求9月周产1000台、年底周产2000-2500台(年化约10万台)。Fremont产线7月末启动试产，Giga Texas专属工厂在建。",
          "date": "2026.07.10", "link": "https://new.qq.com/rain/a/20260710A07RWK00", "link_text": "腾讯新闻"},
         {"dot": "hw", "title": "1000+台Optimus Gen-3在Fremont工厂内部运行",
          "desc": "内部测试与AI训练，Fremont产线改造进行中，Model S/X产线已转产机器人。",
          "date": "2026.04.01", "link": "https://www.teslarati.com/tesla-optimus-project-fires-up-musk-sees-production-line-progress/", "link_text": "Teslarati"},
     ]},

    {"name": "1X Technologies", "avatar": "1", "avatar_class": "av-intl", "type": "intl",
     "tags": "vla hw", "subtitle": "NEO Home Robot · 25-DoF灵巧手 · Redwood AI · 首批交付",
     "works": [
         {"dot": "hw", "title": "NEO发布25-DoF灵巧手并开启Expert Mode消费者交付",
          "desc": "单手可完成叠衣服、拧瓶盖等精细家务，NEO Home Robot持续进入家庭场景，定价$5.5万。",
          "date": "2026.07.17", "link": "https://www.1x.tech/neo", "link_text": "1X官网"},
         {"dot": "hw", "title": "NEO首批消费者交付：全球首款家用人形机器人进入家庭",
          "desc": "NEO Home Robot定价$5.5万，Redwood AI驱动，折叠衣物、整理房间等家务任务，持续学习进化。",
          "date": "2026.06.11", "link": "https://www.1x.tech/neo", "link_text": "1X官网"},
     ]},

    {"name": "Google DeepMind", "avatar": "G", "avatar_class": "av-intl", "type": "intl",
     "tags": "vla wm", "subtitle": "Gemini Robotics · Apptronik Robot Park · RT-2 · 开放数据",
     "works": [
         {"dot": "vla", "title": "Gemini Robotics On-Device发布，Apptronik Robot Park宣布建设",
          "desc": "端侧机器人VLA能力再进一步，同时宣布在德州建设机器人公园以加速真实世界数据收集与验证。",
          "date": "2026.07.01", "link": "https://deepmind.google/models/gemini-robotics/", "link_text": "DeepMind官网"},
         {"dot": "vla", "title": "Gemini Robotics发布：基于Gemini 2.0的VLA模型",
          "desc": "首个将Gemini多模态大模型直接用于机器人控制的系统，端到端架构替代传统'感知-规划-执行'分离式设计。",
          "date": "2026.03.27", "link": "https://deepmind.google/models/gemini-robotics/", "link_text": "DeepMind官网"},
         {"dot": "data", "title": "Open X-Embodiment 2.0发布：200万+真实机器人轨迹",
          "desc": "全球最大开放机器人数据集，支持跨本体VLA模型训练。",
          "date": "2026.01.10", "link": "https://ai.googleblog.com", "link_text": "Google Research"},
     ]},

    {"name": "Genesis AI", "avatar": "Ge", "avatar_class": "av-intl", "type": "intl",
     "tags": "vla hw sim", "subtitle": "GENE-26.5 · Genesis World 1.0开源 · 全栈仿真",
     "works": [
         {"dot": "sim", "title": "正式开源Genesis World 1.0全栈仿真训练平台",
          "desc": "包含三大自主研发核心模块，可将复杂技能训练周期压缩80%、落地测试成本降低65%，sim-to-real验证Pearson 0.8996。",
          "date": "2026.07.03", "link": "https://cxgn.cn/17467.html", "link_text": "创新观察"},
         {"dot": "sim", "title": "Genesis World v1.2.2发布：触觉传感器与高保真摩擦模型",
          "desc": "面向灵巧操作训练的触觉噪声选项、非凸碰撞检测与elliptic friction cone，CPU仿真速度最高提升30%。",
          "date": "2026.07.11", "link": "https://www.laumy.tech/notes/posts/%E8%A1%8C%E4%B8%9A%E5%8A%A8%E6%80%81/%E7%AB%AF%E4%BE%A7-ai-%E4%B8%8E%E6%9C%BA%E5%99%A8%E4%BA%BA%E6%8A%80%E6%9C%AF%E9%9B%B7%E8%BE%BE2026-07-15", "link_text": "技术雷达"},
         {"dot": "vla", "title": "GENE-26.5发布：首个机器人基础模型系统",
          "desc": "单模型让机器人自主打蛋、弹钢琴、切番茄、解魔方，全程1倍速自主运行。",
          "date": "2026.05.06", "link": "https://robohub.app/zh/news/genesis-ai-gene-26-5-robot-manipulation", "link_text": "RoboHub"},
     ]},

    {"name": "Skild AI", "avatar": "S", "avatar_class": "av-intl", "type": "intl",
     "tags": "vla", "subtitle": "Skild Brain · 14亿美元C轮 · 估值$14B",
     "works": [
         {"dot": "rongzi", "title": "完成14亿美元C轮融资，估值突破140亿美元",
          "desc": "SoftBank领投，18个月内完成最大机器人融资轮次，构建行业首个统一机器人基础模型Skild Brain，跨本体、跨任务、跨场景泛化。",
          "date": "2026.01.14", "link": "https://www.businesswire.com/news/home/20260114335623/en/Skild-AI-Raises-%241.4B-Now-Valued-Over-%2414B", "link_text": "BusinessWire"},
         {"dot": "vla", "title": "Skild Brain：omni-bodied robot foundation model",
          "desc": "软件层定位，不造本体，训练数据量至少为竞品的1000倍，可适配四足、人形、桌面臂、移动平台等多种形态。",
          "date": "2026.01.14", "link": "https://www.skild.ai", "link_text": "Skild AI官网"},
     ]},

    # === 学术机构 ===
    {"name": "清华大学 (AIR/EIR)", "avatar": "清", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla data", "subtitle": "Harness VLA · LDA-1B · X-VLA · 具身智能研究院",
     "works": [
         {"dot": "vla", "title": "提出Harness VLA：用Harness Layer释放冻结VLA能力",
          "desc": "System层框架让冻结VLA专注接触密集操作，Agentic Planner学习原语组织方式，LIBERO-Pro扰动评测成功率82.4%，arXiv:2607.08448。",
          "date": "2026.07.23", "link": "https://harnessvla.github.io/", "link_text": "项目主页"},
         {"dot": "vla", "title": "银河通用联合清华AIR发布LDA-1B，登顶RSS 2026",
          "desc": "1.6B参数WAM框架，首次在隐空间统一世界模型与VLA，虚实共融数据利用与跨本体泛化。",
          "date": "2026.05.10", "link": "https://air.tsinghua.edu.cn/info/1007/2467.htm", "link_text": "清华AIR"},
         {"dot": "vla", "title": "X-VLA开源：全面刷新机器人基准性能记录",
          "desc": "首个实现120min无辅助自主叠衣任务的全开源模型（公开数据、代码与权重）。",
          "date": "2026.01.16", "link": "https://air.tsinghua.edu.cn/info/1007/2467.htm", "link_text": "清华AIR"},
     ]},

    {"name": "北京大学", "avatar": "北", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla data", "subtitle": "EgoSteer · VLA综述 · SynData · 灵巧操作",
     "works": [
         {"dot": "vla", "title": "北大-灵初联合开源EgoSteer双灵巧手通用操作大模型",
          "desc": "基于Qwen3-VL 2B，9600小时人类第一视角视频预训练，陌生语义新任务成功率62%，模型/代码/系统全开源，arXiv:2607.09701。",
          "date": "2026.07.24", "link": "https://www.psibot.ai?p=2929", "link_text": "灵初智能官网"},
         {"dot": "vla", "title": "北大-灵初发布具身VLA全面综述",
          "desc": "一文看清VLA技术路线与前沿进展，灵初智能联合创始人陈源培与北大杨耀东共同担任通讯作者。",
          "date": "2026.02.10", "link": "https://www.pku.edu.cn", "link_text": "北京大学官网"},
         {"dot": "data", "title": "PKU-SynData-10K发布：1万条高保真厨房场景合成数据",
          "desc": "与灵初智能联合发布，为VLA模型训练提供高质量合成数据支撑。",
          "date": "2026.02.10", "link": "https://www.pku.edu.cn", "link_text": "北京大学官网"},
     ]},

    {"name": "西湖大学", "avatar": "西", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla hw", "subtitle": "西湖o1 · GAE身外化身 · 空中操作机器人",
     "works": [
         {"dot": "hw", "title": "西湖机器人西湖o1亮相WAIC，5个月完成三轮数亿元融资",
          "desc": "西湖大学首个AI机器人成果转化项目，全栈自研人形机器人西湖o1及GAE身外化身系统展示实时交互与运动控制。",
          "date": "2026.07.20", "link": "https://www.toutiao.com/article/7664497190856933942", "link_text": "钱江晚报"},
         {"dot": "hw", "title": "西湖风形科技推出M500空中操作机器人",
          "desc": "基于Nature发表的空中近距离操作成果，实现6级强风下亚厘米级空中对接与工具交换，面向电力巡检等高空作业。",
          "date": "2026.07.29", "link": "https://36kr.com/p/3916152471285379", "link_text": "36氪"},
     ]},

    {"name": "UC Berkeley", "avatar": "B", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla data sim", "subtitle": "GaP · 数字表亲 · Do as I Do · RoboArena",
     "works": [
         {"dot": "vla", "title": "UC Berkeley/NVIDIA/CMU/Bosch提出GaP图策略系统",
          "desc": "Graph-as-Policy将任务建模为图并在仿真中自我改进，再部署到真实机器人，面向变分自动化商业场景，arXiv:2607.05369。",
          "date": "2026.07.16", "link": "https://new.qq.com/rain/a/20260716A03T0F00", "link_text": "腾讯新闻"},
         {"dot": "data", "title": "Do as I Do：互联网视频到真实灵巧手端到端流水线",
          "desc": "从单目RGB视频重建4D手物交互并迁移到22-DoF Sharpa Wave灵巧手，生成500条验证轨迹并部署10项真实任务，arXiv:2606.19333。",
          "date": "2026.07.07", "link": "https://dev.to/future_x/futurex-physical-ai-daily-issue-50-0707-4b8k", "link_text": "FutureX"},
         {"dot": "sim", "title": "数字表亲框架发布：大幅降低跨本体Sim2Real差距",
          "desc": "通过生成'数字表亲'而非精确数字孪生，实现低成本跨本体迁移。",
          "date": "2026.01.25", "link": "https://berkeley.edu", "link_text": "UC Berkeley"},
     ]},

    {"name": "Stanford", "avatar": "S", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla data", "subtitle": "RoboTTT · FPL · Ego-Pi · MOO · Behavior-1K",
     "works": [
         {"dot": "vla", "title": "Stanford/NVIDIA/UT Austin发布RoboTTT长程记忆系统",
          "desc": "上下文长度扩展至8000时间步（超4分钟连续历史），比现有最优策略提升三个数量级，推理不增加延迟，arXiv:2607.15275。",
          "date": "2026.07.27", "link": "https://new.qq.com/rain/a/20260727A0A9LA00", "link_text": "腾讯新闻"},
         {"dot": "vla", "title": "Freeform Preference Learning (FPL)提升长程操作38个百分点",
          "desc": "Chelsea Finn团队提出自由形式偏好学习，让机器人沿速度/安全/仔细等自然语言维度学习，RSS 2026，arXiv:2606.32027。",
          "date": "2026.07.02", "link": "https://embodiedglobal.com/es/categories/research?page=5", "link_text": "Embodied Global"},
         {"dot": "vla", "title": "Ego-Pi：VLA微调的ego-centric人类视角方法",
          "desc": "CVPR 2026发表，专注于ego-centric视角的VLA微调方法，提升第一人称操作任务性能。",
          "date": "2026.06.03", "link": "https://www.aib.vote/en/news/stanford-ai-lab-cvpr-2026-research", "link_text": "Stanford AI Lab"},
     ]},

    {"name": "智源研究院 (BAAI)", "avatar": "源", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla wm", "subtitle": "SoulAgent · RoboBrain Orca · 智源大会 · VISTA世界模型",
     "works": [
         {"dot": "wm", "title": "发布RoboBrain Orca世界模型：12.5万小时无标注视频训练",
          "desc": "用12.5万小时无标注视频数据训练，让AI通过'看视频'自主学习物体运动规律和场景演变逻辑。",
          "date": "2026.07.02", "link": "http://www.zqrb.cn/gscy/qiyexinxi/2026-07-02/A1782955137529.html", "link_text": "证券日报"},
         {"dot": "vla", "title": "SoulAgent亮相全球数字经济大会",
          "desc": "智源推出的个人智能体产品，在6月智源大会完成万人级实战验证。",
          "date": "2026.07.02", "link": "http://www.zqrb.cn/gscy/qiyexinxi/2026-07-02/A1782955137529.html", "link_text": "证券日报"},
         {"dot": "wm", "title": "2026智源大会：具身智能CEO华山论剑",
          "desc": "6月12-13日北京举办，200+顶尖专家与40+AI企业CEO，郭彦东定调'世界模型是VLA体系核心组件'。",
          "date": "2026.06.12", "link": "https://hub.baai.ac.cn/view/55174", "link_text": "智源Hub"},
     ]},

    {"name": "中科院自动化所", "avatar": "中", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla wm", "subtitle": "VLA-R1 · 世界模型+RL",
     "works": [
         {"dot": "vla", "title": "VLA-R1：融合世界模型与强化学习",
          "desc": "隐空间统一世界模型预测与VLA动作生成，引入R1-style强化学习优化。",
          "date": "2026.02.28", "link": "https://www.ia.cas.cn", "link_text": "中科院官网"},
     ]},

    {"name": "鹏城实验室", "avatar": "鹏", "avatar_class": "av-lab", "type": "lab",
     "tags": "vla data", "subtitle": "VidMan · 视频驱动操作",
     "works": [
         {"dot": "data", "title": "大规模互联网视频数据集构建",
          "desc": "从YouTube等平台自动采集和标注百万级机器人相关视频，为VidMan提供训练数据支撑。",
          "date": "2026.01.15", "link": "https://www.pcl.ac.cn", "link_text": "鹏城实验室"},
     ]},
]

# ========== CORE SUMMARY ==========
summary_trends = [
    {"num": "1", "title": "VLA架构跃迁：从端到端到类脑再到操作系统，'堆模型堆不出大脑'成为产业共识",
     "content": "2026年VLA架构经历端到端VLA(pi0.7/Figure Helix 02)→增强型VLA(千寻Spirit v1.6/银河通用LDA-1B)→类脑VLA(智平方NeuroVLA)三代跃迁。7月逐际动力COSA 0.5(2026.07.15)进一步提出'堆模型堆不出大脑'，模型是技能、脑是操作系统，System 0全身运动+System 1 VLA/WAM+System 2大语言/世界模型的三层架构首次系统性定义人形大脑系统。Figure Helix 02(2026.07)新增System 0高频关节力矩控制层，4分钟61个连贯动作全程无人工干预。清华Harness VLA(2026.07.23)则在系统层提出Harness Layer，让冻结VLA专注接触密集操作，LIBERO-Pro扰动评测达82.4%。"},
    {"num": "2", "title": "世界模型深度融合：从独立路线到VLA核心组件，再到操作系统级认知引擎",
     "content": "世界模型正在经历'竞争路线→核心组件→操作系统引擎'的三阶段融合。6月智源大会定调'世界模型是VLA体系中的核心组件'；7月逐际动力COSA 0.5将世界模型升格为System 2大脑操作系统的核心引擎。智在无界Being-H0.8(2026.07.28)首次将触觉模态引入隐式世界动作模型预训练；灵初智能Psi-W0(2026.04)与Psi-R2策略模型组成双系统；极佳视界GigaWorld(2026.07)与NVIDIA Cosmos 3(2026.05)持续推动世界模型在仿真与真实任务中的闭环。"},
    {"num": "3", "title": "量产元年冲刺：中国产量有望破10万台，真实产线交付成为检验标准",
     "content": "工信部(2026.07.08)表态2026年中国人形机器人全年整机产量有望突破10万台。智元第1.5万台(2026.06.28)、宇树累计约1.1万台且IPO注册获批(2026.07.02)、至简动力i7 Pro百台交付(2026.07.06)、星动纪元启动千台级交付(2026.07.06)。海外市场Figure 03部署BMW Spartanburg物流排序(2026.07.05)，Tesla Optimus Gen-3方案评审通过并给出年底年化10万台目标(2026.07.10)，1X NEO首批家庭交付并发布25-DoF灵巧手(2026.07.17)。"},
    {"num": "4", "title": "数据与开源生态爆发：人类视频、触觉、仿真平台与开源模型并行推进",
     "content": "北京人形机器人创新中心数据训练基地(2026.07)日产能超500小时，目标100万小时。北大-灵初EgoSteer(2026.07.24)用9600小时人类第一视角视频训练双灵巧手模型并开源。Genesis AI开源Genesis World 1.0(2026.07.03)与v1.2.2触觉仿真(2026.07.11)。NVIDIA GR00T N1.7(2026.06.01)与智源RoboBrain Orca(2026.07.02)分别从开源模型与无标注视频两个方向扩展数据边界。"},
    {"num": "5", "title": "融资格局重构：大脑/操作系统赛道估值狂飙，PI、逐际动力、Skild引领全球",
     "content": "PI寻求10亿美元融资估值$11B(2026.07.14)；逐际动力Pre-IPO估值150亿元，半年累计融资4亿美元(2026.07.14)；Skild AI 14亿美元C轮估值$14B(2026.01)。国内智平方/自变量/千寻/星海图/星动纪元估值均突破200亿。宇树科技IPO拟募资42亿。资本重心从'造机器人本体'加速转向'机器人大脑+操作系统+数据闭环'。"},
]

summary_biz = [
    {"region": "中国国内", "trend": "量产10万台+操作系统元年+真实产线交付", "players": "智元(1.5万台/WAIC新品)、宇树(IPO+1.1万台)、逐际动力(COSA 0.5+Pre-IPO)、千寻(Moz2/Spirit v1.6)、智平方(NeuroVLA)、星海图(G0.5+Kengo)、星动纪元(50亿/诚通基金)、极佳视界(WAIC全系列)、银河通用(LDA-1B)、自变量(WALL-B/APEC)、灵初(EgoSteer)、至简动力(i7 Pro百台)"},
    {"region": "海外市场", "trend": "工厂规模化部署+家庭交付+融资翻倍", "players": "Figure(BMW Spartanburg物流排序)、PI($11B估值/pi0.7)、Tesla(Optimus年化10万台)、1X(NEO 25-DoF灵巧手)、NVIDIA(Cosmos 3/GR00T N1.7/WAM)、Genesis(GENE-26.5/Genesis World开源)、Skild($14B估值)"},
    {"region": "学术前沿", "trend": "Harness Layer+长程记忆+人类视频+触觉世界模型", "players": "清华(Harness VLA)、北大(EgoSteer)、Stanford(RoboTTT/FPL)、UCBerkeley(GaP/Do as I Do)、智源(RoboBrain Orca)、西湖(西湖o1/空中操作机器人)"},
]

# ========== JS (kept from original) ==========
JS = r'''
// ===== SIDEBAR =====
function toggleSidebar() {
    var sb = document.getElementById('sidebar');
    var mn = document.getElementById('mainContent');
    var btn = document.getElementById('sidebarToggle');
    sb.classList.toggle('collapsed');
    mn.classList.toggle('expanded');
    btn.textContent = sb.classList.contains('collapsed') ? '\u00bb' : '\u00ab';
}

// Active nav on scroll
var sections = ['summary', 'hotspots', 'teams'];
window.addEventListener('scroll', function() {
    var scrollY = window.scrollY + 100;
    for (var i = sections.length - 1; i >= 0; i--) {
        var el = document.getElementById('section-' + sections[i]);
        if (el && el.offsetTop <= scrollY) {
            document.querySelectorAll('.sidebar-nav a').forEach(function(a) { a.classList.remove('active'); });
            document.querySelector('.sidebar-nav a[data-nav="' + sections[i] + '"]').classList.add('active');
            break;
        }
    }
});

// Smooth scroll for nav links
document.querySelectorAll('.sidebar-nav a').forEach(function(a) {
    a.addEventListener('click', function(e) {
        e.preventDefault();
        var target = document.querySelector(this.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

// ===== HOTSPOT LOAD MORE =====
var hsPage = 10;
var hsExpanded = false;
var allHsItems = document.querySelectorAll('.hotspot-item');
function loadMoreHotspots() {
    var btn = document.getElementById('loadMoreBtn');
    if (!hsExpanded) {
        allHsItems.forEach(function(item) {
            if (item.style.display === 'none') {
                if (item.matchesHsFilter !== false) {
                    var searchBox = document.querySelector('.hotspot-controls .search-box');
                    var searchVal = searchBox ? searchBox.value.toLowerCase() : '';
                    if (!searchVal || item.innerText.toLowerCase().includes(searchVal)) {
                        item.style.display = '';
                    }
                }
            }
        });
        hsExpanded = true;
        btn.textContent = '\u2191 \u6536\u8d77';
    } else {
        var visibleItems = Array.from(allHsItems).filter(function(it) { return it.style.display !== 'none'; });
        var count = 0;
        for (var i = 0; i < visibleItems.length; i++) {
            count++;
            if (count > 10) {
                visibleItems[i].style.display = 'none';
            }
        }
        hsExpanded = false;
        updateLoadMoreBtn();
    }
}

function resetHsView() {
    var visibleItems = Array.from(allHsItems).filter(function(it) { return it.style.display !== 'none'; });
    var count = 0;
    for (var i = 0; i < visibleItems.length; i++) {
        count++;
        if (count > 10) {
            visibleItems[i].style.display = 'none';
        }
    }
    hsExpanded = false;
    updateLoadMoreBtn();
}

// ===== HOTSPOT FILTER =====
var activeHsFilters = new Set();
function toggleHsFilter(btn, tag) {
    if (activeHsFilters.has(tag)) {
        activeHsFilters.delete(tag);
        btn.classList.remove('active');
    } else {
        activeHsFilters.add(tag);
        btn.classList.add('active');
    }
    applyHsFilters();
}

function applyHsFilters() {
    var searchVal = (document.querySelector('.hotspot-controls .search-box') || {}).value || '';
    searchVal = searchVal.toLowerCase();
    allHsItems.forEach(function(item) {
        var tag = item.getAttribute('data-hs-tag');
        var text = item.innerText.toLowerCase();
        var matchTag = activeHsFilters.size === 0 || activeHsFilters.has(tag);
        var matchSearch = !searchVal || text.includes(searchVal);
        var show = matchTag && matchSearch;
        item.style.display = show ? '' : 'none';
        item.matchesHsFilter = matchTag;
    });
    resetHsView();
}

function filterHotspots(val) {
    var v = val.toLowerCase();
    allHsItems.forEach(function(item) {
        var text = item.innerText.toLowerCase();
        var tag = item.getAttribute('data-hs-tag');
        var matchTag = activeHsFilters.size === 0 || activeHsFilters.has(tag);
        var matchSearch = !v || text.includes(v);
        item.style.display = (matchTag && matchSearch) ? '' : 'none';
        item.matchesHsFilter = matchTag;
    });
    resetHsView();
}

function updateLoadMoreBtn() {
    var visible = Array.from(allHsItems).filter(function(it) { return it.style.display !== 'none'; });
    var btn = document.getElementById('loadMoreBtn');
    if (visible.length <= 10) {
        var allHidden = allHsItems.length - visible.length;
        btn.style.display = (allHidden <= 0) ? 'none' : '';
        btn.textContent = '\u2193 \u52a0\u8f7d\u66f4\u591a (' + (allHsItems.length - visible.length) + '\u6761)';
        hsExpanded = false;
    } else {
        if (hsExpanded) {
            btn.style.display = '';
            btn.textContent = '\u2191 \u6536\u8d77';
        } else {
            btn.style.display = '';
            var hiddenCount = visible.length - 10;
            btn.textContent = '\u2193 \u52a0\u8f7d\u66f4\u591a (' + hiddenCount + '\u6761)';
        }
    }
}

// ===== TEAM CATEGORY FILTER =====
var activeCategory = 'all';
function filterCategory(cat, btn) {
    activeCategory = cat;
    document.querySelectorAll('.cat-chip').forEach(function(c) { c.classList.remove('active'); });
    btn.classList.add('active');
    applyTeamFilters();
}

// ===== TEAM TAG FILTER =====
var activeTeamTags = new Set();
function toggleTeamTag(btn, tag) {
    if (activeTeamTags.has(tag)) {
        activeTeamTags.delete(tag);
        btn.classList.remove('active');
    } else {
        activeTeamTags.add(tag);
        btn.classList.add('active');
    }
    applyTeamFilters();
}

function applyTeamFilters() {
    var cards = document.querySelectorAll('#section-teams .card');
    var visible = 0;
    cards.forEach(function(card) {
        var type = card.getAttribute('data-type');
        var tags = card.getAttribute('data-tags').split(' ');
        var matchCat = activeCategory === 'all' || type === activeCategory;
        var matchTag = activeTeamTags.size === 0 || tags.some(function(t) { return activeTeamTags.has(t); });
        var show = matchCat && matchTag;
        card.style.display = show ? '' : 'none';
        if (show) visible++;
    });
    document.getElementById('emptyState').style.display = visible === 0 ? '' : 'none';
}

// ===== EXPAND/COLLAPSE TEAM CARDS =====
function toggleCard(btn) {
    var container = btn.previousElementSibling;
    if (container.classList.contains('is-collapsed')) {
        container.classList.remove('is-collapsed');
        container.classList.add('is-expanded');
        btn.textContent = '\u25b2 \u6536\u8d77';
    } else {
        container.classList.remove('is-expanded');
        container.classList.add('is-collapsed');
        var count = container.querySelectorAll('.work-item').length;
        btn.textContent = '\u2193 \u5c55\u5f00\u66f4\u591a (' + count + ')';
    }
}
'''

# ========== HTML GENERATION ==========
def escape(text):
    return html.escape(text, quote=False)

def gen_hotspot_item(hs, hidden=False):
    tag_cls = TAG_MAP.get(hs['tag'], 'ht-tag-jishu')
    style = ' style="display:none"' if hidden else ''
    return (
        f"<div class='hotspot-item'{style} data-hs-tag='{escape(hs['tag'])}'>\n"
        f"      <span class='hotspot-date'>{escape(hs['date'])}</span>\n"
        f"      <span class='hotspot-tag {tag_cls}'>{escape(hs['tag'])}</span>\n"
        f"      <div class='hotspot-body'>\n"
        f"        <div class='hotspot-title'>{escape(hs['title'])}</div>\n"
        f"        <div class='hotspot-desc'>{escape(hs['desc'])}</div>\n"
        f"        <a class='hotspot-link' href='{escape(hs['link'])}' target='_blank'>\u2192 {escape(hs['link_text'])}</a>\n"
        f"      </div>\n"
        f"    </div>"
    )

def gen_team_card(team):
    works = team['works']
    if not works:
        return ''

    first_work = works[0]
    extra_works = works[1:]

    tags_html = ' '.join(
        f"<span class='tag tag-{t}'>{t.upper()}</span>" for t in team['tags'].split()
    )

    first_work_html = (
        f"<div class='work-item'>\n"
        f"        <div class='work-title'><span class='work-dot work-dot-{first_work['dot']}'></span>{escape(first_work['title'])}</div>\n"
        f"        <div class='work-desc'>{escape(first_work['desc'])}</div>\n"
        f"        <div class='work-meta'><span class='work-date'>{escape(first_work['date'])}</span> <a class='work-link' href='{escape(first_work['link'])}' target='_blank'>\u2192 {escape(first_work['link_text'])}</a></div>\n"
        f"      </div>"
    )

    if extra_works:
        extra_items_html = ''.join(
            f"<div class='work-item'>\n"
            f"            <div class='work-title'><span class='work-dot work-dot-{w['dot']}'></span>{escape(w['title'])}</div>\n"
            f"            <div class='work-desc'>{escape(w['desc'])}</div>\n"
            f"            <div class='work-meta'><span class='work-date'>{escape(w['date'])}</span> <a class='work-link' href='{escape(w['link'])}' target='_blank'>\u2192 {escape(w['link_text'])}</a></div>\n"
            f"          </div>"
            for w in extra_works
        )
        extra_section = (
            f"<div class=\"extra-items is-collapsed\">{extra_items_html}</div>\n"
            f"      <button class=\"expand-toggle\" onclick=\"toggleCard(this)\">\u2193 \u5c55\u5f00\u66f4\u591a ({len(extra_works)})</button>"
        )
    else:
        extra_section = ''

    return (
        f"<div class='card' data-type='{team['type']}' data-tags='{team['tags']}'>\n"
        f"      <div class='card-header'>\n"
        f"        <div class='avatar {team['avatar_class']}'>{escape(team['avatar'])}</div>\n"
        f"        <div class='card-title'>\n"
        f"          <h3>{escape(team['name'])}</h3>\n"
        f"          <div class='subtitle'>{escape(team['subtitle'])}</div>\n"
        f"          <div class='card-tags'>{tags_html}</div>\n"
        f"        </div>\n"
        f"      </div>\n"
        f"      <div class='card-body'>\n"
        f"      {first_work_html}\n"
        f"      {extra_section}\n"
        f"      </div>\n"
        f"    </div>"
    )

def gen_html():
    # Count categories
    cn_count = sum(1 for t in teams if t['type'] == 'cn')
    intl_count = sum(1 for t in teams if t['type'] == 'intl')
    lab_count = sum(1 for t in teams if t['type'] == 'lab')
    total_count = len(teams)
    hs_count = len(hotspots)
    hidden_hs = hs_count - 10

    # Hotspot items: first 10 visible, rest hidden
    hs_html = ''.join(
        gen_hotspot_item(hs, hidden=(i >= 10))
        for i, hs in enumerate(hotspots)
    )

    # Team cards
    teams_html = ''.join(gen_team_card(t) for t in teams)

    # Hotspot filter buttons
    filter_tags = ['技术', '融资', '产品', '评测', '开源', '世界模型', '采访', '直播', '生态', '论文']
    filter_html = ' '.join(
        f"<button class='hs-filter' onclick='toggleHsFilter(this, \"{t}\")'>{t}</button>"
        for t in filter_tags
    )

    # Summary trends
    trends_html = ''.join(
        f"<li><span class='trend-num'>{t['num']}</span><strong>{escape(t['title'])}</strong><br/>{escape(t['content'])}</li>\n"
        for t in summary_trends
    )

    # Summary biz
    biz_html = ''.join(
        f"<div class='biz-item'><div class='biz-region'>{escape(b['region'])}</div><div class='biz-trend'>{escape(b['trend'])}</div><div class='biz-players'>{escape(b['players'])}</div></div>\n"
        for b in summary_biz
    )

    full_html = (
        f"<!DOCTYPE html>\n<html lang='zh'>\n<head>\n"
        f"<meta charset='UTF-8'>\n"
        f"<meta name='viewport' content='content=device-width, initial-scale=1.0'>\n"
        f"<title>robotera VLA\u56e2\u961f\u8c03\u7814\u62a5\u544a-2026.07</title>\n"
        f"<style>\n{CSS}\n</style>\n"
        f"</head>\n<body>\n"

        # Sidebar
        f"<div class='sidebar' id='sidebar'>\n"
        f"  <div class='sidebar-header'>\n"
        f"    <span class='sidebar-title'>VLA\u8c03\u7814\u62a5\u544a</span>\n"
        f"    <button class='sidebar-toggle' id='sidebarToggle' onclick='toggleSidebar()'>\u00ab</button>\n"
        f"  </div>\n"
        f"  <div class='sidebar-nav'>\n"
        f"    <a href='#section-summary' data-nav='summary'><span class='nav-icon'>\u2756</span> <span>\u6838\u5fc3\u6458\u8981</span></a>\n"
        f"    <a href='#section-hotspots' data-nav='hotspots'><span class='nav-icon'>\u2728</span> <span>\u6700\u65b0\u70ed\u70b9</span></a>\n"
        f"    <a href='#section-teams' data-nav='teams'><span class='nav-icon'>\U0001f3e0</span> <span>\u91cd\u8981\u56e2\u961f</span></a>\n"
        f"  </div>\n"
        f"</div>\n"

        # Main content
        f"<div class='main' id='mainContent'>\n"

        # Header
        f"<div class='header'>\n"
        f"  <h1>robotera VLA\u56e2\u961f\u8c03\u7814\u62a5\u544a-2026.07</h1>\n"
        f"  <p>\u5177\u8eab\u667a\u80fd / VLA\u6a21\u578b / \u4e16\u754c\u6a21\u578b / \u4eba\u5f62\u673a\u5668\u4eba\u5168\u8c03\u7814 &middot; \u66f4\u65b0\u65e5\u671f 2026.07.29</p>\n"
        f"  <div class='meta-bar'>\n"
        f"    <span class='meta-badge badge-cn'>{cn_count}\u5bb6\u56fd\u5185\u4f01\u4e1a</span>\n"
        f"    <span class='meta-badge badge-intl'>{intl_count}\u5bb6\u6d77\u5916\u4f01\u4e1a</span>\n"
        f"    <span class='meta-badge badge-lab'>{lab_count}\u5bb6\u5b66\u672f\u673a\u6784</span>\n"
        f"    <span class='meta-badge badge-vla'>{hs_count}\u6761\u70ed\u70b9</span>\n"
        f"  </div>\n"
        f"</div>\n"

        # Content area
        f"<div class='content'>\n"

        # === Summary section ===
        f"<div class='section-block' id='section-summary'>\n"
        f"  <h2 class='section-title'>\u2756 \u6838\u5fc3\u6458\u8981</h2>\n"
        f"  <div class='summary-section'>\n"
        f"    <h3>\u4e94\u5927\u6280\u672f\u8d8b\u52bf</h3>\n"
        f"    <ul>\n{trends_html}</ul>\n"
        f"  </div>\n"
        f"  <div class='summary-section'>\n"
        f"    <h3>\u5546\u4e1a\u5e03\u5c40\u52a8\u6001</h3>\n"
        f"    <div class='biz-grid'>\n{biz_html}</div>\n"
        f"  </div>\n"
        f"</div>\n"

        # === Hotspots section ===
        f"<div class='section-block' id='section-hotspots'>\n"
        f"  <h2 class='section-title'>\u2728 \u6700\u65b0\u70ed\u70b9</h2>\n"
        f"  <div class='hotspot-controls'>\n"
        f"    <input class='search-box' placeholder='\u641c\u7d22\u70ed\u70b9...' oninput='filterHotspots(this.value)'>\n"
        f"    <div class='hs-filter-group'>\n{filter_html}</div>\n"
        f"  </div>\n"
        f"  <div class='hotspot-list'>\n{hs_html}\n  </div>\n"
        f"  <button class='load-more-btn' id='loadMoreBtn' onclick='loadMoreHotspots()'>\u2193 \u52a0\u8f7d\u66f4\u591a ({hidden_hs}\u6761)</button>\n"
        f"</div>\n"

        # === Teams section ===
        f"<div class='section-block' id='section-teams'>\n"
        f"  <h2 class='section-title'>\U0001f3e0 \u91cd\u8981\u56e2\u961f</h2>\n"
        f"  <div class='team-category-bar'>\n"
        f"    <button class='cat-chip cat-all active' onclick='filterCategory(\"all\", this)'>\u5168\u90e8 <span class='cat-count'>{total_count}</span></button>\n"
        f"    <button class='cat-chip cat-cn' onclick='filterCategory(\"cn\", this)'>\u56fd\u5185\u4f01\u4e1a <span class='cat-count'>{cn_count}</span></button>\n"
        f"    <button class='cat-chip cat-intl' onclick='filterCategory(\"intl\", this)'>\u56fd\u5916\u4f01\u4e1a <span class='cat-count'>{intl_count}</span></button>\n"
        f"    <button class='cat-chip cat-lab' onclick='filterCategory(\"lab\", this)'>\u5b66\u672f\u673a\u6784 <span class='cat-count'>{lab_count}</span></button>\n"
        f"  </div>\n"
        f"  <div class='team-tag-filters'>\n"
        f"    <button class='team-tag-btn f-vla' onclick='toggleTeamTag(this, \"vla\")'>VLA</button>\n"
        f"    <button class='team-tag-btn f-wm' onclick='toggleTeamTag(this, \"wm\")'>\u4e16\u754c\u6a21\u578b</button>\n"
        f"    <button class='team-tag-btn f-hw' onclick='toggleTeamTag(this, \"hw\")'>\u786c\u4f53</button>\n"
        f"    <button class='team-tag-btn f-sim' onclick='toggleTeamTag(this, \"sim\")'>\u4eff\u771f</button>\n"
        f"    <button class='team-tag-btn f-data' onclick='toggleTeamTag(this, \"data\")'>\u6570\u636e</button>\n"
        f"  </div>\n"
        f"  <div class='grid'>\n{teams_html}\n  </div>\n"
        f"  <div class='empty-state' id='emptyState' style='display:none'>\u6ca1\u6709\u5339\u914d\u7684\u56e2\u961f</div>\n"
        f"</div>\n"

        f"</div>  <!-- content -->\n"
        f"</div>  <!-- main -->\n"

        # Script
        f"<script>\n{JS}\n</script>\n"
        f"</body>\n</html>"
    )

    return full_html

# ========== WRITE ==========
html_content = gen_html()
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML report written to {OUTPUT_FILE}")
print(f"Total hotspots: {len(hotspots)}, Total teams: {len(teams)}")
print(f"CN teams: {sum(1 for t in teams if t['type'] == 'cn')}")
print(f"INTL teams: {sum(1 for t in teams if t['type'] == 'intl')}")
print(f"LAB teams: {sum(1 for t in teams if t['type'] == 'lab')}")
