#!/bin/bash

# Create package.json
cat > package.json << 'PACKAGE_EOF'
{
  "name": "martechos-suite",
  "version": "1.0.0", 
  "description": "AI-powered marketing suite",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  }
}
PACKAGE_EOF

# Create server.js with correct path
cat > server.js << 'SERVER_EOF'
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files from current directory
app.use(express.static(__dirname));

// API routes
app.get('/api', (req, res) => {
    res.json({ 
        message: 'MartechOS API is running!',
        version: '1.0.0',
        directory: __dirname
    });
});

app.post('/api/generate-creative', (req, res) => {
    const { prompt, platform } = req.body;
    
    const creative = {
        id: 'creative_' + Date.now(),
        prompt,
        platform,
        image_url: \`https://picsum.photos/800/400?random=\${Date.now()}\`,
        ad_copy: \`Discover amazing \${prompt} with our exclusive offer!\`,
        ctr_prediction: (Math.random() * 5 + 1).toFixed(2)
    };

    res.json(creative);
});

app.post('/api/check-compliance', (req, res) => {
    const { ad_copy, target_country } = req.body;
    
    const compliance = {
        is_compliant: true,
        warnings: [],
        suggestions: [],
        dpdp_compliant: target_country === 'IN'
    };

    if (ad_copy.includes('free') && !ad_copy.includes('terms')) {
        compliance.warnings.push('Add terms for "free" claims');
    }

    res.json(compliance);
});

app.get('/api/analytics', (req, res) => {
    res.json({
        total_spend: 50000,
        total_revenue: 175000,
        roi: 250
    });
});

// Serve index.html for root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(\`🚀 Server running on http://localhost:\${PORT}\`);
    console.log(\`📁 Current directory: \${__dirname}\`);
});
SERVER_EOF

# Create index.html
cat > index.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MartechOS - AI Marketing</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="min-h-screen">
        <header class="bg-white shadow-sm">
            <div class="max-w-7xl mx-auto px-4 py-4">
                <h1 class="text-2xl font-bold text-gray-900">🚀 MartechOS - AI Marketing Suite</h1>
            </div>
        </header>

        <section class="py-16 bg-white">
            <div class="max-w-7xl mx-auto px-4">
                <h2 class="text-3xl font-bold text-center mb-8">AI Creative Generator</h2>
                
                <div class="max-w-2xl mx-auto bg-gray-50 p-8 rounded-lg">
                    <form id="creativeForm" class="mb-6">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">What do you want to promote?</label>
                            <input type="text" id="prompt" class="w-full px-3 py-2 border border-gray-300 rounded-md" 
                                   placeholder="e.g., Organic skincare, Tech gadgets, Restaurant deals..." required>
                        </div>
                        
                        <button type="submit" class="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 font-semibold">
                            <i class="fas fa-magic mr-2"></i>Generate AI Creative
                        </button>
                    </form>

                    <div id="creativeResult" class="hidden bg-white p-6 rounded-lg shadow">
                        <h3 class="text-xl font-semibold mb-4">🎨 Your Generated Ad</h3>
                        <img id="creativeImage" src="" class="w-full h-48 object-cover rounded-lg mb-4 border">
                        <p id="creativeCopy" class="text-gray-700 mb-3 text-lg"></p>
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-gray-600">Predicted CTR: <strong id="predictedCtr" class="text-green-600"></strong></span>
                            <button onclick="shareCreative()" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                                <i class="fas fa-share mr-1"></i>Share
                            </button>
                        </div>
                    </div>
                    
                    <div id="creativePlaceholder" class="text-center text-gray-500 py-8 border-2 border-dashed rounded-lg">
                        <i class="fas fa-image text-4xl mb-3 text-gray-300"></i>
                        <p>Your AI-generated ad creative will appear here</p>
                        <p class="text-sm mt-2">Try: "Coffee shop discount" or "Fitness app launch"</p>
                    </div>
                </div>
            </div>
        </section>

        <div class="max-w-2xl mx-auto px-4 mb-8">
            <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="font-semibold text-blue-800 mb-2">💡 Pro Tip</h3>
                <p class="text-blue-700 text-sm">Be specific in your description for better results. Include target audience, key benefits, or unique selling points.</p>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('creativeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const prompt = document.getElementById('prompt').value;
            const button = e.target.querySelector('button');
            
            // Show loading state
            button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Generating...';
            button.disabled = true;

            try {
                const response = await fetch('/api/generate-creative', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt, platform: 'instagram' })
                });

                const creative = await response.json();
                
                // Update UI with results
                document.getElementById('creativeImage').src = creative.image_url;
                document.getElementById('creativeImage').alt = creative.ad_copy;
                document.getElementById('creativeCopy').textContent = creative.ad_copy;
                document.getElementById('predictedCtr').textContent = creative.ctr_prediction + '%';
                
                // Show results, hide placeholder
                document.getElementById('creativePlaceholder').classList.add('hidden');
                document.getElementById('creativeResult').classList.remove('hidden');
                
            } catch (error) {
                alert('Error generating creative: ' + error.message);
            } finally {
                // Reset button
                button.innerHTML = '<i class="fas fa-magic mr-2"></i>Generate AI Creative';
                button.disabled = false;
            }
        });

        function shareCreative() {
            const copy = document.getElementById('creativeCopy').textContent;
            const ctr = document.getElementById('predictedCtr').textContent;
            alert(\`Share this creative!\\n\\n"\${copy}"\\n\\nPredicted CTR: \${ctr}\`);
        }

        // Check if server is running
        fetch('/api')
            .then(response => response.json())
            .then(data => console.log('Server connected:', data))
            .catch(err => console.log('Server connection failed:', err));
    </script>
</body>
</html>
HTML_EOF

echo "✅ All files created successfully!"
echo "📁 Files in current directory:"
ls -la
echo ""
echo "🚀 To run the application:"
echo "   npm install"
echo "   npm start"
echo ""
echo "🌐 Then open: http://localhost:5000"
