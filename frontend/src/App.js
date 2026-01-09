import React, { useState } from 'react';

function App() {
  const [height, setHeight] = useState('');
  const [width, setWidth] = useState('');
  const [mass, setMass] = useState('');
  const [colorScore, setColorScore] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          height,
          width,
          mass,
          color_score: colorScore,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ fruit: 'Error: Failed to fetch', model: '', confidence: 0 });
    }
  };

  const containerStyle = {
    maxWidth: '500px',
    margin: '50px auto',
    padding: '30px',
    borderRadius: '10px',
    backgroundColor: '#f7f7f7',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
    fontFamily: 'Arial, sans-serif',
    textAlign: 'center'
  };

  const inputStyle = {
    width: '80%',
    padding: '10px',
    margin: '10px 0',
    borderRadius: '5px',
    border: '1px solid #ccc',
    fontSize: '16px'
  };

  const buttonStyle = {
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#28a745',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer'
  };

  return (
    <div style={containerStyle}>
      <h2>Fruit Classifier 🍎🍊🍋</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Height"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
          style={inputStyle}
          required
        />
        <input
          type="number"
          placeholder="Width"
          value={width}
          onChange={(e) => setWidth(e.target.value)}
          style={inputStyle}
          required
        />
        <input
          type="number"
          placeholder="Mass"
          value={mass}
          onChange={(e) => setMass(e.target.value)}
          style={inputStyle}
          required
        />
        <input
          type="number"
          placeholder="Color Score"
          value={colorScore}
          onChange={(e) => setColorScore(e.target.value)}
          style={inputStyle}
          step="0.01"
          required
        />
        <br />
        <button type="submit" style={buttonStyle}>Predict Fruit</button>
      </form>

      {result && (
        <div style={{ marginTop: '20px', color: '#333' }}>
          <h3>Predicted Fruit: {result.fruit}</h3>
          <p style={{ fontSize: '14px', color: '#555' }}>
            Confidence: {Math.round(result.confidence * 100)}% <br />
            This prediction was made using <strong>{result.model}</strong>.
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
