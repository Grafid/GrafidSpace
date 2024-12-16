import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class LeadQualificationModel:
    def __init__(self):
        self.model = None
        self.preprocessor = None
    
    def prepare_data(self, data_path):
        """
        Prepare and preprocess lead data
        
        Features to consider:
        - Demographics
        - Service type interest
        - Engagement level
        - Budget indicators
        - Property/space characteristics
        """
        df = pd.read_csv(data_path)
        
        # Define feature groups
        categorical_features = [
            'service_type', 
            'property_size', 
            'industry_type', 
            'source_channel'
        ]
        numerical_features = [
            'annual_budget', 
            'property_square_feet', 
            'previous_service_count',
            'website_engagement_score'
        ]
        
        # Preprocessing pipeline
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])
        
        # Prepare X and y
        X = df[categorical_features + numerical_features]
        y = df['is_qualified_lead']
        
        return X, y
    
    def train_model(self, X, y):
        """
        Train Random Forest classifier for lead qualification
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Full pipeline with preprocessing and model
        self.model = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=100, 
                random_state=42
            ))
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        
        return self.model
    
    def predict_lead_quality(self, lead_data):
        """
        Predict lead qualification probability
        
        Args:
            lead_data (dict): Lead information dictionary
        
        Returns:
            float: Probability of being a qualified lead
        """
        if not self.model:
            raise ValueError("Model not trained. Call train_model first.")
        
        # Convert lead data to DataFrame
        lead_df = pd.DataFrame([lead_data])
        
        # Predict probability
        lead_probability = self.model.predict_proba(lead_df)[:, 1]
        
        return lead_probability[0]
    
    def generate_lead_insights(self, lead_data):
        """
        Generate actionable insights for each lead
        """
        probability = self.predict_lead_quality(lead_data)
        
        insights = {
            'qualification_score': probability,
            'recommended_action': self._determine_action(probability),
            'potential_service_match': self._match_service_type(lead_data)
        }
        
        return insights
    
    def _determine_action(self, probability):
        """
        Determine follow-up action based on lead probability
        """
        if probability > 0.8:
            return 'Immediate Personal Outreach'
        elif probability > 0.5:
            return 'Nurture with Targeted Content'
        else:
            return 'Low Priority / Monitoring'
    
    def _match_service_type(self, lead_data):
        """
        Recommend most suitable service type
        """
        service_mapping = {
            'small_residential': 'Closet & Room Optimization',
            'medium_commercial': 'Office Workflow Solutions',
            'large_industrial': 'Comprehensive Inventory Management'
        }
        
        # Logic to map lead characteristics to service type
        return service_mapping.get(
            f"{lead_data.get('property_size', 'unknown')}_{lead_data.get('service_type', 'unknown')}", 
            'Custom Consultation'
        )

def main():
    # Example usage
    model = LeadQualificationModel()
    
    # Prepare and train on historical data
    X, y = model.prepare_data('lead_historical_data.csv')
    model.train_model(X, y)
    
    # Example lead evaluation
    new_lead = {
        'service_type': 'residential',
        'property_size': 'medium',
        'annual_budget': 5000,
        'property_square_feet': 1200,
        'source_channel': 'social_media'
    }
    
    insights = model.generate_lead_insights(new_lead)
    print(insights)

if __name__ == "__main__":
    main()
