import pandas as pd
import os

def finalize_files_for_facts_benchmark():
    src_context = 'R06_data01 - R06_data01.csv'
    src_request = 'R06_data01_gaiyou - R06_data01_gaiyou.csv'
    src_sources = '00 - 00.csv'
    
    df_context = pd.read_csv(src_context)
    df_request = pd.read_csv(src_request)
    df_souces = pd.read_csv(src_sources)

    df_context.to_csv('data/context_document.csv', index=False, encoding='utf-8-sig')
    df_request.to_csv('data/user_request.csv', index=False, encoding='utf-8-sig')
    df_souces.to_csv('data/souces.csv', index=False, encoding='utf-8-sig')


    print("✅ クレンジング完了")
    print("- data/context_document.csv:")
    print("- data/user_request.csv:")
    print("- data/souces.csv:")

if __name__ == "__main__":
    finalize_files_for_facts_benchmark()