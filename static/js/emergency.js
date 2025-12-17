/**
 * Emergency Detection and Response JavaScript
 * 
 * Handles emergency detection, alerts, and response functionality
 */

// Emergency detection configuration
const EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', 'stroke', 'seizure', 'unconscious',
    'severe bleeding', 'difficulty breathing', 'choking', 'severe headache',
    'severe abdominal pain', 'severe allergic reaction', 'overdose'
];

const EMERGENCY_SYMPTOMS = [
    'chest pain', 'shortness of breath', 'severe headache', 'loss of consciousness',
    'severe bleeding', 'difficulty speaking', 'severe nausea', 'severe dizziness'
];

/**
 * Check if symptoms indicate emergency
 */
function detectEmergency(symptoms) {
    if (!symptoms || !Array.isArray(symptoms)) {
        return false;
    }
    
    const symptomsText = symptoms.join(' ').toLowerCase();
    
    return EMERGENCY_KEYWORDS.some(keyword => 
        symptomsText.includes(keyword.toLowerCase())
    );
}

/**
 * Analyze emergency severity
 */
function analyzeEmergencySeverity(symptoms, prediction) {
    let severity = 'low';
    let emergencyScore = 0;
    
    // Check symptoms
    if (symptoms) {
        symptoms.forEach(symptom => {
            if (EMERGENCY_SYMPTOMS.includes(symptom.toLowerCase())) {
                emergencyScore += 2;
            }
        });
    }
    
    // Check prediction severity
    if (prediction && prediction.severity) {
        switch (prediction.severity.toLowerCase()) {
            case 'high':
                emergencyScore += 3;
                break;
            case 'medium':
                emergencyScore += 1;
                break;
        }
    }
    
    // Determine severity level
    if (emergencyScore >= 4) {
        severity = 'critical';
    } else if (emergencyScore >= 2) {
        severity = 'high';
    } else if (emergencyScore >= 1) {
        severity = 'medium';
    }
    
    return {
        severity: severity,
        score: emergencyScore,
        isEmergency: emergencyScore >= 2
    };
}

/**
 * Generate emergency recommendations
 */
function generateEmergencyRecommendations(symptoms, severity) {
    const recommendations = [];
    
    switch (severity) {
        case 'critical':
            recommendations.push('Call 911 immediately');
            recommendations.push('Do not drive yourself to the hospital');
            recommendations.push('Stay calm and follow dispatcher instructions');
            break;
            
        case 'high':
            recommendations.push('Seek immediate medical attention');
            recommendations.push('Go to the nearest emergency room');
            recommendations.push('Call ahead to notify the hospital');
            break;
            
        case 'medium':
            recommendations.push('Contact your doctor immediately');
            recommendations.push('Consider urgent care if doctor unavailable');
            recommendations.push('Monitor symptoms closely');
            break;
            
        default:
            recommendations.push('Monitor symptoms');
            recommendations.push('Contact healthcare provider if symptoms worsen');
            break;
    }
    
    return recommendations;
}

/**
 * Show emergency alert with details
 */
function showDetailedEmergencyAlert(emergencyData) {
    const alertElement = document.getElementById('emergency-alert');
    const messageElement = document.getElementById('emergency-message');
    
    if (!alertElement || !messageElement) {
        console.error('Emergency alert elements not found');
        return;
    }
    
    // Build alert message
    let alertMessage = 'EMERGENCY DETECTED! ';
    
    if (emergencyData.severity === 'critical') {
        alertMessage += 'This appears to be a critical emergency. ';
    } else if (emergencyData.severity === 'high') {
        alertMessage += 'This appears to be a serious medical emergency. ';
    }
    
    alertMessage += 'Please seek immediate medical attention.';
    
    if (emergencyData.recommendations && emergencyData.recommendations.length > 0) {
        alertMessage += '\n\nRecommendations:\n• ' + emergencyData.recommendations.join('\n• ');
    }
    
    messageElement.textContent = alertMessage;
    alertElement.classList.remove('hidden');
    
    // Add severity class for styling
    alertElement.className = `emergency-alert severity-${emergencyData.severity}`;
    
    // Scroll to alert
    alertElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Log emergency event
    logEmergencyEvent(emergencyData);
    
    // Auto-focus emergency button
    const emergencyButton = document.getElementById('call-ambulance');
    if (emergencyButton) {
        setTimeout(() => emergencyButton.focus(), 500);
    }
}

/**
 * Log emergency event
 */
function logEmergencyEvent(emergencyData) {
    const eventData = {
        timestamp: new Date().toISOString(),
        type: 'emergency_detected',
        severity: emergencyData.severity,
        score: emergencyData.score,
        symptoms: emergencyData.symptoms,
        user_session: HealthcareApp.getCurrentUserSession()
    };
    
    // Send to server for logging
    HealthcareApp.makeRequest('/log-emergency', 'POST', eventData)
        .then(response => {
            console.log('Emergency event logged:', response);
        })
        .catch(error => {
            console.error('Failed to log emergency event:', error);
        });
}

/**
 * Simulate emergency call with location
 */
function simulateEmergencyCallWithLocation() {
    // Get current location if available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const location = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                
                simulateEmergencyCall(location);
            },
            function(error) {
                console.warn('Location not available:', error.message);
                simulateEmergencyCall();
            }
        );
    } else {
        simulateEmergencyCall();
    }
}

/**
 * Enhanced emergency call simulation
 */
function simulateEmergencyCall(location = null) {
    let message = '🚨 EMERGENCY CALL SIMULATION 🚨\n\n';
    message += 'Calling Emergency Services (911)...\n\n';
    
    if (location) {
        message += `Location: ${location.latitude.toFixed(6)}, ${location.longitude.toFixed(6)}\n`;
        message += 'Location has been shared with emergency services.\n\n';
    }
    
    message += 'Emergency services have been notified.\n';
    message += 'Help is on the way.\n\n';
    message += '⚠️ This is a simulation for academic purposes only.\n';
    message += 'In a real emergency, call your local emergency number immediately!';
    
    alert(message);
    
    // Show follow-up notification
    HealthcareApp.showNotification('Emergency services contacted successfully', 'success');
    
    // Log the call
    logEmergencyCall(location);
}

/**
 * Log emergency call
 */
function logEmergencyCall(location = null) {
    const callData = {
        timestamp: new Date().toISOString(),
        type: 'emergency_call',
        location: location,
        user_session: HealthcareApp.getCurrentUserSession()
    };
    
    HealthcareApp.makeRequest('/log-emergency-call', 'POST', callData)
        .then(response => {
            console.log('Emergency call logged:', response);
        })
        .catch(error => {
            console.error('Failed to log emergency call:', error);
        });
}

/**
 * Check for emergency in real-time as user types symptoms
 */
function checkEmergencyRealTime(inputElement) {
    if (!inputElement) return;
    
    inputElement.addEventListener('input', function() {
        const symptoms = this.value.toLowerCase();
        const hasEmergencyKeywords = EMERGENCY_KEYWORDS.some(keyword => 
            symptoms.includes(keyword)
        );
        
        if (hasEmergencyKeywords) {
            showQuickEmergencyWarning();
        } else {
            hideQuickEmergencyWarning();
        }
    });
}

/**
 * Show quick emergency warning
 */
function showQuickEmergencyWarning() {
    let warningElement = document.getElementById('quick-emergency-warning');
    
    if (!warningElement) {
        warningElement = document.createElement('div');
        warningElement.id = 'quick-emergency-warning';
        warningElement.className = 'quick-emergency-warning';
        warningElement.innerHTML = `
            <div class="warning-content">
                <span class="warning-icon">⚠️</span>
                <span class="warning-text">Your symptoms may indicate an emergency. Consider seeking immediate medical attention.</span>
                <button onclick="simulateEmergencyCallWithLocation()" class="btn btn-emergency btn-sm">Call Emergency</button>
            </div>
        `;
        
        // Insert after the symptom input
        const symptomInput = document.getElementById('symptom-text') || document.querySelector('.form-textarea');
        if (symptomInput && symptomInput.parentNode) {
            symptomInput.parentNode.insertBefore(warningElement, symptomInput.nextSibling);
        }
    }
    
    warningElement.style.display = 'block';
}

/**
 * Hide quick emergency warning
 */
function hideQuickEmergencyWarning() {
    const warningElement = document.getElementById('quick-emergency-warning');
    if (warningElement) {
        warningElement.style.display = 'none';
    }
}

/**
 * Initialize emergency detection on symptom inputs
 */
function initializeEmergencyDetection() {
    // Add real-time checking to symptom inputs
    const symptomInputs = document.querySelectorAll('#symptom-text, .symptom-input');
    symptomInputs.forEach(input => {
        checkEmergencyRealTime(input);
    });
    
    // Override the ambulance call button if it exists
    const ambulanceButton = document.getElementById('call-ambulance');
    if (ambulanceButton) {
        ambulanceButton.onclick = simulateEmergencyCallWithLocation;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeEmergencyDetection);

// Export functions for global use
window.EmergencySystem = {
    detectEmergency,
    analyzeEmergencySeverity,
    generateEmergencyRecommendations,
    showDetailedEmergencyAlert,
    simulateEmergencyCallWithLocation,
    checkEmergencyRealTime
};