// AgentOS Dashboard JavaScript
class AgentOSDashboard {
    constructor() {
        this.agents = [];
        this.events = [];
        this.init();
    }

    init() {
        this.loadSampleData();
        this.renderAgents();
        this.renderEvents();
        this.initCharts();
        this.bindEvents();
        this.startLiveUpdates();
    }

    loadSampleData() {
        // Sample agent data
        this.agents = [
            {
                id: 'finance-bot-1',
                name: 'Financial Analyst',
                status: 'running',
                resources: { cpu: '15%', memory: '2.1GB', cost: '$4.20' },
                permissions: ['read_finance', 'write_reports'],
                runtime: '2h 34m',
                health: 'excellent'
            },
            {
                id: 'research-bot-2', 
                name: 'Research Assistant',
                status: 'running',
                resources: { cpu: '28%', memory: '3.4GB', cost: '$8.75' },
                permissions: ['read_research', 'web_search'],
                runtime: '1h 12m',
                health: 'good'
            },
            {
                id: 'customer-support-1',
                name: 'Customer Support',
                status: 'running', 
                resources: { cpu: '8%', memory: '1.2GB', cost: '$2.10' },
                permissions: ['read_tickets', 'send_emails'],
                runtime: '4h 56m',
                health: 'excellent'
            },
            {
                id: 'data-processor-1',
                name: 'Data Processor',
                status: 'warning',
                resources: { cpu: '85%', memory: '8.1GB', cost: '$15.30' },
                permissions: ['read_datasets', 'process_data'],
                runtime: '0h 45m',
                health: 'warning'
            }
        ];

        // Sample events
        this.events = [
            { time: '2 minutes ago', type: 'security', message: 'ACL permission check passed for finance-bot-1', severity: 'info' },
            { time: '5 minutes ago', type: 'resource', message: 'High CPU usage detected on data-processor-1', severity: 'warning' },
            { time: '12 minutes ago', type: 'system', message: 'Snapshot created for research-bot-2', severity: 'info' },
            { time: '25 minutes ago', type: 'security', message: 'New agent registered: customer-support-1', severity: 'info' },
            { time: '1 hour ago', type: 'system', message: 'Daily quota enforcement completed', severity: 'info' }
        ];
    }

    renderAgents() {
        const container = document.getElementById('agents-list');
        container.innerHTML = this.agents.map(agent => `
            <div class="agent-card border-l-4 ${this.getBorderColor(agent.health)} bg-white rounded-lg p-4 mb-4 shadow-sm">
                <div class="flex justify-between items-start">
                    <div class="flex items-center space-x-3">
                        <div class="w-3 h-3 rounded-full ${this.getStatusColor(agent.health)}"></div>
                        <div>
                            <h3 class="font-semibold text-gray-800">${agent.name}</h3>
                            <p class="text-sm text-gray-600">ID: ${agent.id}</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="inline-block px-2 py-1 text-xs rounded ${this.getStatusBadgeColor(agent.status)}">
                            ${agent.status.toUpperCase()}
                        </span>
                        <p class="text-xs text-gray-500 mt-1">Runtime: ${agent.runtime}</p>
                    </div>
                </div>
                
                <div class="mt-3 grid grid-cols-3 gap-2 text-sm">
                    <div class="text-center">
                        <p class="text-gray-600">CPU</p>
                        <p class="font-semibold ${this.getResourceColor(agent.resources.cpu)}">${agent.resources.cpu}</p>
                    </div>
                    <div class="text-center">
                        <p class="text-gray-600">Memory</p>
                        <p class="font-semibold">${agent.resources.memory}</p>
                    </div>
                    <div class="text-center">
                        <p class="text-gray-600">Cost</p>
                        <p class="font-semibold text-green-600">${agent.resources.cost}</p>
                    </div>
                </div>

                <div class="mt-3 flex justify-between items-center">
                    <div class="flex space-x-1">
                        ${agent.permissions.map(perm => 
                            `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${perm}</span>`
                        ).join('')}
                    </div>
                    <button class="kill-agent-btn bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1 rounded transition duration-200" data-agent-id="${agent.id}">
                        <i class="fas fa-power-off mr-1"></i>Kill
                    </button>
                </div>
            </div>
        `).join('');

        // Bind kill buttons
        document.querySelectorAll('.kill-agent-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const agentId = e.target.closest('button').dataset.agentId;
                this.killAgent(agentId);
            });
        });
    }

    renderEvents() {
        const container = document.getElementById('recent-events');
        container.innerHTML = this.events.map(event => `
            <div class="flex items-start space-x-3 p-2 rounded-lg ${this.getEventBackground(event.severity)}">
                <i class="fas ${this.getEventIcon(event.type)} mt-1 ${this.getEventIconColor(event.severity)}"></i>
                <div class="flex-1">
                    <p class="text-sm text-gray-800">${event.message}</p>
                    <p class="text-xs text-gray-500">${event.time}</p>
                </div>
            </div>
        `).join('');
    }

    initCharts() {
        // Resource Usage Chart
        const resourceCtx = document.getElementById('resourceChart').getContext('2d');
        this.resourceChart = new Chart(resourceCtx, {
            type: 'doughnut',
            data: {
                labels: ['CPU', 'Memory', 'Storage', 'Network'],
                datasets: [{
                    data: [45, 28, 15, 12],
                    backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Resource Distribution'
                    }
                }
            }
        });

        // Security Events Chart
        const securityCtx = document.getElementById('securityChart').getContext('2d');
        this.securityChart = new Chart(securityCtx, {
            type: 'bar',
            data: {
                labels: ['ACL Checks', 'Quota Enforcements', 'Kill Events', 'Audit Logs'],
                datasets: [{
                    label: 'Security Events',
                    data: [142, 28, 3, 89],
                    backgroundColor: '#10B981',
                    borderColor: '#059669',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Security Events (Today)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    bindEvents() {
        // Kill switch button
        document.getElementById('kill-all-btn').addEventListener('click', () => {
            this.activateKillSwitch();
        });
    }

    activateKillSwitch() {
        if (confirm('🚨 ARE YOU SURE? This will immediately terminate ALL running agents!')) {
            // Simulate kill switch activation
            document.body.style.animation = 'pulse 0.5s 3';
            document.getElementById('kill-all-btn').innerHTML = '<i class="fas fa-skull-crossbones mr-2"></i>KILLING ALL AGENTS...';
            document.getElementById('kill-all-btn').classList.add('bg-red-800');
            
            setTimeout(() => {
                alert('✅ All agents have been terminated safely.');
                document.getElementById('kill-all-btn').innerHTML = '<i class="fas fa-skull-crossbones mr-2"></i>KILL SWITCH ACTIVATED';
                document.getElementById('kill-all-btn').classList.add('opacity-50');
                document.getElementById('kill-all-btn').disabled = true;
                
                // Update UI
                this.agents.forEach(agent => agent.status = 'terminated');
                this.renderAgents();
                this.addEvent('system', 'Emergency kill switch activated - all agents terminated', 'critical');
            }, 2000);
        }
    }

    killAgent(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent && confirm(`Terminate agent ${agent.name}?`)) {
            agent.status = 'terminated';
            this.renderAgents();
            this.addEvent('security', `Agent terminated: ${agent.name} (${agentId})`, 'warning');
        }
    }

    addEvent(type, message, severity = 'info') {
        const event = {
            time: 'Just now',
            type,
            message,
            severity
        };
        this.events.unshift(event);
        if (this.events.length > 5) this.events.pop();
        this.renderEvents();
    }

    startLiveUpdates() {
        // Simulate live updates
        setInterval(() => {
            // Randomly update resource usage
            this.agents.forEach(agent => {
                if (agent.status === 'running') {
                    const cpuChange = (Math.random() - 0.5) * 10;
                    const currentCpu = parseInt(agent.resources.cpu);
                    const newCpu = Math.max(5, Math.min(95, currentCpu + cpuChange));
                    agent.resources.cpu = Math.round(newCpu) + '%';
                    
                    // Update cost based on usage
                    const costPerMinute = parseFloat(agent.resources.cost.replace('$', '')) / 60;
                    agent.resources.cost = '$' + (parseFloat(agent.resources.cost.replace('$', '')) + costPerMinute).toFixed(2);
                }
            });
            this.renderAgents();
        }, 5000);
    }

    // Helper methods for styling
    getBorderColor(health) {
        const colors = {
            excellent: 'border-green-500',
            good: 'border-blue-500', 
            warning: 'border-yellow-500',
            critical: 'border-red-500'
        };
        return colors[health] || 'border-gray-500';
    }

    getStatusColor(health) {
        const colors = {
            excellent: 'bg-green-500',
            good: 'bg-blue-500',
            warning: 'bg-yellow-500 pulse-warning',
            critical: 'bg-red-500 pulse-warning'
        };
        return colors[health] || 'bg-gray-500';
    }

    getStatusBadgeColor(status) {
        const colors = {
            running: 'bg-green-100 text-green-800',
            warning: 'bg-yellow-100 text-yellow-800',
            terminated: 'bg-red-100 text-red-800',
            paused: 'bg-gray-100 text-gray-800'
        };
        return colors[status] || 'bg-gray-100 text-gray-800';
    }

    getResourceColor(usage) {
        const percent = parseInt(usage);
        if (percent > 80) return 'text-red-600';
        if (percent > 60) return 'text-yellow-600';
        return 'text-green-600';
    }

    getEventBackground(severity) {
        const colors = {
            info: 'bg-blue-50',
            warning: 'bg-yellow-50',
            critical: 'bg-red-50'
        };
        return colors[severity] || 'bg-gray-50';
    }

    getEventIcon(type) {
        const icons = {
            security: 'fa-shield-alt',
            resource: 'fa-microchip',
            system: 'fa-cog'
        };
        return icons[type] || 'fa-info-circle';
    }

    getEventIconColor(severity) {
        const colors = {
            info: 'text-blue-500',
            warning: 'text-yellow-500',
            critical: 'text-red-500'
        };
        return colors[severity] || 'text-gray-500';
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new AgentOSDashboard();
});
