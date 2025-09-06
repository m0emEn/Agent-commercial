


// Function to load real data from CSV



// Sample clients data (fallback)


// Export clients - will use real data if loaded, otherwise sample data
export const clients = [{
  id: 1,
  name: "Ahmed Ben Ali",
  email: "ahmed.benali@email.com",
  phone: "+216 22 123 456",
  age: 35,
  gender: "Male",
  profession: "Engineer",
  familyStatus: "Married",
  location: "Tunis, Tunisia",
  status: "Active",
  joinDate: "2023-01-15",
  lastContact: "2024-01-10",
  totalContracts: 3,
  totalValue: 45000,
  monthlyPremium: 500,
  riskProfile: "Medium",
  preferredContact: "email",
  notes: "Prefers email communication, interested in life insurance"
},
{
  id: 2,
  name: "Fatma Khelil",
  email: "fatma.khelil@email.com",
  phone: "+216 98 765 432",
  age: 28,
  gender: "Female",
  profession: "Teacher",
  familyStatus: "Single",
  location: "Sfax, Tunisia",
  status: "Active",
  joinDate: "2023-03-20",
  lastContact: "2024-01-08",
  totalContracts: 2,
  totalValue: 25000,
  monthlyPremium: 300,
  riskProfile: "Low",
  preferredContact: "whatsapp",
  notes: "Very responsive via WhatsApp"
},
{
  id: 3,
  name: "Mohamed Trabelsi",
  email: "mohamed.trabelsi@email.com",
  phone: "+216 55 987 654",
  age: 42,
  gender: "Male",
  profession: "Doctor",
  familyStatus: "Married",
  location: "Sousse, Tunisia",
  status: "Active",
  joinDate: "2022-11-10",
  lastContact: "2024-01-05",
  totalContracts: 4,
  totalValue: 75000,
  monthlyPremium: 800,
  riskProfile: "Low",
  preferredContact: "phone",
  notes: "High-value client, prefers phone calls"
}
]





export const dashboardStats = {
  totalClients: clients.length,
  activeContracts: 2100,
  monthlyRevenue: 45230,
  pendingClaims: 45,
  clientGrowth: 8.2,
  contractGrowth: 12.5,
  revenueGrowth: 15.3,
  claimResolutionRate: 94.2
}

export const recentActivities = [
  {
    id: 1,
    type: "New Client",
    description: "Ahmed Ben Ali registered",
    timestamp: "2024-01-15T10:30:00Z",
    clientId: 1
  },
  {
    id: 2,
    type: "Claim Filed",
    description: "Auto accident claim filed",
    timestamp: "2024-01-15T14:20:00Z",
    clientId: 1,
    claimId: 1
  },
  {
    id: 3,
    type: "Contract Renewal",
    description: "Health insurance renewed",
    timestamp: "2024-01-14T09:15:00Z",
    clientId: 2,
    contractId: 3
  }
]

export const aiRecommendations = [
  {
    id: 1,
    clientId: 1,
    product: "Home Insurance",
    probability: 85,
    reasoning: "Client has auto and life insurance, owns property, high probability for home insurance",
    estimatedPremium: 400,
    estimatedCoverage: 150000,
    priority: "High",
    lastUpdated: "2024-01-15T10:00:00Z"
  },
  {
    id: 2,
    clientId: 2,
    product: "Travel Insurance",
    probability: 72,
    reasoning: "Young professional, travels frequently, no travel coverage",
    estimatedPremium: 150,
    estimatedCoverage: 50000,
    priority: "Medium",
    lastUpdated: "2024-01-15T10:00:00Z"
  },
  {
    id: 3,
    clientId: 3,
    product: "Disability Insurance",
    probability: 68,
    reasoning: "High-income professional, relies on income, no disability coverage",
    estimatedPremium: 500,
    estimatedCoverage: 100000,
    priority: "Medium",
    lastUpdated: "2024-01-15T10:00:00Z"
  }
]

// Helper functions
export const getClientById = (id) => {
  return clients.find(client => client.id === parseInt(id))
}



export const getRecommendationsByClientId = (clientId) => {
  return aiRecommendations.filter(rec => rec.clientId === parseInt(clientId))
}
