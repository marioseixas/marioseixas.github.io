---
title: Tasks [mermaid]
date: 2024-05-21
tags: tasks
info: aberto.
type: post
layout: post
---

<div class="mermaid">
graph TD
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

    H -->|Yes| L["Urgent, Time-Sensitive, Multi-Day"]
    H -->|No| M["Urgent, Time-Sensitive, Single-Day"]
    
    I -->|Yes| N["Not Urgent, Time-Sensitive, Multi-Day"]
    I -->|No| O["Not Urgent, Time-Sensitive, Single-Day"]

    J -->|Yes| P["Urgent, Not Time-Sensitive, Multi-Day"]
    J -->|No| Q["Urgent, Not Time-Sensitive, Single-Day"]

    K -->|Yes| R["Not Urgent, Not Time-Sensitive, Multi-Day"]
    K -->|No| S["Not Urgent, Not Time-Sensitive, Single-Day"]

    L --> LA["Action: Schedule this task immediately, breaking it down into manageable steps across multiple days to meet the deadline."]
    M --> MA["Action: Prioritize and complete this task by the end of the day. Ensure all resources are focused on meeting the deadline."]
    N --> NA["Action: Schedule this task, breaking it down into steps to be completed over multiple days before the deadline."]
    O --> OA["Action: Plan to complete this task on the day of the deadline, ensuring all necessary preparations are made in advance."]
    P --> PA["Action: Begin this task immediately and plan the work over multiple days, ensuring consistent progress until completion."]
    Q --> QA["Action: Complete this task as soon as possible within the same day. Ensure immediate attention and action."]
    R --> RA["Action: Allocate time for this task in your schedule, working on it gradually over multiple days without urgency."]
    S --> SA["Action: Plan to complete this task in a single day when time permits, without prioritizing it over more urgent tasks."]

</div>
