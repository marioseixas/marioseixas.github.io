{% mermaid %}
graph LR
    subgraph Inputs
        A[External & Internal Phenomena] --> B(Sensory Perceptions)
        A --> C(Emotions)
        A --> D(Memories)
    end

    B --> E[Attention/Awareness - Gatekeeper]
    C --> E
    D --> E

    subgraph Cognitive Processing
        E --> F{Thoughts Generation}
        F --> G{Processing Thoughts - Intention & Experience}
        G --> H{Intentional Decision-Making}
    end

    H --> I[Actions & Responses]
    I --> J[Outcome & Impact - Meaning & Fulfillment]

    J --> K[Feedback Loop - Learning & Adjustment]
    K --> E

    subgraph Constraints
        L[Distractions & Manipulations] --> E
        M[Cognitive Budget - Finite Tokens] --> F
        M --> G
        M --> H
        N[Latency & Irretrievability - Time Cost] --> F
        N --> G
        N --> H
    end

    style M fill:#f9f,stroke:#333,stroke-width:2px
    style N fill:#f9f,stroke:#333,stroke-width:2px
{% endmermaid %}
