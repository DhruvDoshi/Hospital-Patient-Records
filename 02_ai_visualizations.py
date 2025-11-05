"""
AI-Assisted Visualization Creation - Task 1
============================================
This script generates comprehensive visualizations using AI-assisted techniques.

Author: Task 1 Team Member
Date: November 5, 2025
AI Tools Used: GitHub Copilot, Matplotlib, Seaborn, Plotly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set visualization styles
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 11

class AIVisualizationGenerator:
    """
    AI-Assisted Visualization Generator
    Creates comprehensive visualizations using AI prompting techniques
    """
    
    def __init__(self):
        """Load and prepare data"""
        print("="*80)
        print("AI-ASSISTED VISUALIZATION GENERATION")
        print("="*80)
        print("\n📊 Loading datasets...")
        
        self.patients = pd.read_csv('patients.csv')
        self.encounters = pd.read_csv('encounters.csv')
        self.procedures = pd.read_csv('procedures.csv')
        self.organizations = pd.read_csv('organizations.csv')
        self.payers = pd.read_csv('payers.csv')
        
        # Prepare data
        self._prepare_data()
        
        print("✓ Data loaded and prepared for visualization\n")
    
    def _prepare_data(self):
        """Prepare data for visualization"""
        # Convert dates
        self.encounters['START'] = pd.to_datetime(self.encounters['START'])
        self.encounters['STOP'] = pd.to_datetime(self.encounters['STOP'])
        self.patients['BIRTHDATE'] = pd.to_datetime(self.patients['BIRTHDATE'])
        
        # Calculate features
        today = pd.Timestamp.now()
        self.patients['AGE'] = (today - self.patients['BIRTHDATE']).dt.days / 365.25
        self.patients['AGE_GROUP'] = pd.cut(
            self.patients['AGE'], 
            bins=[0, 18, 35, 50, 65, 100],
            labels=['0-18', '19-35', '36-50', '51-65', '65+']
        )
        
        self.encounters['DURATION_HOURS'] = (
            self.encounters['STOP'] - self.encounters['START']
        ).dt.total_seconds() / 3600
        
        self.encounters['COVERAGE_RATE'] = (
            self.encounters['PAYER_COVERAGE'] / self.encounters['TOTAL_CLAIM_COST'] * 100
        ).fillna(0)
        
        self.encounters['YEAR'] = self.encounters['START'].dt.year
        self.encounters['MONTH'] = self.encounters['START'].dt.month
        self.encounters['MONTH_NAME'] = self.encounters['START'].dt.month_name()
        self.encounters['DAY_OF_WEEK'] = self.encounters['START'].dt.day_name()
        self.encounters['HOUR'] = self.encounters['START'].dt.hour
    
    def create_demographic_dashboard(self):
        """
        AI PROMPT USED: "Create a comprehensive 4-panel demographic dashboard 
        showing age distribution, gender breakdown, race distribution, and age pyramid."
        
        AI RESPONSE: Generated multi-panel demographic visualization code.
        """
        print("Creating Demographic Dashboard...")
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Patient Demographics Dashboard (AI-Generated)', 
                     fontsize=20, fontweight='bold', y=0.995)
        
        # 1. Age Distribution
        axes[0, 0].hist(self.patients['AGE'], bins=30, color='skyblue', 
                       edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(self.patients['AGE'].mean(), color='red', 
                          linestyle='--', linewidth=2, label=f"Mean: {self.patients['AGE'].mean():.1f}")
        axes[0, 0].axvline(self.patients['AGE'].median(), color='green', 
                          linestyle='--', linewidth=2, label=f"Median: {self.patients['AGE'].median():.1f}")
        axes[0, 0].set_title('Age Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Age (years)', fontsize=12)
        axes[0, 0].set_ylabel('Number of Patients', fontsize=12)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Gender Distribution (Pie Chart)
        gender_counts = self.patients['GENDER'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']
        explode = (0.05, 0.05)
        axes[0, 1].pie(gender_counts, labels=['Male', 'Female'], autopct='%1.1f%%',
                      colors=colors, explode=explode, shadow=True, startangle=90,
                      textprops={'fontsize': 12, 'fontweight': 'bold'})
        axes[0, 1].set_title('Gender Distribution', fontsize=14, fontweight='bold')
        
        # 3. Race Distribution
        race_counts = self.patients['RACE'].value_counts()
        axes[1, 0].barh(race_counts.index, race_counts.values, color='lightcoral')
        axes[1, 0].set_title('Race Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Number of Patients', fontsize=12)
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        for i, v in enumerate(race_counts.values):
            axes[1, 0].text(v, i, f' {v:,}', va='center', fontweight='bold')
        
        # 4. Age Groups by Gender (Stacked Bar)
        age_gender = pd.crosstab(self.patients['AGE_GROUP'], self.patients['GENDER'])
        age_gender.plot(kind='bar', stacked=True, ax=axes[1, 1], 
                       color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
        axes[1, 1].set_title('Age Groups by Gender', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Age Group', fontsize=12)
        axes[1, 1].set_ylabel('Number of Patients', fontsize=12)
        axes[1, 1].legend(['Male', 'Female'], title='Gender')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('demographics_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: demographics_dashboard.png\n")
        plt.close()
    
    def create_financial_dashboard(self):
        """
        AI PROMPT USED: "Create a financial analysis dashboard with 
        cost distributions, revenue trends, encounter type breakdown, and coverage analysis."
        
        AI RESPONSE: Generated comprehensive financial visualization code.
        """
        print("Creating Financial Dashboard...")
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Financial Analysis Dashboard (AI-Generated)', 
                     fontsize=20, fontweight='bold', y=0.995)
        
        # 1. Total Claim Cost Distribution
        axes[0, 0].hist(self.encounters['TOTAL_CLAIM_COST'], bins=50, 
                       color='green', alpha=0.7, edgecolor='black')
        axes[0, 0].axvline(self.encounters['TOTAL_CLAIM_COST'].mean(), 
                          color='red', linestyle='--', linewidth=2,
                          label=f"Mean: ${self.encounters['TOTAL_CLAIM_COST'].mean():.2f}")
        axes[0, 0].set_title('Claim Cost Distribution', fontsize=13, fontweight='bold')
        axes[0, 0].set_xlabel('Cost ($)', fontsize=11)
        axes[0, 0].set_ylabel('Frequency', fontsize=11)
        axes[0, 0].set_xlim(0, 10000)  # Focus on main range
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Revenue by Encounter Type
        revenue_by_type = self.encounters.groupby('ENCOUNTERCLASS')['TOTAL_CLAIM_COST'].sum().sort_values()
        axes[0, 1].barh(revenue_by_type.index, revenue_by_type.values, color='steelblue')
        axes[0, 1].set_title('Revenue by Encounter Type', fontsize=13, fontweight='bold')
        axes[0, 1].set_xlabel('Total Revenue ($)', fontsize=11)
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        for i, v in enumerate(revenue_by_type.values):
            axes[0, 1].text(v, i, f' ${v:,.0f}', va='center', fontweight='bold')
        
        # 3. Monthly Revenue Trend
        monthly_revenue = self.encounters.groupby(
            self.encounters['START'].dt.to_period('M')
        )['TOTAL_CLAIM_COST'].sum()
        axes[0, 2].plot(range(len(monthly_revenue)), monthly_revenue.values, 
                       marker='o', linewidth=2, color='darkgreen', markersize=4)
        axes[0, 2].fill_between(range(len(monthly_revenue)), monthly_revenue.values, 
                                alpha=0.3, color='green')
        axes[0, 2].set_title('Monthly Revenue Trend', fontsize=13, fontweight='bold')
        axes[0, 2].set_xlabel('Month', fontsize=11)
        axes[0, 2].set_ylabel('Revenue ($)', fontsize=11)
        axes[0, 2].grid(True, alpha=0.3)
        axes[0, 2].tick_params(axis='x', rotation=45)
        
        # 4. Insurance Coverage Rate Distribution
        axes[1, 0].hist(self.encounters['COVERAGE_RATE'].dropna(), bins=40, 
                       color='coral', edgecolor='black', alpha=0.7)
        axes[1, 0].axvline(self.encounters['COVERAGE_RATE'].mean(), 
                          color='red', linestyle='--', linewidth=2,
                          label=f"Mean: {self.encounters['COVERAGE_RATE'].mean():.1f}%")
        axes[1, 0].set_title('Insurance Coverage Rate', fontsize=13, fontweight='bold')
        axes[1, 0].set_xlabel('Coverage (%)', fontsize=11)
        axes[1, 0].set_ylabel('Frequency', fontsize=11)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Average Cost by Encounter Type
        avg_cost = self.encounters.groupby('ENCOUNTERCLASS')['TOTAL_CLAIM_COST'].mean().sort_values()
        axes[1, 1].bar(range(len(avg_cost)), avg_cost.values, color='orange', alpha=0.8)
        axes[1, 1].set_xticks(range(len(avg_cost)))
        axes[1, 1].set_xticklabels(avg_cost.index, rotation=45, ha='right')
        axes[1, 1].set_title('Average Cost by Encounter Type', fontsize=13, fontweight='bold')
        axes[1, 1].set_ylabel('Average Cost ($)', fontsize=11)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        # 6. Top 10 Most Expensive Encounters
        top_costs = self.encounters.nlargest(10, 'TOTAL_CLAIM_COST')
        axes[1, 2].barh(range(10), top_costs['TOTAL_CLAIM_COST'].values, color='crimson', alpha=0.8)
        axes[1, 2].set_yticks(range(10))
        axes[1, 2].set_yticklabels([f"#{i+1}" for i in range(10)])
        axes[1, 2].set_title('Top 10 Highest Cost Encounters', fontsize=13, fontweight='bold')
        axes[1, 2].set_xlabel('Cost ($)', fontsize=11)
        axes[1, 2].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('financial_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: financial_dashboard.png\n")
        plt.close()
    
    def create_clinical_dashboard(self):
        """
        AI PROMPT USED: "Create clinical operations dashboard showing 
        encounter volumes, procedure frequencies, diagnosis patterns, and duration analysis."
        
        AI RESPONSE: Generated clinical operations visualization code.
        """
        print("Creating Clinical Operations Dashboard...")
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Clinical Operations Dashboard (AI-Generated)', 
                     fontsize=20, fontweight='bold', y=0.995)
        
        # 1. Encounter Volume by Type
        encounter_counts = self.encounters['ENCOUNTERCLASS'].value_counts()
        axes[0, 0].pie(encounter_counts, labels=encounter_counts.index, autopct='%1.1f%%',
                      startangle=90, textprops={'fontsize': 10})
        axes[0, 0].set_title('Encounter Volume by Type', fontsize=14, fontweight='bold')
        
        # 2. Top 15 Most Common Procedures
        top_procedures = self.procedures['DESCRIPTION'].value_counts().head(15)
        axes[0, 1].barh(range(15), top_procedures.values, color='mediumseagreen')
        axes[0, 1].set_yticks(range(15))
        axes[0, 1].set_yticklabels([desc[:40] for desc in top_procedures.index], fontsize=9)
        axes[0, 1].set_title('Top 15 Most Common Procedures', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Frequency', fontsize=11)
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        axes[0, 1].invert_yaxis()
        
        # 3. Encounter Duration Distribution
        axes[1, 0].hist(self.encounters['DURATION_HOURS'].clip(upper=24), bins=50, 
                       color='purple', alpha=0.7, edgecolor='black')
        axes[1, 0].axvline(self.encounters['DURATION_HOURS'].mean(), 
                          color='red', linestyle='--', linewidth=2,
                          label=f"Mean: {self.encounters['DURATION_HOURS'].mean():.2f} hrs")
        axes[1, 0].set_title('Encounter Duration Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Duration (hours)', fontsize=11)
        axes[1, 0].set_ylabel('Frequency', fontsize=11)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Top 10 Encounter Descriptions
        top_encounters = self.encounters['DESCRIPTION'].value_counts().head(10)
        axes[1, 1].bar(range(10), top_encounters.values, color='darkorange', alpha=0.8)
        axes[1, 1].set_xticks(range(10))
        axes[1, 1].set_xticklabels([desc[:25] + '...' for desc in top_encounters.index], 
                                   rotation=45, ha='right', fontsize=9)
        axes[1, 1].set_title('Top 10 Encounter Types', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('Frequency', fontsize=11)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('clinical_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: clinical_dashboard.png\n")
        plt.close()
    
    def create_temporal_analysis(self):
        """
        AI PROMPT USED: "Create temporal analysis visualizations showing 
        yearly trends, monthly patterns, day-of-week distribution, and hourly peaks."
        
        AI RESPONSE: Generated time-based visualization code.
        """
        print("Creating Temporal Analysis Dashboard...")
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Temporal Pattern Analysis (AI-Generated)', 
                     fontsize=20, fontweight='bold', y=0.995)
        
        # 1. Encounters by Year
        yearly = self.encounters['YEAR'].value_counts().sort_index()
        axes[0, 0].bar(yearly.index, yearly.values, color='royalblue', alpha=0.8)
        axes[0, 0].plot(yearly.index, yearly.values, color='red', marker='o', 
                       linewidth=2, markersize=8)
        axes[0, 0].set_title('Encounter Volume by Year', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Year', fontsize=11)
        axes[0, 0].set_ylabel('Number of Encounters', fontsize=11)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # 2. Encounters by Month
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly = self.encounters['MONTH_NAME'].value_counts().reindex(month_order)
        axes[0, 1].plot(range(12), monthly.values, marker='o', linewidth=3, 
                       markersize=10, color='forestgreen')
        axes[0, 1].fill_between(range(12), monthly.values, alpha=0.3, color='green')
        axes[0, 1].set_xticks(range(12))
        axes[0, 1].set_xticklabels([m[:3] for m in month_order], fontsize=10)
        axes[0, 1].set_title('Seasonal Pattern (Monthly)', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('Number of Encounters', fontsize=11)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Encounters by Day of Week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow = self.encounters['DAY_OF_WEEK'].value_counts().reindex(day_order)
        colors_dow = ['orange' if d in ['Saturday', 'Sunday'] else 'steelblue' for d in day_order]
        axes[1, 0].bar(range(7), dow.values, color=colors_dow, alpha=0.8)
        axes[1, 0].set_xticks(range(7))
        axes[1, 0].set_xticklabels([d[:3] for d in day_order], fontsize=10)
        axes[1, 0].set_title('Weekly Pattern (Day of Week)', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('Number of Encounters', fontsize=11)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        axes[1, 0].legend(['Weekday', 'Weekend'], loc='upper right')
        
        # 4. Encounters by Hour of Day
        hourly = self.encounters['HOUR'].value_counts().sort_index()
        axes[1, 1].bar(hourly.index, hourly.values, color='crimson', alpha=0.7)
        axes[1, 1].set_title('Daily Pattern (Hourly Distribution)', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Hour of Day', fontsize=11)
        axes[1, 1].set_ylabel('Number of Encounters', fontsize=11)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].set_xticks(range(0, 24, 2))
        
        plt.tight_layout()
        plt.savefig('temporal_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: temporal_dashboard.png\n")
        plt.close()
    
    def create_risk_analysis_dashboard(self):
        """
        AI PROMPT USED: "Create risk analysis dashboard showing high-cost patients, 
        high utilizers, cost distribution, and patient segmentation."
        
        AI RESPONSE: Generated risk stratification visualization code.
        """
        print("Creating Risk Analysis Dashboard...")
        
        # Calculate patient-level statistics
        patient_stats = self.encounters.groupby('PATIENT').agg({
            'Id': 'count',
            'TOTAL_CLAIM_COST': 'sum',
            'DURATION_HOURS': 'sum'
        }).rename(columns={'Id': 'ENCOUNTER_COUNT'})
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Patient Risk Analysis Dashboard (AI-Generated)', 
                     fontsize=20, fontweight='bold', y=0.995)
        
        # 1. Encounters per Patient Distribution
        axes[0, 0].hist(patient_stats['ENCOUNTER_COUNT'], bins=50, 
                       color='indianred', alpha=0.7, edgecolor='black')
        axes[0, 0].axvline(patient_stats['ENCOUNTER_COUNT'].mean(), 
                          color='blue', linestyle='--', linewidth=2,
                          label=f"Mean: {patient_stats['ENCOUNTER_COUNT'].mean():.1f}")
        axes[0, 0].set_title('Encounter Frequency per Patient', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Number of Encounters', fontsize=11)
        axes[0, 0].set_ylabel('Number of Patients', fontsize=11)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_xlim(0, 50)
        
        # 2. Total Cost per Patient Distribution
        axes[0, 1].hist(patient_stats['TOTAL_CLAIM_COST'], bins=50, 
                       color='gold', alpha=0.7, edgecolor='black')
        axes[0, 1].axvline(patient_stats['TOTAL_CLAIM_COST'].mean(), 
                          color='red', linestyle='--', linewidth=2,
                          label=f"Mean: ${patient_stats['TOTAL_CLAIM_COST'].mean():.2f}")
        axes[0, 1].set_title('Total Cost per Patient', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Total Cost ($)', fontsize=11)
        axes[0, 1].set_ylabel('Number of Patients', fontsize=11)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_xlim(0, 50000)
        
        # 3. Patient Segmentation (Scatter Plot)
        sample = patient_stats.sample(min(1000, len(patient_stats)))
        scatter = axes[1, 0].scatter(sample['ENCOUNTER_COUNT'], 
                                    sample['TOTAL_CLAIM_COST'],
                                    c=sample['TOTAL_CLAIM_COST'], 
                                    cmap='YlOrRd', alpha=0.6, s=50)
        axes[1, 0].set_title('Patient Segmentation (Cost vs Utilization)', 
                            fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Number of Encounters', fontsize=11)
        axes[1, 0].set_ylabel('Total Cost ($)', fontsize=11)
        axes[1, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[1, 0], label='Total Cost ($)')
        
        # 4. High-Risk Patient Categories
        categories = {
            'Low Risk\n(<5 encounters)': len(patient_stats[patient_stats['ENCOUNTER_COUNT'] < 5]),
            'Medium Risk\n(5-10 encounters)': len(patient_stats[(patient_stats['ENCOUNTER_COUNT'] >= 5) & 
                                                                (patient_stats['ENCOUNTER_COUNT'] < 10)]),
            'High Risk\n(≥10 encounters)': len(patient_stats[patient_stats['ENCOUNTER_COUNT'] >= 10])
        }
        
        colors_risk = ['lightgreen', 'gold', 'crimson']
        axes[1, 1].pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
                      colors=colors_risk, explode=(0, 0, 0.1), shadow=True,
                      textprops={'fontsize': 11, 'fontweight': 'bold'})
        axes[1, 1].set_title('Patient Risk Stratification', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('risk_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: risk_analysis_dashboard.png\n")
        plt.close()
    
    def create_interactive_plotly_dashboard(self):
        """
        AI PROMPT USED: "Create an interactive Plotly dashboard with 
        hover information, drill-down capabilities, and responsive design."
        
        AI RESPONSE: Generated interactive Plotly visualization code.
        """
        print("Creating Interactive Plotly Dashboard...")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Monthly Revenue Trend', 'Encounter Type Distribution',
                          'Top 10 Procedures by Cost', 'Age vs Cost Analysis'),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. Monthly Revenue Trend
        monthly_revenue = self.encounters.groupby(
            self.encounters['START'].dt.to_period('M')
        )['TOTAL_CLAIM_COST'].sum().reset_index()
        monthly_revenue['START'] = monthly_revenue['START'].astype(str)
        
        fig.add_trace(
            go.Scatter(x=monthly_revenue['START'], y=monthly_revenue['TOTAL_CLAIM_COST'],
                      mode='lines+markers', name='Monthly Revenue',
                      line=dict(color='green', width=3),
                      marker=dict(size=8)),
            row=1, col=1
        )
        
        # 2. Encounter Type Distribution
        encounter_counts = self.encounters['ENCOUNTERCLASS'].value_counts()
        fig.add_trace(
            go.Bar(x=encounter_counts.index, y=encounter_counts.values,
                  name='Encounter Types',
                  marker=dict(color='steelblue')),
            row=1, col=2
        )
        
        # 3. Top 10 Procedures by Cost
        top_proc_cost = self.procedures.groupby('DESCRIPTION')['BASE_COST'].sum().nlargest(10)
        fig.add_trace(
            go.Bar(x=top_proc_cost.values, y=[desc[:40] for desc in top_proc_cost.index],
                  orientation='h', name='Top Procedures',
                  marker=dict(color='coral')),
            row=2, col=1
        )
        
        # 4. Age vs Cost (Sample)
        patient_cost = self.encounters.groupby('PATIENT')['TOTAL_CLAIM_COST'].sum()
        patient_age_cost = self.patients[['Id', 'AGE']].merge(
            patient_cost.reset_index(), left_on='Id', right_on='PATIENT'
        ).sample(min(500, len(patient_cost)))
        
        fig.add_trace(
            go.Scatter(x=patient_age_cost['AGE'], y=patient_age_cost['TOTAL_CLAIM_COST'],
                      mode='markers', name='Age vs Cost',
                      marker=dict(color='purple', size=6, opacity=0.6)),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=900,
            showlegend=False,
            title_text="Interactive Hospital Analytics Dashboard (AI-Generated)",
            title_font_size=20
        )
        
        fig.write_html('interactive_dashboard.html')
        print("✓ Saved: interactive_dashboard.html\n")

def main():
    """Main execution function"""
    print("\n🎨 Starting AI-Assisted Visualization Generation...\n")
    
    viz = AIVisualizationGenerator()
    
    viz.create_demographic_dashboard()
    viz.create_financial_dashboard()
    viz.create_clinical_dashboard()
    viz.create_temporal_analysis()
    viz.create_risk_analysis_dashboard()
    viz.create_interactive_plotly_dashboard()
    
    print("="*80)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("="*80)
    print("\nGenerated Files:")
    print("  1. demographics_dashboard.png")
    print("  2. financial_dashboard.png")
    print("  3. clinical_dashboard.png")
    print("  4. temporal_dashboard.png")
    print("  5. risk_analysis_dashboard.png")
    print("  6. interactive_dashboard.html")
    print("\nNext: Run python 03_ai_dashboard.py for consolidated dashboard")

if __name__ == "__main__":
    main()
