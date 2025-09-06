import React, { useState } from 'react';
import { Eye, Edit } from 'lucide-react';
import { Typewriter } from 'react-simple-typewriter';
import Modal from "./Modal";

const Client = ({ rec }) => {
  const [showTypewriter, setShowTypewriter] = useState(false);
  const [showContact, setShowContact] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [pitch, setPitch] = useState("");
  const [loading, setLoading] = useState(false);
  rec.NOM_PRENOM = rec.TYPE_PERSONNE === 'MORALE' ? rec.RAISON_SOCIALE : rec.NOM_PRENOM;

  // Fetch pitch from backend
  const generatePitch = async (data) => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/generate_pitch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const result = await response.json();
      return result.pitch;
    } catch (err) {
      console.error("Failed to generate pitch:", err);
      return "Failed to generate pitch.";
    }finally{
      setLoading(false);

    }
  };

  const handleGenerate = async () => {
    const data = {
      client_id: rec.REF_PERSONNE,
      age: Number(rec.AGE),
      job:rec.TYPE_PERSONNE === "MORALE" ? rec.LIB_SECTEUR_ACTIVITE
        : rec.LIB_PROFESSION,
      type:rec.TYPE_PERSONNE,
      recommended_products: rec.LIB_PRODUIT,
    };
    const generated = await generatePitch(data);
  generated.replace(/\*\*/g, "");   
   
    setPitch(generated);
    setShowTypewriter(true);
    setShowContact(true);
  };

  

  return (
    <div key={rec.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start space-x-4">
        <div className="flex-1 min-w-0">
          {/* Client Info */}
          <div className="flex items-start justify-between mb-3">
            <div>
            <p className="text-sm text-gray-500">ID:{rec.clientId}</p>
              <h3 className="text-lg font-semibold text-gray-900">
                {rec.TYPE_PERSONNE === "MORALE" ? rec.RAISON_SOCIALE : rec.NOM_PRENOM}
              </h3>
              <p className="text-sm text-gray-500">
                {rec.TYPE_PERSONNE === "MORALE" ? rec.LIB_SECTEUR_ACTIVITE : rec.LIB_PROFESSION} • {rec.clientPhone}
              </p>
            </div>
          </div>

          {/* Recommendations */}
          <div className="mb-4">
            <h4 className="text-xl font-bold text-gray-900 mb-2">Top Recommandations</h4>
            <ol className="list-decimal ml-6">
              {rec.LIB_PRODUIT.map((prod, index) => (
                <li key={index}>{prod}</li>
              ))}
            </ol>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between">
            <div className="flex space-x-3">
              <button
                className="inline-flex items-center cursor-pointer px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100"
                onClick={handleGenerate}
              >
                <Eye className="w-4 h-4 mr-1" />
                Generate Pitch
              </button>
              
            </div>

            {showContact && (
              <button
                className="px-4 cursor-pointer py-2 bg-blue-500 text-white rounded-lg"
                onClick={() => setShowModal(true)}
              >
                Contact Now
              </button>
            )}
          </div>

          {/* Pitch Display */}
          <div className="mt-4">
            <div  id={`pitch-${rec.clientId}`} className=" rounded bg-gray-50">
            {loading && (
              <div className="flex space-x-1 items-center p-4 rounded bg-gray-50">
                  <span className="w-4 h-4 rounded-full animate-pulse" style={{backgroundColor: '#DF2C27'}}></span>

              </div>
            )}
              {showTypewriter && <Typewriter words={[pitch]} loop={1} typeSpeed={10} />}
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      <Modal
        isOpen={showModal}
        generatedPitch={pitch}
        onClose={() => setShowModal(false)}
        client={rec}
      />
    </div>
  );
};

export default Client;
