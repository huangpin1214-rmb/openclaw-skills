#!/usr/bin/env python3
"""
流程图导出工具 - 生成 PNG/SVG/PDF
需要先安装 @mermaid-js/mermaid-cli

npm install -g @mermaid-js/mermaid-cli
"""

import subprocess
import sys
import os

def install_mermaid():
    """安装 Mermaid CLI"""
    print("正在安装 @mermaid-js/mermaid-cli...")
    try:
        subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'], check=True)
        print("✅ 安装成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        return False

def generate_image(input_file, output_file, format='png'):
    """生成图片"""
    if not os.path.exists(input_file):
        print(f"❌ 文件不存在: {input_file}")
        return False
    
    cmd = ['mmdc', '-i', input_file, '-o', output_file]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 已生成: {output_file}")
        return True
    except FileNotFoundError:
        print("❌ mmdc 命令未找到，请先安装: npm install -g @mermaid-js/mermaid-cli")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("""
📊 流程图导出工具

用法:
  python3 export.py install          # 安装依赖
  python3 export.py generate <文件>  # 生成图片

示例:
  python3 export.py install
  python3 export.py generate login.mmd
        """)
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'install':
        install_mermaid()
    elif cmd == 'generate':
        if len(sys.argv) < 3:
            print("用法: python3 export.py generate <mermaid文件>")
            return
        input_file = sys.argv[2]
        base = os.path.splitext(input_file)[0]
        generate_image(input_file, f"{base}.png", 'png')
    else:
        print(f"未知命令: {cmd}")

if __name__ == "__main__":
    main()
