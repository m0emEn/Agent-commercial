import React, { useState } from 'react'
import { X, Save, Send, Mail, MessageSquare, Phone, Eye, Edit3 } from 'lucide-react'

const PitchEditor = ({ isOpen, onClose, recommendation, onSave, onSend }) => {
  const [subject, setSubject] = useState(recommendation?.pitch?.subject || '')
  const [content, setContent] = useState(recommendation?.pitch?.content || '')
  const [previewMode, setPreviewMode] = useState(false)

  if (!isOpen) return null

  const handleSave = () => {
    const updatedPitch = {
      subject,
      content,
      lastModified: new Date().toISOString()
    }
    onSave(updatedPitch)
    onClose()
  }

  const handleSend = (channel) => {
    const pitch = {
      subject,
      content,
      channel,
      sentAt: new Date().toISOString()
    }
    onSend(pitch)
    onClose()
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" onClick={onClose}>
          <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          {/* Header */}
          <div className="bg-white px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">Edit Commercial Pitch</h3>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setPreviewMode(!previewMode)}
                  className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  {previewMode ? <Edit3 className="w-4 h-4 mr-1" /> : <Eye className="w-4 h-4 mr-1" />}
                  {previewMode ? 'Edit' : 'Preview'}
                </button>
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white px-6 py-4">
            {previewMode ? (
              <div className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-gray-500 mb-2">Email Preview</h4>
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="border-b border-gray-200 pb-2 mb-4">
                      <p className="text-sm text-gray-600">To: {recommendation?.clientEmail}</p>
                      <p className="text-sm text-gray-600">Subject: {subject}</p>
                    </div>
                    <div className="whitespace-pre-wrap text-sm text-gray-800">
                      {content}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {/* Subject */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Subject Line
                  </label>
                  <input
                    type="text"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter email subject..."
                  />
                </div>

                {/* Content */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Message Content
                  </label>
                  <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    rows={12}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your message content..."
                  />
                </div>

                {/* AI Suggestions */}
                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-blue-900 mb-2">AI Suggestions</h4>
                  <div className="space-y-2 text-sm text-blue-800">
                    <p>• Personalize the opening with the client's name</p>
                    <p>• Highlight specific benefits relevant to their profile</p>
                    <p>• Include a clear call-to-action</p>
                    <p>• Mention their current coverage gaps</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-4 flex items-center justify-between">
            <div className="flex space-x-2">
              <button
                onClick={() => handleSend('email')}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-lg text-sm font-medium text-white hover:opacity-90"
                style={{backgroundColor: '#DF2C27'}}
              >
                <Mail className="w-4 h-4 mr-2" />
                Send Email
              </button>
              <button
                onClick={() => handleSend('whatsapp')}
                className="inline-flex items-center px-4 py-2 bg-green-600 border border-transparent rounded-lg text-sm font-medium text-white hover:bg-green-700"
              >
                <MessageSquare className="w-4 h-4 mr-2" />
                Send WhatsApp
              </button>
              <button
                onClick={() => handleSend('sms')}
                className="inline-flex items-center px-4 py-2 bg-gray-600 border border-transparent rounded-lg text-sm font-medium text-white hover:bg-gray-700"
              >
                <Phone className="w-4 h-4 mr-2" />
                Send SMS
              </button>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="inline-flex items-center px-4 py-2 bg-gray-600 border border-transparent rounded-lg text-sm font-medium text-white hover:bg-gray-700"
              >
                <Save className="w-4 h-4 mr-2" />
                Save Draft
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PitchEditor
