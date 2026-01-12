import pandas as pd
import os

def finalize_files_for_facts_benchmark():
    # 入力パス
    src_context = 'R06_data01 - R06_data01.csv'
    src_request = 'R06_data01_gaiyou - R06_data01_gaiyou.csv'
    
    # 1. データの読み込み
    df_context = pd.read_csv(src_context)
    df_request = pd.read_csv(src_request)

    # --- 2. context_document.csv の整形 ---
    # entity_class_name を含め、元の横持ち構造を維持して保存
    df_context.to_csv('data/context_document.csv', index=False, encoding='utf-8-sig')

    # --- 3. user_request.csv の整形（examples.csv の項目順に準拠） ---
    df_request.to_csv('data/user_request.csv', index=False, encoding='utf-8-sig')

    print("✅ クレンジング完了")
    print("- data/context_document.csv:")
    print("- data/user_request.csv:")

if __name__ == "__main__":
    finalize_files_for_facts_benchmark()