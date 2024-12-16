def subscribe_to_campaign(self, customer: Customer, campaign_id: str) -> Dict:
        """
        Add customer to specific marketing campaign
        
        Features:
        - Tag-based segmentation
        - Campaign tracking
        - Automated email sequences
        """
        try:
            endpoint = f'{self.base_url}/campaigns/{campaign_id}/subscribers'
            payload = {
                'email': customer.email,
                'first_name': customer.name.split()[0],
                'tags': [
                    f'service_{customer.service_type}',
                    'new_lead',
                    f'source_{customer.source}'
                ]
            }
            
            response = requests.post(
                endpoint, 
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }, 
                data=json.dumps(payload)
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Marketing Tool Integration Error: {e}")
            raise IntegrationError(f"Failed to subscribe to campaign: {e}")
    
    def create_email_sequence(self, customer: Customer) -> Dict:
        """
        Generate personalized email marketing sequence
        
        Sequences based on:
        - Service type
        - Lead score
        - Customer profile
        """
        email_sequences = {
            'residential': [
                {
                    'subject': 'Transform Your Living Space',
                    'content': 'Personalized home organization tips...',
                    'delay_days': 0
                },
                {
                    'subject': 'Free Consultation Invite',
                    'content': 'Exclusive offer for home organization...',
                    'delay_days': 3
                }
            ],
            'commercial': [
                {
                    'subject': 'Optimize Your Workspace Efficiency',
                    'content': 'Strategies for better office organization...',
                    'delay_days': 0
                },
                {
                    'subject': 'Custom Office Solution Walkthrough',
                    'content': 'Tailored organizational strategies...',
                    'delay_days': 5
                }
            ]
        }
        
        try:
            endpoint = f'{self.base_url}/email_sequences'
            payload = {
                'customer_email': customer.email,
                'sequence': email_sequences.get(
                    customer.service_type, 
                    email_sequences['residential']
                )
            }
            
            response = requests.post(
                endpoint, 
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }, 
                data=json.dumps(payload)
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Email Sequence Creation Error: {e}")
            raise IntegrationError(f"Failed to create email sequence: {e}")

class OrganizationalServiceIntegrator:
    def __init__(self, crm_api_key: str, marketing_api_key: str):
        """
        Orchestrate CRM and Marketing Tool Integrations
        
        Comprehensive customer journey management
        """
        self.crm = CRMIntegration(crm_api_key)
        self.marketing = MarketingToolIntegration(marketing_api_key)
        self.lead_qualification_model = LeadQualificationModel()
    
    def process_new_lead(self, lead_data: Dict) -> Dict:
        """
        Comprehensive lead processing workflow
        
        Steps:
        1. Qualify lead
        2. Create CRM contact
        3. Initiate marketing sequence
        4. Generate actionable insights
        """
        try:
            # Qualify lead
            lead_insights = self.lead_qualification_model.generate_lead_insights(lead_data)
            
            # Create customer profile
            customer = Customer(
                name=lead_data.get('name', ''),
                email=lead_data.get('email', ''),
                phone=lead_data.get('phone', ''),
                service_type=lead_data.get('service_type', ''),
                lead_score=lead_insights['qualification_score'],
                status=lead_insights['recommended_action']
            )
            
            # Create in CRM
            crm_response = self.crm.create_customer(customer)
            
            # Marketing automation based on lead score
            if lead_insights['qualification_score'] > 0.5:
                # Subscribe to campaign
                campaign_response = self.marketing.subscribe_to_campaign(
                    customer, 
                    campaign_id='organizational_services_nurture'
                )
                
                # Create email sequence
                email_sequence = self.marketing.create_email_sequence(customer)
            
            return {
                'crm_response': crm_response,
                'lead_insights': lead_insights,
                'marketing_actions': campaign_response if 'campaign_response' in locals() else None
            }
        
        except Exception as e:
            logging.error(f"Lead Processing Error: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }

def main():
    # Example configuration (use environment variables in production)
    CRM_API_KEY = 'your_crm_api_key'
    MARKETING_API_KEY = 'your_marketing_api_key'
    
    # Initialize integrator
    integrator = OrganizationalServiceIntegrator(
        crm_api_key=CRM_API_KEY, 
        marketing_api_key=MARKETING_API_KEY
    )
    
    # Example lead processing
    new_lead = {
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'phone': '555-123-4567',
        'service_type': 'residential',
        'property_size': 'medium',
        'annual_budget': 5000
    }
    
    # Process lead
    result = integrator.process_new_lead(new_lead)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
