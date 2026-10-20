from core.retriever import search

questions = [
    "测量时看不到波形，应该检查什么？",
    "RL并联时，各支路电压是否相同？",
    "有效值与峰值有什么关系？",
    "电路仿真运行后，波形完全不见了，怎么办？",
    "一次函数的图像为什么只有一条直线？",
]

for question in questions:
    results = search("circuit", question)

    print(f"\n问题：{question}")

    if results:
        for item in results:
            print(f"找到资料：{item['id']} —— {item['title']}")
    else:
        print("没有找到资料")