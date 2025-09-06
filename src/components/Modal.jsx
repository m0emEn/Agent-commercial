import React, { useState, useEffect } from 'react'
import { Mail, MessageCircle, X, ArrowLeft, Send, User, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import emailjs from '@emailjs/browser'

const Modal = ({ isOpen, onClose, client, generatedPitch }) => {
  const [channel, setChannel] = useState('') // 'email' or 'whatsapp'
  const [emailSubject, setEmailSubject] = useState("")
  const [emailMessage, setEmailMessage] = useState("")
  const [recipientEmail, setRecipientEmail] = useState("")
  const [isAnimating, setIsAnimating] = useState(false)
  const [isSending, setIsSending] = useState(false)

  const EMAILJS_SERVICE_ID = 'service_o3mkpws'
  const EMAILJS_TEMPLATE_ID = 'template_odhhdf8'
  const EMAILJS_PUBLIC_KEY = 'eA4Fwo5prZOw7iNwl'

  // Initialize EmailJS
  useEffect(() => {
    emailjs.init(EMAILJS_PUBLIC_KEY)
  }, [])

  // Initialize form when modal opens
  useEffect(() => {
    if (isOpen) {
      setChannel('')
      setIsAnimating(true)
      setEmailMessage(generatedPitch || "")
      setRecipientEmail(client?.email || "")
      setEmailSubject(`Insurance Opportunity - ${client?.NOM_PRENOM || 'Client'}`)
    } else {
      setIsAnimating(false)
    }
  }, [isOpen, client, generatedPitch])

  const handleSendEmail = async () => {
    if (!recipientEmail || !emailSubject || !emailMessage) {
      toast.error('Please fill in all required fields')
      return
    }

    setIsSending(true)

    try {
      const templateParams = {
        to_email: recipientEmail,
        to_name: client?.NOM_PRENOM || 'Client',
        from_name: 'BH Assurance Agent', // Replace with actual agent name
        from_email: 'agent@bhassurance.com', // Replace with actual agent email
        subject: emailSubject,
        message: emailMessage,
        client_id: client?.clientId || '',
        // Add any other template variables you need
      }

      const result = await emailjs.send(
        EMAILJS_SERVICE_ID,
        EMAILJS_TEMPLATE_ID,
        templateParams
      )

      if (result.status === 200) {
        toast.success('Email sent successfully!')
        onClose()
      } else {
        throw new Error('Email sending failed')
      }
    } catch (error) {
      console.error('EmailJS Error:', error)
      toast.error('Failed to send email. Please try again.')
    } finally {
      setIsSending(false)
    }
  }

  const handleClose = () => {
    setIsAnimating(false)
    setTimeout(() => onClose(), 150)
  }

  if (!isOpen) return null

  return (
    <div 
      className={`fixed inset-0 z-50 flex items-center justify-center p-4 transition-all duration-300 ${
        isAnimating ? 'bg-black bg-opacity-60 backdrop-blur-sm' : 'bg-black bg-opacity-0'
      }`}
      style={{
        backgroundColor: isAnimating ? 'rgba(0, 0, 0, 0.6)' : 'rgba(0, 0, 0, 0)',
        backdropFilter: isAnimating ? 'blur(4px)' : 'none'
      }}
      onClick={handleClose}
    >
      <div 
        className={`bg-white rounded-2xl w-full max-w-lg shadow-2xl relative transform transition-all duration-300 ${
          isAnimating ? 'scale-100 opacity-100 translate-y-0' : 'scale-95 opacity-0 translate-y-4'
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                {!channel ? client?.NOM_PRENOM : channel === 'email' ? 'Send Email' : 'WhatsApp Chat'}
              </h2>
              <p className="text-sm text-gray-500">{client?.clientId}</p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors duration-200"
            disabled={isSending}
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {!channel ? (
            <div className="space-y-6">
              <div className="text-center">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Choose Communication Channel</h3>
                <p className="text-gray-600">How would you like to reach out to {client?.NOM_PRENOM}?</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setChannel('email')}
                  className="group flex flex-col items-center p-6 border-2 border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 hover:shadow-md"
                >
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3 group-hover:bg-blue-200 transition-colors">
                    <Mail className="w-6 h-6 text-blue-600" />
                  </div>
                  <span className="font-medium text-gray-900">Email</span>
                  <span className="text-sm text-gray-500 mt-1">Professional outreach</span>
                </button>

                <button
                  onClick={() => setChannel('whatsapp')}
                  className="group flex flex-col items-center p-6 border-2 border-gray-200 rounded-xl hover:border-green-300 hover:bg-green-50 transition-all duration-200 hover:shadow-md"
                >
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3 group-hover:bg-green-200 transition-colors">
                    <MessageCircle className="w-6 h-6 text-green-600" />
                  </div>
                  <span className="font-medium text-gray-900">WhatsApp</span>
                  <span className="text-sm text-gray-500 mt-1">Instant messaging</span>
                </button>
              </div>
            </div>
          ) : channel === 'email' ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  To <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="email"
                    value={recipientEmail}
                    onChange={(e) => setRecipientEmail(e.target.value)}
                    placeholder="client@example.com"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200"
                    disabled={isSending}
                  />
                  <Mail className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Subject <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={emailSubject}
                  onChange={(e) => setEmailSubject(e.target.value)}
                  placeholder="Enter email subject..."
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200"
                  disabled={isSending}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message <span className="text-red-500">*</span>
                </label>
                <textarea
                  value={emailMessage}
                  onChange={(e) => setEmailMessage(e.target.value)}
                  placeholder="Enter your message..."
                  rows={8}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 resize-none"
                  disabled={isSending}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {emailMessage.length} characters
                </p>
              </div>

              <div className="flex justify-between pt-4">
                <button
                  type="button"
                  onClick={() => setChannel('')}
                  className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors duration-200"
                  disabled={isSending}
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </button>
                <button
                  type="button"
                  onClick={handleSendEmail}
                  disabled={isSending || !recipientEmail || !emailSubject || !emailMessage}
                  className="flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  {isSending ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Send Email
                    </>
                  )}
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageCircle className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">WhatsApp Chat</h3>
                <p className="text-gray-600">Start a conversation with {client?.NOM_PRENOM}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-2">Preview message:</p>
                <div className="bg-white rounded-lg p-3 border-l-4 border-green-400">
                  <p className="text-gray-800">Hello {client?.NOM_PRENOM}, I hope you're doing well! 👋</p>
                </div>
              </div>

              <a
                href={`https://wa.me/${client?.clientPhone?.replace(/\D/g, '')}?text=${encodeURIComponent(`Hello ${client?.NOM_PRENOM}, I hope you're doing well!`)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="block w-full text-center px-6 py-4 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium"
              >
                <MessageCircle className="w-5 h-5 inline mr-2" />
                Open WhatsApp Chat
              </a>

              <button
                onClick={() => setChannel('')}
                className="flex items-center justify-center w-full px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to options
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Modal