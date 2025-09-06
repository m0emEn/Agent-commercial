import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  Brain, 
  Menu, 
  X,
  Bell,
  User,
  Settings,
  LogOut,
  TrendingUp,
  Target,
  Clock,
  CheckCircle
} from 'lucide-react'

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  const navigation = [
    { name: 'Recommendations', href: '/', icon: Brain },
  ]

  const stats = [
    { label: 'Vie', value: '30,951', icon: CheckCircle, color: 'text-green-600', category: 'Branch Count' },
    { label: 'Automobile', value: '7,089', icon: Clock, color: 'text-blue-600', category: 'Branch Count' },
    { label: 'Risques Divers', value: '5,333', icon: Target, color: 'text-purple-600', category: 'Branch Count' },
    { label: 'Incendie', value: '1,837', icon: TrendingUp, color: 'text-red-600', category: 'Branch Count' },
    { label: 'Transport', value: '83', icon: CheckCircle, color: 'text-indigo-600', category: 'Branch Count' },
    { label: 'Groupe-Maladie', value: '71', icon: Target, color: 'text-pink-600', category: 'Branch Count' },
    { label: 'Engineering', value: '57', icon: TrendingUp, color: 'text-gray-600', category: 'Branch Count' },
    { label: 'Active', value: '22,065', icon: CheckCircle, color: 'text-green-600', category: 'Contract Status' },
    { label: 'Expired', value: '57,308', icon: Clock, color: 'text-gray-500', category: 'Contract Status' },
    { label: 'Resiliated', value: '13,595', icon: Target, color: 'text-red-600', category: 'Contract Status' },
    { label: 'Suspended', value: '10', icon: CheckCircle, color: 'text-amber-600', category: 'Contract Status' },
    { label: 'Reduced', value: '2', icon: TrendingUp, color: 'text-orange-600', category: 'Contract Status' },
    { label: 'En Instance/Devise', value: '1', icon: Clock, color: 'text-yellow-600', category: 'Contract Status' },
  ]

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/'
    }
    return location.pathname.startsWith(path)
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="absolute inset-0 bg-gray-600 opacity-75"></div>
        </div>
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <div className="flex items-center">
            <img src='https://bh-assurance.com/assets/images/favicon.ico' className='w-7 h-7'/>
            <span className="ml-3 text-xl font-semibold text-gray-900">BH Assurance</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex flex-col h-full">
          {/* Navigation */}
          <nav className="mt-8 px-4">
            <div className="space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                      isActive(item.href)
                        ? 'text-white border-r-2' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    style={isActive(item.href) ? {backgroundColor: '#DF2C27'} : {}}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className="w-5 h-5 mr-3" />
                    {item.name}
                  </Link>
                )
              })}
            </div>
          </nav>

          {/* Stats Card */}
          <div className="px-4 mt-8 flex-1 flex flex-col">
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 flex-1">
              <h3 className="text-sm font-semibold text-gray-900 mb-4">Quick Stats</h3>
              <div className="space-y-6 overflow-y-auto">
                {['Branch Count', 'Contract Status'].map((category) => (
                  <div key={category}>
                    <h4 className="text-xs font-medium text-gray-700 mb-2">{category}</h4>
                    <div className="space-y-3">
                      {stats.filter(stat => stat.category === category).map((stat, index) => {
                        const Icon = stat.icon
                        return (
                          <div key={index} className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="p-1">
                                <Icon className={`w-4 h-4 ${stat.color}`} />
                              </div>
                              <span className="text-xs text-gray-600">{stat.label}</span>
                            </div>
                            <span className="text-sm font-semibold text-gray-900">{stat.value}</span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="p-4 border-t border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-gray-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">Agent Name</p>
                  <p className="text-xs text-gray-500 truncate">agent@bhassurance.com</p>
                </div>
                <div className="flex space-x-1">
                  <button className="p-1 text-gray-400 hover:text-gray-600">
                    <Settings className="w-4 h-4" />
                  </button>
                  <button className="p-1 text-gray-400 hover:text-gray-600">
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between h-16 px-6">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-600"
            >
              <Menu className="w-6 h-6" />
            </button>

            <div className="flex-1 lg:ml-0 ml-4">
              <h1 className="text-2xl font-semibold text-gray-900">
                {navigation.find(item => isActive(item.href))?.name || 'BH Assurance'}
              </h1>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full flex items-center justify-center" style={{backgroundColor: '#DF2C27'}}>
                  <span className="text-white text-sm font-medium">AN</span>
                </div>
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-gray-900">Agent Name</p>
                  <p className="text-xs text-gray-500">Online</p>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout