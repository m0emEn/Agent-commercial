import React, { useState } from 'react'
import { X, Send, Mail, MessageSquare, Phone, Paperclip, Smile } from 'lucide-react'

const CommunicationModal = ({ isOpen, onClose, client, onSend }) => {
  const [message, setMessage] = useState('')
  const [subject, setSubject] = useState('')
  const [channel, setChannel] = useState('email')
  const [attachments, setAttachments] = useState([])

  if (!isOpen) return null

  const handleSend = () => {
    const communication = {
      clientId: client.id,
      clientName: client.name,
      clientEmail: client.email,
      clientPhone: client.phone,
      channel,
      subject,
      message,
      attachments,
      sentAt: new Date().toISOString(),
      status: 'sent'
    }
    onSend(communication)
    setMessage('')
    setSubject('')
    setAttachments([])
    onClose()
  }

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files)
    setAttachments(prev => [...prev, ...files])
  }

  const removeAttachment = (index) => {
    setAttachments(prev => prev.filter((_, i) => i !== index))
  }

  const getChannelIcon = (channel) => {
    switch (channel) {
      case 'email':
        return <Mail className="w-5 h-5" />
      case 'whatsapp':
        return <MessageSquare className="w-5 h-5" />
      case 'sms':
        return <Phone className="w-5 h-5" />
      default:
        return <Mail className="w-5 h-5" />
    }
  }

  const getChannelColor = (channel) => {
    switch (channel) {
      case 'email':
        return {backgroundColor: '#DF2C27', hover: 'hover:opacity-90'}
      case 'whatsapp':
        return {backgroundColor: '#25D366', hover: 'hover:opacity-90'}
      case 'sms':
        return {backgroundColor: '#6B7280', hover: 'hover:opacity-90'}
      default:
        return {backgroundColor: '#DF2C27', hover: 'hover:opacity-90'}
    }
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" onClick={onClose}>
          <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          {/* Header */}
          <div className="bg-white px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-900">Send Message</h3>
                <p className="text-sm text-gray-500">to {client.name}</p>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white px-6 py-4">
            <div className="space-y-4">
              {/* Channel Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Communication Channel
                </label>
                <div className="flex space-x-2">
                  {[
                    { value: 'email', label: 'Email', icon: Mail },
                    { value: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
                    { value: 'sms', label: 'SMS', icon: Phone }
                  ].map((option) => {
                    const Icon = option.icon
                    return (
                      <button
                        key={option.value}
                        onClick={() => setChannel(option.value)}
                        className={`flex items-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors ${
                          channel === option.value
                            ? 'border-blue-500 bg-blue-50 text-blue-700'
                            : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <Icon className="w-4 h-4 mr-2" />
                        {option.label}
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Subject (for email) */}
              {channel === 'email' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Subject
                  </label>
                  <input
                    type="text"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter email subject..."
                  />
                </div>
              )}

              {/* Message */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message
                </label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder={`Enter your ${channel} message...`}
                />
              </div>

              {/* Attachments */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Attachments
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-4">
                  <input
                    type="file"
                    multiple
                    onChange={handleFileUpload}
                    className="hidden"
                    id="file-upload"
                  />
                  <label
                    htmlFor="file-upload"
                    className="cursor-pointer flex items-center justify-center space-x-2 text-gray-600 hover:text-gray-800"
                  >
                    <Paperclip className="w-5 h-5" />
                    <span>Click to attach files or drag and drop</span>
                  </label>
                </div>
                {attachments.length > 0 && (
                  <div className="mt-2 space-y-2">
                    {attachments.map((file, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-50 rounded-lg p-2">
                        <span className="text-sm text-gray-700">{file.name}</span>
                        <button
                          onClick={() => removeAttachment(index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Quick Templates */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quick Templates
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    'Follow-up on recent discussion',
                    'Policy renewal reminder',
                    'New product offer',
                    'Appointment scheduling'
                  ].map((template) => (
                    <button
                      key={template}
                      onClick={() => setSubject(template)}
                      className="text-left p-2 text-sm text-gray-600 bg-gray-50 rounded-lg hover:bg-gray-100"
                    >
                      {template}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-4 flex items-center justify-between">
            <div className="text-sm text-gray-500">
              {channel === 'email' && `Sending to: ${client.email}`}
              {channel === 'whatsapp' && `Sending to: ${client.phone}`}
              {channel === 'sms' && `Sending to: ${client.phone}`}
            </div>
            <div className="flex space-x-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSend}
                disabled={!message.trim()}
                className={`inline-flex items-center px-4 py-2 border border-transparent rounded-lg text-sm font-medium text-white ${getChannelColor(channel).hover} disabled:opacity-50 disabled:cursor-not-allowed`}
                style={getChannelColor(channel)}
              >
                {getChannelIcon(channel)}
                <span className="ml-2">Send {channel.charAt(0).toUpperCase() + channel.slice(1)}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CommunicationModal
