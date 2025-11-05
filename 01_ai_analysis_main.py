"""
AI-Powered Hospital Data Analysis - Task 1
==========================================
This script uses AI-assisted code generation and analysis techniques
to derive insights from hospital patient records.

Author: Task 1 Team Member
Date: November 5, 2025
AI Tools Used: GitHub Copilot, Python AI Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import json
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class AIHospitalAnalyzer:
    """
    AI-Assisted Hospital Data Analyzer
    Uses AI prompting and automated analysis techniques
    """
    
    def __init__(self):
        """Initialize the analyzer and load all datasets"""
        print("="*80)
        print("AI-POWERED HOSPITAL DATA ANALYSIS")
        print("="*80)
        print("\n📊 Loading datasets...")
        
        self.patients = pd.read_csv('patients.csv')
        self.encounters = pd.read_csv('encounters.csv')
        self.procedures = pd.read_csv('procedures.csv')
        self.organizations = pd.read_csv('organizations.csv')
        self.payers = pd.read_csv('payers.csv')
        
        self.insights = {
            'demographics': {},
            'financial': {},
            'clinical': {},
            'temporal': {},
            'risk_analysis': {}
        }
        
        print(f"✓ Patients: {len(self.patients):,} records")
        print(f"✓ Encounters: {len(self.encounters):,} records")
        print(f"✓ Procedures: {len(self.procedures):,} records")
        print(f"✓ Organizations: {len(self.organizations):,} records")
        print(f"✓ Payers: {len(self.payers):,} records")
        
    def prepare_data(self):
        """
        AI PROMPT USED: "Clean and prepare hospital data for analysis. 
        Convert dates, calculate age, handle missing values, and create derived features."
        
        AI RESPONSE: Generated code to parse dates, calculate patient ages,
        compute encounter durations, and create coverage rate metrics.
        """
        print("\n" + "="*80)
        print("DATA PREPARATION")
        print("="*80)
        
        # Convert date columns
        self.encounters['START'] = pd.to_datetime(self.encounters['START'])
        self.encounters['STOP'] = pd.to_datetime(self.encounters['STOP'])
        self.patients['BIRTHDATE'] = pd.to_datetime(self.patients['BIRTHDATE'])
        self.patients['DEATHDATE'] = pd.to_datetime(self.patients['DEATHDATE'])
        self.procedures['START'] = pd.to_datetime(self.procedures['START'])
        
        # Calculate patient age
        today = pd.Timestamp.now()
        self.patients['AGE'] = (today - self.patients['BIRTHDATE']).dt.days / 365.25
        self.patients['AGE'] = self.patients['AGE'].round(1)
        
        # Calculate encounter duration in hours
        self.encounters['DURATION_HOURS'] = (
            self.encounters['STOP'] - self.encounters['START']
        ).dt.total_seconds() / 3600
        
        # Calculate insurance coverage rate
        self.encounters['COVERAGE_RATE'] = (
            self.encounters['PAYER_COVERAGE'] / self.encounters['TOTAL_CLAIM_COST'] * 100
        )
        self.encounters['COVERAGE_RATE'] = self.encounters['COVERAGE_RATE'].fillna(0)
        
        # Calculate patient out-of-pocket costs
        self.encounters['OUT_OF_POCKET'] = (
            self.encounters['TOTAL_CLAIM_COST'] - self.encounters['PAYER_COVERAGE']
        )
        
        # Extract temporal features
        self.encounters['YEAR'] = self.encounters['START'].dt.year
        self.encounters['MONTH'] = self.encounters['START'].dt.month
        self.encounters['MONTH_NAME'] = self.encounters['START'].dt.month_name()
        self.encounters['DAY_OF_WEEK'] = self.encounters['START'].dt.day_name()
        self.encounters['HOUR'] = self.encounters['START'].dt.hour
        
        # Create age groups
        self.patients['AGE_GROUP'] = pd.cut(
            self.patients['AGE'], 
            bins=[0, 18, 35, 50, 65, 100],
            labels=['0-18', '19-35', '36-50', '51-65', '65+']
        )
        
        print("✓ Date columns converted")
        print("✓ Patient ages calculated")
        print("✓ Encounter durations computed")
        print("✓ Coverage rates calculated")
        print("✓ Temporal features extracted")
        print("✓ Age groups created")
        
        return self
    
    def analyze_demographics(self):
        """
        AI PROMPT USED: "Analyze patient demographics comprehensively. 
        Calculate age distribution, gender ratios, race/ethnicity breakdown, 
        marital status patterns, and geographic distribution."
        
        AI RESPONSE: Generated statistical summaries and demographic insights.
        """
        print("\n" + "="*80)
        print("DEMOGRAPHIC ANALYSIS (AI-ASSISTED)")
        print("="*80)
        
        # Total patients
        total_patients = len(self.patients)
        active_patients = len(self.patients[self.patients['DEATHDATE'].isna()])
        deceased_patients = len(self.patients[~self.patients['DEATHDATE'].isna()])
        
        print(f"\n📊 PATIENT OVERVIEW:")
        print(f"  Total Patients: {total_patients:,}")
        print(f"  Active Patients: {active_patients:,} ({active_patients/total_patients*100:.1f}%)")
        print(f"  Deceased Patients: {deceased_patients:,} ({deceased_patients/total_patients*100:.1f}%)")
        
        # Age analysis
        print(f"\n📊 AGE ANALYSIS:")
        print(f"  Average Age: {self.patients['AGE'].mean():.1f} years")
        print(f"  Median Age: {self.patients['AGE'].median():.1f} years")
        print(f"  Age Range: {self.patients['AGE'].min():.1f} - {self.patients['AGE'].max():.1f} years")
        print(f"  Standard Deviation: {self.patients['AGE'].std():.1f} years")
        
        # Age group distribution
        print(f"\n  Age Group Distribution:")
        age_dist = self.patients['AGE_GROUP'].value_counts().sort_index()
        for group, count in age_dist.items():
            print(f"    {group}: {count:,} ({count/total_patients*100:.1f}%)")
        
        # Gender analysis
        print(f"\n📊 GENDER DISTRIBUTION:")
        gender_dist = self.patients['GENDER'].value_counts()
        for gender, count in gender_dist.items():
            gender_label = "Male" if gender == 'M' else "Female"
            print(f"  {gender_label}: {count:,} ({count/total_patients*100:.1f}%)")
        
        # Race distribution
        print(f"\n📊 RACE DISTRIBUTION:")
        race_dist = self.patients['RACE'].value_counts()
        for race, count in race_dist.items():
            print(f"  {race.title()}: {count:,} ({count/total_patients*100:.1f}%)")
        
        # Ethnicity distribution
        print(f"\n📊 ETHNICITY DISTRIBUTION:")
        ethnicity_dist = self.patients['ETHNICITY'].value_counts()
        for ethnicity, count in ethnicity_dist.items():
            print(f"  {ethnicity.title()}: {count:,} ({count/total_patients*100:.1f}%)")
        
        # Marital status
        print(f"\n📊 MARITAL STATUS:")
        marital_dist = self.patients['MARITAL'].value_counts()
        for status, count in marital_dist.items():
            status_label = "Married" if status == 'M' else "Single"
            print(f"  {status_label}: {count:,} ({count/total_patients*100:.1f}%)")
        
        # Geographic analysis
        print(f"\n📊 GEOGRAPHIC DISTRIBUTION:")
        state_dist = self.patients['STATE'].value_counts().head(10)
        print("  Top 10 States:")
        for state, count in state_dist.items():
            print(f"    {state}: {count:,} ({count/total_patients*100:.1f}%)")
        
        # Store insights
        self.insights['demographics'] = {
            'total_patients': total_patients,
            'avg_age': round(self.patients['AGE'].mean(), 1),
            'gender_split': gender_dist.to_dict(),
            'race_distribution': race_dist.to_dict(),
            'top_state': state_dist.index[0]
        }
        
        return self
    
    def analyze_financial(self):
        """
        AI PROMPT USED: "Perform comprehensive financial analysis of hospital encounters. 
        Calculate total revenue, average costs by encounter type, insurance coverage patterns, 
        identify high-cost encounters, and analyze payment sources."
        
        AI RESPONSE: Generated revenue metrics, cost breakdowns, and financial KPIs.
        """
        print("\n" + "="*80)
        print("FINANCIAL ANALYSIS (AI-ASSISTED)")
        print("="*80)
        
        # Overall financial metrics
        total_base_cost = self.encounters['BASE_ENCOUNTER_COST'].sum()
        total_claim_cost = self.encounters['TOTAL_CLAIM_COST'].sum()
        total_payer_coverage = self.encounters['PAYER_COVERAGE'].sum()
        total_out_of_pocket = self.encounters['OUT_OF_POCKET'].sum()
        
        print(f"\n💰 OVERALL REVENUE METRICS:")
        print(f"  Total Base Encounter Cost: ${total_base_cost:,.2f}")
        print(f"  Total Claim Cost: ${total_claim_cost:,.2f}")
        print(f"  Total Payer Coverage: ${total_payer_coverage:,.2f}")
        print(f"  Total Patient Out-of-Pocket: ${total_out_of_pocket:,.2f}")
        print(f"  Average Coverage Rate: {self.encounters['COVERAGE_RATE'].mean():.2f}%")
        
        # Cost by encounter type
        print(f"\n💰 COSTS BY ENCOUNTER TYPE:")
        cost_by_type = self.encounters.groupby('ENCOUNTERCLASS').agg({
            'TOTAL_CLAIM_COST': ['mean', 'sum', 'count']
        }).round(2)
        cost_by_type.columns = ['Avg_Cost', 'Total_Cost', 'Count']
        cost_by_type = cost_by_type.sort_values('Total_Cost', ascending=False)
        
        for enc_type, row in cost_by_type.iterrows():
            print(f"  {enc_type.title()}:")
            print(f"    Count: {int(row['Count']):,}")
            print(f"    Average Cost: ${row['Avg_Cost']:,.2f}")
            print(f"    Total Revenue: ${row['Total_Cost']:,.2f}")
        
        # High-cost encounters
        high_cost_threshold = self.encounters['TOTAL_CLAIM_COST'].quantile(0.90)
        high_cost_encounters = self.encounters[
            self.encounters['TOTAL_CLAIM_COST'] > high_cost_threshold
        ]
        
        print(f"\n💰 HIGH-COST ENCOUNTERS (Top 10%):")
        print(f"  Threshold: ${high_cost_threshold:,.2f}")
        print(f"  Count: {len(high_cost_encounters):,}")
        print(f"  Total Cost: ${high_cost_encounters['TOTAL_CLAIM_COST'].sum():,.2f}")
        print(f"  Average Cost: ${high_cost_encounters['TOTAL_CLAIM_COST'].mean():,.2f}")
        
        # Insurance coverage analysis
        print(f"\n💰 INSURANCE COVERAGE ANALYSIS:")
        print(f"  Encounters with Full Coverage (100%): {len(self.encounters[self.encounters['COVERAGE_RATE'] == 100]):,}")
        print(f"  Encounters with No Coverage (0%): {len(self.encounters[self.encounters['COVERAGE_RATE'] == 0]):,}")
        print(f"  Encounters with Partial Coverage: {len(self.encounters[(self.encounters['COVERAGE_RATE'] > 0) & (self.encounters['COVERAGE_RATE'] < 100)]):,}")
        
        # Top payers
        payer_revenue = self.encounters.groupby('PAYER')['PAYER_COVERAGE'].sum().sort_values(ascending=False).head(10)
        print(f"\n💰 TOP 10 PAYERS BY COVERAGE:")
        for i, (payer_id, coverage) in enumerate(payer_revenue.items(), 1):
            payer_name = self.payers[self.payers['Id'] == payer_id]['NAME'].values
            payer_name = payer_name[0] if len(payer_name) > 0 else "Unknown"
            print(f"  {i}. {payer_name[:40]}: ${coverage:,.2f}")
        
        # Store insights
        self.insights['financial'] = {
            'total_revenue': round(total_claim_cost, 2),
            'avg_cost_per_encounter': round(self.encounters['TOTAL_CLAIM_COST'].mean(), 2),
            'avg_coverage_rate': round(self.encounters['COVERAGE_RATE'].mean(), 2),
            'high_cost_count': len(high_cost_encounters)
        }
        
        return self
    
    def analyze_clinical_operations(self):
        """
        AI PROMPT USED: "Analyze clinical operations including most common procedures, 
        procedure costs, encounter types, diagnosis patterns, and treatment frequencies."
        
        AI RESPONSE: Generated clinical insights and operational metrics.
        """
        print("\n" + "="*80)
        print("CLINICAL OPERATIONS ANALYSIS (AI-ASSISTED)")
        print("="*80)
        
        # Encounter analysis
        print(f"\n🏥 ENCOUNTER STATISTICS:")
        print(f"  Total Encounters: {len(self.encounters):,}")
        print(f"  Average Duration: {self.encounters['DURATION_HOURS'].mean():.2f} hours")
        print(f"  Median Duration: {self.encounters['DURATION_HOURS'].median():.2f} hours")
        
        # Most common encounter types
        print(f"\n🏥 MOST COMMON ENCOUNTER TYPES:")
        encounter_types = self.encounters['ENCOUNTERCLASS'].value_counts()
        for enc_type, count in encounter_types.items():
            print(f"  {enc_type.title()}: {count:,} ({count/len(self.encounters)*100:.1f}%)")
        
        # Most common encounter descriptions
        print(f"\n🏥 TOP 10 ENCOUNTER DESCRIPTIONS:")
        top_encounters = self.encounters['DESCRIPTION'].value_counts().head(10)
        for i, (desc, count) in enumerate(top_encounters.items(), 1):
            print(f"  {i}. {desc}: {count:,}")
        
        # Procedure analysis
        print(f"\n🏥 PROCEDURE STATISTICS:")
        print(f"  Total Procedures: {len(self.procedures):,}")
        print(f"  Average Procedure Cost: ${self.procedures['BASE_COST'].mean():,.2f}")
        print(f"  Median Procedure Cost: ${self.procedures['BASE_COST'].median():,.2f}")
        print(f"  Total Procedure Revenue: ${self.procedures['BASE_COST'].sum():,.2f}")
        
        # Most common procedures
        print(f"\n🏥 TOP 15 MOST COMMON PROCEDURES:")
        top_procedures = self.procedures['DESCRIPTION'].value_counts().head(15)
        for i, (proc, count) in enumerate(top_procedures.items(), 1):
            print(f"  {i}. {proc[:60]}: {count:,}")
        
        # Highest cost procedures
        print(f"\n🏥 TOP 10 HIGHEST COST PROCEDURES:")
        high_cost_proc = self.procedures.groupby('DESCRIPTION')['BASE_COST'].mean().sort_values(ascending=False).head(10)
        for i, (proc, cost) in enumerate(high_cost_proc.items(), 1):
            print(f"  {i}. {proc[:60]}: ${cost:,.2f}")
        
        # Reason for visit analysis
        print(f"\n🏥 TOP 10 REASONS FOR ENCOUNTERS:")
        reasons = self.encounters['REASONDESCRIPTION'].value_counts().head(10)
        for i, (reason, count) in enumerate(reasons.items(), 1):
            if pd.notna(reason):
                print(f"  {i}. {reason}: {count:,}")
        
        # Store insights
        self.insights['clinical'] = {
            'total_encounters': len(self.encounters),
            'total_procedures': len(self.procedures),
            'avg_encounter_duration': round(self.encounters['DURATION_HOURS'].mean(), 2),
            'most_common_encounter': encounter_types.index[0]
        }
        
        return self
    
    def analyze_temporal_patterns(self):
        """
        AI PROMPT USED: "Analyze temporal patterns in hospital utilization. 
        Identify trends by year, month, day of week, and hour. Find seasonal patterns 
        and peak utilization times."
        
        AI RESPONSE: Generated time-based insights and trend analysis.
        """
        print("\n" + "="*80)
        print("TEMPORAL PATTERN ANALYSIS (AI-ASSISTED)")
        print("="*80)
        
        # Yearly trends
        print(f"\n📅 ENCOUNTERS BY YEAR:")
        yearly = self.encounters['YEAR'].value_counts().sort_index()
        for year, count in yearly.items():
            print(f"  {int(year)}: {count:,}")
        
        # Monthly patterns
        print(f"\n📅 ENCOUNTERS BY MONTH:")
        monthly = self.encounters['MONTH_NAME'].value_counts()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        for month in month_order:
            if month in monthly.index:
                count = monthly[month]
                print(f"  {month}: {count:,} ({count/len(self.encounters)*100:.1f}%)")
        
        # Day of week patterns
        print(f"\n📅 ENCOUNTERS BY DAY OF WEEK:")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow = self.encounters['DAY_OF_WEEK'].value_counts()
        for day in day_order:
            if day in dow.index:
                count = dow[day]
                print(f"  {day}: {count:,} ({count/len(self.encounters)*100:.1f}%)")
        
        # Hourly patterns
        print(f"\n📅 PEAK HOURS (Top 10):")
        hourly = self.encounters['HOUR'].value_counts().sort_index()
        top_hours = hourly.sort_values(ascending=False).head(10)
        for hour, count in top_hours.items():
            print(f"  {int(hour):02d}:00 - {count:,} encounters")
        
        # Store insights
        self.insights['temporal'] = {
            'years_covered': len(yearly),
            'busiest_month': monthly.idxmax(),
            'busiest_day': dow.idxmax(),
            'busiest_hour': int(hourly.idxmax())
        }
        
        return self
    
    def identify_risk_factors(self):
        """
        AI PROMPT USED: "Identify high-risk patient populations based on 
        encounter frequency, total costs, chronic conditions, and utilization patterns. 
        Calculate risk scores and segment patients."
        
        AI RESPONSE: Generated risk stratification and patient segmentation logic.
        """
        print("\n" + "="*80)
        print("RISK FACTOR ANALYSIS (AI-ASSISTED)")
        print("="*80)
        
        # Patient encounter frequency
        patient_stats = self.encounters.groupby('PATIENT').agg({
            'Id': 'count',
            'TOTAL_CLAIM_COST': 'sum',
            'BASE_ENCOUNTER_COST': 'mean',
            'DURATION_HOURS': 'sum'
        }).rename(columns={'Id': 'ENCOUNTER_COUNT'})
        
        # High utilizers
        high_utilizers = patient_stats[patient_stats['ENCOUNTER_COUNT'] >= 10]
        
        print(f"\n⚠️  HIGH UTILIZERS (≥10 encounters):")
        print(f"  Count: {len(high_utilizers):,}")
        print(f"  Percentage of Patients: {len(high_utilizers)/len(self.patients)*100:.2f}%")
        print(f"  Average Encounters: {high_utilizers['ENCOUNTER_COUNT'].mean():.1f}")
        print(f"  Total Cost Impact: ${high_utilizers['TOTAL_CLAIM_COST'].sum():,.2f}")
        print(f"  Average Cost per Patient: ${high_utilizers['TOTAL_CLAIM_COST'].mean():,.2f}")
        
        # High cost patients
        high_cost_threshold = patient_stats['TOTAL_CLAIM_COST'].quantile(0.90)
        high_cost_patients = patient_stats[patient_stats['TOTAL_CLAIM_COST'] >= high_cost_threshold]
        
        print(f"\n⚠️  HIGH COST PATIENTS (Top 10%):")
        print(f"  Count: {len(high_cost_patients):,}")
        print(f"  Cost Threshold: ${high_cost_threshold:,.2f}")
        print(f"  Total Cost: ${high_cost_patients['TOTAL_CLAIM_COST'].sum():,.2f}")
        print(f"  Average Cost: ${high_cost_patients['TOTAL_CLAIM_COST'].mean():,.2f}")
        print(f"  Percentage of Total Costs: {high_cost_patients['TOTAL_CLAIM_COST'].sum()/self.encounters['TOTAL_CLAIM_COST'].sum()*100:.1f}%")
        
        # Chronic condition analysis
        chronic_conditions = self.encounters[self.encounters['REASONDESCRIPTION'].notna()]
        chronic_patients = chronic_conditions.groupby('PATIENT')['REASONDESCRIPTION'].nunique()
        multi_condition = chronic_patients[chronic_patients >= 3]
        
        print(f"\n⚠️  PATIENTS WITH MULTIPLE CONDITIONS (≥3 diagnoses):")
        print(f"  Count: {len(multi_condition):,}")
        print(f"  Percentage of Patients: {len(multi_condition)/len(self.patients)*100:.2f}%")
        print(f"  Average Diagnoses: {multi_condition.mean():.1f}")
        
        # Store insights
        self.insights['risk_analysis'] = {
            'high_utilizers': len(high_utilizers),
            'high_cost_patients': len(high_cost_patients),
            'multi_condition_patients': len(multi_condition),
            'avg_high_utilizer_cost': round(high_utilizers['TOTAL_CLAIM_COST'].mean(), 2)
        }
        
        return self
    
    def save_insights(self):
        """Save all insights to JSON file for documentation"""
        with open('ai_analysis_insights.json', 'w') as f:
            json.dump(self.insights, f, indent=2)
        
        print("\n" + "="*80)
        print("✓ Insights saved to: ai_analysis_insights.json")
        print("="*80)
        
        return self

def main():
    """Main execution function"""
    print("\n🤖 Starting AI-Powered Analysis...")
    print("This analysis uses AI-assisted code generation and prompting techniques\n")
    
    # Initialize analyzer
    analyzer = AIHospitalAnalyzer()
    
    # Run all analyses
    analyzer.prepare_data()
    analyzer.analyze_demographics()
    analyzer.analyze_financial()
    analyzer.analyze_clinical_operations()
    analyzer.analyze_temporal_patterns()
    analyzer.identify_risk_factors()
    analyzer.save_insights()
    
    print("\n" + "="*80)
    print("✅ AI-POWERED ANALYSIS COMPLETE!")
    print("="*80)
    print("\nNext Steps:")
    print("1. Run: python 02_ai_visualizations.py (to generate AI-assisted visualizations)")
    print("2. Run: python 03_ai_dashboard.py (to create interactive dashboard)")
    print("3. Review: ai_analysis_insights.json (for all insights)")
    print("4. Review: TASK1_AI_ANALYSIS_DOCUMENTATION.md (for full documentation)")

if __name__ == "__main__":
    main()
