import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './TruckView.css';

const TruckView = () => {
  const [hoveredBatch, setHoveredBatch] = useState(null);
  const { id } = useParams(); 
  const navigate = useNavigate();

  const handleTriggerAuction = async (batch) => {
    try {
      await axios.get('http://127.0.0.1:5000/api/auction/test-trigger');
      alert(`✅ Flash Auction triggered successfully for ${batch.name}! All nearby shops have been notified.`);
    } catch (error) {
      console.error("Failed to trigger auction:", error);
      alert("❌ Failed to connect to the server.");
    }
  };

  const truckDetails = {
    id: id, 
    distanceLeft: "87 km",
    daysLeft: "3 Hours",
    destination: "Durgapur Central Hub",
  };

  // Expanded database with realistic frozen/packaged food imagery and a denser grid
  const cargoBatches = [
    { id: 'FRZ-M1', name: 'Frozen Ground Beef', temp: -2, health: 'Warning', expiry: '3 Days', image: 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=200&q=80', spanRow: 2, spanCol: 2, isSpoiling: true },
    { id: 'FRZ-P1', name: 'Frozen Peas 20kg', temp: -18, health: 'Excellent', expiry: '6 Months', image: 'https://images.unsplash.com/photo-1598974542316-24e03bc29c0f?auto=format&fit=crop&w=200&q=80', spanRow: 1, spanCol: 1, isSpoiling: false },
    { id: 'FRZ-C1', name: 'Frozen Chicken Breasts', temp: 15, health: 'Critical', expiry: '1 Day', image: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=200&q=80', spanRow: 2, spanCol: 1, isSpoiling: true },
    { id: 'DRY-M2', name: 'Milk Crates (Tetra)', temp: 4, health: 'Good', expiry: '14 Days', image: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=200&q=80', spanRow: 1, spanCol: 2, isSpoiling: false },
    { id: 'DRY-E1', name: 'Egg Cartons 50x', temp: 6, health: 'Good', expiry: '20 Days', image: 'https://images.unsplash.com/photo-1506976785307-8732e854ad02?auto=format&fit=crop&w=200&q=80', spanRow: 1, spanCol: 1, isSpoiling: false },
    { id: 'FRZ-I1', name: 'Ice Cream Tubs', temp: -15, health: 'Good', expiry: '3 Months', image: 'https://images.unsplash.com/photo-1558500057-081498b4c023?auto=format&fit=crop&w=200&q=80', spanRow: 2, spanCol: 2, isSpoiling: false },
    { id: 'FRZ-F1', name: 'Frozen Salmon Fillets', temp: -18, health: 'Excellent', expiry: '4 Months', image: 'https://images.unsplash.com/photo-1485921325833-c519f76c4927?auto=format&fit=crop&w=200&q=80', spanRow: 1, spanCol: 1, isSpoiling: false },
    { id: 'PRD-A1', name: 'Apple Pallets', temp: 5, health: 'Good', expiry: '10 Days', image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6faa6?auto=format&fit=crop&w=200&q=80', spanRow: 2, spanCol: 1, isSpoiling: false },
    { id: 'PRD-T1', name: 'Tomato Crates', temp: 22, health: 'Warning', expiry: '4 Days', image: 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=200&q=80', spanRow: 1, spanCol: 2, isSpoiling: true },
    { id: 'PRD-B1', name: 'Banana Boxes', temp: 12, health: 'Good', expiry: '5 Days', image: 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?auto=format&fit=crop&w=200&q=80', spanRow: 1, spanCol: 3, isSpoiling: false },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: 'sans-serif', padding: '20px', backgroundColor: '#f1f5f9', minHeight: '100vh' }}>
      
      {/* Back Button */}
      <div style={{ width: '100%', maxWidth: '900px', marginBottom: '20px' }}>
        <button 
          onClick={() => navigate('/')} 
          style={{ padding: '10px 20px', backgroundColor: '#334155', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', color: 'white', display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          ⬅ Back to Fleet Dashboard
        </button>
      </div>

      {/* Truck Info Header */}
      <div style={{ backgroundColor: '#0f172a', color: 'white', padding: '20px 40px', borderRadius: '12px', marginBottom: '30px', textAlign: 'center', width: '100%', maxWidth: '700px', boxShadow: '0 10px 25px rgba(0,0,0,0.2)' }}>
        <h1 style={{ margin: '0 0 15px 0', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
          <span style={{ color: '#3b82f6' }}>LIVE TRACKING:</span> {truckDetails.id}
        </h1>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '16px', color: '#cbd5e1', fontWeight: 'bold' }}>
          <span>📍 {truckDetails.destination}</span>
          <span>🛣️ {truckDetails.distanceLeft} remaining</span>
          <span>⏱️ ETA: {truckDetails.daysLeft}</span>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '60px', alignItems: 'flex-start' }}>
        
        {/* The Road Background */}
        <div className="animated-road" style={{ width: '360px', height: '700px', padding: '20px', borderRadius: '16px', display: 'flex', justifyContent: 'center', overflow: 'hidden', boxShadow: 'inset 0 0 50px rgba(0,0,0,0.5)' }}>
          
          {/* The Detailed Truck Assembly */}
          <div className="truck-wrapper">
            
            {/* Cab Tires */}
            <div className="wheel w-cab-l"></div>
            <div className="wheel w-cab-r"></div>
            
            {/* Cab */}
            <div className="truck-cab">
              <div className="windshield"></div>
            </div>
            
            {/* Joint */}
            <div className="trailer-joint"></div>
            
            {/* Trailer Body */}
            <div className="truck-trailer">
              {/* Trailer Tires */}
              <div className="wheel w-mid-l"></div>
              <div className="wheel w-mid-r"></div>
              <div className="wheel w-mid-l2"></div>
              <div className="wheel w-mid-r2"></div>
              <div className="wheel w-back-l"></div>
              <div className="wheel w-back-r"></div>
              <div className="wheel w-back-l2"></div>
              <div className="wheel w-back-r2"></div>

              {/* Cargo Grid (Now 3 Columns for denser packing) */}
              <div className="cargo-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '6px', overflowY: 'auto', flex: 1, padding: '4px' }}>
                
                {cargoBatches.map((batch) => (
                  <div 
                    key={batch.id}
                    onMouseEnter={() => setHoveredBatch(batch)}
                    onMouseLeave={() => setHoveredBatch(null)}
                    style={{ 
                      gridRow: `span ${batch.spanRow}`, 
                      gridColumn: `span ${batch.spanCol}`,
                      backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.7)), url(${batch.image})`, // Added dark overlay for realism
                      backgroundSize: 'cover',
                      backgroundPosition: 'center',
                      border: batch.isSpoiling ? '3px solid #ef4444' : '2px solid #94a3b8',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      minHeight: '75px',
                      position: 'relative',
                      boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
                    }}
                  >
                    {batch.isSpoiling && <div style={{ position: 'absolute', top: -5, right: -5, backgroundColor: '#ef4444', color: 'white', padding: '4px 6px', fontSize: '10px', fontWeight: '900', borderRadius: '4px', border: '2px solid white', zIndex: 5, animation: 'pulse 1.5s infinite' }}>⚠️ ALERT</div>}
                    <div style={{ position: 'absolute', bottom: '5px', left: '5px', color: 'white', fontSize: '11px', fontWeight: 'bold', backgroundColor: 'rgba(0,0,0,0.6)', padding: '2px 6px', borderRadius: '4px' }}>
                      {batch.id}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* The Hover Information Panel */}
        <div style={{ width: '350px', backgroundColor: 'white', border: '1px solid #cbd5e1', borderRadius: '12px', padding: '25px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)' }}>
          <h3 style={{ marginTop: 0, borderBottom: '3px solid #f1f5f9', paddingBottom: '15px', color: '#1e293b', fontSize: '20px' }}>📦 IoT Batch Diagnostics</h3>
          
          {hoveredBatch ? (
            <div style={{ animation: 'fadeIn 0.2s ease-in' }}>
              <div style={{ height: '120px', width: '100%', backgroundImage: `url(${hoveredBatch.image})`, backgroundSize: 'cover', backgroundPosition: 'center', borderRadius: '8px', marginBottom: '15px' }}></div>
              
              <h2 style={{ color: hoveredBatch.isSpoiling ? '#ef4444' : '#0f172a', margin: '10px 0', fontSize: '22px' }}>{hoveredBatch.name}</h2>
              <p style={{ color: '#64748b', margin: '0 0 15px 0' }}><strong>ID:</strong> {hoveredBatch.id}</p>
              
              <div style={{ display: 'flex', alignItems: 'center', backgroundColor: '#f8fafc', padding: '15px', borderRadius: '8px', marginBottom: '15px' }}>
                <span style={{ fontSize: '32px', marginRight: '15px' }}>🌡️</span>
                <div>
                  <div style={{ fontSize: '14px', color: '#64748b', fontWeight: 'bold', textTransform: 'uppercase' }}>Sensor Temp</div>
                  <div style={{ fontSize: '28px', fontWeight: '900', color: hoveredBatch.isSpoiling ? '#ef4444' : '#10b981' }}>
                    {hoveredBatch.temp}°C
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #e2e8f0', paddingBottom: '10px', marginBottom: '10px' }}>
                <span style={{ color: '#64748b' }}>Health Status:</span>
                <span style={{ color: hoveredBatch.isSpoiling ? '#ef4444' : '#10b981', fontWeight: 'bold' }}>{hoveredBatch.health}</span>
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                <span style={{ color: '#64748b' }}>Projected Expiry:</span>
                <span style={{ fontWeight: 'bold', color: '#0f172a' }}>{hoveredBatch.expiry}</span>
              </div>

              {hoveredBatch.isSpoiling && (
                <button 
                  onClick={() => handleTriggerAuction(hoveredBatch)}
                  style={{ backgroundColor: '#ef4444', color: 'white', border: 'none', padding: '15px', width: '100%', borderRadius: '8px', fontSize: '16px', fontWeight: '900', cursor: 'pointer', transition: '0.2s', boxShadow: '0 4px 6px rgba(239, 68, 68, 0.3)' }}
                  onMouseOver={(e) => e.target.style.transform = 'scale(1.02)'}
                  onMouseOut={(e) => e.target.style.transform = 'scale(1)'}
                >
                  ⚡ TRIGGER FLASH AUCTION
                </button>
              )}
            </div>
          ) : (
            <div style={{ color: '#94a3b8', textAlign: 'center', marginTop: '60px', padding: '20px' }}>
              <span style={{ fontSize: '50px', display: 'block', marginBottom: '15px' }}>🖱️</span>
              <p style={{ fontSize: '16px', lineHeight: '1.5' }}>Hover over the cargo grid on the truck to pull live IoT sensor data for each batch.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default TruckView;