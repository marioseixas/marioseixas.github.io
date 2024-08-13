---
title: Task Prioritization [mermaid]
date: 2024-05-21
tags: [tasks, productivity]
type: post
layout: post
---

<div class="mermaid">
flowchart TD
    A[Start] --> B{Specific<br>deadline?}
    B -->|Yes| C{Delay causes<br>harm?}
    B -->|No| D{Delay causes<br>harm?}
    
    subgraph "Urgency & Time-Sensitivity"
        C -->|Yes| E[Urgent &<br>Time-Sensitive]
        C -->|No| F[Not Urgent &<br>Time-Sensitive]
        D -->|Yes| G[Urgent &<br>Not Time-Sensitive]
        D -->|No| H[Not Urgent &<br>Not Time-Sensitive]
    end
    
    E & F & G & H --> I{Multi-day<br>task?}
    
    subgraph "Task Duration & Final Categorization"
        I -->|Yes| J[Multi-Day]
        I -->|No| K[Single-Day]
        
        J --> L{Type?}
        K --> M{Type?}
        
        L -->|E| N[Schedule immediately,<br>break into steps]
        L -->|F| O[Schedule,<br>break into steps]
        L -->|G| P[Begin immediately,<br>plan work]
        L -->|H| Q[Allocate time,<br>work gradually]
        
        M -->|E| R[Prioritize and<br>complete today]
        M -->|F| S[Plan for<br>deadline day]
        M -->|G| T[Complete<br>ASAP today]
        M -->|H| U[Complete when<br>possible]
    end
    
    N & O & P & Q & R & S & T & U --> V[End]
</div>
