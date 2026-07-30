"""多工具 Agent 示例：客服场景，需要串联查客户 → 查订单 → 查库存 → 算退款 → 建工单。"""

import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

# ---------- 模拟业务数据 ----------
CUSTOMERS = {
    "alice": {
        "id": "C001",
        "name": "Alice Chen",
        "email": "alice@example.com",
        "tier": "gold",
        "city": "Singapore",
    },
    "bob": {
        "id": "C002",
        "name": "Bob Wang",
        "email": "bob@example.com",
        "tier": "silver",
        "city": "Shanghai",
    },
}

ORDERS = {
    "C001": [
        {
            "order_id": "ORD-1001",
            "product_id": "SKU-WATCH",
            "product": "Smart Watch Pro",
            "qty": 1,
            "unit_price": 299.0,
            "status": "delivered",
            "purchased_at": "2026-06-01",
        },
        {
            "order_id": "ORD-1008",
            "product_id": "SKU-BUD",
            "product": "Wireless Earbuds",
            "qty": 2,
            "unit_price": 89.0,
            "status": "shipped",
            "purchased_at": "2026-07-20",
        },
    ],
    "C002": [
        {
            "order_id": "ORD-2003",
            "product_id": "SKU-KEYBOARD",
            "product": "Mechanical Keyboard",
            "qty": 1,
            "unit_price": 159.0,
            "status": "delivered",
            "purchased_at": "2026-05-15",
        },
    ],
}

INVENTORY = {
    "SKU-WATCH": {"name": "Smart Watch Pro", "stock": 12, "warehouse": "SG"},
    "SKU-BUD": {"name": "Wireless Earbuds", "stock": 0, "warehouse": "SG"},
    "SKU-KEYBOARD": {"name": "Mechanical Keyboard", "stock": 5, "warehouse": "SH"},
}

# 会员等级对应的额外退款加成比例
TIER_BONUS = {"gold": 0.10, "silver": 0.05, "bronze": 0.0}

TICKETS: list[dict] = []


# ---------- Tools ----------
@tool
def lookup_customer(name: str) -> str:
    """按客户姓名查找客户档案（id / email / 会员等级 / 城市）。

    Args:
        name: 客户姓名，支持模糊匹配，如 Alice
    """
    print(f"[tool] lookup_customer(name={name!r})")
    key = name.strip().lower().split()[0]
    customer = CUSTOMERS.get(key)
    if not customer:
        for c in CUSTOMERS.values():
            if name.lower() in c["name"].lower():
                customer = c
                break
    if not customer:
        return json.dumps({"error": f"customer '{name}' not found"})
    return json.dumps(customer, ensure_ascii=False)


@tool
def get_orders(customer_id: str) -> str:
    """按客户 ID 拉取历史订单列表。

    Args:
        customer_id: 客户 ID，例如 C001
    """
    print(f"[tool] get_orders(customer_id={customer_id!r})")
    orders = ORDERS.get(customer_id, [])
    if not orders:
        return json.dumps({"error": f"no orders for {customer_id}"})
    return json.dumps({"customer_id": customer_id, "orders": orders}, ensure_ascii=False)


@tool
def check_inventory(product_id: str) -> str:
    """查询商品库存与所在仓库。

    Args:
        product_id: 商品 SKU，例如 SKU-WATCH
    """
    print(f"[tool] check_inventory(product_id={product_id!r})")
    item = INVENTORY.get(product_id)
    if not item:
        return json.dumps({"error": f"unknown product {product_id}"})
    return json.dumps({"product_id": product_id, **item}, ensure_ascii=False)


@tool
def calculate_refund(
    unit_price: float,
    qty: int,
    tier: str,
    reason: str = "defect",
) -> str:
    """根据单价、数量、会员等级和退款原因计算应退金额。

    规则：
    - defect / wrong_item: 全额退款 + 会员加成
    - change_mind: 退 80%，无加成
    - late_delivery: 退 50% + 会员加成

    Args:
        unit_price: 单价
        qty: 数量
        tier: 会员等级 gold / silver / bronze
        reason: 退款原因 defect / wrong_item / change_mind / late_delivery
    """
    print(
        f"[tool] calculate_refund(unit_price={unit_price}, qty={qty}, "
        f"tier={tier!r}, reason={reason!r})"
    )
    subtotal = unit_price * qty
    bonus_rate = TIER_BONUS.get(tier.lower(), 0.0)

    if reason in ("defect", "wrong_item"):
        base_rate, apply_bonus = 1.0, True
    elif reason == "change_mind":
        base_rate, apply_bonus = 0.8, False
    elif reason == "late_delivery":
        base_rate, apply_bonus = 0.5, True
    else:
        return json.dumps({"error": f"unknown reason '{reason}'"})

    refund = subtotal * base_rate
    bonus = refund * bonus_rate if apply_bonus else 0.0
    total = round(refund + bonus, 2)

    return json.dumps(
        {
            "subtotal": subtotal,
            "base_rate": base_rate,
            "bonus_rate": bonus_rate if apply_bonus else 0.0,
            "bonus": round(bonus, 2),
            "refund_total": total,
            "currency": "USD",
        },
        ensure_ascii=False,
    )


@tool
def create_support_ticket(
    customer_id: str,
    order_id: str,
    issue: str,
    refund_amount: float,
    priority: str = "normal",
) -> str:
    """创建客服工单，记录退款处理结果。

    Args:
        customer_id: 客户 ID
        order_id: 订单 ID
        issue: 问题简述
        refund_amount: 建议退款金额
        priority: 优先级 low / normal / high
    """
    print(
        f"[tool] create_support_ticket(customer_id={customer_id!r}, "
        f"order_id={order_id!r}, refund_amount={refund_amount}, priority={priority!r})"
    )
    ticket = {
        "ticket_id": f"TKT-{1000 + len(TICKETS) + 1}",
        "customer_id": customer_id,
        "order_id": order_id,
        "issue": issue,
        "refund_amount": refund_amount,
        "priority": priority,
        "status": "open",
    }
    TICKETS.append(ticket)
    return json.dumps(ticket, ensure_ascii=False)


# ---------- Agent ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2,
)

SYSTEM = """你是电商客服助手。处理退换货请求时必须按顺序使用工具，不要凭空编造数据：
1. lookup_customer 查客户档案
2. get_orders 查订单
3. check_inventory 确认相关商品是否有货（便于建议换货）
4. calculate_refund 按规则计算退款
5. create_support_ticket 建工单

最后用中文给出简洁总结：客户信息、涉及订单、库存结论、退款金额、工单号。"""

agent = create_agent(
    model=llm,
    tools=[
        lookup_customer,
        get_orders,
        check_inventory,
        calculate_refund,
        create_support_ticket,
    ],
    system_prompt=SYSTEM,
)

USER_QUERY = (
    "客户 Alice 说她 7 月买的 Wireless Earbuds 有质量问题要退货。"
    "请按流程处理：查她的档案和订单，看看这款耳机还有没有库存可以换货，"
    "按 defect 原因算退款，并开一张 high 优先级工单。"
    "最后告诉我退多少钱、工单号，以及是否建议换货。"
)

response = agent.invoke({"messages": [{"role": "user", "content": USER_QUERY}]})

print("=" * 60)
print("最终回复:")
print(response["messages"][-1].content)
print("=" * 60)
print(f"已创建工单数: {len(TICKETS)}")
if TICKETS:
    print("工单详情:", json.dumps(TICKETS, ensure_ascii=False, indent=2))
