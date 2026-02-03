import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

file_path = r'C:\Users\ASUS\Downloads\python\Account_Summary_Report_20260203135044237.csv'

df = pd.read_csv(file_path, header=None)

for idx in range(len(df)):
    if df.iloc[idx, 1] == 'Date':
        header_row = idx
        break

df = pd.read_csv(file_path, skiprows=header_row)

df.columns = df.columns.str.strip()

df_cleaned = df.dropna(how='all')

date_col = 'Date' if 'Date' in df_cleaned.columns else df_cleaned.columns[1]
withdrawal_col = None
deposit_col = None

for col in df_cleaned.columns:
    if 'Withdrawal' in col or 'withdrawal' in col:
        withdrawal_col = col
    if 'Deposit' in col or 'deposit' in col:
        deposit_col = col

df_cleaned = df_cleaned.dropna(subset=[date_col, withdrawal_col, deposit_col], how='all')

df_cleaned[withdrawal_col] = pd.to_numeric(df_cleaned[withdrawal_col], errors='coerce').fillna(0)
df_cleaned[deposit_col] = pd.to_numeric(df_cleaned[deposit_col], errors='coerce').fillna(0)

df_cleaned[date_col] = pd.to_datetime(df_cleaned[date_col], format='%d-%b-%Y', errors='coerce')

df_cleaned = df_cleaned.dropna(subset=[date_col])

df_cleaned['Month'] = df_cleaned[date_col].dt.to_period('M')
df_cleaned['Month_Str'] = df_cleaned[date_col].dt.strftime('%b-%Y')

monthly_summary = df_cleaned.groupby('Month_Str').agg({
    withdrawal_col: ['sum', 'max', 'min'],
    deposit_col: ['sum', 'max', 'min']
}).reset_index()

monthly_summary.columns = ['Month', 'Total_Withdrawal', 'Max_Withdrawal', 'Min_Withdrawal', 
                           'Total_Deposit', 'Max_Deposit', 'Min_Deposit']

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

fig = plt.figure(figsize=(18, 14))

ax1 = plt.subplot(3, 3, 1)
months = monthly_summary['Month']
x = np.arange(len(months))
width = 0.35
ax1.bar(x - width/2, monthly_summary['Total_Withdrawal'], width, label='Withdrawal', color='#e74c3c', alpha=0.8)
ax1.bar(x + width/2, monthly_summary['Total_Deposit'], width, label='Deposit', color='#2ecc71', alpha=0.8)
ax1.set_xlabel('Month', fontsize=10, fontweight='bold')
ax1.set_ylabel('Amount (₹)', fontsize=10, fontweight='bold')
ax1.set_title('Monthly Withdrawal vs Deposit', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(months, rotation=45, ha='right', fontsize=9)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

ax2 = plt.subplot(3, 3, 2)
ax2.plot(months, monthly_summary['Total_Withdrawal'], marker='o', color='#e74c3c', linewidth=2, markersize=8, label='Total Withdrawal')
ax2.fill_between(range(len(months)), monthly_summary['Total_Withdrawal'], alpha=0.3, color='#e74c3c')
ax2.set_xlabel('Month', fontsize=10, fontweight='bold')
ax2.set_ylabel('Amount (₹)', fontsize=10, fontweight='bold')
ax2.set_title('Withdrawal Trend Over Time', fontsize=12, fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)

ax3 = plt.subplot(3, 3, 3)
ax3.plot(months, monthly_summary['Total_Deposit'], marker='s', color='#2ecc71', linewidth=2, markersize=8, label='Total Deposit')
ax3.fill_between(range(len(months)), monthly_summary['Total_Deposit'], alpha=0.3, color='#2ecc71')
ax3.set_xlabel('Month', fontsize=10, fontweight='bold')
ax3.set_ylabel('Amount (₹)', fontsize=10, fontweight='bold')
ax3.set_title('Deposit Trend Over Time', fontsize=12, fontweight='bold')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)

ax4 = plt.subplot(3, 3, 4)
colors_max = plt.cm.Reds(np.linspace(0.4, 0.8, len(months)))
ax4.bar(months, monthly_summary['Max_Withdrawal'], color=colors_max, alpha=0.8)
ax4.set_xlabel('Month', fontsize=10, fontweight='bold')
ax4.set_ylabel('Amount (₹)', fontsize=10, fontweight='bold')
ax4.set_title('Maximum Withdrawal per Month', fontsize=12, fontweight='bold')
ax4.tick_params(axis='x', rotation=45)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
ax4.grid(axis='y', alpha=0.3)

ax5 = plt.subplot(3, 3, 5)
colors_max_dep = plt.cm.Greens(np.linspace(0.4, 0.8, len(months)))
ax5.bar(months, monthly_summary['Max_Deposit'], color=colors_max_dep, alpha=0.8)
ax5.set_xlabel('Month', fontsize=10, fontweight='bold')
ax5.set_ylabel('Amount (₹)', fontsize=10, fontweight='bold')
ax5.set_title('Maximum Deposit per Month', fontsize=12, fontweight='bold')
ax5.tick_params(axis='x', rotation=45)
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
ax5.grid(axis='y', alpha=0.3)

ax6 = plt.subplot(3, 3, 6)
colors_min = plt.cm.Oranges(np.linspace(0.4, 0.8, len(months)))
ax6.bar(months, monthly_summary['Min_Withdrawal'], color=colors_min, alpha=0.8)
ax6.set_xlabel('Month', fontsize=10, fontweight='bold')
ax6.set_ylabel('Amount (₹)', fontsize=10, fontweight='bold')
ax6.set_title('Minimum Withdrawal per Month', fontsize=12, fontweight='bold')
ax6.tick_params(axis='x', rotation=45)
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
ax6.grid(axis='y', alpha=0.3)

ax7 = plt.subplot(3, 3, 7)
net_balance = monthly_summary['Total_Deposit'] - monthly_summary['Total_Withdrawal']
colors_net = ['#2ecc71' if x > 0 else '#e74c3c' for x in net_balance]
ax7.bar(months, net_balance, color=colors_net, alpha=0.8)
ax7.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax7.set_xlabel('Month', fontsize=10, fontweight='bold')
ax7.set_ylabel('Net Amount (₹)', fontsize=10, fontweight='bold')
ax7.set_title('Net Balance (Deposit - Withdrawal)', fontsize=12, fontweight='bold')
ax7.tick_params(axis='x', rotation=45)
plt.setp(ax7.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
ax7.grid(axis='y', alpha=0.3)

ax8 = plt.subplot(3, 3, 8)
daily_transactions = df_cleaned.groupby(df_cleaned[date_col].dt.date).size()
ax8.hist(daily_transactions, bins=20, color='#3498db', alpha=0.7, edgecolor='black')
ax8.set_xlabel('Number of Transactions per Day', fontsize=10, fontweight='bold')
ax8.set_ylabel('Frequency', fontsize=10, fontweight='bold')
ax8.set_title('Daily Transactions Distribution', fontsize=12, fontweight='bold')
ax8.grid(axis='y', alpha=0.3)

ax9 = plt.subplot(3, 3, 9)
total_withdrawal = df_cleaned[withdrawal_col].sum()
total_deposit = df_cleaned[deposit_col].sum()
sizes = [total_withdrawal, total_deposit]
labels = [f'Expense\n₹{total_withdrawal:,.0f}', f'Income\n₹{total_deposit:,.0f}']
colors_pie = ['#e74c3c', '#2ecc71']
wedges, texts, autotexts = ax9.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', 
                                     startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax9.set_title('Total Income vs Expense', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(r'C:\Users\ASUS\Downloads\python\Account_Analysis.png', dpi=300, bbox_inches='tight')
print("✓ Chart saved as: Account_Analysis.png")
print(f"✓ File location: C:\\Users\\ASUS\\Downloads\\python\\Account_Analysis.png")
print("\n" + "="*100)
print("MONTHLY SUMMARY TABLE:")
print("="*100)
print(monthly_summary.to_string(index=False))

print("\n" + "="*100)
print("OVERALL STATISTICS:")
print("="*100)
print(f"Total Transactions: {len(df_cleaned)}")
print(f"Total Withdrawal: ₹ {total_withdrawal:,.2f}")
print(f"Total Deposit: ₹ {total_deposit:,.2f}")
print(f"Net Balance: ₹ {total_deposit - total_withdrawal:,.2f}")
print(f"Average Daily Withdrawal: ₹ {df_cleaned[withdrawal_col].mean():,.2f}")
print(f"Average Daily Deposit: ₹ {df_cleaned[deposit_col].mean():,.2f}")
print(f"Highest Single Transaction: ₹ {max(df_cleaned[withdrawal_col].max(), df_cleaned[deposit_col].max()):,.2f}")
