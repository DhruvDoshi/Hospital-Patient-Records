"""
Additional Visualizations for Missing Analyses
Creates 4 new dashboards for:
1. Admissions/Readmissions over time
2. Length of Stay analysis
3. Average Cost per Visit
4. Procedures covered by Insurance
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set professional style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (20, 12)
plt.rcParams['font.size'] = 11

class AdditionalVisualizations:
    def __init__(self):
        """Initialize and load data"""
        print("Loading data...")
        self.encounters = pd.read_csv('encounters.csv')
        self.procedures = pd.read_csv('procedures.csv')
        self.patients = pd.read_csv('patients.csv')
        
        # Convert dates
        self.encounters['START'] = pd.to_datetime(self.encounters['START'])
        self.encounters['STOP'] = pd.to_datetime(self.encounters['STOP'])
        
        # Calculate duration
        self.encounters['DURATION_HOURS'] = (
            self.encounters['STOP'] - self.encounters['START']
        ).dt.total_seconds() / 3600
        self.encounters['DURATION_DAYS'] = self.encounters['DURATION_HOURS'] / 24
        
        # Extract year
        self.encounters['YEAR'] = self.encounters['START'].dt.year
        
        print(f"✓ Loaded {len(self.encounters):,} encounters")
        print(f"✓ Loaded {len(self.procedures):,} procedures")
        print(f"✓ Loaded {len(self.patients):,} patients")
    
    def create_admissions_dashboard(self):
        """Dashboard 1: Admissions and Readmissions over Time"""
        print("\n📊 Creating Admissions/Readmissions Dashboard...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        fig.suptitle('Hospital Admissions & Readmissions Analysis', 
                     fontsize=22, fontweight='bold', y=0.995)
        
        # 1. Yearly Admissions Trend
        yearly_admissions = self.encounters.groupby('YEAR').size()
        axes[0, 0].plot(yearly_admissions.index, yearly_admissions.values, 
                       marker='o', linewidth=3, markersize=10, color='#2E86AB')
        axes[0, 0].fill_between(yearly_admissions.index, yearly_admissions.values, 
                                alpha=0.3, color='#2E86AB')
        axes[0, 0].set_title('Total Admissions by Year', fontsize=16, fontweight='bold', pad=15)
        axes[0, 0].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Number of Encounters', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add value labels
        for x, y in zip(yearly_admissions.index, yearly_admissions.values):
            axes[0, 0].text(x, y, f'{y:,}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Readmission Rate Analysis
        patient_encounter_counts = self.encounters.groupby('PATIENT').size()
        readmission_data = pd.DataFrame({
            'Encounter_Count': patient_encounter_counts
        })
        readmission_data['Category'] = pd.cut(
            readmission_data['Encounter_Count'],
            bins=[0, 1, 5, 10, 20, 50, 100, 1000],
            labels=['1 visit', '2-5 visits', '6-10 visits', '11-20 visits', 
                   '21-50 visits', '51-100 visits', '100+ visits']
        )
        
        category_counts = readmission_data['Category'].value_counts().sort_index()
        colors = ['#06A77D', '#F4D35E', '#EE964B', '#F95738', '#C1121F', '#780000', '#370617']
        bars = axes[0, 1].barh(range(len(category_counts)), category_counts.values, color=colors)
        axes[0, 1].set_yticks(range(len(category_counts)))
        axes[0, 1].set_yticklabels(category_counts.index)
        axes[0, 1].set_title('Patient Readmission Distribution', fontsize=16, fontweight='bold', pad=15)
        axes[0, 1].set_xlabel('Number of Patients', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, category_counts.values)):
            axes[0, 1].text(val, i, f' {val:,} ({val/len(patient_encounter_counts)*100:.1f}%)', 
                          va='center', fontweight='bold', fontsize=10)
        
        # 3. Monthly Admission Patterns
        self.encounters['MONTH'] = self.encounters['START'].dt.month
        monthly_admissions = self.encounters.groupby('MONTH').size()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        bars = axes[1, 0].bar(range(1, 13), monthly_admissions.values, 
                             color='#A23B72', edgecolor='black', linewidth=1.5)
        axes[1, 0].set_xticks(range(1, 13))
        axes[1, 0].set_xticklabels(month_names, rotation=45)
        axes[1, 0].set_title('Admissions by Month (All Years)', fontsize=16, fontweight='bold', pad=15)
        axes[1, 0].set_xlabel('Month', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Number of Encounters', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Highlight peak month
        peak_idx = monthly_admissions.argmax()
        bars[peak_idx].set_color('#F18F01')
        
        # Add value labels
        for i, val in enumerate(monthly_admissions.values):
            axes[1, 0].text(i+1, val, f'{val:,}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Key Statistics Box
        axes[1, 1].axis('off')
        
        total_patients = len(patient_encounter_counts)
        readmitted_patients = len(patient_encounter_counts[patient_encounter_counts > 1])
        avg_encounters = patient_encounter_counts.mean()
        max_encounters = patient_encounter_counts.max()
        
        stats_text = f"""
        KEY READMISSION STATISTICS
        
        Total Unique Patients: {total_patients:,}
        
        Patients with Readmissions: {readmitted_patients:,}
        Readmission Rate: {readmitted_patients/total_patients*100:.1f}%
        
        Average Encounters/Patient: {avg_encounters:.2f}
        Maximum Encounters (1 patient): {max_encounters:,}
        
        Total Encounters (All Years): {len(self.encounters):,}
        
        Peak Year: {yearly_admissions.idxmax()} ({yearly_admissions.max():,} encounters)
        Lowest Year: {yearly_admissions.idxmin()} ({yearly_admissions.min():,} encounters)
        
        Growth Rate (2011-2021): {((yearly_admissions[2021]/yearly_admissions[2011])-1)*100:.1f}%
        """
        
        axes[1, 1].text(0.1, 0.5, stats_text, fontsize=14, family='monospace',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig('admissions_readmissions_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: admissions_readmissions_dashboard.png")
        plt.close()
    
    def create_length_of_stay_dashboard(self):
        """Dashboard 2: Length of Stay Analysis"""
        print("\n📊 Creating Length of Stay Dashboard...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        fig.suptitle('Hospital Length of Stay Analysis', 
                     fontsize=22, fontweight='bold', y=0.995)
        
        # 1. Distribution of Stay Duration (log scale for better visibility)
        axes[0, 0].hist(self.encounters['DURATION_HOURS'], bins=50, 
                       color='#5E548E', edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(self.encounters['DURATION_HOURS'].mean(), 
                          color='red', linestyle='--', linewidth=2, label='Mean')
        axes[0, 0].axvline(self.encounters['DURATION_HOURS'].median(), 
                          color='green', linestyle='--', linewidth=2, label='Median')
        axes[0, 0].set_title('Distribution of Stay Duration', fontsize=16, fontweight='bold', pad=15)
        axes[0, 0].set_xlabel('Duration (Hours)', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency', fontsize=12, fontweight='bold')
        axes[0, 0].legend(fontsize=12)
        axes[0, 0].set_yscale('log')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Average Stay by Encounter Type
        avg_by_type = self.encounters.groupby('ENCOUNTERCLASS')['DURATION_HOURS'].mean().sort_values()
        colors_type = plt.cm.Spectral(np.linspace(0, 1, len(avg_by_type)))
        bars = axes[0, 1].barh(range(len(avg_by_type)), avg_by_type.values, color=colors_type)
        axes[0, 1].set_yticks(range(len(avg_by_type)))
        axes[0, 1].set_yticklabels(avg_by_type.index)
        axes[0, 1].set_title('Average Stay Duration by Encounter Type', 
                            fontsize=16, fontweight='bold', pad=15)
        axes[0, 1].set_xlabel('Average Duration (Hours)', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, val in enumerate(avg_by_type.values):
            axes[0, 1].text(val, i, f' {val:.2f}h ({val/24:.2f}d)', 
                          va='center', fontweight='bold')
        
        # 3. Stay Duration Over Time (Yearly Trend)
        yearly_avg_duration = self.encounters.groupby('YEAR')['DURATION_HOURS'].mean()
        axes[1, 0].plot(yearly_avg_duration.index, yearly_avg_duration.values,
                       marker='o', linewidth=3, markersize=10, color='#06A77D')
        axes[1, 0].fill_between(yearly_avg_duration.index, yearly_avg_duration.values,
                                alpha=0.3, color='#06A77D')
        axes[1, 0].set_title('Average Stay Duration Trend', fontsize=16, fontweight='bold', pad=15)
        axes[1, 0].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Average Duration (Hours)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add value labels
        for x, y in zip(yearly_avg_duration.index, yearly_avg_duration.values):
            axes[1, 0].text(x, y, f'{y:.1f}h', ha='center', va='bottom', fontweight='bold')
        
        # 4. Length of Stay Statistics by Type
        axes[1, 1].axis('off')
        
        stats_by_type = self.encounters.groupby('ENCOUNTERCLASS').agg({
            'DURATION_HOURS': ['mean', 'median', 'count']
        }).round(2)
        
        stats_text = "LENGTH OF STAY BY ENCOUNTER TYPE\n\n"
        stats_text += f"{'Type':<15} {'Avg (h)':<10} {'Avg (d)':<10} {'Median (h)':<12} {'Count':<10}\n"
        stats_text += "="*70 + "\n"
        
        for encounter_type in stats_by_type.index:
            avg_h = stats_by_type.loc[encounter_type, ('DURATION_HOURS', 'mean')]
            avg_d = avg_h / 24
            median_h = stats_by_type.loc[encounter_type, ('DURATION_HOURS', 'median')]
            count = int(stats_by_type.loc[encounter_type, ('DURATION_HOURS', 'count')])
            stats_text += f"{encounter_type:<15} {avg_h:<10.2f} {avg_d:<10.2f} {median_h:<12.2f} {count:<10,}\n"
        
        overall_avg = self.encounters['DURATION_HOURS'].mean()
        overall_median = self.encounters['DURATION_HOURS'].median()
        stats_text += "="*70 + "\n"
        stats_text += f"\nOVERALL AVERAGE: {overall_avg:.2f} hours ({overall_avg/24:.2f} days)"
        stats_text += f"\nOVERALL MEDIAN: {overall_median:.2f} hours ({overall_median/24:.2f} days)"
        
        axes[1, 1].text(0.05, 0.5, stats_text, fontsize=11, family='monospace',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5),
                       verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig('length_of_stay_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: length_of_stay_dashboard.png")
        plt.close()
    
    def create_cost_per_visit_dashboard(self):
        """Dashboard 3: Average Cost per Visit"""
        print("\n📊 Creating Cost per Visit Dashboard...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        fig.suptitle('Average Cost per Visit Analysis', 
                     fontsize=22, fontweight='bold', y=0.995)
        
        # 1. Cost Distribution (log scale)
        axes[0, 0].hist(self.encounters['TOTAL_CLAIM_COST'], bins=50,
                       color='#C1121F', edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(self.encounters['TOTAL_CLAIM_COST'].mean(),
                          color='yellow', linestyle='--', linewidth=3, label='Mean')
        axes[0, 0].axvline(self.encounters['TOTAL_CLAIM_COST'].median(),
                          color='cyan', linestyle='--', linewidth=3, label='Median')
        axes[0, 0].set_title('Distribution of Visit Costs', fontsize=16, fontweight='bold', pad=15)
        axes[0, 0].set_xlabel('Cost ($)', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency (log scale)', fontsize=12, fontweight='bold')
        axes[0, 0].legend(fontsize=12)
        axes[0, 0].set_yscale('log')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Average Cost by Encounter Type
        cost_by_type = self.encounters.groupby('ENCOUNTERCLASS')['TOTAL_CLAIM_COST'].mean().sort_values()
        colors = ['#06A77D', '#F4D35E', '#EE964B', '#F95738', '#C1121F', '#780000']
        bars = axes[0, 1].barh(range(len(cost_by_type)), cost_by_type.values, color=colors)
        axes[0, 1].set_yticks(range(len(cost_by_type)))
        axes[0, 1].set_yticklabels(cost_by_type.index)
        axes[0, 1].set_title('Average Cost by Encounter Type', fontsize=16, fontweight='bold', pad=15)
        axes[0, 1].set_xlabel('Average Cost ($)', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, val in enumerate(cost_by_type.values):
            axes[0, 1].text(val, i, f' ${val:,.2f}', va='center', fontweight='bold', fontsize=11)
        
        # 3. Cost Trend Over Time
        yearly_avg_cost = self.encounters.groupby('YEAR')['TOTAL_CLAIM_COST'].mean()
        axes[1, 0].plot(yearly_avg_cost.index, yearly_avg_cost.values,
                       marker='s', linewidth=3, markersize=10, color='#F18F01')
        axes[1, 0].fill_between(yearly_avg_cost.index, yearly_avg_cost.values,
                                alpha=0.3, color='#F18F01')
        axes[1, 0].set_title('Average Cost per Visit Trend', fontsize=16, fontweight='bold', pad=15)
        axes[1, 0].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Average Cost ($)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add value labels
        for x, y in zip(yearly_avg_cost.index, yearly_avg_cost.values):
            axes[1, 0].text(x, y, f'${y:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # 4. Cost Statistics Table
        axes[1, 1].axis('off')
        
        cost_stats_by_type = self.encounters.groupby('ENCOUNTERCLASS').agg({
            'TOTAL_CLAIM_COST': ['mean', 'median', 'sum', 'count']
        }).round(2)
        
        total_cost = self.encounters['TOTAL_CLAIM_COST'].sum()
        avg_cost = self.encounters['TOTAL_CLAIM_COST'].mean()
        median_cost = self.encounters['TOTAL_CLAIM_COST'].median()
        
        stats_text = "COST STATISTICS BY ENCOUNTER TYPE\n\n"
        stats_text += f"{'Type':<15} {'Avg Cost':<15} {'Median':<15} {'Total':<15} {'%':<8}\n"
        stats_text += "="*70 + "\n"
        
        for encounter_type in cost_stats_by_type.index:
            avg = cost_stats_by_type.loc[encounter_type, ('TOTAL_CLAIM_COST', 'mean')]
            median = cost_stats_by_type.loc[encounter_type, ('TOTAL_CLAIM_COST', 'median')]
            total = cost_stats_by_type.loc[encounter_type, ('TOTAL_CLAIM_COST', 'sum')]
            pct = (total / total_cost) * 100
            stats_text += f"{encounter_type:<15} ${avg:>13,.0f} ${median:>13,.0f} ${total:>13,.0f} {pct:>6.1f}%\n"
        
        stats_text += "="*70 + "\n"
        stats_text += f"\nOVERALL STATISTICS:"
        stats_text += f"\nTotal Revenue: ${total_cost:,.2f}"
        stats_text += f"\nAverage Cost/Visit: ${avg_cost:,.2f}"
        stats_text += f"\nMedian Cost/Visit: ${median_cost:,.2f}"
        stats_text += f"\nTotal Encounters: {len(self.encounters):,}"
        
        axes[1, 1].text(0.05, 0.5, stats_text, fontsize=11, family='monospace',
                       bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5),
                       verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig('cost_per_visit_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: cost_per_visit_dashboard.png")
        plt.close()
    
    def create_insurance_coverage_dashboard(self):
        """Dashboard 4: Procedures Covered by Insurance"""
        print("\n📊 Creating Insurance Coverage Dashboard...")
        
        # Merge procedures with encounters to get coverage info
        procedures_with_coverage = self.procedures.merge(
            self.encounters[['Id', 'PAYER_COVERAGE', 'TOTAL_CLAIM_COST', 'ENCOUNTERCLASS']], 
            left_on='ENCOUNTER', 
            right_on='Id',
            how='left'
        )
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        fig.suptitle('Insurance Coverage Analysis for Procedures', 
                     fontsize=22, fontweight='bold', y=0.995)
        
        # 1. Coverage vs No Coverage Pie Chart
        total_procedures = len(procedures_with_coverage)
        covered = len(procedures_with_coverage[procedures_with_coverage['PAYER_COVERAGE'] > 0])
        not_covered = total_procedures - covered
        
        sizes = [covered, not_covered]
        labels = [f'Covered\n{covered:,}\n({covered/total_procedures*100:.1f}%)',
                 f'Not Covered\n{not_covered:,}\n({not_covered/total_procedures*100:.1f}%)']
        colors = ['#06A77D', '#C1121F']
        explode = (0.05, 0.05)
        
        axes[0, 0].pie(sizes, labels=labels, colors=colors, explode=explode,
                      autopct='', startangle=90, textprops={'fontsize': 14, 'fontweight': 'bold'})
        axes[0, 0].set_title('Procedure Insurance Coverage Overview', 
                            fontsize=16, fontweight='bold', pad=15)
        
        # 2. Coverage by Encounter Type
        coverage_by_type = procedures_with_coverage.groupby('ENCOUNTERCLASS').apply(
            lambda x: (x['PAYER_COVERAGE'] > 0).sum() / len(x) * 100
        ).sort_values()
        
        bars = axes[0, 1].barh(range(len(coverage_by_type)), coverage_by_type.values,
                              color=plt.cm.RdYlGn(coverage_by_type.values / 100))
        axes[0, 1].set_yticks(range(len(coverage_by_type)))
        axes[0, 1].set_yticklabels(coverage_by_type.index)
        axes[0, 1].set_title('Insurance Coverage Rate by Encounter Type', 
                            fontsize=16, fontweight='bold', pad=15)
        axes[0, 1].set_xlabel('Coverage Rate (%)', fontsize=12, fontweight='bold')
        axes[0, 1].set_xlim(0, 100)
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, val in enumerate(coverage_by_type.values):
            axes[0, 1].text(val, i, f' {val:.1f}%', va='center', fontweight='bold')
        
        # 3. Average Coverage Amount by Type
        avg_coverage_by_type = procedures_with_coverage.groupby('ENCOUNTERCLASS')['PAYER_COVERAGE'].mean().sort_values()
        
        bars = axes[1, 0].bar(range(len(avg_coverage_by_type)), avg_coverage_by_type.values,
                             color='#5E548E', edgecolor='black', linewidth=1.5)
        axes[1, 0].set_xticks(range(len(avg_coverage_by_type)))
        axes[1, 0].set_xticklabels(avg_coverage_by_type.index, rotation=45, ha='right')
        axes[1, 0].set_title('Average Insurance Payment per Procedure by Type', 
                            fontsize=16, fontweight='bold', pad=15)
        axes[1, 0].set_ylabel('Average Coverage ($)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        axes[1, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add value labels
        for i, val in enumerate(avg_coverage_by_type.values):
            axes[1, 0].text(i, val, f'${val:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Coverage Statistics
        axes[1, 1].axis('off')
        
        total_claim = procedures_with_coverage['TOTAL_CLAIM_COST'].sum()
        total_coverage = procedures_with_coverage['PAYER_COVERAGE'].sum()
        total_patient_cost = total_claim - total_coverage
        coverage_rate = (total_coverage / total_claim * 100) if total_claim > 0 else 0
        
        avg_coverage = procedures_with_coverage[procedures_with_coverage['PAYER_COVERAGE'] > 0]['PAYER_COVERAGE'].mean()
        
        coverage_stats = procedures_with_coverage.groupby('ENCOUNTERCLASS').agg({
            'PAYER_COVERAGE': lambda x: (x > 0).sum(),
            'ENCOUNTER': 'count'
        })
        coverage_stats['Coverage_Rate'] = (coverage_stats['PAYER_COVERAGE'] / coverage_stats['ENCOUNTER'] * 100).round(1)
        
        stats_text = "INSURANCE COVERAGE STATISTICS\n\n"
        stats_text += f"Total Procedures: {total_procedures:,}\n"
        stats_text += f"Procedures with Coverage: {covered:,} ({covered/total_procedures*100:.1f}%)\n"
        stats_text += f"Procedures without Coverage: {not_covered:,} ({not_covered/total_procedures*100:.1f}%)\n\n"
        
        stats_text += f"Total Claim Amount: ${total_claim:,.2f}\n"
        stats_text += f"Total Insurance Coverage: ${total_coverage:,.2f}\n"
        stats_text += f"Total Patient Responsibility: ${total_patient_cost:,.2f}\n"
        stats_text += f"Overall Coverage Rate: {coverage_rate:.1f}%\n\n"
        
        stats_text += f"Avg Coverage (when covered): ${avg_coverage:,.2f}\n\n"
        
        stats_text += "COVERAGE RATE BY TYPE:\n"
        stats_text += "-" * 35 + "\n"
        for encounter_type in coverage_stats.index:
            rate = coverage_stats.loc[encounter_type, 'Coverage_Rate']
            count = int(coverage_stats.loc[encounter_type, 'ENCOUNTER'])
            stats_text += f"{encounter_type:<15} {rate:>6.1f}% ({count:>6,} proc)\n"
        
        axes[1, 1].text(0.05, 0.5, stats_text, fontsize=12, family='monospace',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5),
                       verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig('insurance_coverage_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: insurance_coverage_dashboard.png")
        plt.close()
    
    def create_all_dashboards(self):
        """Create all 4 additional dashboards"""
        print("\n" + "="*80)
        print("CREATING ADDITIONAL VISUALIZATIONS")
        print("="*80)
        
        self.create_admissions_dashboard()
        self.create_length_of_stay_dashboard()
        self.create_cost_per_visit_dashboard()
        self.create_insurance_coverage_dashboard()
        
        print("\n" + "="*80)
        print("✅ ALL ADDITIONAL DASHBOARDS CREATED SUCCESSFULLY!")
        print("="*80)
        print("\n📁 Generated Files:")
        print("  1. admissions_readmissions_dashboard.png")
        print("  2. length_of_stay_dashboard.png")
        print("  3. cost_per_visit_dashboard.png")
        print("  4. insurance_coverage_dashboard.png")
        print("\n🎯 Total: 4 new dashboards with 16 charts")

if __name__ == "__main__":
    viz = AdditionalVisualizations()
    viz.create_all_dashboards()
