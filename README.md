requirements

google-generativeai
python-dotenv
pyyaml
colorama

.env
API KEY

llm_routing_system/
│
├── config/
│ └── config.yaml # Configuration settings
│
├── agents/
│ ├── init.py
│ ├── base_agent.py # Base agent class
│ ├── l1_agent.py # Reception agent
│ ├── l2_agent.py # Developer agent
│ └── l3_agent.py # Senior agent
│
├── routing/
│ ├── init.py
│ └── router.py # Main routing logic
│
├── utils/
│ ├── init.py
│ └── logger.py # Logging utilities
│
├── mcp/
│ ├── go.mod # go module file
│ └── main.go # script for mcp server
│
├── .env # Environment variables
├── requirements.txt # Python dependencies
├── main.py # Entry point
└── README.md # Documentation
