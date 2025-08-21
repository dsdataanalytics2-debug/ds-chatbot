#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Excel file structure
"""

import pandas as pd

def check_excel_structure():
    """Check the structure of medicine_data.xlsx"""
    try:
        # Read Excel file
        df = pd.read_excel('medicine_data.xlsx')
        
        print("=" * 60)
        print("📊 Excel File Structure Analysis")
        print("=" * 60)
        
        print(f"📋 Total rows: {len(df)}")
        print(f"📋 Total columns: {len(df.columns)}")
        print()
        
        print("📝 Column names:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        print()
        
        print("📄 First few rows:")
        print(df.head(3).to_string())
        print()
        
        print("🔍 Sample data for first medicine:")
        if len(df) > 0:
            first_row = df.iloc[0]
            for col in df.columns:
                value = first_row[col]
                print(f"  {col}: {value}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    check_excel_structure()
