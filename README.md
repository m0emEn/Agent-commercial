# BH Assurance - Insurance Platform Frontend

A comprehensive React-based frontend for the BH Assurance insurance platform, providing agents with powerful tools for client management, AI-driven recommendations, and automated communication.

## 🚀 Features

### 📊 Dashboard
- **Real-time Statistics**: Client count, revenue, conversion rates, and AI recommendations
- **Interactive Charts**: Sales trends, product distribution, and performance metrics
- **Recent Activity**: Quick access to recent clients and their status
- **Quick Actions**: Direct links to key functions

### 👥 Client Management
- **Client Search & Filtering**: Advanced search by name, email, phone, or status
- **Detailed Client Profiles**: Complete client information with contract history
- **Contract Management**: View and manage all client insurance contracts
- **Communication History**: Track all interactions with clients

### 🤖 AI Recommendations
- **Personalized Suggestions**: AI-powered product recommendations based on client profiles
- **Probability Scoring**: Match probability percentages for each recommendation
- **Priority Classification**: High, medium, and low priority recommendations
- **Automated Pitch Generation**: Pre-written commercial pitches ready for customization

### 💬 Communication Tools
- **Multi-channel Messaging**: Email, WhatsApp, and SMS integration
- **Pitch Editor**: Rich text editor for customizing commercial pitches
- **Template Library**: Quick templates for common communication scenarios
- **Attachment Support**: File attachments for documents and proposals

### 📱 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Mode**: User preference support (coming soon)
- **Accessibility**: WCAG compliant design patterns
- **Performance Optimized**: Fast loading and smooth animations

## 🛠️ Technology Stack

- **React 19**: Latest React with modern hooks and features
- **Vite**: Fast build tool and development server
- **TailwindCSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Recharts**: Beautiful and responsive charts
- **Lucide React**: Modern icon library
- **React Hot Toast**: Elegant notifications
- **Date-fns**: Date manipulation library

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## 🏗️ Project Structure

```
frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Main layout with sidebar
│   │   ├── ClientForm.jsx      # Client add/edit form
│   │   ├── PitchEditor.jsx     # Pitch editing modal
│   │   └── CommunicationModal.jsx # Communication modal
│   ├── pages/
│   │   ├── Dashboard.jsx       # Main dashboard
│   │   ├── Clients.jsx         # Client listing page
│   │   ├── ClientDetails.jsx   # Individual client details
│   │   └── Recommendations.jsx # AI recommendations
│   ├── App.jsx                 # Main app component
│   ├── main.jsx               # App entry point
│   └── index.css              # Global styles
├── package.json
└── README.md
```

## 🎨 Design System

### Color Palette
- **Primary Blue**: #3B82F6 (buttons, links, active states)
- **Success Green**: #10B981 (success states, positive metrics)
- **Warning Yellow**: #F59E0B (warnings, pending states)
- **Error Red**: #EF4444 (errors, high priority)
- **Neutral Gray**: #6B7280 (text, borders, backgrounds)

### Typography
- **Font Family**: Inter (system fallbacks)
- **Headings**: Font weights 600-700
- **Body Text**: Font weight 400
- **Small Text**: Font weight 500

### Components
- **Cards**: Rounded corners (12px), subtle shadows
- **Buttons**: Rounded corners (8px), hover effects
- **Forms**: Clean inputs with focus states
- **Modals**: Backdrop blur, smooth animations

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_NAME=BH Assurance
VITE_APP_VERSION=1.0.0
```

### API Integration
The frontend is designed to work with a Flask backend. Update the API endpoints in the components to match your backend routes.

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🚀 Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy automatically on push

### Netlify
1. Connect your repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Deploy

### Traditional Hosting
1. Run `npm run build`
2. Upload the `dist` folder to your web server
3. Configure your server to serve the built files

## 🧪 Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Style
- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Add comments for complex logic
- Keep components small and focused

## 🔮 Future Enhancements

- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Bulk operations for clients
- [ ] Export functionality (PDF, Excel)
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Client segmentation
- [ ] Performance monitoring
- [ ] PWA capabilities
- [ ] Offline support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for BH Assurance**