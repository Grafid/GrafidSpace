import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  Button, 
  Select, 
  Input, 
  Textarea 
} from '@/components/ui/';
import { Calendar } from '@/components/ui/calendar';
import { Check, MapPin, Clock, Phone, Mail } from 'lucide-react';

const BookingInterface = () => {
  const [step, setStep] = useState(1);
  const [serviceType, setServiceType] = useState(null);
  const [customerDetails, setCustomerDetails] = useState({
    name: '',
    email: '',
    phone: '',
    propertySize: '',
    specificNeeds: ''
  });
  const [selectedDate, setSelectedDate] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);

  // Service type options
  const serviceTypes = [
    { 
      value: 'residential', 
      label: 'Residential Organization', 
      description: 'Closets, kitchens, garages, and room decluttering'
    },
    { 
      value: 'commercial', 
      label: 'Commercial Organization', 
      description: 'Office setups, storage solutions, workflow optimization'
    },
    { 
      value: 'industrial', 
      label: 'Industrial Organization', 
      description: 'Inventory systems, shelving, space utilization'
    },
    { 
      value: 'virtual', 
      label: 'Virtual Consultation', 
      description: 'Online organizational coaching and digital layouts'
    }
  ];

  // Fetch available slots when date is selected
  useEffect(() => {
    if (selectedDate && serviceType) {
      // Simulated slot fetching
      const mockSlots = [
        '9:00 AM', '10:30 AM', '1:00 PM', '2:30 PM', '4:00 PM'
      ];
      setAvailableSlots(mockSlots);
    }
  }, [selectedDate, serviceType]);

  const renderServiceTypeSelection = () => (
    <Card className="w-full max-w-md">
      <CardHeader>Select Service Type</CardHeader>
      <CardContent>
        {serviceTypes.map((type) => (
          <Button 
            key={type.value}
            onClick={() => {
              setServiceType(type.value);
              setStep(2);
            }}
            className="w-full mb-2"
            variant={serviceType === type.value ? 'default' : 'outline'}
          >
            {type.label}
            <p className="text-xs text-muted-foreground">{type.description}</p>
          </Button>
        ))}
      </CardContent>
    </Card>
  );

  const renderCustomerDetailsForm = () => (
    <Card className="w-full max-w-md">
      <CardHeader>Your Details</CardHeader>
      <CardContent>
        <Input 
          placeholder="Full Name" 
          value={customerDetails.name}
          onChange={(e) => setCustomerDetails({
            ...customerDetails, 
            name: e.target.value
          })}
          className="mb-2"
        />
        <Input 
          placeholder="Email Address" 
          type="email"
          value={customerDetails.email}
          onChange={(e) => setCustomerDetails({
            ...customerDetails, 
            email: e.target.value
          })}
          className="mb-2"
        />
        <Input 
          placeholder="Phone Number" 
          type="tel"
          value={customerDetails.phone}
          onChange={(e) => setCustomerDetails({
            ...customerDetails, 
            phone: e.target.value
          })}
          className="mb-2"
        />
        <Select 
          placeholder="Property/Space Size"
          options={[
            { value: 'small', label: 'Small (Under 500 sq ft)' },
            { value: 'medium', label: 'Medium (500-1500 sq ft)' },
            { value: 'large', label: 'Large (Over 1500 sq ft)' }
          ]}
          onChange={(value) => setCustomerDetails({
            ...customerDetails, 
            propertySize: value
          })}
          className="mb-2"
        />
        <Textarea 
          placeholder="Specific Organizational Needs" 
          value={customerDetails.specificNeeds}
          onChange={(e) => setCustomerDetails({
            ...customerDetails, 
            specificNeeds: e.target.value
          })}
          className="mb-2"
        />
        <Button 
          onClick={() => setStep(3)}
          disabled={
            !customerDetails.name || 
            !customerDetails.email || 
            !customerDetails.phone
          }
        >
          Next: Select Appointment
        </Button>
      </CardContent>
    </Card>
  );

  const renderAppointmentSelection = () => (
    <Card className="w-full max-w-md">
      <CardHeader>Choose Appointment</CardHeader>
      <CardContent>
        <Calendar 
          mode="single"
          selected={selectedDate}
          onSelect={setSelectedDate}
          disabled={(date) => 
            date < new Date() || date > new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
          }
        />
        {selectedDate && (
          <div className="mt-4">
            <h3 className="font-bold mb-2">Available Slots</h3>
            <div className="grid grid-cols-3 gap-2">
              {availableSlots.map((slot) => (
                <Button 
                  key={slot} 
                  variant="outline"
                  onClick={() => setStep(4)}
                >
                  {slot}
                </Button>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );

  const renderConfirmation = () => (
    <Card className="w-full max-w-md text-center">
      <CardContent className="flex flex-col items-center justify-center p-6">
        <Check className="w-16 h-16 text-green-500 mb-4" />
        <h2 className="text-2xl font-bold mb-2">Booking Confirmed!</h2>
        <p className="mb-4">Your consultation is scheduled</p>
        <div className="space-y-2 text-left w-full">
          <div className="flex items-center">
            <MapPin className="mr-2" />
            {serviceType === 'virtual' ? 'Online Consultation' : 'On-site Visit'}
          </div>
          <div className="flex items-center">
            <Clock className="mr-2" />
            {selectedDate?.toLocaleDateString()} at {availableSlots[0]}
          </div>
          <div className="flex items-center">
            <Phone className="mr-2" />
            {customerDetails.phone}
          </div>
          <div className="flex items-center">
            <Mail className="mr-2" />
            {customerDetails.email}
          </div>
        </div>
        <Button className="mt-4" onClick={() => setStep(1)}>
          Book Another Consultation
        </Button>
      </CardContent>
    </Card>
  );

  const renderStep = () => {
    switch(step) {
      case 1: return renderServiceTypeSelection();
      case 2: return renderCustomerDetailsForm();
      case 3: return renderAppointmentSelection();
      case 4: return renderConfirmation();
      default: return renderServiceTypeSelection();
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      {renderStep()}
    </div>
  );
};

export default BookingInterface;
