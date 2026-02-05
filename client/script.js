// API Configuration
// Use relative URLs for Vercel deployment, localhost for local development
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : '/api';

// Smooth scroll function
function scrollToPredictor() {
    document.getElementById('predictor').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Reset form function
function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('predictor').scrollIntoView({
        behavior: 'smooth'
    });
}

// Initialize application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌾 AgriPredict Application Started');

    await loadOptions();
    await loadFeatureImportance();

    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', handlePrediction);

    setDefaultValues();
});

// Load options from API
async function loadOptions() {
    try {
        const response = await fetch(`${API_BASE_URL}/options`);
        const data = await response.json();

        // Populate crop dropdown
        const cropSelect = document.getElementById('crop');
        data.crops.forEach(crop => {
            const option = document.createElement('option');
            option.value = crop;
            option.textContent = crop;
            cropSelect.appendChild(option);
        });

        // Populate soil type dropdown
        const soilSelect = document.getElementById('soil');
        data.soil_types.forEach(soilType => {
            const option = document.createElement('option');
            option.value = soilType;
            option.textContent = soilType;
            document.getElementById('soil_type').appendChild(option);
        });

        // Populate country dropdown (from the dataset)
        const countries = ['India', 'USA', 'China', 'Brazil', 'Argentina', 'Australia'];
        const countrySelect = document.getElementById('country');
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });

        console.log('✅ Options loaded successfully');
    } catch (error) {
        console.error('❌ Error loading options:', error);
        alert('Could not connect to the server. Please ensure the Flask server is running on port 5000.');
    }
}

// Load feature importance
async function loadFeatureImportance() {
    try {
        const response = await fetch(`${API_BASE_URL}/feature-importance`);
        const data = await response.json();
        displayFeatureImportance(data.features);
        console.log('✅ Feature importance loaded');
    } catch (error) {
        console.error('❌ Error loading feature importance:', error);
        document.getElementById('featureImportance').innerHTML =
            '<p class="loading-state">Unable to load feature insights</p>';
    }
}

// Display feature importance with simple explanations
function displayFeatureImportance(features) {
    const container = document.getElementById('featureImportance');

    // Feature explanations for everyone
    const explanations = {
        'Avg_Rainfall_mm': 'How much rain your crops get - more water usually means bigger harvests!',
        'Avg_Temp_C': 'The temperature affects how fast plants grow',
        'Crop': 'Different crops naturally produce different amounts',
        'Fertilizer_used': 'Plant food that helps crops grow stronger',
        'Country': 'Different regions have different growing conditions',
        'Climate_Zone': 'Whether it\'s hot, cold, or just right for your crop',
        'Season': 'When you plant makes a big difference',
        'Irrigation': 'Having water supply when needed',
        'ph_level': 'How acidic or alkaline your soil is',
        'Soil_Type': 'Different soils hold different amounts of water and nutrients'
    };

    let html = '';
    const topFeatures = features.slice(0, 6);

    topFeatures.forEach(feature => {
        const explanation = explanations[feature.name.replace(/ /g, '_')] || 'Important factor for crop growth';
        html += `
            <div class="feature-item">
                <div class="feature-header">
                    <span class="feature-name">${feature.name.replace(/_/g, ' ')}</span>
                    <span class="feature-value">${feature.rf_importance}%</span>
                </div>
                <div class="feature-bar">
                    <div class="feature-fill" style="width: ${feature.rf_importance}%"></div>
                </div>
                <p style="font-size: 14px; color: var(--grey-dark); margin-top: 8px;">
                    ${explanation}
                </p>
            </div>
        `;
    });

    container.innerHTML = html;
}

// Set sample default values
function setDefaultValues() {
    document.getElementById('crop').value = 'Rice';
    document.getElementById('temperature').value = '28';
    document.getElementById('rainfall').value = '1200';
    document.getElementById('humidity').value = '70';
    document.getElementById('ph_level').value = '6.8';
    document.getElementById('field_area').value = '5';
    document.getElementById('fertilizer_used').value = '150';
    document.getElementById('irrigation').value = '1';
}

// Handle prediction
async function handlePrediction(event) {
    event.preventDefault();

    const button = document.getElementById('predictBtn');
    const originalHtml = button.innerHTML;

    try {
        // Show loading
        button.disabled = true;
        button.innerHTML = '<span class="button-text">Analyzing your data...</span> ⏳';

        // Get form data
        const country = document.getElementById('country').value;
        const formData = {
            crop: document.getElementById('crop').value,
            soil_type: document.getElementById('soil_type').value,
            temperature: parseFloat(document.getElementById('temperature').value),
            rainfall: parseFloat(document.getElementById('rainfall').value),
            humidity: parseFloat(document.getElementById('humidity').value),
            ph_level: parseFloat(document.getElementById('ph_level').value),
            field_area: parseFloat(document.getElementById('field_area').value),
            irrigation: parseInt(document.getElementById('irrigation').value),
            fertilizer_used: parseFloat(document.getElementById('fertilizer_used').value),
            model: 'random_forest' // Use default model
        };

        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Prediction failed');

        const result = await response.json();

        // Display results with rich explanations
        displayResults(result, formData, country);

        // Scroll to results
        setTimeout(() => {
            document.getElementById('resultsSection').scrollIntoView({
                behavior: 'smooth'
            });
        }, 300);

    } catch (error) {
        console.error('❌ Prediction error:', error);
        alert('Oops! Something went wrong. Please check your internet connection and try again.');
    } finally {
        button.disabled = false;
        button.innerHTML = originalHtml;
    }
}

// Display results with rich context
function displayResults(result, formData, country) {
    const resultsSection = document.getElementById('resultsSection');
    const prediction = result.prediction;

    // Update main values
    document.getElementById('yieldPerHectare').textContent =
        prediction.yield_per_hectare.toFixed(1);
    document.getElementById('totalYield').textContent =
        prediction.total_yield.toFixed(1);
    document.getElementById('modelUsed').textContent = result.model_used;

    // Update confidence range
    const lower = prediction.confidence_interval.lower;
    const upper = prediction.confidence_interval.upper;

    document.getElementById('minYield').textContent =
        `${lower.toFixed(1)} Hg/Ha (Minimum)`;
    document.getElementById('maxYield').textContent =
        `${upper.toFixed(1)} Hg/Ha (Maximum)`;

    // Animate confidence bar
    const range = upper - lower;
    const maxValue = upper + 20;
    const barWidth = ((upper - lower) / maxValue) * 100;

    setTimeout(() => {
        document.getElementById('confidenceBar').style.width = '80%';
    }, 300);

    // Generate rich explanation
    const explanation = generateExplanation(prediction, formData, country);
    document.getElementById('explanationContent').innerHTML = explanation;

    // Show results
    resultsSection.style.display = 'block';
    resultsSection.classList.add('animate-in');

    console.log('✅ Results displayed successfully');
}

// Generate detailed, simple explanation
function generateExplanation(prediction, formData, country) {
    const yieldPerHa = prediction.yield_per_hectare;
    const totalYield = prediction.total_yield;
    const fieldArea = formData.field_area;

    // Convert to more understandable units
    const totalKg = (totalYield * 100).toFixed(0); // hectograms to kg
    const totalTonnes = (totalYield / 10).toFixed(2); // hectograms to tonnes

    // Determine if yield is good, average, or low
    let yieldQuality = 'average';
    let yieldEmoji = '👍';

    if (formData.crop === 'Sugarcane' && yieldPerHa > 600) {
        yieldQuality = 'excellent';
        yieldEmoji = '🎉';
    } else if (formData.crop === 'Rice' && yieldPerHa > 40) {
        yieldQuality = 'excellent';
        yieldEmoji = '🎉';
    } else if (formData.crop === 'Wheat' && yieldPerHa > 35) {
        yieldQuality = 'excellent';
        yieldEmoji = '🎉';
    } else if (yieldPerHa < 15) {
        yieldQuality = 'below average';
        yieldEmoji = '💡';
    }

    let html = `
        <p><strong>${yieldEmoji} Your Expected Harvest:</strong></p>
        <ul>
            <li>From your <strong>${fieldArea} hectare</strong> field, you can expect to harvest approximately <strong>${totalKg} kilograms</strong> (or ${totalTonnes} tonnes) of ${formData.crop}.</li>
            <li>This is a <strong>${yieldQuality}</strong> yield for ${formData.crop} crops.</li>
        </ul>
        
        <p style="margin-top: 16px;"><strong>💰 What This Means:</strong></p>
        <ul>`;

    // Add contextual insights based on crop type
    if (formData.crop === 'Rice') {
        html += `<li>This amount of rice can feed approximately ${Math.round(totalKg / 150)} people for a year!</li>`;
    } else if (formData.crop === 'Wheat') {
        html += `<li>You could make approximately ${Math.round(totalKg * 1.3)} loaves of bread with this harvest!</li>`;
    } else if (formData.crop === 'Maize') {
        html += `<li>This maize could produce enough flour for thousands of tortillas or cornmeal!</li>`;
    }

    html += `</ul>
        
        <p style="margin-top: 16px;"><strong>🌟 Key Factors Helping Your Crop:</strong></p>
        <ul>`;

    // Personalized insights
    if (formData.rainfall > 1000) {
        html += `<li>Good rainfall (${formData.rainfall}mm) will provide plenty of water for your crops</li>`;
    }
    if (formData.irrigation === 1) {
        html += `<li>Having irrigation gives you control over water supply - this boosts yield!</li>`;
    }
    if (formData.fertilizer_used > 100) {
        html += `<li>Your fertilizer usage (${formData.fertilizer_used} kg/ha) will help plants grow strong</li>`;
    }
    if (formData.temperature >= 20 && formData.temperature <= 30) {
        html += `<li>Temperature of ${formData.temperature}°C is ideal for most crops</li>`;
    }

    html += `</ul>`;

    // Add improvement tips if yield is low
    if (yieldQuality === 'below average') {
        html += `
            <p style="margin-top: 16px;"><strong>💡 Tips to Improve Your Yield:</strong></p>
            <ul>`;

        if (formData.fertilizer_used < 100) {
            html += `<li>Consider using more fertilizer (currently ${formData.fertilizer_used} kg/ha)</li>`;
        }
        if (formData.irrigation === 0 && formData.rainfall < 800) {
            html += `<li>Installing irrigation could significantly boost your harvest</li>`;
        }
        if (formData.ph_level < 6 || formData.ph_level > 7.5) {
            html += `<li>Adjusting soil pH closer to 6.5-7.0 could help</li>`;
        }

        html += `</ul>`;
    }

    return html;
}

// Utility functions
console.log('✅ AgriPredict Script Loaded');
