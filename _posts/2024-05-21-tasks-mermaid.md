---
title: Tasks [mermaid]
date: 2024-05-21
tags: tasks
info: aberto.
type: post
layout: post
---

<div class="mermaid">
flowchart TD
    A["Does this task have a specific deadline?"] -->|Yes| B["Will delaying this task past its deadline cause immediate harm or significant negative consequences?"]
    A -->|No| C["Will delaying this task cause immediate harm or significant negative consequences?"]

    B -->|Yes| D["Urgent & Time-Sensitive"]
    B -->|No| E["Not Urgent & Time-Sensitive"]
    
    C -->|Yes| F["Urgent & Not Time-Sensitive"]
    C -->|No| G["Not Urgent & Not Time-Sensitive"]

    D --> H["Does this task require multiple days to complete?"]
    E --> I["Does this task require multiple days to complete?"]
    F --> J["Does this task require multiple days to complete?"]
    G --> K["Does this task require multiple days to complete?"]

    H -->|Yes| L["Urgent, Time-Sensitive, Multi-Day\nSchedule immediately, break into steps."]
    H -->|No| M["Urgent, Time-Sensitive, Single-Day\nPrioritize and complete today."]
    
    I -->|Yes| N["Not Urgent, Time-Sensitive, Multi-Day\nSchedule, break into steps."]
    I -->|No| O["Not Urgent, Time-Sensitive, Single-Day\nPlan to complete on deadline day."]

    J -->|Yes| P["Urgent, Not Time-Sensitive, Multi-Day\nBegin immediately, plan work."]
    J -->|No| Q["Urgent, Not Time-Sensitive, Single-Day\nComplete ASAP today."]

    K -->|Yes| R["Not Urgent, Not Time-Sensitive, Multi-Day\nAllocate time, work gradually."]
    K -->|No| S["Not Urgent, Not Time-Sensitive, Single-Day\nComplete in one day when possible."]
</div>
