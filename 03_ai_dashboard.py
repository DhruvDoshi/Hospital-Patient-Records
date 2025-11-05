"""
AI-Powered Consolidated Dashboard - Task 1
===========================================
This script creates a comprehensive, all-in-one dashboard combining all insights.

Author: Task 1 Team Member
Date: November 5, 2025
AI Tools Used: GitHub Copilot, Plotly Dash
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

class AIConsolidatedDashboard:
    """
    AI-Generated Consolidated Dashboard
    Creates a single comprehensive view of all hospital analytics
    """
    
    def __init__(self):
        """Initialize and load data"""
        print("="*80)
        print("AI-POWERED CONSOLIDATED DASHBOARD")
        print("="*80)
        print("\n📊 Loading datasets...")
        
        self.patients = pd.read_csv('patients.csv')
        self.encounters = pd.read_csv('encounters.csv')
        self.procedures = pd.read_csv('procedures.csv')
        
        self._prepare_data()
        print("✓ Data loaded and prepared\n")
    
    def _prepare_data(self):
        """Prepare data for dashboard"""
        # Convert dates
        self.encounters['START'] = pd.to_datetime(self.encounters['START'])
        self.patients['BIRTHDATE'] = pd.to_datetime(self.patients['BIRTHDATE'])
        
        # Calculate features
        today = pd.Timestamp.now()
        self.patients['AGE'] = (today - self.patients['BIRTHDATE']).dt.days / 365.25
        
        self.encounters['COVERAGE_RATE'] = (
            self.encounters['PAYER_COVERAGE'] / self.encounters['TOTAL_CLAIM_COST'] * 100
        ).fillna(0)
        
        self.encounters['MONTH'] = self.encounters['START'].dt.to_period('M').astype(str)
    
    def create_master_dashboard(self):
        """
        AI PROMPT USED: "Create a comprehensive multi-panel dashboard combining 
        demographics, financials, clinical operations, temporal trends, and risk analysis 
        in one interactive view."
        
        AI RESPONSE: Generated comprehensive dashboard with 6 key visualizations.
        """
        print("Creating Master Dashboard...")
        
        # Create 3x2 subplot layout
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Patient Demographics by Age Group',
                'Monthly Revenue Trend',
                'Encounter Type Distribution', 
                'Insurance Coverage Rate',
                'Top 10 Most Common Procedures',
                'Patient Risk Segmentation'
            ),
            specs=[
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "pie"}, {"type": "histogram"}],
                [{"type": "bar"}, {"type": "pie"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.15
        )
        
        # 1. Age Group Distribution
        age_bins = pd.cut(self.patients['AGE'], bins=[0, 18, 35, 50, 65, 100],
                         labels=['0-18', '19-35', '36-50', '51-65', '65+'])
        age_counts = age_bins.value_counts().sort_index()
        
        fig.add_trace(
            go.Bar(x=age_counts.index, y=age_counts.values,
                  marker=dict(color='skyblue', line=dict(color='darkblue', width=2)),
                  name='Age Groups'),
            row=1, col=1
        )
        
        # 2. Monthly Revenue Trend
        monthly_rev = self.encounters.groupby('MONTH')['TOTAL_CLAIM_COST'].sum()
        
        fig.add_trace(
            go.Scatter(x=monthly_rev.index, y=monthly_rev.values,
                      mode='lines+markers',
                      line=dict(color='green', width=3),
                      marker=dict(size=8, color='darkgreen'),
                      name='Revenue'),
            row=1, col=2
        )
        
        # 3. Encounter Type Distribution
        encounter_counts = self.encounters['ENCOUNTERCLASS'].value_counts()
        
        fig.add_trace(
            go.Pie(labels=encounter_counts.index, values=encounter_counts.values,
                  name='Encounter Types',
                  marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])),
            row=2, col=1
        )
        
        # 4. Coverage Rate Distribution
        fig.add_trace(
            go.Histogram(x=self.encounters['COVERAGE_RATE'],
                        nbinsx=40,
                        marker=dict(color='coral', line=dict(color='darkred', width=1)),
                        name='Coverage Rate'),
            row=2, col=2
        )
        
        # 5. Top 10 Procedures
        top_proc = self.procedures['DESCRIPTION'].value_counts().head(10)
        
        fig.add_trace(
            go.Bar(y=[desc[:35] + '...' if len(desc) > 35 else desc for desc in top_proc.index],
                  x=top_proc.values,
                  orientation='h',
                  marker=dict(color='mediumseagreen'),
                  name='Procedures'),
            row=3, col=1
        )
        
        # 6. Risk Segmentation
        patient_encounters = self.encounters.groupby('PATIENT').size()
        risk_categories = {
            'Low Risk (<5)': len(patient_encounters[patient_encounters < 5]),
            'Medium Risk (5-10)': len(patient_encounters[(patient_encounters >= 5) & (patient_encounters < 10)]),
            'High Risk (≥10)': len(patient_encounters[patient_encounters >= 10])
        }
        
        fig.add_trace(
            go.Pie(labels=list(risk_categories.keys()), 
                  values=list(risk_categories.values()),
                  marker=dict(colors=['lightgreen', 'gold', 'crimson']),
                  name='Risk Levels'),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=1400,
            showlegend=False,
            title_text="Hospital Analytics - Comprehensive AI-Generated Dashboard",
            title_font_size=24,
            title_x=0.5,
            font=dict(size=11)
        )
        
        # Update axes
        fig.update_xaxes(title_text="Age Group", row=1, col=1)
        fig.update_yaxes(title_text="Number of Patients", row=1, col=1)
        
        fig.update_xaxes(title_text="Month", tickangle=45, row=1, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
        
        fig.update_xaxes(title_text="Coverage Rate (%)", row=2, col=2)
        fig.update_yaxes(title_text="Frequency", row=2, col=2)
        
        fig.update_xaxes(title_text="Number of Occurrences", row=3, col=1)
        fig.update_yaxes(title_text="Procedure", row=3, col=1)
        
        # Save dashboard
        fig.write_html('ai_consolidated_dashboard.html')
        print("✓ Saved: ai_consolidated_dashboard.html\n")
        
        return fig

def main():
    """Main execution function"""
    print("\n🎯 Creating Consolidated AI Dashboard...\n")
    
    dashboard = AIConsolidatedDashboard()
    dashboard.create_master_dashboard()
    
    print("="*80)
    print("✅ CONSOLIDATED DASHBOARD CREATED!")
    print("="*80)
    print("\nOpen 'ai_consolidated_dashboard.html' in your browser to view the dashboard.")
    print("\nAll AI-powered analysis and visualizations are complete!")

if __name__ == "__main__":
    main()
