#!/usr/bin/env python3
"""
测试脚本：验证ZhipuAI API连接和初始化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_zhipu_api():
    """测试ZhipuAI API连接"""
    
    print("=" * 60)
    print("测试：ZhipuAI API连接")
    print("=" * 60)
    
    try:
        # 导入依赖
        print("1. 导入ZhipuAI库...")
        from zhipuai import ZhipuAI
        print("✅ ZhipuAI库导入成功")
        
        # 导入配置
        print("\n2. 导入API配置...")
        from config import AI_API_KEY
        print("✅ API配置导入成功")
        print(f"   API Key前缀: {AI_API_KEY[:10]}..." if AI_API_KEY else "❌ API Key为空")
        
        # 初始化客户端
        print("\n3. 初始化ZhipuAI客户端...")
        client = ZhipuAI(api_key=AI_API_KEY)
        print("✅ ZhipuAI客户端初始化成功")
        
        # 测试简单对话
        print("\n4. 测试API调用...")
        test_messages = [
            {"role": "user", "content": "你好，请简单回复一下，确认连接正常"}
        ]
        
        response = client.chat.completions.create(
            model="glm-4",
            messages=test_messages,
            temperature=0.1
        )
        
        print("✅ API调用成功")
        print(f"   模型响应: {response.choices[0].message.content}")
        
        # 测试夜报相关的prompt
        print("\n5. 测试夜报类型的prompt...")
        night_prompt = """
        作为私人秘书，请简单总结以下信息：
        - 今日完成任务：学习Python, 写代码
        - 明日计划：继续开发项目
        请用一句话总结。
        """
        
        response2 = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": night_prompt}],
            temperature=0.3
        )
        
        print("✅ 夜报prompt测试成功")
        print(f"   响应内容: {response2.choices[0].message.content}")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 可能需要安装: pip install zhipuai")
        return False
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        print("💡 可能的原因:")
        print("   1. API Key无效或过期")
        print("   2. 网络连接问题")
        print("   3. ZhipuAI API服务异常")
        print("   4. 模型名称不正确")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ZhipuAI API测试全部通过！")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_zhipu_api()